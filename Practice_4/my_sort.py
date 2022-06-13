"""Модуль сортировки"""
import logger
from typing import Optional, Union
from random import randint, shuffle


def my_sort(array: list, reverse: bool = False,
            key: Optional[callable] = None, cmp: Optional[callable] = None) -> list:
    """
    Функция сортировки. Получает массив значений int/str.
    :param array: сам массив значений
    :param reverse: если нужно считать с конца
    :param key: функция для обработки каждого значений
    :param cmp: кастомная функция для сравнения
    :return: возвращает list отсортированных значений
    """
    shuffle(array)  # Перемешиваем массив для более разнообразноо начального представления
    logger.clear_log()  # Очищаем прошлые логи сортировки
    logger.log_updater(array=array)  # Добавляем начальное значенения массива
    if key:  # Если есть функция key
        for index in range(len(array)):
            array[index] = key(array[index])
    if not cmp:  # Если нет кастомной функции сравнения, применяется базовая
        cmp = _default_cmp
    if array:  # Если массив не пустой
        results = _quick_sort(array, array, reverse, cmp)
    else:
        results = []
    logger.log_updater(array=results)  # Обновляем конечное значение отсортированного массива
    return results


def _default_cmp(first_item: Union[int, str], second_item: Union[int, str]) -> bool:
    """
    Базовая функция сравнения двух значений.
    :param first_item: первое значение
    :param second_item: второе значение
    :return: bool. Возвращает True, если первое значение не меньше второго.
    """
    return first_item >= second_item


def _quick_sort(array: list, current_array_part: list = None, reverse: bool = False,
                cmp: Optional[callable] = None, pivot_left: int = 0, pivot_right: int = 0) -> list:
    """
    Функция быстрой сортировки
    :param array:  весь массив значений
    :param current_array_part: конкретная часть, в которой выбирается опорный элемент
    :param reverse: если сортировка по невозрастанию
    :param cmp: функция сравнения
    :param pivot_left: расстояние слева от  массива до начала выбранной части с опорным элементом
    :param pivot_right: расстояние справа от выбранной части с опорным элементом до начала массива
    :return: выбранную часть с опорным элементом, но уже отсортированную
    """

    # Случайным образом выбираем опорный элемент
    pivot = randint(0, len(current_array_part) - 1)

    # До какого значения нужно проходить проверку элементов с опорным
    distance = len(current_array_part)
    i = 0
    while i < distance:
        # Сохраняем значения в логи
        logger.log_updater(array=array,  current_array_part=current_array_part, pivot=pivot,
                           pivot_right=pivot_right, pivot_left=pivot_left, current_element=i)
        if i < pivot and (reverse != cmp(current_array_part[i], current_array_part[pivot])):
            current_array_part.insert(len(current_array_part) - 1, current_array_part.pop(i))
            pivot -= 1
            distance -= 1
            i -= 1
        elif i > pivot and (reverse == cmp(current_array_part[i], current_array_part[pivot])):
            current_array_part.insert(0, current_array_part.pop(i))
            pivot += 1
        i += 1

    # Применяем отсортированную выбранную часть к начальному массиву
    for j in range(len(current_array_part)):
        array[j + pivot_left] = current_array_part[j]

    # Обновляем оффсеты для выбранной части уже до и после опорного элемента
    pivot_right += (len(current_array_part) - 1 - pivot)
    pivot_left += pivot
    if pivot > 1:
        current_array_part[:pivot] = _quick_sort(array, current_array_part[:pivot], reverse, cmp,
                                                 pivot_left - pivot, pivot_right + 1)
    if pivot < len(current_array_part) - 2:
        current_array_part[pivot + 1:] = _quick_sort(array, current_array_part[pivot + 1:],
                                                     reverse, cmp, pivot_left + 1,
                                                     pivot_right - (len(current_array_part) - 1 -
                                                                    pivot))

    return current_array_part
