Программа для реализации построения лабиринта и нахождения пути с помощью алгоритма "Поиск в глубину".
разработал студент СФУ ИКИТ группы КИ20-17/2Б Смыков Алексей.

Теги для запуска:
-he: высота лабиринта
-wi: ширина лабиринта
-o: путь до выходного файла
-i: путь до входного файла
-s: флаг для решения лабиринта
-g: флаг для создания гифки

Примеры запуска:
python main.py -he 10 -wi 10 -o maze_0.png -g true
python main.py -he 10 -wi 10 -o maze_1.txt -g true 

python main.py -i maze_0.png -o maze_2.txt -g true -s true
python main.py -i maze_1.txt -o maze_3.png -g true -s true

python main.py -he 15 -wi 15 -o maze_4.txt -g true -s true
python main.py -he 15 -wi 15 -o maze_5.png -g true -s true
