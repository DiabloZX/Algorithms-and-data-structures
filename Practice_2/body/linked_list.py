"""Модуль связного списка"""

from typing import Union


class LinkedListItem:
    """Класс элемента ссписка"""
    def __init__(self, data=None) -> None:
        """Инициализация"""
        self.data = data
        self.next_item_ = None
        self.previous_item_ = None

    @property
    def next_item(self) -> object:
        """Получить ссылку на следующий элемент"""
        return self.next_item_

    @next_item.setter
    def next_item(self, item) -> None:
        """Установить ссылку на следующий элемент"""
        self.next_item_ = item
        item.previous_item_ = self

    @property
    def previous_item(self) -> object:
        """Получить ссылку на предыдущий элемент"""
        return self.previous_item_

    @previous_item.setter
    def previous_item(self, item) -> None:
        """Установить ссылку на предыдущий элемент"""
        self.previous_item_ = item
        item.next_item_ = self


class LinkedList:
    """Класс списка"""
    def __init__(self, first_item: LinkedListItem = None) -> None:
        """Инициализация"""
        self.first_item = None
        self.last = None
        self.length = 0
        self.iterator_counter = -1

        if first_item is not None and isinstance(first_item, LinkedListItem):
            self.first_item = first_item
            self.last = self.first_item.previous_item_
            self.tmp_item = self.first_item.next_item_
            self.length += 1
            while self.tmp_item != self.first_item:
                # Если передается список через узел, то добавляем все узлы через проход кругом
                self.length += 1
                self.tmp_item = self.tmp_item.next_item_

    def _append_chooser(self, data: object, right: bool) -> None:
        """Вспомогательная функция добавления элемента с конца или с начала на выбор"""
        if not isinstance(data, LinkedListItem):
            new_item = LinkedListItem(data)
            if self.first_item is None:
                self.first_item = new_item
                self.last = new_item
                self.last.next_item = self.first_item
            else:
                self.first_item.previous_item = new_item
                self.last.next_item = new_item
                if right:
                    self.last = new_item
                else:
                    self.first_item = new_item
            self.length += 1

    def append_left(self, data: object) -> None:
        """Добавить элемент слева (с начала)"""
        self._append_chooser(data, False)

    def append_right(self, data: object) -> None:
        """Добавить элемент справа (с конца)"""
        self._append_chooser(data, True)

    def append(self, data: object) -> None:
        """Добавить элемент справа (с конца)"""
        self._append_chooser(data, True)

    def insert(self, index: int, data: object) -> None:
        """Добавить элемент по индексу"""
        if not isinstance(data, LinkedListItem):
            if index == 0:
                self.append_left(data)
            elif index == self.length:
                self.append_right(data)
            else:
                new_item = LinkedListItem(data)
                old_item = self.item_data(index=index)
                if old_item is None:
                    return
                old_item.previous_item_.next_item = new_item
                old_item.previous_item = new_item
                self.length += 1

    def remove(self, data: object) -> None:
        """Удалить элемент из списка"""
        if not isinstance(data, LinkedListItem):
            delete_item = self.item_data(data=data)
            if delete_item is None:
                raise ValueError()
            self.length -= 1
            if self.length == 0:
                self.first_item = None
                self.last = None
            else:
                if delete_item == self.first_item:
                    self.first_item = self.first_item.next_item_
                    self.last.next_item = self.first_item
                elif delete_item == self.last:
                    self.last = self.last.previous_item_
                    self.last.next_item = self.first_item
                else:
                    delete_item.previous_item_.next_item = delete_item.next_item_

    def change_item_index(self, item: LinkedListItem, new_index: int) -> None:
        """Переместить элемент на новый индекс"""
        if item is None or new_index < 0 or new_index > self.length - 1:
            return
        self.remove(item)
        self.insert(new_index, item)

    def item_data(self, index=None, data=None) -> Union[LinkedListItem, None]:
        """Получить элемент по содержимому или индексу"""
        item = self.first_item
        for i in range(self.length):
            if i == index or item.data == data:
                return item
            item = item.next_item_
        return None

    def __reversed__(self) -> object:
        reversed_list = LinkedList()
        for item in self:
            reversed_list.append_left(item.data)
        return reversed_list

    def __str__(self) -> str:
        string = "["
        for item in self:
            string += str(item.data) + ","
        if len(string) > 1:
            return string[:-1] + "]"
        return string + "]"

    def __len__(self) -> int:
        return self.length

    def __contains__(self, data: object) -> bool:
        item = self.first_item
        for _ in range(self.length):
            if data == item.data:
                return True
            item = item.next_item
        return False

    def __iter__(self) -> iter:
        return self

    def __next__(self) -> LinkedListItem:
        self.iterator_counter += 1
        if self.iterator_counter == self.length:
            self.iterator_counter = -1
            raise StopIteration
        return self.item_data(index=self.iterator_counter)

    def __getitem__(self, index: int) -> object:
        if index > self.length - 1 or abs(index) > self.length:
            raise IndexError()
        negative_index = 0
        if index < 0:
            negative_index = self.length + index
        return self.item_data(index=(max(index, negative_index))).data
