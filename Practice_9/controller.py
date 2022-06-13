"""
Модуль для обработки аргументов и управления выходными данными модуля поиска подстрок,
также управялет выводом результата
"""

import numpy as np
import concurrent.futures

from colorama import init, Fore
from fuzzy_search import find_substring_cords

COLORS = list(vars(Fore).values())
del COLORS[4]
del COLORS[-3]

CMD = "cmd"
COLORED = "color"
FILE = "file"
OUTPUT_FILE = "result.txt"


def calculate_and_print(string: str, substrings: str, output_type: str, entries_count: int, inaccuracy: int,
                        threads_count: int, reverse: bool) -> None:
    """
    Вызываемая функция контроллера для поиска подстрок и обработки результата
    :return: None
    """

    # Инициализация раскрашивателя
    init()

    # Поиск подстрок с помощью потоков
    string_slices = list(_splitter(string, threads_count))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures_generator = (
            executor.submit(
                _find_substring_cords,
                string_slice,
                substrings,
                inaccuracy
            )
            for string_slice in string_slices)
        result_matrix = [result.result() for result in futures_generator]

        string_slice_count = 0
        cords = []
        for data_index, result in enumerate(result_matrix):
            for res in result:
                res = np.array(res)
                res += string_slice_count
                cords.append(res)
            string_slice_count += len(string_slices[data_index])

    # В случае реверса, будем брать результаты в обратном порядке
    if reverse:
        cords = list(reversed(cords))

    # Если указано количество вхождений, то берем только их
    if entries_count != -1:
        cords = cords[:entries_count]

    if not cords:
        print("No substrings")

    # Обработка результата в зависимости от типа вывода
    if output_type == CMD:
        _cmd_output(cords, string)
    elif output_type == COLORED:
        _color_output(cords, string)
    else:
        _file_output(cords, string)


def _find_substring_cords(string: str,
                          substrings: tuple,
                          inaccuracy: int) -> list:
    """
    Функция, в которой используется модуль нечеткого поиска.
    В этот модуль отправляются параметры строки, подстроки и нечеткость,
    на выход получаем координаты вхождений подстроки
    :param string: строка, где ищем
    :param substrings: подстрока, что ищем
    :param inaccuracy: нечеткость
    :return: список координат начала и конца подстроки
    """
    cords = []
    for substring in substrings:
        cords_for_current_substring = find_substring_cords(string, substring, inaccuracy)
        cords += cords_for_current_substring
    return cords


def _splitter(string: str, part_count: int):
    """
    Разбивает строки на n частей
    :param string: Строка для разбиения
    :param part_count: Количество разбиений
    :return: Итерaтор разбитых строк
    """
    part_size = len(string) // part_count
    if len(string) % part_count:
        part_size += 1

    iterator = iter(string)

    for _ in range(part_count):
        accumulator = list()
        for _ in range(part_size):
            try:
                accumulator.append(next(iterator))
            except StopIteration:
                break
        yield ''.join(accumulator)


def _color_output(cords: np.array, string: str):
    """
    Выводит текст в консоль, раскрашивая подстроки которые были найдены
    :param cords: Словарь координат начала и конца подстрок в строке
    :param string: Сама строка в которой был поиск
    :return: None
    """
    result = ''
    for i in range(len(string)):
        symbol = string[i]
        for j in range(len(cords)):
            if cords[j][0] <= i < cords[j][1]:
                symbol = COLORS[j % len(COLORS)] + string[i] + Fore.RESET
        result += symbol
    print(result)


def _file_output(cords: np.array, string: str):
    """
    Выводит найденные подстроки в файл
    :param cords: Массив координат вхождений
    :param string: Строка, в которй происходил поиск
    :return: None
    """
    with open(OUTPUT_FILE, "w") as file:
        for current_cords in cords:
            file.write(f"{string[current_cords[0]: current_cords[1] + 1]} ")
        print("Saved in 'result.txt'")


def _cmd_output(cords: np.array, string: str):
    """
    Вывод найденных подстрок в консоль
    :param cords: Массив индексов вхождений
    :param string: Строка, в которй происходил поиск
    :return: None
    """
    for current_cords in cords:
        print(string[current_cords[0]: current_cords[1]], end=" ")
    print()
