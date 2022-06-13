"""Практическая работа №4 - Сортировка и визуализация"""
import sys
import argparse
import my_sort
import json
import sort_visualization


def _create_parser():
    """
    Парсер для считывания команд из терминала
    :return: объект типа ArgumentParser с аргументами для заполнения
    """
    parse_object = argparse.ArgumentParser()
    parse_object.add_argument('-f', '--file', help='Path to file with data', default=None, type=str)
    parse_object.add_argument('-l', '--input_list', help='input list data', default=None, type=str)
    parse_object.add_argument('-r', '--reversed', help='Boolean for reversed', default=False,
                              type=bool)
    parse_object.add_argument('-k', '--key', help='Key function for list', default=None,
                              type=callable)
    parse_object.add_argument('-c', '--cmp', help='Cmp function for sorting', default=None,
                              type=callable)
    parse_object.add_argument('--list', default=None, type=list)
    return parse_object


if __name__ == '__main__':
    parser = _create_parser()  # Создаем объект для парсинга
    namespace = parser.parse_args(sys.argv[1:])  # Загружаем в него данные из cmd
    if namespace.input_list:  # Если введен массив с консоли
        namespace.list = [int(item) if item.isdigit() or (item[1:].isdigit() and item[0] == '-')
                          else item for item in namespace.input_list.split(',')]
    if namespace.file:  # Если введен файл (имя файла)
        file = open(namespace.file, 'r')
        namespace.list = [int(item) if item.isdigit() or (item[1:].isdigit() and item[0] == '-')
                          else item for item in file.read().split(',')]
        file.close()

    # Заполняем обычный массив, переводя из str в int, если всё значения - числа
    namespace.list = namespace.list if all(isinstance(each, int) for each in namespace.list) else \
        list(map(str, namespace.list))

    # Получаем сам уже отсортированный массив
    results = my_sort.my_sort(namespace.list, namespace.reversed, namespace.key, namespace.cmp)

    # Выводим отсортированный массив в консоль (почему бы нет, удобнее смотреть)
    print(results)

    # Записываем результат в файл
    with open("results.json", "w") as file:
        json.dump(results, file, indent=3)
    with open("log.json", "r") as file:
        sort_visualization.visualize(json.load(file))
