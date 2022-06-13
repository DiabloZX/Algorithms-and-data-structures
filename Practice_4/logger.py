"""Модуль для хранения шагов сортировки"""
import json


def log_updater(array: list = None, current_array_part: list = None, pivot: int = None,
                pivot_right: int = 0, pivot_left: int = 0, current_element: int = None):
    """
    Функция для обновления логов.
    Открывает и закрывает json файл на каждом шаге (надо бы пофиксить)
    :param array: массив значений
    :param current_array_part: выбранная часть массива с опорным элементом
    :param pivot: опорный элемент
    :param pivot_right: оффсет справа
    :param pivot_left: оффсет справа
    :param current_element: элемент, который сравнивается
    :return: None
    """
    try:
        with open("log.json", "r") as file:
            log = json.load(file)
    except Exception:
        log = []
    log.append({"array": array, "current_array_part": current_array_part, "pivot": pivot,
                "pivot_right": pivot_right, "pivot_left": pivot_left,
                "current_element": current_element})

    with open("log.json", "w") as file:
        json.dump(log, file, indent=3)


def clear_log():
    """
    Функция для очистки прошлых логов
    :return: None
    """
    with open("log.json", "w") as file:
        json.dump([], file, indent=3)
