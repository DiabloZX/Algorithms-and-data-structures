"""
Модуль списка узлов.
"""


class NodeList (list):
    """
    Класс списка узлов для более удобного обращения к узлам.
    Наследуется от класса списка.
    """
    def __init__(self):
        super().__init__()

    def add_row(self):
        """
        Функция добавления новой строки.
        :return: None.
        """
        self.append([])

    def get_item(self, cords: tuple, x_offset: int = 0, y_offset: int = 0):
        """
        Функция для удобного получения узла по координатам.
        :param cords: координаты узла, которого нужно получить из двумерного списка.
        :param x_offset: смещение по координатам по x.
        :param y_offset: смещение по координатам по y.
        :return: значение списка в полученных координатах.
        """
        return self[cords[0] + x_offset][cords[1] + y_offset]

    def get_item_between(self, cords_1: tuple, cords_2: tuple):
        """
        Функция для получения узла, лежащего между двумя координатами.
        Используется для получения координат стены, так как имеем координаты соседних узлов.
        :param cords_1: координаты первого узла.
        :param cords_2: координаты второго узла.
        :return: значение списка в координатах между двумя полученными.
        """
        return self[int((cords_1[0] + cords_2[0]) / 2)][int((cords_1[1] + cords_2[1]) / 2)]

    def set_item(self, cords: tuple, item):
        """
        Функция для установления новых параметров уже имеющемуся узлу.
        :param cords: координаты узла в двумерном списке.
        :param item: новое значение.
        :return: None.
        """
        self[cords[0]][cords[1]] = item

    def clear(self):
        """
        Функция очистки списка.
        :return: None.
        """
        super().__init__()
