Варианты использования:

1) Для проверки работы с разным типом файлов: 
python main.py -f unsorted\data_1.txt,unsorted\data_2.csv,unsorted\data_1.txt,unsorted\data_2.csv -o sorted\data_1.txt,sorted\data_2.txt,sorted\data_1.csv,sorted\data_2.csv -sk 0,0,0,0

2) Для проверки записи результата в исходный файл (Перепишет файл, поэтому его лучше скопировать, или использовать это в последнюю очередь): 
python main.py -f unsorted\data_1.txt

3) Для проверки реверса:
python main.py -f unsorted\data_1.txt -o sorted\data_1.txt -r true

4) Для проверки ввода key-функции:
python main.py -f unsorted\data_1.txt -o sorted\data_1.txt -k abs

5) Для проверки работы индексов для csv файлов:
python main.py -f unsorted\data_2.csv -o sorted\data_2.csv -sk 1

6) Для проверки работы всех аргументов:
python main.py -f unsorted\data_2.csv -o sorted\data_2.csv -r true -k abs -sk 1

7) Для ПОЛНОЙ проверки всех возможностей программы за раз:
python main.py -f unsorted\data_1.txt,unsorted\data_2.csv,unsorted\data_1.txt,unsorted\data_2.csv -o sorted\data_1.txt,sorted\data_2.txt,sorted\data_1.csv,sorted\data_2.csv -r true,true,false,false -k abs,abs -sk 0,1,0,0

*аргументы записываются через запятую без пропусков
*записываются сначала все значения для какого-либо типа

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

-f Пути для файлов, которые нужно сортировать (обязательный аргумент)
-o выходные пути, куда записать результат (необязательный аргумент)
-r сортировать ли в обратном порядке (необязательный аргумент)
-k какую key-функцию применить (необязательный аргумент)
-sk ключ для csv файла (обязательный аргумент для каждого csv файла)