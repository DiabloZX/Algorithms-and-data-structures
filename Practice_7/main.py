"""
Модуль main для запуска программы.
Практическая работа №7 - построение лабиринта и поиск пути.
Выполнил студент группы КИ20-17/2Б Смыков Алексей.
"""

import sys
import time
import argparse

from maze_maker import Maze


def _create_parser():
    """
    Парсер для считывания команд из терминала.
    :return: объект типа ArgumentParser с аргументами для заполнения.
    """
    parse_object = argparse.ArgumentParser()

    parse_object.add_argument(
        '-i', '--input_path', help='Path to saved maze', type=str, required=False)
    parse_object.add_argument(
        '-o', '--output_path', help='Path to save maze', type=str,  required=True)
    parse_object.add_argument(
        '-he', '--height', help='Height of maze', type=int, required=False)
    parse_object.add_argument(
        '-wi', '--width', help='Width of maze', type=int,  required=False)
    parse_object.add_argument(
        '-s', '--solve', help='Solve maze after creating', type=bool, required=False)
    parse_object.add_argument(
        '-g', '--gif', help='Create gif after program',  default=False, type=bool, required=False)

    return parse_object


def main():
    """
    Точка входа, начало программы.
    """
    parser = _create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if (not namespace.height or not namespace.width) + (not namespace.input_path) != 1:
        print("Error! Must be input path or maze parameters for generation new!")
        return

    start = time.perf_counter()
    if namespace.input_path:
        maze = Maze()
        maze.load(namespace.input_path)
    else:
        maze = Maze(namespace.height, namespace.width)
        maze.build(namespace.gif)
    if namespace.solve:
        maze.solve(namespace.gif)
    if namespace.gif:
        maze.gif(namespace.output_path)
    maze.save(namespace.output_path)
    print("Completed for", int((time.perf_counter() - start) * 100) / 100, "seconds")


if __name__ == '__main__':
    main()
