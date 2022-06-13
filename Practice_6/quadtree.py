"""
Модуль для квадродерева с классами узла и самого квадродерева.
"""

from typing import Optional
import numpy as np

ROOTS_IN_TREE = 4


class Node:
    """
    Класс узла, хранит в себе данные, которые являются обязательными при создании узла.
    Имеет геттер-методы для каждого поля.
    """

    def __init__(self, img: np.ndarray, mean_color: np.ndarray, cords_south_west: tuple,
                 cords_north_east: tuple) -> None:
        self._img = img
        self._mean_color = mean_color
        self._cords_south_west = cords_south_west
        self._cords_north_east = cords_north_east

        width = img.shape[0]
        height = img.shape[1]

        self._cords_south_west_for_roots = \
            [(cords_south_west[0] + height / 2, cords_south_west[1]),
             (cords_south_west[0] + height / 2, cords_south_west[1] + width / 2),
             (cords_south_west[0], cords_south_west[1]),
             (cords_south_west[0], cords_south_west[1] + width / 2)]
        self._cords_north_east_for_roots = \
            [(cords_north_east[0], cords_north_east[1] - width / 2),
             (cords_north_east[0], cords_north_east[1]),
             (cords_north_east[0] - height / 2, cords_north_east[1] - width / 2),
             (cords_north_east[0] - height / 2, cords_north_east[1])]

    @property
    def img(self):
        """
        Геттер-свойство для обращения к полю.
        :return: np.ndarray - изображение, содержащееся в узле.
        """
        return self._img

    @property
    def mean_color(self):
        """
        Геттер-свойство для обращения к полю.
        :return: np.ndarray - средний цвет изображения, содержащееся в узле.
        """
        return self._mean_color

    @property
    def cords_south_west(self):
        """
        Геттер-свойство для обращения к полю.
        :return: tuple - координаты левого нижнего угла квадродерева.
        """
        return self._cords_south_west

    @property
    def cords_north_east(self):
        """
        Геттер-свойство для обращения к полю.
        :return: tuple - координаты правого верхнего угла квадродерева.
        """
        return self._cords_north_east

    @property
    def cords_south_west_for_roots(self):
        """
        Геттер-свойство для обращения к полю.
        :return: list - список координат левого нижнего угла корней квадродерева.
        """
        return self._cords_south_west_for_roots

    @property
    def cords_north_east_for_roots(self):
        """
        Геттер-свойство для обращения к полю.
        :return: list - список координат правого верхнего угла корней квадродерева.
        """
        return self._cords_north_east_for_roots


class QuadTree:
    """
    Класс Квадродерева.
    Имеет информацию о главном родительском узле и 4 дочерних узла, корня (roots).
    В дереве может храниться либо информация о главном узле, если нет дочерних узлов-корней,
    либо узлы-корни и, соответственно, информация в каждом из них,
    не может одновременно быть информация о главном узле и корни
    """

    def __init__(self):
        self._data = None
        self._final = True
        self._roots = [None] * 4

    @property
    def data(self) -> Optional[Node]:
        """
        Геттер-свойство для обращения к полю.
        :return: Node - поле, содержащее узел с информацией.
        """
        return self._data

    @data.setter
    def data(self, data: Node):
        """
        Сеттер-свойство для обращения к полю.
        :return: Node - узел, содержащий информацию.
        """
        self.clear_roots(data)

    @property
    def final(self) -> bool:
        """
        Геттер-свойство для обращения к полю.
        :return: bool - флаг, последний ли это узел в глубину, или есть еще корни.
        """
        return self._final

    @property
    def roots(self) -> list:
        """
        Геттер-свойство для обращения к полю.
        :return: list - список корней квадродерева.
        """
        return self._roots

    @roots.setter
    def roots(self, roots_data: list):
        """
        Сеттер-свойство для обращения к полю.
        :return: list - список узлов с информацией для корней квадродерева.
        """
        self.create_roots(roots_data)

    def clear_roots(self, data: Node):
        """
        Функция очистки дочерних узлов, в таких случаях должна появляться информация о главном
        родительском узле.
        :param data: Информация, которая будет записана в self.data, информация о главном узле.
        """
        for i in range(ROOTS_IN_TREE):
            self.roots[i] = None
        self._final = True
        self._data = data

    def create_roots(self, roots_data: list):
        """
        Функция для создания корней.
        В таком случае удаляется информация о главном узле и информация в каждом корне должна быть,
        так как это конечный узел.
        :param roots_data: Информация, которая будет записана в узлы (в главный узел для каждого
        дочернего дерева, т.к. каждый корень уже является самостоятельным деревом с главным узлом).
        """
        self._data = None
        self._final = False
        for i in range(ROOTS_IN_TREE):
            self.roots[i] = QuadTree()
            self.roots[i].data = roots_data[i]

    def get_all_roots_data(self) -> list:
        """
        Функция для получения списка информации о всех узлах, входящих в область дерева.
        :return: list - список информации об узлах
        """
        roots = []
        if not self._final:
            for i in range(ROOTS_IN_TREE):
                root_cords = self.roots[i].get_all_roots_data()
                for j in root_cords:
                    roots.append(j)
        else:
            roots.append(self.data)
        return roots
