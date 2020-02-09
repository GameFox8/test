# Задача Pyhon – анализ успешности сотрудников

## Задача
Есть N файлов excel в папке. В файлах лежит информация о планах работы и сотрудниках участвующих в проектах. 

Колонки:
* Название проекта
* Руководитель – сотрудник ответственный за проект
* Дата сдачи (палн и факт) – планируемая и фактическая дата сдачи проекта
* Список сотрудников (план и факт) – сколько человеко-дней каждого сотрудника потрачено на проект по плану и по факту.

Сотрудников и проектов может быть сколько угодно в каждом файле. В каждом файле полезная информация лежит только на первом листе.
Необходимо по этим файлам оценить успешность сотрудников. Критерий для успешности выбрать самому.
Сделать вывод списка сотрудников в порядке их успешности по выбранному критерию.

## Используемые библиотеки
* openpyxl (<https://openpyxl.readthedocs.io/en/stable/>)
* sycopg2 (<https://github.com/psycopg/psycopg2>)
