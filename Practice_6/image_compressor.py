"""
Модуль сжатия картинки с помощью квадродерева.
"""

from typing import Union
import functools
import operator
import os
import imageio
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from quadtree import Node, QuadTree

AUTHOR_COMPRESS_CONSTANT = 10
MAX_COMPRESS_LEVEL = 10
GIF_FRAME_LEVEL_WAIT_TIME = 5
ROOTS_IN_TREE = 4
COLOR_IN_RGB = 3
GIF_FRAME_WAIT_TIME = 1


def compress_and_show(image_path: str, level: int = 0, compress_ratio: int = 0,
                      borders: bool = False, make_gif: bool = False) -> None:
    """
    Функция для сжатия картинки.
    Получает входные данные, в том числе путь к изображению и сжимает его с помощью квадродерева.
    При необходимости создает gif-изображение.
    :param image_path: путь к изображению.
    :param level: степень пикселизации, чем больше, тем больше пикселей и разрешение сжатого
    изображения.
    :param compress_ratio: степень сжатия, чем больше, тем больше сжатия.
    :param borders: флаг для показа границ квадродеревьев.
    :param make_gif: флаг для создания гифки.
    """
    compressed_image = _compress_step(image_path, level, compress_ratio, borders)
    compressed_image.axis("off")
    compressed_image.savefig(f"compressed_{image_path.split('.')[0]}.png", bbox_inches="tight",
                             pad_inches=0)
    compressed_image.close()

    if make_gif:
        filenames = []
        for step in range(level):
            for step_2 in range(compress_ratio):
                image_compress_gif_step = _compress_step(
                    image_path, step, compress_ratio - step_2 - 1, borders)

                time = GIF_FRAME_WAIT_TIME
                if step_2 == compress_ratio - 1:
                    time = GIF_FRAME_LEVEL_WAIT_TIME
                filename = f'{step}_{step_2}.png'
                for _ in range(time):
                    filenames.append(filename)

                image_compress_gif_step.axis("off")
                image_compress_gif_step.savefig(filename, bbox_inches="tight", pad_inches=0)
                image_compress_gif_step.close()

        with imageio.get_writer(f'compressed_{image_path.split(".")[0]}.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(filenames):
            os.remove(filename)


def _compress_step(image_path: str, level: int = 0, compress_ratio: int = 0,
                   borders: bool = False) -> plt:
    """
    Функция создания одного шага сжатия картинки.
    Создана для сокращения кода, вызывается на каждый шаг при создании гифки.
    :param image_path: путь к изображению.
    :param level: степень пикселизации, чем больше, тем больше пикселей и разрешение сжатого
    изображения.
    :param compress_ratio: степень сжатия, чем больше, тем больше сжатия.
    :param borders: флаг для показа границ квадродеревьев.
    :return: plt - плот с готовым изображением и границами при необходимости.
    """
    image = mpimg.imread(image_path)
    compressor = _ImageCompressor(image)
    compressor.insert_image_to_tree_recursion(compressor.quadtree, level)

    if compress_ratio < 0:
        compress_ratio = 0
    elif compress_ratio > MAX_COMPRESS_LEVEL:
        compress_ratio = MAX_COMPRESS_LEVEL

    compressor.compress(compressor.quadtree, compress_ratio)
    plt.imshow(compressor.get_image(compressor.quadtree))

    if borders:
        rectangles = compressor.get_pixels_cords()
        scale = image.shape[1] / image.shape[0]
        for i in rectangles:
            plt.gca().add_patch(
                Rectangle((i.cords_south_west[1] * scale,
                           (image.shape[1] - i.cords_south_west[0] - i.img.shape[1]) / scale),
                          i.img.shape[1],
                          i.img.shape[0],
                          linewidth=0.1,
                          edgecolor='black',
                          facecolor='none'))
    return plt


class _ImageCompressor:
    """
    Класс сжимателя картинки. Использует рекурсивный вызов деревьев и функции для обработки
    изображения.
    """

    def __init__(self, image: mpimg.imread) -> None:
        self.quadtree = QuadTree()
        self.quadtree.data = Node(
            image,
            _calculate_mean(image).astype(int),
            (0, 0),
            (image.shape[0], image.shape[1]))

    def insert_image_to_tree_recursion(self, quadtree: QuadTree, level: int = 0) -> None:
        """
        Функция 'вставки' изображения в квадродерево. Рекурсивная.
        :param quadtree: квадродерево, в которое нужно вставить очередной кусок изображения.
        :param level: Глубина вставки.
        """
        width = quadtree.data.cords_north_east[0] - quadtree.data.cords_south_west[0]
        height = quadtree.data.cords_north_east[1] - quadtree.data.cords_south_west[1]

        if min(abs(width), abs(height)) > 1 and level > 0:
            split_img = _split_image_quad(quadtree.data.img)
            roots_data = []

            for i in range(ROOTS_IN_TREE):
                roots_data.append(Node(split_img[i],
                                       _calculate_mean(split_img[i]).astype(int),
                                       quadtree.data.cords_south_west_for_roots[i],
                                       quadtree.data.cords_north_east_for_roots[i]))

            quadtree.create_roots(roots_data)
            for each in quadtree.roots:
                self.insert_image_to_tree_recursion(each, level - 1)

    def compress(self, quadtree: QuadTree, compress_ratio: int) -> None:
        """
        Функция сжатия изображения. Соединяет пиксели похожего цвета в один со средним цветом.
        Рекурсивная.
        :param quadtree: квадродерево, в котором будет проводиться проверка на возможность
        соединения частей.
        :param compress_ratio: степень сжатия. Влияет на вероятность, что части будут соединены.
        """
        roots = quadtree.roots
        for each in roots:
            if each and not each.final:
                self.compress(each, compress_ratio)

        if None not in roots and \
                roots[0].final and roots[1].final and roots[2].final and roots[3].final:
            images = []
            for i in range(ROOTS_IN_TREE):
                images.append(roots[i].data.img)
            if _color_can_be_combined_checker(images, compress_ratio):
                combined_img = self.get_image(quadtree)
                quadtree.clear_roots(Node(combined_img,
                                          _calculate_mean(combined_img).astype(int),
                                          (roots[2].data.cords_south_west[0],
                                           roots[2].data.cords_south_west[1]),
                                          (roots[1].data.cords_south_west[0],
                                           roots[1].data.cords_south_west[1])))

    def get_pixels_cords(self) -> list[Node]:
        """
        Функция для получения координат пикселей. Используется для пост-добавления границ пикселей.
        :return: list() - список координат.
        """
        return self.quadtree.get_all_roots_data()

    def get_image(self, quadtree: QuadTree) -> Union[np.tile, np.ndarray]:
        """
        Функция для получения изображения по уровню. Используется для конечного получения сжатого
        изображения
        или для получения частей изображения при сжатии. Рекурсивная.
        :param quadtree: квадродерево, чьё изображение нам нужно получить.
        :return: np.ndarray - изображение в виде numpy массива.
        """
        if not quadtree.final:
            roots = quadtree.roots
            images = []
            for i in range(ROOTS_IN_TREE):
                images.append(self.get_image(roots[i]))
            return _combine_image_quad(images)

        return np.tile(quadtree.data.mean_color,
                       [quadtree.data.img.shape[0], quadtree.data.img.shape[1], 1])


def _color_can_be_combined_checker(imgs: list, ratio: int) -> bool:
    """
    Функция для проверки можно ли соединить части с похожими цветами, или нет.
    :param imgs: список изображений, по которым будет определяться, возможно ли сжатие, или нет.
    :param ratio: степень сжатия. параметр, определяющий, будут ли 4 части совмещены в одну.
    :return: bool, можно ли объединить изображение в одно, или нет
    """
    combined_img = _combine_image_quad(imgs)
    imgs_means = []

    for i in imgs:
        imgs_means.append(_calculate_mean(i))
    combined_img_mean = _calculate_mean(combined_img)

    for i in range(ROOTS_IN_TREE):
        for j in range(COLOR_IN_RGB):
            if abs(imgs_means[i][j] - combined_img_mean[j]) > ratio * AUTHOR_COMPRESS_CONSTANT:
                return False
    return True


def _calculate_mean(image: np.ndarray) -> np.ndarray:
    """
    Функция для получения среднего цвета переданного изображения.
    :param image: изображение.
    :return: np.mean - средний цвет.
    """
    return np.mean(image, axis=(0, 1))


def _split_image_quad(image: np.ndarray) -> list:
    """
    Функция разделения изображения на 4 изображения одинакового размера.
    :param image: изображение.
    :return: массив из 4 разделённых изображений.
    """
    half_split = np.array_split(image, 2)
    res = map(lambda x: np.array_split(x, 2, axis=1), half_split)
    return functools.reduce(operator.add, res)


def _combine_image_quad(imgs: list) -> np.ndarray:
    """
    Функция для соединения переданных 4 картинок одинакового размера в одно изображение.
    :param imgs: список изображений, которые будут объединяться.
    :return: соединённое изображение.
    """
    top = np.concatenate((imgs[0], imgs[1]), axis=1)
    bottom = np.concatenate((imgs[2], imgs[3]), axis=1)
    return np.concatenate((top, bottom), axis=0)
