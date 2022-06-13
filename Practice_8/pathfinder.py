"""
Модуль для поиска кратчайшего пути среди 6137 населеных пунктов (задача Коммивояжера).
Выполнил студент СФУ ИКИТ группы КИ20-17/2Б Смыков Алексей.
"""

import csv

from node import Node
from Algorythms.distancer import distance_counter
from Algorythms.saver import save
from Algorythms.brootforce import randomcounter
from Algorythms.knn import greed
from Algorythms.ants import antcolony


def main():
    """
    Основная главная функция.
    START HERE.
    :return:
    """
    tmp_file = open('data.csv', 'r', encoding='UTF-8', newline='')
    file = csv.reader(tmp_file)

    i = 0
    nodes = []

    # Переводим записи из таблицы в список узлов
    for row in file:
        if i != 0:
            nodes.append(Node(row[0], row[3], (float(row[5]) / 100, float(row[6]) / 100), row[1], row[2]))

        i += 1

    tmp_file.close()

    """# Далее, пропускаем через муравьиный алгоритм, где указываем сильыне феромоны на начальном пути
    path = antcolony.calculate(nodes)
    print('<!> Ant colony method max result:', distance_counter(path))"""

    # Сначала обрабатываем список через "Жадный алгоритм"
    path = greed.calculate(nodes.copy())
    print('<!> Greed method result:', distance_counter(path))

    # После, для улучшения результата, обрабатываем список через полный перебор на небольших частях
    path = randomcounter.calculate(path)
    print('<!> Broot force method max result:', distance_counter(path))

    save(path)


if __name__ == '__main__':
    main()
