"""
Модуль узла для работы с лабиринтом.
"""


class Node:
    """
    Класс узла для связи координат и флага о состоянии узла
    """

    def __init__(self, cords: tuple[int, int], color: list[int, int, int]):
        """
        :param cords: координаты для узла.
        """
        self._cords = cords
        self._color = color
        self._checked = False

    @property
    def cords(self):
        """
        Условие для получения данных об узле.
        :return: tuple[int, int] _cords координаты об узле
        """
        return self._cords

    @property
    def color(self):
        """
        Условие для получения данных об узле.
        :return: list[int, int, int] _color цвет клетки
        """
        return self._color

    @color.setter
    def color(self, color: list[int, int, int]):
        """
        Условие для установки данных об узле.
        """
        self._color = color

    @property
    def checked(self):
        """
        Условие для получения данных об узле.
        :return: bool _in_maze флаг о состоянии узла
        """
        return self._checked

    @checked.setter
    def checked(self, state: bool):
        """
        Условие для установки данных об узле.
        """
        self._checked = state
