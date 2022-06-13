"""
Модуль с полезными функциями для поиска расстояния.
"""

import math


def distance_counter(normal_path):
    """
    Функция для поиска длины пути.
    :param normal_path: список узлов.
    :return: float длина пути.
    """
    distance = 0
    for i in range(len(normal_path)):
        if i != 0:
            new_dist = dist(normal_path[i], normal_path[i - 1])
            distance += new_dist

    # Также не забываем добавить расстояние между последним и первым элементом для полного цикла
    distance += dist(normal_path[0], normal_path[-1])
    return distance


def dist(node_1, node_2):
    """
    Функция для поиска расстояния между двумя узлами.
    :param node_1: первый узел.
    :param node_2: второй узел.
    :return: float расстояние между узлами.
    """
    return math.dist([node_1.cords[0], node_1.cords[1]],
                     [node_2.cords[0], node_2.cords[1]])
