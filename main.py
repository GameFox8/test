import os
from src.ExcelParser import parse_projects
from src import DbProjects as dp

path = 'employees/'


def main():
    files = [r + x for r, d, f in os.walk(path) for x in f]

    db = dp.Postgre(database='postgres', user='postgres', password='456789boks')
    db.create_database('test_1')    # создат базу данных с нужной струтурой для работы

    for file in files:
        for project in parse_projects(file):
            db.add_project(project)

    variance_rating = db.get_variance_rating()
    print('Рейтинг сотрудников по среднеквадратическому отклонению человекодней от плана:')
    for id_e, fio, variance in variance_rating:
        print('fio: {:18s} \t variance: {:10g}'.format(fio, variance))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
