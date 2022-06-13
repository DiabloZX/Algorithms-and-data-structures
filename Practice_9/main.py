"""
Главный запускаемый модуль для нчеткого поиска подстроки в строке. Запускать этот модуль
"""

import sys
import time
import argparse
from controller import calculate_and_print


def _create_parser():
    """
    Парсер для считывания команд из терминала.
    :return: объект типа ArgumentParser с аргументами для заполнения.
    """
    parse_object = argparse.ArgumentParser()

    parse_object.add_argument(
        '-f', '--file', help='Path to file with string', type=str, required=False)
    parse_object.add_argument(
        '-o', '--output', help='Output type (color, txt, cmd)', type=str, required=True,
        choices=('color', 'file', 'cmd'))
    parse_object.add_argument(
        '-s', '--string', help='String, where find', type=str, required=False)
    parse_object.add_argument(
        '-ss', '--substrings', help='Substrings, what find', type=str, required=True)
    parse_object.add_argument(
        '-c', '--cursive', help='Cursive sensitivity', default=False, type=bool, required=False)
    parse_object.add_argument(
        '-l', '--last', help='Find method (last/first)', default=False, type=bool, required=False)
    parse_object.add_argument(
        '-k', '--count', help='Find first k substring', type=int, required=False)
    parse_object.add_argument(
        '-i', '--inaccuracy', help='Inaccuracy for algorythm', default=1, type=int, required=False)
    parse_object.add_argument(
        '-t', '--threads', help='Count of threads', default=1, type=int, required=False)

    return parse_object


def main():
    """
    Точка входа, начало программы.
    """
    parser = _create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    _arguments_normalizer(namespace)
    _arguments_checker(namespace)

    string = namespace.string
    substrings = tuple(i for i in namespace.substrings.split(','))
    count = int(namespace.count) if namespace.count is not None else -1

    start = time.perf_counter()
    calculate_and_print(string, substrings, namespace.output, count, int(namespace.inaccuracy), int(namespace.threads),
                        bool(namespace.last))
    print("Completed for", int((time.perf_counter() - start) * 100) / 100, "seconds")


def _arguments_normalizer(namespace):
    """
    Функция нормализации параметров для их дальнейшего использования
    :param namespace: парсер с аргументами
    :return: None
    """
    if namespace.file:
        namespace.string = _get_string_from_file(namespace.file)

    if bool(namespace.cursive):
        namespace.string = namespace.string.lower()
        namespace.substrings = namespace.substrings.lower()


def _arguments_checker(namespace):
    """
    Функция для проверки аргументов на корректность
    :param namespace: парсер с аргументами
    :return: None
    """
    for substring in namespace.substrings.split(","):
        if len(namespace.string) < len(substring):
            print("Substring can't be more, than string")
            raise AttributeError

        if len(substring) < int(namespace.inaccuracy):
            print("Threads count can't be more, than string")
            raise AttributeError

    if namespace.count and len(namespace.string) < int(namespace.count):
        print("Entries count can't be more, than string")
        raise AttributeError

    if len(namespace.string) < int(namespace.threads):
        print("Threads count can't be more, than string")
        raise AttributeError

    if namespace.string is None and namespace.file is None:
        print("You must enter string or file with string")
        raise AttributeError


def _get_string_from_file(path: str):
    """
    Функция для получения строки из файла, если введене файл
    :param path: Путь к файлу
    :return: Строка из файла
    """
    with open(path, 'r', encoding='UTF8') as file:
        text = file.read()
        file.close()
    return text


if __name__ == '__main__':
    main()
