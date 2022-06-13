"""
Модуль для построения лабиринта.
Содержит класс Maze, есть функции построения лабиринта и поиск пути.
Также возможно сохранение как в картинку, так и в гиф-анимацию.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from node import Node
from node_list import NodeList
import numpy as np
from PIL import Image

RGB_MAX_VALUE = 255
RGB_MIN_VALUE = 0

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]


class Maze:
    """
    Класс лабиринта. Содержит в себе лабиринт, может построить его по вызову функции и также
    построить путь прохождения лабиринта.
    """

    def __init__(self, height: int = None, width: int = None):

        # Параметры лабиринта
        self.height = height
        self.width = width

        # Список клеточек (узлов) для сохранения информации о клеточки
        self.nodes = NodeList()

        # Список кадров для анимации
        self.frames = []

    def _add_node_by_color(self, color: list, x: int = None, y: int = None):
        """
        Функция для заполнения списка узлов, исходя из переданных данных.
        :param color: цвет клетки.
        :param x: координата клетки.
        :param y: координата клетки.
        """
        if color == BLACK:
            self.nodes[len(self.nodes) - 1].append(Node((x, y), BLACK))
        else:
            self.nodes[len(self.nodes) - 1].append(Node((x, y), WHITE))

    def _get_colors_from_nodes(self) -> list[list[list[int, int, int], ...], ...]:
        """
        Функция для обращения к полю цвета всех узлов в списке.
        :return: list двумерный список параметров цвета узлов.
        """
        return list(map(lambda my_list: list(map(lambda item: item.color, my_list)), self.nodes))

    def _build_maze_base(self):
        """
        Функция для постройки фундамента лабиринта: создает массив с черными блоками (стенами)
        и белыми (точки, соединяющие путь).
        :return: None.
        """
        for i in range(self.height * 2 + 1):
            self.nodes.append([])
            for j in range(self.width * 2 + 1):
                if i % 2 == 0 or j % 2 == 0:
                    self._add_node_by_color(BLACK, i, j)
                else:
                    self._add_node_by_color(WHITE, i, j)

    def _get_way_variants(self, cords: list, path_find: bool = False):
        """
        Функция для просчета возможных вариантов дальнейшего движения.
        :param cords: координаты текущего узла (позиции).
        :param path_find: флаг, если сейчас ищется путь, а не строится лабиринт.
        :return: list[tuple, ...] - список возможных координат следующих узлов для продвижения.
        """
        variants = []
        if cords[0] != 1 and not self.nodes.get_item(cords, -2).checked \
                and ((self.nodes.get_item(cords, -1).color == WHITE) + path_find != 1):
            variants.append((cords[0] - 2, cords[1]))
        if cords[1] != 1 and not self.nodes.get_item(cords, 0, -2).checked \
                and ((self.nodes.get_item(cords, 0, -1).color == WHITE) + path_find != 1):
            variants.append((cords[0], cords[1] - 2))
        if cords[1] != self.width * 2 - 1 and not self.nodes.get_item(cords, 0, 2).checked \
                and ((self.nodes.get_item(cords, 0, 1).color == WHITE) + path_find != 1):
            variants.append((cords[0], cords[1] + 2))
        if cords[0] != self.height * 2 - 1 and not self.nodes.get_item(cords, 2).checked \
                and ((self.nodes.get_item(cords, 1).color == WHITE) + path_find != 1):
            variants.append((cords[0] + 2, cords[1]))
        return variants

    def _maze_walker(self, make_gif: bool = False, path_find: bool = False):
        """
        Функция прохода по лабиринту в случае построения и в случае поиска пути.
        :param make_gif: флаг для создания гифки.
        :param path_find: флаг если данный обход - это поиск пути, а не построение.
        :return: None.
        """
        cords = [1, 1]
        stack = [self.nodes.get_item(cords)]
        step = 1
        progress = 0
        max_progress = self.height * self.width * 2 - 1
        last = None
        while not (path_find and not (cords[0] != self.height * 2 - 1 or
                                      cords[1] != self.width * 2 - 1)):
            if not path_find and int(step / max_progress * 10) > progress:
                progress = int(step / max_progress * 10)
                print(f"progress: {progress * 10}%")
            step += 1
            # Если клетка еще не в лабиринте, пометить ее как "в лабиринте"
            if not self.nodes.get_item(cords).checked:
                self.nodes.get_item(cords).checked = True

            if make_gif:
                # Для создания гифки меняем текущую клеточку на красный и добавляем изображение
                # в список кадров
                self.nodes.get_item(cords).color = RED
                self.frames.append(Image.fromarray(np.array(self._get_colors_from_nodes(),
                                                            dtype='uint8'), mode='RGB'))
                self.nodes.get_item(cords).color = WHITE

            # Считаем количество возможных путей для прохода
            variants = self._get_way_variants(cords, path_find)

            # Если есть куда пойти
            if variants:

                # Выбираем случайный путь
                variant = variants[random.randint(0, len(variants) - 1)]

                if path_find:
                    self.nodes.get_item(cords).color = RED
                    self.nodes.get_item_between(cords, variant).color = RED
                else:
                    self.nodes.get_item_between(cords, variant).color = WHITE
                cords = variant

                # Добавляем узел в список пути
                stack.append(self.nodes.get_item(cords))

            # Если некуда идти, идём назад и убираем узел из списка пути
            elif len(stack) > 1:
                stack.pop(len(stack) - 1)
                cords = stack[len(stack) - 1].cords
                if path_find:
                    self.nodes.get_item(cords).color = WHITE
                    self.nodes.get_item_between(cords, last).color = WHITE

            # Когда путь закончился, считаем что соединили все узлы
            else:
                break
            last = cords

        if path_find:
            self.nodes.get_item((self.height * 2 - 1, self.width * 2 - 1)).color = RED

        if make_gif:

            # Для создания гифки меняем текущую клеточку на красный и добавляем изображение
            # в список кадров
            self.nodes.get_item(cords).color = RED
            for _ in range(20):
                self.frames.append(Image.fromarray(np.array(self._get_colors_from_nodes(),
                                                            dtype='uint8'), mode='RGB'))
            self.nodes.get_item(cords).color = WHITE

    def _build_maze_paths(self, make_gif: bool = False):
        """
        Функция для постройки самих путей с помощью алгоритма поиска в глубину.
        :param make_gif: флаг для создания гифки.
        :return: None.
        """
        self._maze_walker(make_gif)

    def _path_find(self, make_gif: bool = False):
        """
        Функция поиска пути (решения лабиринта).
        :param make_gif: флаг для создания гифки.
        :return: None.
        """
        # Снимаем с каждого узла пометку, что он был проверен, для дальнейшего обхода
        for i in range(self.height * 2 + 1):
            for j in range(self.width * 2 + 1):
                if self.nodes.get_item((i, j)):
                    self.nodes.get_item((i, j)).checked = False

        self._maze_walker(make_gif, True)

    def _load_from_txt(self, path: str):
        """
        Функция загрузки лабиринта из txt.
        :param path: путь до файла, который загружать.
        :return: None.
        """
        self.nodes.clear()
        color = [BLACK, WHITE, RED]
        with open(path, 'r') as file:
            row_number = 0
            item_number = 0

            # Заполняем массивы изображения и узлов
            for row in file:
                self.nodes.append([])
                item_number = 0
                print(row)
                for item in row[:-1]:
                    self._add_node_by_color(color[int(item)], row_number, item_number)
                    item_number += 1
                row_number += 1

            self.height = int((row_number - 1) / 2)
            self.width = int((item_number - 1) / 2)

    def _load_from_img(self, path: str):
        """
        Функция загрузки лабиринта из jpg/png.
        :param path: путь до файла, который загружать.
        :return: None.
        """
        image = mpimg.imread(path)
        self.nodes.clear()
        self.height = int((len(image) - 1) / 2)
        self.width = int((len(image[0]) - 1) / 2)

        # Заполняем массивы изображения и узлов
        for i in range(len(image)):
            self.nodes.add_row()
            for j in range(len(image[i])):
                # Конвертируем значение цвета из np.ndarray в list
                item = [int(RGB_MAX_VALUE * value) for value in image[i][j][:-1]]
                self._add_node_by_color(item, i, j)

    def _save_to_txt(self, path: str):
        """
        Функция сохранения лабиринта в формате txt.
        :param path: путь до файла, куда сохранять.
        :return: None.
        """
        with open(path, 'w') as file:
            for row in self.nodes:
                file.write(
                    f"""{''.join(list(map(lambda node: str(0) if node.color == BLACK
                    else str(1) if node.color == WHITE else str(2), row)))}\n""")

    def _save_to_img(self, path: str):
        """
        Функция сохранения лабиринта в формате jpg/png.
        :param path: путь до файла, куда сохранять.
        :return: None.
        """
        fig = plt.figure(frameon=False)
        fig.set_size_inches(self.width * 2 + 1, self.height * 2 + 1)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self._get_colors_from_nodes())
        fig.savefig(path, dpi=1)

    def build(self, make_gif: bool = False):
        """
        Функция создания лабиринта.
        Может создать гифка построения самих путей.
        :param make_gif: флаг для создания гифки.
        :return: None.
        """
        print("Building maze...")
        self._build_maze_base()
        self._build_maze_paths(make_gif)

    def solve(self, make_gif: bool = False):
        """
        Функция решения лабиринта.
        :param make_gif: флаг для создания гифки.
        :return: None.
        """
        print("Solving maze...")
        self._path_find(make_gif)

    def load(self, path: str):
        """
        Функция загрузки лабиринта из txt или jpg/png.
        :param path: путь до файла, который загружать.
        :return: None.
        """
        print("Loading maze...")
        file_type = path.split(".")[-1]
        if file_type == "txt":
            self._load_from_txt(path)
        else:
            self._load_from_img(path)

    def save(self, path: str):
        """
        Функция сохранения лабиринта в txt или jpg/png.
        :param path: путь до файла, куда сохранять.
        :return: None.
        """
        print("Saving maze...")
        file_type = path.split(".")[-1]
        if file_type == "txt":
            self._save_to_txt(path)
        else:
            self._save_to_img(path)

    def gif(self, path: str):
        """
        Функция создания гифки.
        :param path: путь до файла, куда сохранять.
        :return: None.
        """
        print("Making gif...")
        self.frames[0].save(
            f'{path.split(".")[0]}.gif',
            append_images=self.frames[1:],
            duration=20 + 5000 / self.width / self.height,
            loop=True,
            save_all=True,
            optimize=True)
