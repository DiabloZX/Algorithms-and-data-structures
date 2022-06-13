# cython: language_level=3
# distutils: language = c

# Указываем компилятору, что используется Python 3 и целевой формат
# языка Си (во что компилируем, поддерживается Си и C++)


# Также понадобятся функции управления памятью
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

# Для преоразования Python объекта float в Сишный тип и обратно
from cpython.float cimport PyFloat_FromDouble, PyFloat_AsDouble
from cpython.long cimport PyLong_FromLong, PyLong_AsLong


# Так как хотим использовать массив для разных типов, указывая только
# код типа без дополнительных замарочек, то используем самописный
# дескриптор. Он будет хранить функции получения и записи значения в
# массив для нужных типов. Упрощенны аналог дескриптора из модуля array:
# https://github.com/python/cpython/blob/243b6c3b8fd3144450c477d99f01e31e7c3ebc0f/Modules/arraymodule.c#L32
cdef struct arraydescr:
    # код типа, один символ
    char* typecode
    # размер одного элемента массива
    int itemsize
    # функция получения элемента массива по индексу. Обратите внимание,
    # что она возвращает Python тип object. Вот так выглядит сигнатура на Си:
    # PyObject* (*getitem)(struct arrayobject *, Py_ssize_t)
    object(*getitem)(array, size_t)
    # функция записи элемента массива по индексу. Третий аргумент это
    # записываемое значение, оно приходит из Python. Сигнатура на Си:
    # int (*setitem)(struct arrayobject*, Py_ssize_t, PyObject*)
    int(*setitem)(array, size_t, object)


cdef object double_getitem(array a, size_t index):
    # Функция получения значения из массива для типа double.
    # Обратите внимание, что Cython сам преобразует Сишное значение типа
    # double в аналогичны объект PyObject
    return (<double *> a.data)[index]


cdef int double_setitem(array a, size_t index, object obj):
    # Функция записи значения в массив для типа double. Здесь нужно
    # самими извлеч значение из объекта PyObject.
    if not isinstance(obj, int) and not isinstance(obj, float):
        return -1

    # Преобразования Python объекта в Сишный
    cdef double value = PyFloat_AsDouble(obj)

    if index >= 0:
        # Не забываем преобразовывать тип, т.к. a.data имеет тип char
        (<double *> a.data)[index] = value
    return 0

cdef object int_getitem(array a, size_t index):
    # Функция получения значения из массива для типа double.
    # Обратите внимание, что Cython сам преобразует Сишное значение типа
    # double в аналогичны объект PyObject
    return (<long *> a.data)[index]


cdef int int_setitem(array a, size_t index, object obj):
    # Функция записи значения в массив для типа double. Здесь нужно
    # самими извлеч значение из объекта PyObject.
    if not isinstance(obj, int):
        return -1

    # Преобразования Python объекта в Сишный
    cdef long value = PyLong_AsLong(obj)

    if index >= 0:
        # Не забываем преобразовывать тип, т.к. a.data имеет тип char
        (<long *> a.data)[index] = value
    return 0


# Если нужно работать с несколькими типами используем массив дескрипторов:
# https://github.com/python/cpython/blob/243b6c3b8fd3144450c477d99f01e31e7c3ebc0f/Modules/arraymodule.c#L556
cdef arraydescr[2] descriptors = [
        arraydescr("d", sizeof(double), double_getitem, double_setitem),
        arraydescr("i", sizeof(long), int_getitem, int_setitem),
    ]

# Зачатки произвольных типов, значения - индексы дескрипторов в массиве
cdef enum TypeCode:
    DOUBLE = 0
    INT = 1

# преобразование строкового кода в число
cdef int char_typecode_to_int(str typecode):
    if typecode == "d":
        return TypeCode.DOUBLE
    elif typecode == "i":
        return TypeCode.INT
    return -1

cdef int normalize_index(int index, int length):
    if length > 0:
        if index < 0:
            if abs(index) > length:
                index = 0
            else:
                index = index % length
        elif index >= length:
            index = length
        return index
    raise IndexError()

cdef class array:
    # Класс статического массива.
    # В поле length сохраняем длину массива, а в поле data будем хранить
    # данные. Обратите внимание, что для data используем тип char,
    # занимающий 1 байт. Далее мы будем выделять сразу несколько ячеек
    # этого типа для одного значения другого типа. Например, для
    # хранения одного double используем 8 ячеек для char.
    cdef public size_t length
    cdef char* data
    cdef arraydescr* descr

    # Аналог метода __init__
    def __cinit__(self, str typecode, int size):
        self.length = size

        cdef size_t mtypecode = char_typecode_to_int(typecode)
        self.descr = &descriptors[mtypecode]

        # Выделяем память для массива
        self.data = <char*> PyMem_Malloc(size * self.descr.itemsize)
        if not self.data:
            raise MemoryError()
        self.initialize()


    # Не забываем освобаждать память. Привязываем это действие к объекту
    # Python. Это позволяет освободить память во время сборки мусора.
    def __dealloc__(self):
        PyMem_Free(self.data)


    # Пользовательски метод для примера. Инициализация массива числами
    # от 0 до length - 1. В Cython можно использовать функции из Python,
    # они преобразуются в Сишные аналоги.
    def initialize(self):
        # Объявление переменно цикла позволяет эффективнее комплировать код.
        for i in range(self.length):
            self.__setitem__(i, 0)



    # Добавим возможность получать элементы по индексу.
    def __getitem__(self, int index):
        if 0 <= index < self.length:
            return self.descr.getitem(self, index)
        raise IndexError()

    # Запись элементов по индексу.
    def __setitem__(self, int index, object value):
        if 0 <= index < self.length:
            self.descr.setitem(self, index, value)
        else:
            raise IndexError()

    # Добавление нового элемента в массив с конца.
    def append(self, object value):
        cdef char* new_data = <char*> PyMem_Malloc((self.length + 1) * self.descr.itemsize)

        for i in range(self.length):
            if self.descr.itemsize == sizeof(double):
                (<double *> new_data)[i] = self.descr.getitem(self, i)
            else:
                (<long *> new_data)[i] = self.descr.getitem(self, i)

        if self.descr.itemsize == sizeof(double):
            (<double *> new_data)[self.length] = value
        else:
            (<long *> new_data)[self.length] = value

        PyMem_Free(self.data)
        self.length += 1
        self.data = new_data

    # Добавление нового элемента в массив в нужное место.
    def insert(self, int index, object value):
        if index < 0 or index > self.length:
            index = normalize_index(index, self.length)
        cdef char* t = <char*> PyMem_Malloc(self.length * self.descr.itemsize)
        cdef int j = 0
        for j in range(self.length):
            t[j] = self.descr.getitem(self, j)
        PyMem_Free(self.data)
        self.length += 1
        self.data = <char*> PyMem_Malloc(self.length * self.descr.itemsize)
        cdef int i = 0
        cdef int added = 0
        for i in range(self.length):
                if i == index:
                    self.__setitem__(i, value)
                    added = 1
                else:
                    self.__setitem__(i, t[i - added])
        PyMem_Free(t)

    # Удаление первого вхождения значения в массиве.
    def remove(self, object value):
        cdef char* t = <char*> PyMem_Malloc(self.length * self.descr.itemsize)
        cdef int j
        for j in range(self.length):
            t[j] = self.descr.getitem(self, j)
        PyMem_Free(self.data)
        self.data = <char*> PyMem_Malloc((self.length )* self.descr.itemsize)
        cdef int i
        cdef int deleted = 0
        for i in range(self.length):
            if(t[i] == value and deleted == 0):
                self.length -= 1
                deleted = 1
            elif(i == self.length and deleted == 0):
                deleted = 1
            else:
                self.__setitem__(i - deleted, t[i])
        PyMem_Free(t)

    # Удаление первого вхождения значения в массиве и возврат его.
    def pop(self, int index):
        if index < 0:
            if abs(index) > self.length:
                raise IndexError
            else:
                index = normalize_index(index, self.length)
        if index >= self.length:
            raise IndexError
        cdef char* t = <char*> PyMem_Malloc(self.length * self.descr.itemsize)
        cdef int j
        for j in range(self.length):
            t[j] = self.descr.getitem(self, j)
        PyMem_Free(self.data)
        self.data = <char*> PyMem_Malloc((self.length - 1) * self.descr.itemsize)
        cdef int i
        cdef int deleted = 0
        cdef double item = 0
        for i in range(self.length):
            if(i == index and deleted == 0):
                self.length -= 1
                item = t[i]
                deleted = 1
            elif(i == self.length and deleted == 0):
                deleted = 1
            else:
                self.__setitem__(i - deleted, t[i])
        PyMem_Free(t)
        if self.descr.itemsize == sizeof(int):
            return int(item)
        else:
            return float(item)

    # Функция "разворота" массива.
    def reversed(self):
        cdef char* t = <char*> PyMem_Malloc(self.length * self.descr.itemsize)
        for i in range(self.length):
            t[i] = self.descr.getitem(self, self.length - i - 1)
        return t

    # Функция "разворота" массива.
    def len(self):
        return self.length

    # Функция "разворота" массива.
    def sizeof(self):
        return self.length * self.descr.itemsize