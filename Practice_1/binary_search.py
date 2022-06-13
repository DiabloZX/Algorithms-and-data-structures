"""Модуль бинарного поиска"""


def search(sequence: list, item: float):
    """
    Функция бинарного поиска
    :param sequence: отсортированный массив, в котором будет искаться нужный элемент
    :type sequence: list
    :param item: значение нужного элемента
    :type item: float
    :return: float
    """
    if len(sequence) == 0:
        return None
    mid = len(sequence) // 2
    low = 0
    high = len(sequence) - 1

    while sequence[mid] != item and low <= high:
        if item >= sequence[mid]:
            if abs(low - mid) != 1:
                low = mid + 1
            else:
                low = mid
        else:
            if abs(high - mid) != 1:
                high = mid - 1
            else:
                high = mid
        mid = (low + high) // 2

    if abs(low - high) <= 2 and low < len(sequence) - 1:
        if sequence[low] == item:
            mid = low
    if low > high:
        return None
    else:
        return mid
