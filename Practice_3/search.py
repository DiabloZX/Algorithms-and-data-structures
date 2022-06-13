"""
Модуль для  поиска подстрок в строке
"""
import typing
import json
from time import time


def _get_prefixes(sub_string: str) -> list:
    """
    Префикс-функция для нахождения значений (максимальной длины совпадающих суффикса и префикса)
    для каждого символа подстроки
    :param sub_string: подстрока, в которой ищем значения
    :return: prefixes массив значений для каждого символа
    """
    ss_length = len(sub_string)
    prefixes = [0] * ss_length
    for ss_index in range(ss_length):  # Определяем значения для каждого символа
        for prefix in range(ss_index - 1):
            # Проверяем суффиксы/префиксы всех длин, кроме длины самой строки длины i
            if sub_string[:prefix] == sub_string[-prefix:]:
                # Если суффикс и префикс совпадают, то заносятся в таблицу, иначе остается 0
                # (последним заносится наибольшее значение)
                prefixes[ss_index] = prefix
    return prefixes


def _find_sub_string_entries(search_string: str, sub_string: str) -> list:
    """
    Функция Кнута-Морриса_Пратта (кмп) для нахождения подстроки в строки
    Данная функция сделана для нахождения всех вхождения подстроки в строку
    :param search_string: строка, в которой ведется поиск
    :param sub_string: подстрока, которую необходимо найти
    :return: entries - массив с индексами вхождений
    """
    s_length = len(search_string)
    ss_length = len(sub_string)
    prefixes = _get_prefixes(sub_string)  # Получаем массив префиксов
    entries = []
    s_current_symbol = ss_current_symbol = 0
    while s_current_symbol < s_length and ss_current_symbol < ss_length:
        if search_string[s_current_symbol] == sub_string[ss_current_symbol]:
            # Если символы строки и подстроки совпадают...
            if ss_current_symbol == ss_length - 1:
                # ...и совпал последний символ подстроки, то добавляем индекс в массив вхождений...
                entries.append(s_current_symbol - ss_length + 1)
                s_current_symbol -= ss_length - 1
                ss_current_symbol = 0
            else:
                # ...иначе идём дальше, искать последний символ подстроки
                ss_current_symbol += 1
            s_current_symbol += 1  # В любом случае идем по следующему символу строки
        elif ss_current_symbol:
            # Если символы строки и подстроки не совпали и это не первый символ подстроки...
            ss_current_symbol = prefixes[ss_current_symbol-1]  # ...то шагаем на значение префикса
        else:
            # В любом другом случае шагаем на 1
            s_current_symbol += 1
    return entries


def _search_method_checker(search_string, sub_string, search_method, count):
    """
    Функция для проверки метода поиска: с конца / с начала
    """
    if not count or count > len(search_string):
        count = len(search_string)
    if search_method == "last":
        return _find_sub_string_entries(search_string, sub_string)[::-1][:count]
    return _find_sub_string_entries(search_string, sub_string)[:count]


def _case_sensitivity_checker(search_string, sub_string, search_case_sensitivity, search_method,
                              count):
    """
    Функция для проверки чувствительности регистра
    """
    if not search_case_sensitivity:
        # Если проверка не чувствительна к регистру, делаем всё одного регистра
        search_string = search_string.lower()
        sub_string = sub_string.lower()
    return _search_method_checker(search_string, sub_string, search_method, count)


def _timer(function):
    """
    Декоратор для логирования времени выполнения функции
    """
    def function_decorator(string: str, sub_string: typing.Union[str, tuple],
                           case_sensitivity: bool = False, method: str = 'first',
                           count: typing.Optional[int] = None):
        start = time()
        time_dictionary = {"start_time": start * 1000}
        result = function(string, sub_string, case_sensitivity,
                          method, count)
        time_dictionary["time"] = start * 1000
        with open("time.json", "w") as file:
            json.dump(time_dictionary, file, indent=3)
        return result
    return function_decorator


@_timer
def search(search_string: str,
           sub_string: typing.Union[str, list[str]],
           search_case_sensitivity: bool = False,
           search_method: str = 'first',
           count: typing.Optional[int] = None) -> \
        typing.Optional[typing.Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция для поиска подстрок из списка подстрок и со всеми настройками, возвращает словарь
    подстрок с их индексами или просто кортеж индексов для одной погдстроки
    :param search_string: сама строка
    :param sub_string: подстроки
    :param search_case_sensitivity: чувствительность к регистру (да/нет)
    :param search_method: с какой стороны идти (с начала/с конца)
    :param count: кол-во первых дений подстрок
    :return: substrings_indexes
    """
    if not search_string or not sub_string:
        return None

    if isinstance(sub_string, str):
        # Если одна подстрока
        if len(search_string) < len(sub_string):
            return None
        return tuple(_case_sensitivity_checker(search_string, sub_string, search_case_sensitivity,
                                               search_method, count))

    ss_dict = {}
    for each_sub_string in sub_string:
        # Если массив подстрок
        if len(search_string) < len(each_sub_string):
            ss_dict[each_sub_string] = None
            continue
        ss_dict[each_sub_string] = tuple(_case_sensitivity_checker(search_string, each_sub_string,
                                         search_case_sensitivity, search_method, count))
    return ss_dict


