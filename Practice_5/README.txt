�������� �������������:

1) ��� �������� ������ � ������ ����� ������: 
python main.py -f unsorted\data_1.txt,unsorted\data_2.csv,unsorted\data_1.txt,unsorted\data_2.csv -o sorted\data_1.txt,sorted\data_2.txt,sorted\data_1.csv,sorted\data_2.csv -sk 0,0,0,0

2) ��� �������� ������ ���������� � �������� ���� (��������� ����, ������� ��� ����� �����������, ��� ������������ ��� � ��������� �������): 
python main.py -f unsorted\data_1.txt

3) ��� �������� �������:
python main.py -f unsorted\data_1.txt -o sorted\data_1.txt -r true

4) ��� �������� ����� key-�������:
python main.py -f unsorted\data_1.txt -o sorted\data_1.txt -k abs

5) ��� �������� ������ �������� ��� csv ������:
python main.py -f unsorted\data_2.csv -o sorted\data_2.csv -sk 1

6) ��� �������� ������ ���� ����������:
python main.py -f unsorted\data_2.csv -o sorted\data_2.csv -r true -k abs -sk 1

7) ��� ������ �������� ���� ������������ ��������� �� ���:
python main.py -f unsorted\data_1.txt,unsorted\data_2.csv,unsorted\data_1.txt,unsorted\data_2.csv -o sorted\data_1.txt,sorted\data_2.txt,sorted\data_1.csv,sorted\data_2.csv -r true,true,false,false -k abs,abs -sk 0,1,0,0

*��������� ������������ ����� ������� ��� ���������
*������������ ������� ��� �������� ��� ������-���� ����

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

-f ���� ��� ������, ������� ����� ����������� (������������ ��������)
-o �������� ����, ���� �������� ��������� (�������������� ��������)
-r ����������� �� � �������� ������� (�������������� ��������)
-k ����� key-������� ��������� (�������������� ��������)
-sk ���� ��� csv ����� (������������ �������� ��� ������� csv �����)