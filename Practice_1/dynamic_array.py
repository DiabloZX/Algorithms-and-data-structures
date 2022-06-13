"""Модуль динамического массива"""
from array import array
import my_array


class Array:
    """Класс массива"""
    def __init__(self, type_code: str, initializer: list):
        """
        Конструктор класса Array
        :param type_code: символ для определения тип массива
        :type type_code: str
        :param initializer: начальный набор элементов
        :type initializer: list
        """
        if type_code not in ('d', 'i'):
            raise TypeError
        self.type = type_code
        self.c_array = my_array.array(type_code, len(initializer))
        for i, value in enumerate(initializer):
            if not isinstance(value, int) and type_code == 'i':
                raise TypeError
            self.c_array[i] = value

    def append(self, item: float):  # pylint: disable=R0201
        """
        Метод добавления элемента в конец массива
        :param item: элемент, который будет добавлен в конец массива
        :type item: float
        """
        if isinstance(item, int) or self.type != 'i':
            self.c_array.append(item)
        else:
            raise TypeError

    def insert(self, index: int, item: float):  # pylint: disable=R0201
        """
        Метод вставки элемента по индексу
        :param index: индекс, куда будет добавлен элемент
        :type index: int
        :param item: элемент, который будет добавлен массив
        :type item: float
        """
        if isinstance(index, int) and isinstance(item, int) or self.type != 'i':
            self.c_array.insert(index, item)
        else:
            raise TypeError

    def remove(self, item: float):  # pylint: disable=R0201
        """
        Метод удаления первого вхождения элемента в массиве
        :param item: элемент, который будет удалён
        :type item: float
        """
        if isinstance(item, int) or self.type != 'i':
            self.c_array.remove(item)
        else:
            raise TypeError

    def pop(self, index=-1):  # pylint: disable=R0201
        """
        Метод удаления с возвратом элемента по индексу
        :param index: индекс элемента, который будет удалён
        :type index: int
        :return: float
        """
        if not isinstance(index, int):
            raise TypeError
        return self.c_array.pop(index)

    def __str__(self):
        str_out = "["
        for i in range(self.c_array.length):
            if i == self.c_array.length - 1:
                str_out += str(self.c_array[i])
            else:
                str_out += str(self.c_array[i]) + ", "
        str_out += "]"
        return str_out

    def __reversed__(self):
        return self.__class__(self.type, list(reversed(list(self.c_array))))

    def __setitem__(self, index, item):
        if not isinstance(item, int) and type == 'i':
            raise TypeError
        self.c_array[index] = item

    def __getitem__(self, index):
        return self.c_array[index]

    def __len__(self):
        return self.c_array.len()

    def __sizeof__(self):
        return self.c_array.sizeof()

    def __eq__(self, o: object):
        if isinstance(o, array):
            return o.typecode == self.type and list(o) == list(self.c_array)
        return False
