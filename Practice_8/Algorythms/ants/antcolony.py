"""
Модуль, реализующий
муравьиный алгоритм, для
поиска оптимального пути
"""
import numpy as np
import sys

from random import choices
from ..distancer import *
from ..saver import save_ant_colony_setup
from colorama import Fore, init


ALPHA = 2
BETA = 2
Q = 200
PROXIMITY = 200
EVAPORATION = 0.6

GENERATIONS = 10
ANTS = 10
PATH_IMPORTANCE = 13

ALPHA_ARRAY = [4, 6, 8]
BETA_ARRAY = [3, 4, 6]
Q_ARRAY = [50, 100, 200, 400]
PROXIMITY_ARRAY = [50, 100, 200, 400]
EVAPORATION_ARRAY = [0.8, 0.7, 0.6, 0.5]

GENERATIONS_ARRAY = [10]
ANTS_ARRAY = [2]
PATH_IMPORTANCE_ARRAY = [4, 7, 10]


def calculate(nodes, path=None):
    init()
    print("Calculating by ant colony algorythm...\n=================================")

    colony = AntColony(ALPHA, BETA, Q, PROXIMITY, EVAPORATION)
    np_path = colony.run_ants(_create_matrix(nodes), np.array(path), GENERATIONS, ANTS, PATH_IMPORTANCE)
    return _np_to_array(np_path, nodes)


def calculate_arrays(path, nodes):
    init()
    print("Calculating by ant colony algorythm...\n=================================")
    previous_score = distance_counter(path)

    matrix = _create_matrix(nodes)
    for q in ALPHA_ARRAY:
        for w in BETA_ARRAY:
            for e in Q_ARRAY:
                for r in PROXIMITY_ARRAY:
                    for t in EVAPORATION_ARRAY:
                        for y in GENERATIONS_ARRAY:
                            for u in ANTS_ARRAY:
                                for i in PATH_IMPORTANCE_ARRAY:
                                    colony = AntColony(q, w, e, r, t)
                                    colony.run_ants(matrix.copy(), np.array(path), y, u, i)
                                    score = colony.get_best_score()
                                    print(q, w, e, r, t, y, u, i,
                                          score if score > previous_score else str(score) +
                                          f' {Fore.RED}<!!!>{Fore.RESET} ')
                                    save_ant_colony_setup(q, w, e, r, t, y, u, i, score)


def _np_to_array(np_path, nodes):
    print('Converting path...')
    path = []
    i = 0
    for np_node in np_path:
        sys.stdout.write("\r" + f'  Step: {i + 1} / {len(np_path)}')
        for node in nodes:
            if int(np_node[0]) == int(node.id):
                path.append(node)
                break
        i += 1

    print()
    return path


def _create_matrix(nodes) -> np.array:
    print('Creating matrix...')
    matrix = []

    for i in range(len(nodes)):
        sys.stdout.write("\r" + f'  Step: {i + 1} / {len(nodes)}')
        matrix.append([])
        for j in range(len(nodes)):
            matrix[i].append(dist(nodes[i], nodes[j]))

    print()
    return np.array(matrix)


class AntColony:
    """
    Класс, реализующий логику
    муравьиной колонии
    """

    def __init__(self,
                 alpha: float,
                 betta: float,
                 q_constant: int,
                 proximity_constant: int,
                 evaporation_share: float,
                 thread_count=4
                 ):
        """
        Инициализация колонии муравьев
        :param alpha: Влияние феромонов на выбор муравья
        :param betta: Влияния близости между городами на выбор муравья
        :param q_constant: Константа феромонов
        :param proximity_constant: Константа близости
        :param evaporation_share: Доля испарения феромонов
        """
        self._alpha = alpha
        self._betta = betta
        self._q_constant = q_constant
        self._proximity_constant = proximity_constant
        self._after_evaporation = 1 - evaporation_share

        self._thread_count = thread_count
        self._pheromones = None
        self._proximity = None
        self._probabilities = None
        self._distances = None
        self._best_path = None
        self._best_score = None

    def _ants_group(self,
                    _pheromones: np.array,
                    _proximity: np.array,
                    _distances: np.array,
                    _routes_count: int,
                    _count_ants_in_group: int
                    ):
        pheromone_matrix_delta = distance = ant_path = None

        for _ant in range(_count_ants_in_group):
            start_country = 0
            current_country = start_country
            distance = 0
            probability_matrix = self._probabilities_matrix(_pheromones, _proximity)

            vector_probabilities = self._item_probabilities(probability_matrix, current_country)

            start_routes = np.zeros(_routes_count, dtype=int)
            end_routes = np.zeros(_routes_count, dtype=int)
            city_index = 0

            pheromone_matrix_delta = np.zeros(_pheromones.shape)

            while vector_probabilities.sum() != 0:
                next_country = self._select_unvisited_item(vector_probabilities)

                self._mark_item_visited(probability_matrix, current_country)
                distance += _distances[current_country, next_country]

                start_routes[city_index] = current_country
                end_routes[city_index] = next_country

                current_country = next_country
                vector_probabilities = self._item_probabilities(probability_matrix, current_country)

                city_index += 1

            start_routes[city_index] = current_country
            end_routes[city_index] = start_country

            distance += _distances[current_country, start_country]
            delta_pheromone = self._q_constant / distance

            visited_cities = (np.concatenate((start_routes, end_routes)),
                              np.concatenate((end_routes, start_routes)))

            np.add.at(pheromone_matrix_delta, visited_cities, delta_pheromone)

            ant_path = np.stack((start_routes, end_routes), axis=-1)

        return pheromone_matrix_delta, distance, ant_path

    def run_ants(self, distance_matrix: np.array, starting_path: np.array = None, generations: int = 10,
                 ants_count: int = 1, path_importance: int = 1):
        """
        Запуск поиска пути
        :param distance_matrix: Матрица расстояний между элементами
        :param starting_path: Уже имеющийся путь, переданный муравьям
        :param generations: Количество поколений муравьев
        :param ants_count: Количество муравьев в одном поколении
        :param path_importance: Важность начального пути
        :return: Оптимальный маршрут
        """
        print('Run ants...')

        self._distances = distance_matrix

        rows_count = len(distance_matrix)
        column_count = len(distance_matrix[0])
        routes_count = rows_count

        ants_count = ants_count if ants_count else rows_count

        pheromone_matrix = np.full((rows_count, column_count), 0.5)
        proximity_matrx = self._proximity_matrix(distance_matrix, self._proximity_constant)
        np.fill_diagonal(pheromone_matrix, 0)

        best_distance = np.inf
        best_path = None

        if starting_path:
            for i in range(len(starting_path) - 1):
                pheromone_matrix[int(starting_path[i].id), int(starting_path[i + 1].id)] = path_importance

        for generate in range(generations):
            print(f'  Generation: {generate + 1} / {generations}')
            pheromone_matrix_delta = np.zeros(pheromone_matrix.shape)

            for ant in range(ants_count):
                sys.stdout.write("\r" + f'    Ants: {ant + 1} / {ants_count}')
                start_country = 0
                current_country = start_country
                distance = 0
                probability_matrix = self._probabilities_matrix(pheromone_matrix, proximity_matrx)

                vector_probabilities = self._item_probabilities(probability_matrix, current_country)

                start_routes = np.zeros(routes_count, dtype=int)
                end_routes = np.zeros(routes_count, dtype=int)
                city_index = 0

                while vector_probabilities.sum() != 0:
                    next_country = self._select_unvisited_item(vector_probabilities)

                    self._mark_item_visited(probability_matrix, current_country)
                    distance += distance_matrix[current_country, next_country]

                    start_routes[city_index] = current_country
                    end_routes[city_index] = next_country

                    current_country = next_country
                    vector_probabilities = self._item_probabilities(probability_matrix, current_country)

                    city_index += 1

                start_routes[city_index] = current_country
                end_routes[city_index] = start_country

                distance += distance_matrix[current_country, start_country]
                delta_pheromone = self._q_constant / distance

                visited_cities = (np.concatenate((start_routes, end_routes)),
                                  np.concatenate((end_routes, start_routes)))

                np.add.at(pheromone_matrix_delta, visited_cities, delta_pheromone)

                if distance < best_distance:
                    best_distance = min(best_distance, distance)
                    best_path = np.stack((start_routes, end_routes), axis=-1)

            pheromone_matrix *= self._after_evaporation
            pheromone_matrix += pheromone_matrix_delta

            sys.stdout.write("\r\r\r")

        self._pheromones = pheromone_matrix
        self._proximity = proximity_matrx
        self._probabilities = self._probabilities_matrix(self._pheromones, self._proximity)
        self._best_path = best_path
        self._best_score = best_distance

        print()
        return best_path

    def get_info(self):
        """
        Получить информацию о
        - Матрице близости
        - Матрице феромонов
        - Матрице вероятностей
        :return: None
        """
        print("Proximity:\n", self._proximity)
        print("\nPheromones:\n", self._pheromones)
        print("\nProbabilities:\n", self._probabilities)

    def get_best_score(self) -> float:
        """
        Лучший результат
        :return: Наименьшее расстояние,
        которое нашел алгоритм
        """
        return self._best_score

    def _probabilities_matrix(self, matrix_pheromones: np.array, matrix_proximity: np.array) -> np.array:
        """
        Находит матрицу вероятностей перехода
        из одного города в другой
        :param matrix_pheromones: Матрица феромонов
        :param matrix_proximity: Матрица близости
        :return: Матрица вероятностей
        """
        # Expanding all elements of a matrix to a power
        alpha_pheromones = matrix_pheromones ** self._alpha
        betta_distance = matrix_proximity ** self._betta

        irregular_probability_matrix = alpha_pheromones * betta_distance

        # Divide all elements in the row by the sum of the row
        matrix_probability = irregular_probability_matrix / irregular_probability_matrix.sum(axis=1, keepdims=True)

        return matrix_probability

    @staticmethod
    def _proximity_matrix(matrix_distance: np.array, distance_constant: int) -> np.array:
        """
        Находит матрицу близости между городами
        :param matrix_distance: Матрица расстояний
        :param distance_constant: Константа близости
        :return: Матрица близости
        """
        matrix_proximity = matrix_distance.copy()
        matrix_proximity[matrix_proximity == 0] = np.inf

        matrix_proximity = np.power(matrix_proximity, -1)
        return matrix_proximity * distance_constant

    @staticmethod
    def _mark_item_visited(matrix_probability: np.array, index: int) -> None:
        """
        Помечает город как посещенный
        :param matrix_probability: Матрица вероятностей
        :param index: Индекс города, который нужно пометить
        :return: None
        """
        matrix_probability[:, index] = 0

    @staticmethod
    def _item_probabilities(matrix_probability: np.array, index: int) -> np.array:
        """
        Вероятности перехода из города с индексом index
        во все остальные
        :param matrix_probability: Матрица вероятностей
        :param index: Индекс города
        :return: Массив вероятностей
        """
        return matrix_probability[index]

    @staticmethod
    def _select_unvisited_item(vector_probabilities: np.array):
        """
        Выбор ещё не посещенного города
        :param vector_probabilities: Массив вероятностей
        :return: Индекс следующего города
        """
        cities_indexes = range(len(vector_probabilities))
        if vector_probabilities.sum() == 0:
            raise ValueError("Probabilities sum is 0")
        return choices(cities_indexes, weights=vector_probabilities)[0]
