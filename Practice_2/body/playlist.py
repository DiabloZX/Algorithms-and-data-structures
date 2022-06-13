"""Модуль прдоставляющий основную логику плейлиста"""
import os
import pygame

# Для добавления треков, библиотека дляпроверки имён и получения длинны трека
from mutagen.mp3 import MP3
from .linked_list import LinkedList
from .compostion import Composition

pygame.mixer.init()  # Инициализация mixer
pygame.mixer.music.set_volume(0.02)  # Установление громкости на 15%


class PlayList(LinkedList):
    """
    Класс плейлиста, в котором происходит основная логика, наследуется от класса связного списка
    """
    def __init__(self):
        """
        Инициализиирует класс плейлиста, наследуя его от класса связного списка
        """
        super().__init__()
        self.current_node = None
        self.play_list_name = None
        self.is_paused = False
        self._tracks_files = []

    def add_music_from_folder(self, path):
        """
        Считывает все песни из папки, указаной в file и добавляет их в плейлист
        :return Массив файлов песен
        """
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('mp3'):
                    file = os.path.join(root, file)
                    file = os.path.normpath(file)
                    if file not in self._tracks_files and file != "":
                        self._tracks_files.append(file)
                        self.append(create_new_composition(file))

    def add_track(self, file: str):
        """
        Добавляет в конец плейлиста музыку, файл которой передан в file
        :param file: - файл песни которую нужно добавить
        :type file: str
        """
        file = os.path.normpath(file)

        if file not in self._tracks_files and file.endswith('mp3'):
            self._tracks_files.append(file)
            composition = create_new_composition(file)
            self.append(composition)

    def next_track(self):
        """
        Переключение на следующую песню
        :return Имя текущей песни
        """
        if self.length > 0 and self.current_node:
            self.current_node = self.current_node.next_node
            self.play_current_node()
            if self.is_paused:
                self.is_paused = False
            return self.current_node.data.name
        return None

    def previous_track(self):
        """
        Переключаает на предыдущую песню
        :return Имя текущей песни
        """
        if self.length > 0 and self.current_node and self.current_node.previous_node:
            self.current_node = self.current_node.previous_node
            self.play_current_node()
            if self.is_paused:
                self.is_paused = False
            return self.current_node.data.name
        return None

    def current(self):
        """
        Возвращает имя и продолжительность текущей песни
        :return Кортеж двух элементов, 1 элемент - имя песни, 2 элемент - продолжительность
        """
        if self.current_node:
            return self.current_node.data.name, self.current_node.data.length
        return None

    def play_current_node(self):
        """
        Воспроизводит музыку, начиная с текущей композиции в плейлисте
        """
        pygame.mixer.music.load(self.current_node.data.file)
        pygame.mixer.music.play()

    def play_all(self):
        """
        Воспроизводит музыку, начиная с первой композиции в плейлисте
        """
        if self.is_paused:
            self.is_paused = False
        self.current_node = self.item_data(index=0)
        self.play_current_node()

    def pause_unpause(self):
        """
        Ставит музыку на паузу
        """
        if self.is_paused:
            self.is_paused = False
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def move(self, track_node, index_move):
        """
        Передвигает музыку на индекс: index_move
        Используется при перемещении треков перетаскиванием
        """
        self.change_item_index(track_node, index_move)

    def current_duration_time(self):
        """
        Функция для получения текущего времени проигрывания трека
        :return: duration, время в секундах
        """
        duration = pygame.mixer.music.get_pos() // 1000
        return max(duration, 0)

    def duration_time(self):
        """
        Функция для получения продолжительности текущего в плейлисте трека
        :return: float, время в секундах
        """
        return pygame.mixer.Sound(self.current_node.data.file).get_length() // 1000


def create_new_composition(file: str):
    """
    Создает экземпляр класса Composition из пути (file)
    :param file: Файл с музыкой
    :type: str
    :return Объект класса Composition
    """
    tmp = Composition()
    song = MP3(file)
    duration = round(song.info.length)
    tmp.file = file
    tmp.length = duration
    try:
        tmp.name = str(song.tags.getall('TIT2')[0])
    except IndexError:
        tmp.name = file.split("\\")[-1][:-4]
    return tmp
