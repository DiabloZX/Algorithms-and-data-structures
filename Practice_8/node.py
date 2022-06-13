"""
Модуль реализации узла для хранения данных.
"""


class Node:
    """
    Класс узла для связи координат и флага о состоянии узла, а также других данных.
    """

    def __init__(self, node_id: str, name: str, cords: tuple = None, region: str = None, municipality: str = None):
        """
        Функция инициализации.
        :param node_id: айди населеного пункта из эксель-таблицы.
        :param name: название населеного пункта.
        :param cords: его координаты (как кортеж из двух элементов).
        :param region: регион населеного пункта.
        :param municipality: и его муниципалитет.
        """
        self._id = node_id
        self._name = name
        self._cords = cords
        self._region = region
        self._municipality = municipality

    @property
    def id(self):
        """
        Условие для получения данных об узле.
        :return: str _id айди узла.
        """
        return self._id

    @property
    def name(self):
        """
        Условие для получения данных об узле.
        :return: str _name название узла.
        """
        return self._name

    @property
    def cords(self):
        """
        Условие для получения данных об узле.
        :return: tuple[int, int] _cords координаты об узле.
        """
        return self._cords

    @property
    def region(self):
        """
        Условие для получения данных об узле.
        :return: str _region регион узла.
        """
        return self._region

    @property
    def municipality(self):
        """
        Условие для получения данных об узле.
        :return: str _region муниципалитет узла.
        """
        return self._municipality
