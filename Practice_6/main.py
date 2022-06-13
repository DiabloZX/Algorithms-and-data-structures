"""
Модуль main для запуска программы.
Практическая работа №6 - сжатие изображения с помощью квадродерева.
Выполнил студент группы КИ20-17/2Б Смыков Алексей.
"""

import sys
import time
import argparse

from image_compressor import compress_and_show


def _create_parser():
    """
    Парсер для считывания команд из терминала.
    :return: объект типа ArgumentParser с аргументами для заполнения.
    """
    parse_object = argparse.ArgumentParser()
    parse_object.add_argument('-i', '--image', help='Path to image', type=str, required=True)
    parse_object.add_argument('-l', '--level', help='Compress depth (0-8 is recommended)',
                              default=0, type=int,  required=False)
    parse_object.add_argument('-c', '--compress', help='Image compress ratio (0-10)',
                              default=0,  type=int, required=False)
    parse_object.add_argument('-b', '--borders', help='Add borders to quadtree',
                              default=False, type=bool, required=False)
    parse_object.add_argument('-g', '--gif', help='Create gif after compress',
                              default=False, type=str, required=False)
    return parse_object


def main():
    """
    Точка входа, начало программы.
    """
    parser = _create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    start = time.perf_counter()
    compress_and_show(namespace.image, namespace.level, namespace.compress, namespace.borders,
                      namespace.gif)
    print("Completed for", time.perf_counter() - start)


if __name__ == '__main__':
    main()
