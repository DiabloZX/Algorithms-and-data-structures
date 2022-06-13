"""
Модуль реализации "Жадного алгоритма"
"""

import sys
from ..distancer import *


def calculate(nodes):
    """
    Главная функция, которая все считает и возвращает уже готовый путь.
    :param nodes: изначальный несвязный список узлов.
    :return: list готовый путь
    """
    print("Calculating by greed algorythm...\n=================================")
    path = [nodes.pop(0)]

    # Для красивого вывода прогресса в консоль
    step = 1
    progress = 0
    max_progress = len(nodes) + 1

    while nodes:
        sys.stdout.write("\r" + f'  Step: {step + 1} / {max_progress}')

        # Находим близжайший узел с головы
        head = _found_nearest(nodes, path[len(path) - 1])
        dist_head = dist(path[len(path) - 1], head)

        # Находим близжайший узел с хвоста
        tail = _found_nearest(nodes, path[0])
        dist_tail = dist(path[0], tail)

        # Добавляем в путь близжайший из двух узлов, удаляя его из списка доступных узлов
        if dist_head < dist_tail:
            path.append(head)
            nodes.remove(head)
        else:
            path.insert(0, tail)
            nodes.remove(tail)

        step += 1

    print()
    return path


def _found_nearest(nodes, current):
    """
    Функция поиска близжайшего к узлу соседа.
    :param nodes: список возможных соседей.
    :param current: узел, к которому ищем близжайшего.
    :return: node близжайший сосед.
    """
    min_distance = 10000
    min_node = nodes[0]

    for i in range(len(nodes)):
        tmp_dist = dist(nodes[i], current)

        if tmp_dist < min_distance:
            min_distance = tmp_dist
            min_node = nodes[i]

    return min_node
