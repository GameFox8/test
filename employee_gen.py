import datetime
import pprint
import random
from datetime import timedelta
from openpyxl import Workbook

employees_list = list()

with open('FIO_re.txt') as f:
    employees_list = f.read().split('\n')
    if employees_list[-1] == '':
        employees_list = employees_list[:-1]


class ProjectsCreator:
    project_num = 1
    date_c = datetime.datetime(2018, 9, 17)

    def __init__(self, employees_list, projects_count):
        self.projects_count = projects_count
        self.employees_list = employees_list

    def generate_projects(self):
        project_list = list()
        for i in range(self.projects_count):
            project = dict()
            project['Название проекта'] = 'Проект' + str(self.project_num)
            project['Руководитель'] = self.employees_list[random.randint(0, int(len(self.employees_list) / 3))]
            project['Дата сдачи план.'] = self.date_c.strftime('%d.%m.%Y')
            self.date_c += timedelta(days=random.randint(-3, 3))
            project['Дата сдачи факт.'] = self.date_c.strftime('%d.%m.%Y')
            project['employees'] = list()
            for emp in self.employees_list:
                rnd_plan = random.randint(-1, 10)
                rnd_fact = rnd_plan + random.randint(-3, 3)
                project['employees'].append({(emp + ' план.'): rnd_plan if rnd_plan >= 0 else None,
                                             (emp + ' факт.'): rnd_fact if rnd_fact >= 0 else None})

            project_list.append(project)
            self.date_c += timedelta(days=random.randint(7, 21))
            self.project_num += 1

        self.__class__.project_num = self.project_num
        self.__class__.date_c = self.date_c

        return project_list

emp_count = 0
employees = list()

while emp_count < len(employees_list):
    rnd_batch = emp_count + random.randint(3, 10)
    employees.append(employees_list[emp_count: rnd_batch])
    emp_count = rnd_batch

for index, emp_list in enumerate(employees):
    emp_len = len(emp_list)
    projects = ProjectsCreator(emp_list, random.randint(emp_len, int(emp_len * 1.6))).generate_projects()
    titles = list(projects[0].keys())[:-1]
    titles.extend(sum([list(x.keys()) for x in projects[0]['employees']], []))

    wb = Workbook()

    ws = wb.active
    ws.title = 'Проекты'

    ws.append(titles)

    for project_data in projects:
        data = [project_data['Название проекта'],
                project_data['Руководитель'],
                project_data['Дата сдачи план.'],
                project_data['Дата сдачи факт.'],
                *sum([list(x.values()) for x in project_data['employees']], [])]

        ws.append(data)

    wb.save('employees/employees_data_' + str(index + 1) + '.xlsx')

print('Файлы excel сгенерированны')