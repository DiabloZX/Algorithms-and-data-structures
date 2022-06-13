"""
Модуль, который содержит функции для нечеткого поиска подстрок в строке с помощью алгоритма левентшеина и
вспомогательного алгоритма Ландау-Вишкина
"""

import numpy as np

ADD_OPERATION = 'a'
DELETE_OPERATION = 'd'
CHANGE_OPERATION = 'c'

ADD_COST = 1
DELETE_COST = 1
CHANGE_COST = 1


def find_substring_cords(string: str,
                         substring: str,
                         max_inaccuracy: int = 1) -> tuple:
    """
    Метод нечеткого поиска. Использует модификацию
    алгоритма Левенштейна.
    :param string: Строка, в котрой проводить поиск
    :param substring: Подстрока для поиска
    :param max_inaccuracy: Порог различий подстроки и строки
    :return: Индексы подстрок, найденных нечетким поиском
    """

    inaccuracy_matrix = _create_matrix(substring, string)
    last_row = _get_last_row(inaccuracy_matrix, substring, string)
    substring_cords = _get_substring_cords(inaccuracy_matrix, last_row, max_inaccuracy)

    return substring_cords


def _create_matrix(substring, string):
    inaccuracy_matrix = np.full((len(substring) + 1, len(string) + 1), np.str)
    inaccuracy_matrix[:, 0] = ADD_OPERATION
    inaccuracy_matrix[0, :] = 0

    return inaccuracy_matrix


def _get_substring_cords(inaccuracy_matrix, last_row, max_inaccuracy):

    # Получение индексов конца найденных подстрок
    end_indexes = []
    for i in range(len(last_row)):
        if last_row[i] <= max_inaccuracy:
            end_indexes.append(i)

    # Получение индексов начала найденных подстрок
    start_indexes = _get_substring_starts(inaccuracy_matrix, end_indexes)

    for index in end_indexes:
        index -= 1

    return [cords for cords in zip(start_indexes, end_indexes)]


def _get_substring_starts(inaccuracy_matrix, end_indexes: list) -> list:
    """
    Поиск начала подстрок,
    используя индексы их конца
    :param end_indexes: Массив индексов конца строк
    :return: Индексы начала подстрок
    """
    substring_starts = []

    for index in end_indexes:
        cords = {"row": inaccuracy_matrix.shape[0] - 1, "column": index}
        target_value = inaccuracy_matrix[cords["row"], cords["column"]]

        # Пока не сместимся в самую первую строку
        while target_value != 0:

            # Далее идут обратные переходы по таблице переходов
            if target_value == CHANGE_OPERATION:
                cords["row"] -= 1
                cords["column"] -= 1

            elif target_value == ADD_OPERATION:
                cords["row"] -= 1

            elif target_value == DELETE_OPERATION:
                cords["row"] -= 1

            target_value = inaccuracy_matrix[cords["row"], cords["column"]]

        # Колонка в которую мы пришли, и будет начальным индексом
        substring_starts.append(cords["column"])

    return substring_starts


def _get_last_row(inaccuracy_matrix, substring, string):
    string_length = len(string)
    substring_length = len(substring)
    second_row = [0] * (string_length + 1)

    for substring_index in range(1, substring_length + 1):
        first_row = second_row
        second_row = [substring_index] + [0] * string_length

        for string_index in range(1, string_length + 1):
            min_cost = first_row[string_index] + ADD_COST
            inaccuracy_matrix[substring_index, string_index] = ADD_OPERATION
            delete_cost = second_row[string_index - 1] + DELETE_COST
            if min_cost > delete_cost:
                min_cost = delete_cost
                inaccuracy_matrix[substring_index, string_index] = DELETE_OPERATION

            change_cost = first_row[string_index - 1] + (CHANGE_COST if string[string_index - 1] != substring[substring_index - 1]
                                                         else 0)

            if min_cost > change_cost:
                min_cost = change_cost
                inaccuracy_matrix[substring_index, string_index] = CHANGE_OPERATION

            second_row[string_index] = min_cost

    return np.array(second_row)
