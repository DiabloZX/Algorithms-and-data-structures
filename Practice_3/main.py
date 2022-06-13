import search
import sys
import argparse
import json

from colorama import Fore, init
from time import time


COLORS = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
]


def _int_input(low_border: int, max_border: int, text: str) -> int:
    """
    Функция для ввода целого числа
    :param low_border: нижняя граница для числа
    :param max_border: верхняя граница для числа
    :param text: текст-подсказка при вводе, что за число нужно ввести
    :return: number
    """
    while True:
        try:
            number = int(input(text))
            try:
                low_border <= number <= max_border
            except IndexError:
                print(f"Неверный диапазон! От {low_border} до {max_border}\n")
        except TypeError:
            print("Это не целое число!\n")
        else:
            return number


def _get_time():
    """
    Функция вывода времени выполнения
    Выводит время поиска подстрок и время разукрашивания и вывода строки на экран
    """
    with open('time.json', 'r') as file:
        time_dict = json.load(file)
        print("Sub string found in:", time_dict["time"] - time_dict["start_time"])
        print("String colored and printed in:", time() * 1000 - time_dict["time"])


def _string_painter(string: str, sub_strings: list, sub_strings_entries: dict) -> str:
    """
    Разукразчик строки
    Разукрашивает строку в цветные части, исходя из подстрок
    :param string: строка, которую надо разукрасить
    :param sub_strings: подстроки, будут использоваться для определения цвета покраски
    :param sub_strings_entries: индексы вхождения подстрок в строку
    :return: разукрашенная строка colour_string
    """
    colour_string = ""
    for symbol_index in range(len(string)):
        yes = False
        index = 0
        for i in range(len(sub_strings_entries)):
            # Определяем в какой подстроке может содержаться символ
            substring_string = str(sub_strings[i])
            if sub_strings_entries[substring_string] is not None:
                for j in sub_strings_entries[substring_string]:
                    # Проверяются индексы вхождения для данной подстроки
                    if j <= symbol_index < j + len(substring_string):
                        # Если символ содержится в диапазоне от начала подстроки и до ее конца,
                        # то он в ней
                        yes = True
                        index = i
        if yes:
            # Если символ содержится в какой-нибудь найденной подстроке
            colour_string += str(COLORS[index % len(COLORS)]) + string[symbol_index] + Fore.RESET
        else:
            # Если символ не содержится в подстроке
            colour_string += string[symbol_index]
    return colour_string


def _create_parser():
    """
    Парсер для считывания команд из терминала
    :return:
    """
    parse_object = argparse.ArgumentParser()
    parse_object.add_argument('-f', '--file', default=None, type=str)
    parse_object.add_argument('-l', '--string', default='', type=str)
    parse_object.add_argument('-ss', '--substring', nargs='+', type=str)
    parse_object.add_argument('-c', '--case', default=True, type=bool)
    parse_object.add_argument('-m', '--method', choices=['first', 'last'], default='first',
                              type=str)
    parse_object.add_argument('-k', '--count', nargs='?', default=1, type=int)

    return parse_object


if __name__ == '__main__':
    init()
    parser = _create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.file:
        f = open(namespace.file, 'r')
        namespace.string = f.read()
        f.close()
    results = search.search(namespace.string, namespace.substring, namespace.case, namespace.method,
                            namespace.count)
    if isinstance(results, tuple):
        results = {namespace.substring: results}
    color_string = _string_painter(namespace.string, namespace.substring, results)
    print("\n" + color_string)
    _get_time()
