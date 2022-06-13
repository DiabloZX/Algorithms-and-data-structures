"""Модуль визуализации сортировки"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def visualize(generator: list[dict, ...]):
    """
    Функция визуализации сортировки через matplotlib
    :param generator: массив словарей, где каждый словарь это конкретный шаг
    :return: None
    """
    start_list = generator[0]["array"]
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.set_title(f"Quicksort - {len(start_list)} elements")
    ax.set_axisbelow(True)

    visualization_items = ax.bar(range(len(start_list)), start_list, align="edge") \
        if all(isinstance(x, int) for x in start_list) \
        else ax.bar(range(len(start_list)), [len(i) for i in start_list], align="edge")
    ax.axes.get_xaxis().set_visible(False)
    ax.set_xlim(0, len(start_list))

    _ = animation.FuncAnimation(fig, func=_updater, fargs=(visualization_items,),
                                frames=generator, interval=int(5000/len(start_list)),
                                repeat=False)

    plt.show()


def _updater(step: dict, visualization_items):
    """
    Функция для обновления фрейма диаграммы через данные в шаге
    :param step: словарь с данными о шаге
    :param visualization_items: столбики диаграммы
    :return: None
    """
    array = step["array"]

    # Обновление массива через определённую часть с опорным элементом
    if step["current_array_part"]:
        array[step["pivot_left"]:len(array) - step["pivot_right"]] = step["current_array_part"]

    # Запись элементов массив в столбики визуальной схемы
    for i in range(len(array)):
        if isinstance(array[i], int):
            visualization_items[i].set_height(array[i])
        else:
            visualization_items[i].set_height(len(array[i]))

    # Раскраска столбиков:
    # Светло-серый: обычный цвет столбца
    # Серый: столбец в текущем выбранном интервале
    # Зелёный: опорный элемент
    # красный: текущий элемент, который сравнивается с опорным
    for i in range(len(visualization_items)):
        visualization_items[i].set_facecolor('#dadada')
    if step["current_array_part"]:
        for i in range(step["pivot_left"], len(array) - step["pivot_right"]):
            visualization_items[i].set_facecolor('#b2b2b2')
    if step["pivot"]:
        visualization_items[step["pivot"] + step["pivot_left"]].set_facecolor('#ade3c2')
    if step["current_element"]:
        visualization_items[step["current_element"] + step["pivot_left"]].set_facecolor('#f65d5d')
