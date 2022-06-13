"""
Модуль плеера
Тут содержится класс плеера и пара вспомогательных статических функций
"""

import sys
import math

from PyQt5 import QtWidgets, QtCore  # Модуль для работы с qt
from interfaces import player  # Модуль основного интерфейса плеера
from widgets import track_widget, playlist_widget  # Модуль виджетов для элементов списков QListWidget
from body import playlist, compostion  # Классы плейлиста и композиции


class MainWindow(player.Ui_MainWindow):
    """
    Класс связки визуальной части плеера, всех кнопок и тд с кодом, класс-прослойка
    """
    def __init__(self):
        """
        Инициализация
        """
        self.app = QtWidgets.QApplication(sys.argv)
        self.GenerateWindow = QtWidgets.QMainWindow()
        self.ui = player.Ui_MainWindow()
        self.ui.setupUi(self.GenerateWindow)
        self.ui.Tracks.setDragDropMode(self.ui.Tracks.InternalMove)  # Установка для списков треков Drag&Drop
        self.ui.PlaylistTracks.setDragDropMode(self.ui.PlaylistTracks.InternalMove)  # Здесь тоже установка
        self.GenerateWindow.show()
        self.track_open_source = 0   # Переменная для значения источника открытия окна текущего трека
        self.timer = QtCore.QTimer()  # Установка таймера для обновления текущуего времени трека и ползунка

        self.all_tracks = playlist.PlayList()  # Плейлист всех треков в плеере

        # Установка для плеера всех треков названия, которое будет в писке всех плейлистов
        self.all_tracks.play_list_name = "Все треки"
        self.all_playlists = []  # Питоновский список плейлистов

        # Функция добавления всех треков из указанного файла в плейлист
        self.all_tracks.add_music_from_folder("C:\\music")
        self.all_playlists.append(self.all_tracks)  # Добавления плейлиста всех треков в список всех плейлистов
        self.current_playlist = self.all_tracks  # Установления текущим плейлист всех треков

        # Установление в текущем плейлисте текущим треком первый трек
        self.current_playlist.current_node = self.current_playlist.item_data(index=0)

        # Установление в текущий трек плеера текущий трек из текущего плейлиста в плеере
        self.current_track = self.current_playlist.current_node.data

        # Чтобы при нажатии на кнопку "play" в верхнем меню текущего трека трек снимался с паузы и играл
        self.current_playlist.play_current_node()
        self.pause_unpause_track()
        self.current_playlist.is_paused = True

        # Открываем меню всех треков при запуске плеера
        self._open_tracks()
        # Связываем интерфейс (кнопки и прочее) с функциями
        self._connector()

        sys.exit(self.app.exec_())

    def _connector(self):
        """
        Функция для связывания сигналов с функциями, в основном нажатий на кнопки
        """
        # Кнопки на главных экранах для открытия других экранов
        self.ui.PlaylistsButton.clicked.connect(self._open_playlists)
        self.ui.TracksButton.clicked.connect(self._open_tracks)
        self.ui.PlaylistsButton_2.clicked.connect(self._open_playlists)
        self.ui.TracksButton_2.clicked.connect(self._open_tracks)
        self.ui.AddTrackToPlaylist.clicked.connect(self._open_add_tracks_to_playlist)
        self.ui.PlayPlaylist.clicked.connect(self._open_track_menu_from_play_playlist)
        self.ui.CurrentTrack.clicked.connect(self._open_track_menu_from_current_track)
        self.ui.CurrentTrack_2.clicked.connect(self._open_track_menu_from_playlists)

        # Кнопки в меню трека: пауза, следующий трек, предыдущий и тд
        self.ui.NextTrackButton.clicked.connect(self.next_track)
        self.ui.PreviousTrackButton.clicked.connect(self.previous_track)
        self.ui.PauseTrackButton.clicked.connect(self.pause_unpause_track)
        self.ui.PlayCurrentTrack.clicked.connect(self.pause_unpause_track)
        self.ui.PlayCurrentTrack_2.clicked.connect(self.pause_unpause_track)
        self.ui.GetInfo.clicked.connect(self.get_info)

        # Кнопки для добавления чего-либо куда-либо
        self.ui.AddPlaylist.clicked.connect(self.add_playlist)
        self.ui.AddSelectedTracksToPlaylistButton.clicked.connect(
            self.add_selected_tracks_to_playlist)
        self.ui.AddTrackToPlayer.clicked.connect(self.add_track_to_player)

        # Кнопка очистки выбора треков для добавления в плейлист
        self.ui.ClearTracksSelection.clicked.connect(self.clear_add_track_selection)

        # Кнопки для удаления плейлистов (нет для удаления треков, потому что удаления треков как такового нет)
        self.ui.DeletePlaylists.clicked.connect(self._open_playlist_delete)
        self.ui.DeleteSelectedPlaylistButton.clicked.connect(self.delete_selected_playlists)

        # Кнопки выхода на предыдущее меню, кнопки "назад"
        self.ui.PlaylistDeleteBack.clicked.connect(self._open_playlists)
        self.ui.TrackBack.clicked.connect(self.back_from_track_menu)
        self.ui.PlaylistBack.clicked.connect(self._open_playlists)
        self.ui.TrackToAddBack.clicked.connect(self._open_playlist)

        # При нажатии на элементы списков типа QListWidget
        self.ui.Playlists.itemClicked.connect(self._open_playlist)
        self.ui.TracksToAdd.itemClicked.connect(change_selection)
        self.ui.PlaylistToDelete.itemClicked.connect(change_selection)
        self.ui.Tracks.itemClicked.connect(self._open_track_menu_from_tracks)
        self.ui.PlaylistTracks.itemClicked.connect(self._open_track_menu_from_playlist)

        # Сигналы при перемещении строк в списках, используется при перетаскивании треков
        self.ui.Tracks.model().rowsMoved.connect(self.move_all_tracks)
        self.ui.PlaylistTracks.model().rowsMoved.connect(self.move_playlist_tracks)

        # Сигнал для таймера, используется для обновления информациио текущей продолжительности трека и для полоски
        # прогресса
        self.timer.timeout.connect(self.track_update)

    # Ниже функции для обновлений информации на различных экранах, менюшках
    def _all_tracks_page_update(self):
        """
        Функция для обновления экрана всех треков
        """
        self.ui.Tracks.clear()
        i = 0
        for current_track in self.all_tracks:
            track = QtWidgets.QListWidgetItem()
            track_wg = track_widget.TrackWidget(current_track.data.name,
                                                time_to_str(current_track.data.length),
                                                self.ui.Tracks.size().width() / 15)
            track.setSizeHint(track_wg.widget.sizeHint())
            self.ui.Tracks.addItem(track)
            self.ui.Tracks.setItemWidget(track, track_wg.widget)
            self.ui.Tracks.item(self.ui.Tracks.count() - 1).setData(0, current_track)
            if i == 0 and not self.current_track.name:
                self.current_track = compostion.Composition(
                    current_track.data.file, current_track.data.length, current_track.data.name)
                self.current_playlist.current_node = current_track
                i = 1
        self._current_track_update()

    def _current_track_update(self):
        """
        Функция для обновления виджета текущего трека вверху экранов всех треков и всех плейдистов
        """
        name = self.current_track.name
        if len(self.current_track.name) > self.ui.CurrentTrack.size().width() / 15:
            name = self.current_track.name[:int(self.ui.CurrentTrack.size().width() / 15)] + "..."
        self.ui.CurrentTrack.setText(name)
        self.ui.CurrentTrack_2.setText(name)

        if self.current_playlist.is_paused:
            self.ui.PlayCurrentTrack.setText("⯈")
            self.ui.PlayCurrentTrack_2.setText("⯈")
        else:
            self.ui.PlayCurrentTrack.setText("| |")
            self.ui.PlayCurrentTrack_2.setText("| |")

    def _all_playlists_page_update(self):
        """
        Функция для обновления экрана всех плейлистов
        """
        self.ui.Playlists.clear()
        if len(self.all_playlists) == 0 or self.all_playlists[0].play_list_name != "Все треки":
            self.all_playlists.insert(0, self.all_tracks)
        for current_playlist in self.all_playlists:
            new_playlist = QtWidgets.QListWidgetItem()
            playlist_wg = playlist_widget.PlaylistWidget(current_playlist.play_list_name,
                                                         self.ui.Playlists.size().width() / 15)
            new_playlist.setSizeHint(playlist_wg.widget.sizeHint())
            self.ui.Playlists.addItem(new_playlist)
            self.ui.Playlists.setItemWidget(new_playlist, playlist_wg.widget)
        self._current_track_update()

    def _playlist_delete_page_update(self):
        """
        Функция для обновления экрана удаления плейлистов
        """
        self.ui.PlaylistToDelete.clear()
        i = 0
        for current_playlist in self.all_playlists:
            if i == 0:
                i += 1
                continue
            new_playlist = QtWidgets.QListWidgetItem()
            playlist_wg = playlist_widget.PlaylistWidget(current_playlist.play_list_name,
                                                         self.ui.PlaylistToDelete.size().width() / 15)
            new_playlist.setSizeHint(playlist_wg.widget.sizeHint())
            self.ui.PlaylistToDelete.addItem(new_playlist)
            self.ui.PlaylistToDelete.setItemWidget(new_playlist, playlist_wg.widget)
            self.ui.PlaylistToDelete.item(i - 1).setCheckState(QtCore.Qt.Unchecked)
            i += 1
        self._current_track_update()

    def _playlist_page_update(self, current_playlist: playlist.PlayList):
        """
        Функция для обновления экрана плейлиста
        :param current_playlist: плейлист, который открывает пользователь, а не который текущий в плеере,
        текущйи в плеере это тот, который сейчас играет
        """
        playlist_length = 0
        for track in current_playlist:
            playlist_length += track.data.length
        self.ui.PlaylistName.setText(current_playlist.play_list_name)
        self.ui.PlaylistInfo.setText(str(len(current_playlist)) + " Трека(-ов) | " +
                                     time_to_str(playlist_length))
        self.ui.PlaylistTracks.clear()
        for current_track in current_playlist:
            track = QtWidgets.QListWidgetItem()
            track_wg = track_widget.TrackWidget(current_track.data.name,
                                                time_to_str(current_track.data.length),
                                                self.ui.PlaylistTracks.size().width() / 15)
            track.setSizeHint(track_wg.widget.sizeHint())
            self.ui.PlaylistTracks.addItem(track)
            self.ui.PlaylistTracks.setItemWidget(track, track_wg.widget)

            # Устанавливает инормацию о треке в data виджета трека, потому что иначе я не придумал как ее передать,
            # а просто через text() не получается
            self.ui.PlaylistTracks.item(self.ui.PlaylistTracks.count() - 1).setData(0, current_track)
        if current_playlist.play_list_name == "Все треки":
            self.ui.AddTrackToPlaylist.setEnabled(False)
        else:
            self.ui.AddTrackToPlaylist.setEnabled(True)

    def _add_track_to_playlist_page_update(self):
        """
        Функция для обновления экрана добавления треков в плейлист
        """
        self.ui.TracksToAdd.clear()
        i = 0
        for current_track in self.all_tracks:
            track = QtWidgets.QListWidgetItem()
            track_wg = track_widget.TrackWidget(current_track.data.name,
                                                time_to_str(current_track.data.length),
                                                self.ui.TracksToAdd.size().width() / 15)
            track.setSizeHint(track_wg.widget.sizeHint())
            self.ui.TracksToAdd.addItem(track)
            self.ui.TracksToAdd.setItemWidget(track, track_wg.widget)
            if len(self.all_playlists[self.ui.Playlists.currentRow()]) > 0:
                for playlist_track in self.all_playlists[self.ui.Playlists.currentRow()]:

                    # Устанавливаем треку галочку, если он уже есть в плейлисте
                    if current_track.data.name == playlist_track.data.name or \
                            self.ui.TracksToAdd.item(
                                i).checkState():
                        self.ui.TracksToAdd.item(i).setCheckState(QtCore.Qt.Checked)
                    else:
                        self.ui.TracksToAdd.item(i).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.ui.TracksToAdd.item(i).setCheckState(QtCore.Qt.Unchecked)
            i += 1

    def _track_menu_update(self, track=None, from_current_track: bool = False):
        """
        Функция для обновления экрана открытого трека. Может открываться из разных источников с разными входными данными
        :param track: трек, который был нажат, если открытие экрана при нажатии на случайный трек
        :param from_current_track: открыто ли было меню через нажатие на текущий трек
        :return:
        """

        # Если передан какой-либо трек, то устанавливаем его текущим, иначе берем его, исходя из того,
        # откуда было открыто меню
        if track:
            self.current_track = track
        else:

            # Если открыто с экрана всех треков
            if self.track_open_source == 0 or self.track_open_source == 1:

                # Если открыто НЕ через текущий трек
                # (Если через текущий, то уже выбран нужный трек и ничего менять не надо)
                if not from_current_track:

                    # Если в списке треков выбран какой-либо трек
                    if self.ui.Tracks.currentRow() == -1:
                        self.current_track = self.all_tracks[0]
                    else:
                        self.current_track = self.all_tracks[self.ui.Tracks.currentRow()]

            # Если открыто с экрана плейлиста через нажатие на трек
            elif self.track_open_source == 2:
                self.current_playlist = self.all_playlists[self.ui.Playlists.currentRow()]
                self.current_track = self.current_playlist[self.ui.PlaylistTracks.currentRow()]

            # Если открыто с экрана плейлиста через запуск всего плейлиста с начала
            elif self.track_open_source == 3:
                self.current_playlist = self.all_playlists[self.ui.Playlists.currentRow()]
                self.current_track = self.current_playlist[0]

        self.current_playlist.current_node = self.current_playlist.item_data(data=self.current_track)
        track_name = self.current_track.name
        if len(self.current_track.name) > self.ui.TrackNameInTrackMenu.size().width() / 11:
            track_name = self.current_track.name[:int(
                self.ui.TrackNameInTrackMenu.size().width() / 11)] + "..."

        # Устанавливаем в интерфейс данные о текущем треке
        self.ui.TrackNameInTrackMenu.setText(track_name)
        self.ui.TrackTime.setText(time_to_str(self.current_track.length))
        self.ui.CurrentTrackTime.setText(time_to_str(self.current_playlist.current_duration_time()))
        if self.current_playlist.is_paused:
            self.ui.PauseTrackButton.setText("⯈")
        else:
            self.ui.PauseTrackButton.setText("| |")

    def _open_tracks(self):
        """
        Функция для обновления включения нужного экрана (виджета из StackedWidget) и его обновление
        Сначала открывает нужны экран-виджет, затем обновляет его через функцию обновления нужного экрана
        Эта функция для обновления экрана всех треков
        """
        self.ui.stackedWidget.setCurrentIndex(0)
        self._all_tracks_page_update()

    def _open_playlists(self):
        """
        Для экрана всех плейлистов
        """
        self.ui.stackedWidget.setCurrentIndex(1)
        self._all_playlists_page_update()

    def _open_playlist_delete(self):
        """
        Для экрана удаления плейлистов
        """
        self.ui.stackedWidget.setCurrentIndex(2)
        self._playlist_delete_page_update()

    def _open_playlist(self):
        """
        Для экрана плейлиста
        """
        self.ui.stackedWidget.setCurrentIndex(3)
        self._playlist_page_update(self.all_playlists[self.ui.Playlists.currentRow()])

    def _open_add_tracks_to_playlist(self):
        """
        Для экрана добавления треков в плейлист
        """
        self.ui.stackedWidget.setCurrentIndex(4)
        self._add_track_to_playlist_page_update()

    def _open_track_menu_from_tracks(self):
        """
        Для экрана текущего трека
        Открытие через трек из меню всех треков
        """
        self.ui.stackedWidget.setCurrentIndex(5)
        self.track_open_source = 0
        self.play_and_open_track()

    def _open_track_menu_from_current_track(self):
        """
        Для экрана текущего трека
        Открытие через текущий трек из меню всех треков
        """
        self.ui.stackedWidget.setCurrentIndex(5)
        self.track_open_source = 0
        self._track_menu_update(from_current_track=True)

    def _open_track_menu_from_playlists(self):
        """
        Для экрана текущего трека
        Открытие через трек из меню всех плейлистов
        """
        self.ui.stackedWidget.setCurrentIndex(5)
        self.track_open_source = 1
        self._track_menu_update(from_current_track=True)

    def _open_track_menu_from_playlist(self):
        """
        Для экрана текущего трека
        Открытие через трек из меню плейлиста
        """
        self.ui.stackedWidget.setCurrentIndex(5)
        self.track_open_source = 2
        self.play_and_open_track()

    def _open_track_menu_from_play_playlist(self):
        """
        Для экрана текущего трека
        Открытие через проигрывание всего плейлиста из меню плейлиста
        """

        # Если длинна плейлиста не 0 (плейлист не пустой)
        if len(self.all_playlists[self.ui.Playlists.currentRow()]) > 0:
            self.current_playlist.play_all()
            self.ui.stackedWidget.setCurrentIndex(5)
            self.track_open_source = 3
            self.play_and_open_track()

    def add_track_to_player(self):
        """
        Функция добавления нового трека в сам плеер через файловое диалоговое окно
        """

        # При выборе мп3 файла мы получаем кортеж двух элементов, где путь это первый элемент с индексом 0,
        # нам нужен только он
        self.all_tracks.add_track(QtWidgets.QFileDialog.getOpenFileName(directory="C:\\music")[0])

    def add_playlist(self):
        """
        Функция добавления нового плейлиста через диалоговое окно QInputDialog
        """
        msg = QtWidgets.QInputDialog()
        name = msg.getText(QtWidgets.QWidget(), "Add playlists", "Please, input name of playlist",
                           QtWidgets.QLineEdit.Normal, "")[0]
        new_playlist = playlist.PlayList()
        new_playlist.play_list_name = name

        # Добавляем в список плейлистов новый плейлист и обновляем экран всех плейлистов
        if name:
            self.all_playlists.append(new_playlist)
            self._all_playlists_page_update()

    def add_selected_tracks_to_playlist(self):
        """
        Функция добавления выбраных треков в плейлист.
        Каждый раз плейлист обнуляется и все выбранные треки добавляются заного,
        Удаления не происходит, а лишь перезапись
        """
        name = self.all_playlists[self.ui.Playlists.currentRow()].play_list_name  # Временная переменная для имени
        self.all_playlists[self.ui.Playlists.currentRow()] = playlist.PlayList()  # Обнуляем плейлист
        self.all_playlists[self.ui.Playlists.currentRow()].play_list_name = name  # Присуждаем имя, которое было раньше
        for i in range(self.ui.TracksToAdd.count()):

            # Если виджет трека с галочкой, то добавляем этот трек в плейлист
            if self.ui.TracksToAdd.item(i).checkState():
                self.all_playlists[self.ui.Playlists.currentRow()].add_track(
                    self.all_tracks.item_data(index=i).data.file)
        self._open_playlist()

    def clear_add_track_selection(self):
        """
        Функция для очистки выбора треков в плейлисте
        Снимает все галочки на треках
        Может использоваться для очистки плейлиста
        """
        for i in range(self.ui.TracksToAdd.count()):
            self.ui.TracksToAdd.item(i).setCheckState(QtCore.Qt.Unchecked)

    def delete_selected_playlists(self):
        """
        Перезаписывает список плейлистов, добавляя те плейлисты, на виджетах которых НЕ стоит галочка,
        но не удаляет текущий плейлист из очереди воспроизведения.
        (Если удалился плейлист, который сейчас играет, то он продолжит играть и воспроизведение не остановится,
        также и с треками)
        """
        # Делаем временный список всех плейлистов
        tmp_playlists = self.all_playlists

        # Очищаем список для записи заного уже нужный треков
        self.all_playlists = []
        for i in range(len(tmp_playlists)):

            # Если плейлист не первый (потому что первым является плейлист всех треков и с ним никакие манипуляции
            # делать не разрешено) и плейлист без галочки (потому что галочка стоит за удаление текущего плейлиста,
            # значит удаляем все с галочками и оставляем все без галочек)
            if i != 0 and not self.ui.PlaylistToDelete.item(i - 1).checkState():
                self.all_playlists.append(tmp_playlists[i])
        self._open_playlists()

    def back_from_track_menu(self):
        """
        Функции для кнопки "назад" из меню трека.
        Выходит из меню трека в нужное меню, исходя из того, откуда меню трека было открыто
        """

        # Если открыто было из меню всех треков
        if self.track_open_source == 0:
            self._open_tracks()

        # Если открыто было из меню всех плейлистов
        elif self.track_open_source == 1:
            self._open_playlists()

        # Для всех остальных случаев открыть меню плейлиста (уже текущего)
        else:
            self._open_playlist()

    def move_all_tracks(self):
        """
        Функция для перемещения перетаскиванием элементов из списка всех треков. Срабатывает при перемещении элементов
        QListWidget
        """

        # Место куда будете перенесён выбранный трек
        index_move = self.ui.Tracks.currentRow()

        # Название трека, который будет перемещен
        # (т.к. элементом списка является виджет со своим отдельным классом, то обратиться к тексту самого виджет
        # нельзя (будет выдаваться NoneType) и нужно записывать имя в информацию виджета (data) с ключом "0")
        track = self.ui.Tracks.currentItem().data(0)
        if track is not None:
            self.all_tracks.move(track_node=track, index_move=index_move)

    def move_playlist_tracks(self):
        """
        Функция для перемещения перетаскиванием элементов из списка всех треков плейлиста. Срабатывает при перемещении
        элементов QListWidget
        """

        # Место куда будете перенесён выбранный трек
        index_move = self.ui.PlaylistTracks.currentRow()

        # Название трека, который будет перемещен
        track = self.ui.PlaylistTracks.currentItem().data(0)
        if track is not None:
            self.all_playlists[self.ui.Playlists.currentRow()].move(track_node=track, index_move=index_move)

    def next_track(self):
        """
        Если нажата кнопка переключения на следующий трек
        """

        # Трек начинает играть сразу при переключении, так что снимаем с паузы
        self.start_timer()
        self.current_playlist.is_paused = False
        self.current_playlist.current_node = self.current_playlist.current_node.next_item

        # Если во время переключения открыто меню трека
        if self.ui.stackedWidget.currentIndex() == 5:
            self._track_menu_update(self.current_playlist.current_node.data)
        self.current_playlist.play_current_node()

    def previous_track(self):
        """
        Если нажата кнопка переключения на предыдущий трек
        """

        # Трек начинает играть сразу при переключении, так что снимаем с паузы
        self.start_timer()
        self.current_playlist.is_paused = False
        self.current_playlist.current_node = self.current_playlist.current_node.previous_item

        # Если во время переключения открыто меню трека
        if self.ui.stackedWidget.currentIndex() == 5:
            self._track_menu_update(self.current_playlist.current_node.data)
        self.current_playlist.play_current_node()

    def start_timer(self) -> None:
        """
        Функция начала отсчета для таймера
        """
        self.timer.start(100)

    def stop_timer(self) -> None:
        """
        Функция остановки отсчета таймера
        """
        self.timer.stop()

    def track_update(self) -> None:
        """
        Функция постоянного обновления данных о проигровании трека
        Вызывается таймером каждые 100 милисекунд и обновляет текущее время и ползунок
        """
        self.ui.CurrentTrackTime.setText(time_to_str(self.current_playlist.current_duration_time()))
        self.ui.TrackTime.setText(time_to_str(self.current_track.length))
        self.ui.TrackProgressBar.setValue(self.current_playlist.current_duration_time() / self.current_track.length *
                                          1000)
        if self.current_playlist.current_duration_time() >= self.current_track.length - 1:
            self.next_track()

    def play_and_open_track(self):
        """
        Начать играть текущий трек и открыть меню трека
        """
        self.current_playlist.is_paused = False
        self._track_menu_update()
        self.current_playlist.play_current_node()
        self.start_timer()

    def pause_unpause_track(self):
        """
        При нажатии на кнопки пауз (несколько кнопок: в меню трека и сверху других экранов на текущем треке)
        """

        # Вызов из текущего плейлиста фукции, которая ставит на паузу или снимает с нее
        self.current_playlist.pause_unpause()
        if self.current_playlist.is_paused:
            self.ui.PauseTrackButton.setText("⯈")
            self.ui.PlayCurrentTrack.setText("⯈")
            self.ui.PlayCurrentTrack_2.setText("⯈")
            self.stop_timer()
        else:
            self.ui.PauseTrackButton.setText("| |")
            self.ui.PlayCurrentTrack.setText("| |")
            self.ui.PlayCurrentTrack_2.setText("| |")
            self.start_timer()

    def get_info(self):
        """
        Если пользователь нажимает на знак вопроса в меню трека и хочет получить максимально развёрнутую инфу о треке
        Создается новое текстовое окно-сообщение, где в качестве заголовка окна выступает название трека,
        а путь и время - текст сообщения
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(self.current_track.name)
        msg.setText("Path: " + self.current_track.file + "\nLength: " + time_to_str(self.current_track.length) +
                    " (" + str(self.current_track.length) + "c)")
        msg.exec()


def time_to_str(time: float = 0):
    """
    Функция для перевода секунд (длинны трека) в текстовое представления для интерфейса
    :param time: продолжительность трека
    :return: str строку времени для интерфейса в формате (4:08)
    """
    hours = str(math.floor(time // 3600))
    minutes = str(math.floor(time // 60))
    seconds = str(time % 60)
    if len(seconds) < 2:
        seconds = "0" + seconds
    if hours == "0":  # Если продолжительность меньше часа, то количество часов опускаем
        hours = ""
    else:
        hours += ":"
    return hours + minutes + ":" + seconds


def change_selection(item: QtWidgets.QListWidgetItem):
    """
    Меняет состояние переданного объекта на противоположное переданному (выбрано/не выбрано)
    Вызывается при нажатии на элемент списка QListWidget при выборе трека на добавления или выборе плейлиста на удаление
    :param item: виджет трека
    """
    if item.checkState():
        item.setCheckState(QtCore.Qt.Unchecked)
    else:
        item.setCheckState(QtCore.Qt.Checked)
