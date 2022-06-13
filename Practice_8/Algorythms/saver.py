"""
Модуль описывающий сохранение пути в .csv.
"""

import csv

from .distancer import dist


def save(nodes):
    """
    Функция сохранения пути в .csv файл с id населеного пункта и растоянием между каждым из узлов пути.
    :param nodes: путь с узлами.
    :return: None
    """
    print("Saving...")
    tmp_file = open('path.csv', 'w', encoding='UTF-8', newline='')
    file = csv.writer(tmp_file)

    file.writerow(['Id', 'Predicted'])

    for i in range(len(nodes) - 1):
        file.writerow([nodes[i].id, str(dist(nodes[i], nodes[i + 1]))])

    # Также не забываем сохранить связь последнего узла с первым для завершения полного цикла
    file.writerow([nodes[len(nodes) - 1].id, str(dist(nodes[len(nodes) - 1], nodes[0]))])
    tmp_file.close()


def save_ant_colony_setup(q, w, e, r, t, y, u, i, score):
    tmp_file = open('./ants.csv', 'a', encoding='UTF-8', newline='')
    file = csv.writer(tmp_file)

    file.writerow([q, w, e, r, t, y, u, i, score])

    tmp_file.close()
