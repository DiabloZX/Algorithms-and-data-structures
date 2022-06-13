"""Практическая работа №5 - Внешняя сортировка
*Без потоков
*Без ограничения по памяти"""


import sys
import argparse
import natural_sort
from pathlib import Path


def _create_parser():
    """
    Парсер для считывания команд из терминала
    :return: объект типа ArgumentParser с аргументами для заполнения
    """
    parse_object = argparse.ArgumentParser()
    parse_object.add_argument('-f', '--files', help='Input data paths', type=str, required=True)
    parse_object.add_argument('-o', '--output', help='Output paths', default='', type=str,
                              required=False)
    parse_object.add_argument('-r', '--reversed', help='Boolean for reversed', default='',
                              type=str, required=False)
    parse_object.add_argument('-k', '--key', help='Key function for items', default='',
                              type=str)
    parse_object.add_argument('-sk', '--sortkey', help='Index for csv files', default='',
                              type=str)
    return parse_object


def main():
    """
    Точка входа, начало программы
    :return:
    """
    parser = _create_parser()  # Создаем объект для парсинга
    namespace = parser.parse_args(sys.argv[1:])  # Загружаем в него данные из cmd
    # Разпарсиваем значения по спискам
    input_paths = list(namespace.files.split(','))
    output_paths = list(namespace.output.split(','))
    reverses = list(namespace.reversed.split(','))
    keys = list(namespace.key.split(','))
    sort_keys = list(namespace.sortkey.split(','))

    # Если введено неверное кол-во значений, выдаем ошибку
    if len(input_paths) < len(output_paths) or len(input_paths) < len(reverses) or \
            len(input_paths) < len(keys) or len(input_paths) < len(sort_keys):
        print("Count of non-required parameters can't be more, than paths count")
        raise AttributeError

    for i in range(len(input_paths)):  # Для каждого файла сортируем его
        input_path = Path(input_paths[i])
        output_path = None
        if i < len(output_paths):
            if output_paths[i]:
                output_path = Path(output_paths[i])
        reverse = None
        if i < len(reverses):
            if reverses[i].lower() == 'true':
                reverse = True
            elif reverses[i].lower() == 'false':
                reverse = False
        key = None
        if i < len(keys):
            if keys[i] == 'abs':  # Для примера приведен один вариант парсинга функции
                key = abs
        sort_key = None
        if i < len(sort_keys):
            if sort_keys[i].isdigit():
                sort_key = int(sort_keys[i])
        if not isinstance(sort_key, int) and input_path.suffix == '.csv':
            print('For csv files indexes must be integer, not NoneType')
            raise ValueError
        natural_sort.my_sort(input_path, output_path, reverse, key, sort_key)


if __name__ == '__main__':
    main()
