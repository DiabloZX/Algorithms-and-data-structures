"""Модуль внешней сортировки, через сортировку естественным слиянием"""
from typing import Union, Optional, Callable
from pathlib import Path
import csv

PathType = Union[str, Path]
_RESULTS_PATH = 'results'  # Временный файл для промежуточного результата
_F1 = 'f1'  # Вспомогательный файл для разделения №1
_F2 = 'f2'  # Вспомогательный файл для разделения №2
_TXT = '.txt'
_CSV = '.csv'


def my_sort(src: PathType, output: Optional[PathType] = None, reverse: bool = False,
            key: Optional[Callable] = None, data_key: Optional[int] = None) -> None:
    """
    Функция внешней сортировки
    :param src: Путь к файлу, который нужно отсортировать
    :param output: Путь к файлу, в который нужно сохранить результат (Если None - Сохраняет в
    исходном)
    :param reverse: Сортровка по убыванию/возрастанию
    :param key: Функция применяющаяся перед сравнением элементов
    :param data_key: Индекс столбца в CSV файле
    :return: None
    """
    input_file_type = src.suffix
    if not output:
        output = src  # Если выходной путь не указан, результат записываем в исходный файл
    output_file_type = output.suffix
    if not key:
        key = _default_key
    _key_applicator(key, input_file_type, src, data_key)
    i = 0
    # Сортируем, пока файл не отсортирован
    while not _sort_condition(input_file_type, reverse, data_key) and i < 50:
        print("hiu")
        i += 1
        _split_to_two_files(output_file_type, reverse, data_key)
        _merge_two_files(output_file_type, reverse, data_key)

    result = _opener(Path(_RESULTS_PATH + output_file_type), 'r')
    destination = _opener(Path(str(output) + output_file_type), 'w')
    csv_start = result
    if input_file_type == _CSV:
        csv_start = _opener(Path(src), 'r')
    for row in result:
        if row == '\n':
            continue
        if output_file_type == _CSV:
            destination.writerow(row)
        else:
            destination.write(row)
    # Закрываем и удаляем мусорные файлы
    if output_file_type == _TXT:
        result.close()
        destination.close()
    """
    os.remove(_F1)
    os.remove(_F2)
    os.remove(_RESULTS_PATH)
    os.remove(_TMP_FILE_AFTER_KEY_F)"""


def results_writer(output: Optional[PathType] = None):
    pass


def _key_applicator(key: Callable, file_type: str, path: PathType,
                    data_key: Optional[int] = None) -> None:
    """
    Функция для обрабоки чисел через функцию key
    Сохраняет обработанные числа во временный файл _RESULTS_PATH
    :param key: сама функция
    :param file_type: тип входного файла (csv/txt)
    :param path: путь к начальному файлу
    :param data_key: индекс для csv файла
    :return: None
    """
    file = _opener(path, 'r')
    key_file = _opener(Path(_RESULTS_PATH + file_type), 'w')

    # Прогоняем каждое значение через key-функцию и записываем всё в новый файл
    for row in file:
        row[data_key] = key(row[data_key])
        key_file.writerow(row)
        """if data_key and file_type == _CSV:
            row = row[0].split(';')
            line = ''
            for i in range(data_key):
                print(row)
                if i != 0:
                    line += ';'
                if i == data_key:
                    line += key(row[i])
                line += row[i]
            print(line)
            key_file.writerow(line)
        else:
            key_file.write(key(row))"""
    if file_type == _TXT:
        file.close()
        key_file.close()


def _sort_condition(file_type: str, reverse: bool,
                    data_key: Optional[int] = None) -> bool:
    """
    Функция для определения необходимости сортировки списка чисел
    :param reverse: сортировка должна быть по убыванию
    :return: если файл отсортирован, вернет True, иначе - False
    """
    file = _opener(Path(_RESULTS_PATH + file_type), 'r')
    last_number = None
    for row in file:  # Ищем место, где не выполняется условие для сортировки
        if data_key and file_type == _CSV:
            number = row[data_key]
        else:
            number = row
        if last_number:
            if reverse and last_number < number or not reverse and last_number > number:
                return False
        last_number = number

    if file_type == _TXT:
        file.close()
    return True


def _compare(first: Union[int, str], second: Union[int, str], reverse: bool) -> bool:
    """
    Функция сравнения двух чисел
    :param first: первое значение
    :param second: второе значение
    :param reverse: флаг, что сортировка по убыванию
    :return: вернет True, если первое меньше второго, иначе - False
    При реверсе - результаты обратны
    """
    if first.isdigit() or len(first) > 1 and first[1:].isdigit():
        first = int(first)
    if second.isdigit() or len(second) > 1 and second[1:].isdigit():
        second = int(second)

    if reverse:
        return first >= second
    return first <= second


def _default_key(number: Union[int, str]) -> int:
    """
    Дефолтная key-функция
    :param number: значение
    :return: number без изменений
    """
    return number


def _opener(path: PathType, open_type: str):
    """
    Функция для открытия файлов разных типов
    Переделывает открытый файл в нужный тип, приравнивает открытие csv к открытию txt
    :param path: открытый файл
    :return: вернет открытый файл
    """
    tmp_file = open(path, open_type, encoding='UTF-8', newline='')
    if path.suffix == _TXT:
        file = tmp_file
    else:
        if open_type == 'r':
            file = csv.reader(tmp_file)
        else:
            file = csv.writer(tmp_file)
    return file


def _split_to_two_files(output_type: str, reverse: bool, data_key: Optional[int] = None) -> None:
    """
    Функция разделения файла на два
    :param reverse: если реверс
    :return: None
    """
    start_file = _opener(Path(_RESULTS_PATH + output_type), 'r')
    f_1 = _opener(Path(_F1 + output_type), 'w')
    f_2 = _opener(Path(_F2 + output_type), 'w')
    write_in_first = True
    last_number = None
    last_row = None

    while True:
        try:
            row = next(start_file)
        except StopIteration:
            if last_row:
                try:
                    if write_in_first:
                        f_1.write(last_row)
                    else:
                        f_2.write(last_row)
                except AttributeError:
                    if write_in_first:
                        f_1.writerow(last_row)
                    else:
                        f_2.writerow(last_row)
            break
        if output_type == _CSV and data_key:
            number = row[data_key]
        else:
            number = row
        if last_number and _compare(number, last_number, reverse):
            write_in_first = not write_in_first
        if last_row:
            try:
                if write_in_first:
                    f_1.write(last_row)
                else:
                    f_2.write(last_row)
            except AttributeError:
                if write_in_first:
                    f_1.writerow(last_row)
                else:
                    f_2.writerow(last_row)
        last_number = number
        last_row = row


def _merge_two_files(output_type: str, reverse: bool, data_key: Optional[int] = None) -> None:
    """
    Функция сливания двух файлов в один
    :param reverse: если реверс
    :return: None
    """
    f_1 = _opener(Path(_F1 + output_type), 'r')
    f_2 = _opener(Path(_F2 + output_type), 'r')
    result_file = _opener(Path(_RESULTS_PATH + output_type), 'w')
    toke_from_first = None
    not_first = False
    last_line = None

    # Пока какой-либо из файлов не кончился, выбираем минимальное из верхних значений и
    # записываем в результирующий файл
    row_f1 = next(f_1)
    row_f2 = next(f_2)
    while True:
        if not_first:
            try:
                if toke_from_first:
                    row_f1 = next(f_1)
                    last_line = row_f2
                else:
                    row_f2 = next(f_2)
                    last_line = row_f1
            except StopIteration:
                break
        if output_type == _CSV and data_key:
            number_1 = row_f1[data_key]
            number_2 = row_f2[data_key]
        else:
            number_1 = row_f1
            number_2 = row_f2

        if not _compare(number_1, number_2, reverse):
            try:

                result_file.write(row_f2)
            except AttributeError:
                result_file.writerow(row_f2)
            toke_from_first = False
        else:
            try:
                result_file.write(row_f1)
            except AttributeError:
                result_file.writerow(row_f1)
            toke_from_first = True
        not_first = True

    # Определеяем какой вспомогательный файл кончился
    last_f = f_1
    if toke_from_first:
        last_f = f_2

    # Дозаписываем оставшиеся значения
    while True:
        try:
            result_file.write(last_line)
        except AttributeError:
            result_file.writerow(last_line)

        try:
            if toke_from_first:
                last_line = next(f_2)
            else:
                last_line = next(f_1)
        except StopIteration:
            break

