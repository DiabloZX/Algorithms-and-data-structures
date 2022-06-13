"""
Модуль с функциями для улучшения пути в задачах коммивояжера.
"""

import sys
import math

from ..distancer import distance_counter
from itertools import permutations


CYCLE_COUNT = 8
MIN_SLICE_LEN = 3
MAX_SLICE_LEN = 8


def calculate(path):
    """
    Функция старт, в которую передается путь и возвращается уже улучшенный проработанный путь.
    :param path: путь (список узлов).
    :return: list
    """
    print("Calculating by broot force algorythm...\n=================================")

    # Устанавливается число обходов оптимизации по списку узлов
    for k in range(CYCLE_COUNT):
        print(f'  Cycle: {k + 1} / {CYCLE_COUNT}')

        count = MIN_SLICE_LEN

        # Оптимизация для нескольких длинн частей
        while count < MAX_SLICE_LEN:
            list_of_paths = _split_places(path, count)
            list_of_paths = _part_optimizer(list_of_paths)
            path = _path_normalizer(list_of_paths)

            sys.stdout.write("\r" + f'      Step: {count + 1} / {MAX_SLICE_LEN} ({distance_counter(path)})')
            count += 1

        sys.stdout.write("\r")

        # На каждом шаге сдвигаем список на один элемент,
        # для улучшения оптимизации и чтобы функция обработала больше разных вариантов
        path.append(path.pop(0))

    return path


def _split_places(path, counts):
    """
    Функция разделения пути на части.
    :param path: список узлов, путь.
    :param counts: длинна части, на которую необходимо разделить
    :return:
    """
    list_of_paths = [[]]
    counter = 0

    for i in path:
        list_of_paths[counter].append(i)

        if len(list_of_paths[counter]) > counts:
            list_of_paths.append([])
            counter += 1

            # В конце каждой части добавляем первый узел следующей части, чтобы крайние узлы были связующими
            list_of_paths[counter].append(i)

    return list_of_paths


def _part_optimizer(list_of_paths):
    """
    Функция с алгоритмом полного перебора всех варинатов в частах пути, для нахождения лучшей части.
    :param list_of_paths: список частей.
    :return: list[list]
    """
    new_list_of_paths = []

    for i in range(len(list_of_paths)):
        path = []
        dist = 100000

        # Получаем список всех вариаций перестановок узлов
        variants = permutations(list_of_paths[i][1:-1])

        for variant in variants:
            tmp_path = [list_of_paths[i][0]]
            tmp_path.extend(variant)
            tmp_path.append(list_of_paths[i][-1])
            tmp_dist = 0

            # Считаем длинну данного варианта
            for j in range(len(tmp_path)):
                if j != 0:
                    tmp_dist += math.dist([tmp_path[j].cords[0], tmp_path[j].cords[1]],
                                          [tmp_path[j - 1].cords[0], tmp_path[j - 1].cords[1]])
            # Если вариант лучше, оставляем его
            if tmp_dist < dist:
                dist = tmp_dist
                path = tmp_path.copy()

        new_list_of_paths.append(path)

    return new_list_of_paths


def _path_normalizer(list_of_paths):
    """
    Функция для восстановления списка частей пути в нормальный путь.
    :param list_of_paths: список частей пути.
    :return: list
    """
    normal_path = [list_of_paths[0][0]]

    for i in range(len(list_of_paths)):
        normal_path.extend(list_of_paths[i][1:])

    return normal_path
