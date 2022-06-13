"""
Практическая работа №0
Выполнил студент группы КИ20-17/2Б Смыков Алексей
Моя программа выводит фрактальное дерево с помощью модуля Turtle
"""

import turtle
LENGTH = 75
ANGLE = 45

colors = ['#B1B9FF', '#7280FD', '#2D42FF', '#001AFF', '#2D42FF', '#7280FD', '#B1B9FF', '#FFFFFF']
# Цвета для разукрашивания линий фрактала


def draw_recursion(length: float, iterations_count: int, current_iterations_count: int):
    """
    Функция, которая рисует одну итерацию
    :param length: длинна линии, которую нужно нарисовать
    :type length: float
    :param iterations_count: максимальное кол-во итераций
    :type length: int
    :param current_iterations_count: текущее кол-во итераций
    :type length: int
    :return:
    """
    if current_iterations_count >= iterations_count:
        # Если текущее кол-во итераций превысило максимальное, то рисование заканчивается
        return

    # Сама программа для черепашки, которая "рисует" фрактал
    current_iterations_count = current_iterations_count + 1
    turtle.left(ANGLE)

    # Рисование линии
    turtle.down()
    turtle.width((iterations_count - current_iterations_count))
    turtle.pencolor(colors[(current_iterations_count - 1) % 8])
    turtle.hideturtle()
    turtle.forward(length)
    turtle.up()

    # Рекурсивный вызов
    draw_recursion(length / 1.3, iterations_count, current_iterations_count)

    # Перемещение в изначальную точку
    turtle.backward(length)
    turtle.right(ANGLE)
    turtle.right(ANGLE)

    # Рисование линии
    turtle.down()
    turtle.width((iterations_count - current_iterations_count))
    turtle.pencolor(colors[(current_iterations_count - 1) % 8])
    turtle.hideturtle()
    turtle.forward(length)
    turtle.up()

    # Рекурсивный вызов
    draw_recursion(length / 1.3, iterations_count, current_iterations_count)

    # Перемещение в изначальную точку
    turtle.backward(length)
    turtle.left(ANGLE)


def main():
    """
    Гланвная функция программы
    :return:
    """
    iterations_count = 0
    current_iterations_count = 0

    turtle.reset()
    turtle.screensize(10000, 10000)
    turtle.left(90)
    turtle.tracer(10000)
    # Задаём начальные параметры

    while True:
        #Выводит на экран все рисунки с увеличением глубины итераций без остановки
        draw_recursion(LENGTH, iterations_count, current_iterations_count)
        turtle.clear()
        iterations_count += 1


if __name__ == "__main__":
    main()
