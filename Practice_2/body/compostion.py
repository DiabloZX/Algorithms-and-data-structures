class Composition:
    """Класс предоставляющий композицию"""

    def __init__(self, file=None, length=None, name=None):
        """Инициализация
            Инициализируются поля: путь к файлу и длинна композиции
        """
        self.file = file
        self.length = length
        self.name = name

    def __str__(self):
        """Строковое представление
            Выводит строковое представление файла
            :return Строковое представление файла
        """
        return self.file

    def __eq__(self, other):
        """Метод сравнения
            Сравнивает два объекта по определенным правилам
            :param other: Некий объект с которым сравнивается композиция
            :type other: object
            :return Равны либо Неравны значения этих объектов
        """
        return self.file == other
