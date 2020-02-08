import copy
import openpyxl


def parse_projects(file_path):
    projects = list()
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheet = wb.active

    fio_list = [{'fio': x.value[:-6]} for x in list(sheet.rows)[0][4::2]]

    for row in sheet.iter_rows(min_row=2):
        project = dict()
        project['title'] = row[0].value
        project['manager_fio'] = row[1].value
        project['date_plan'] = row[2].value
        project['date_fact'] = row[3].value
        project['employees'] = copy.deepcopy(fio_list)

        for i, cell in enumerate(row[4::2]):
            project['employees'][i]['days_plan'] = cell.value

        for i, cell in enumerate(row[5::2]):
            project['employees'][i]['days_fact'] = cell.value

        projects.append(project)

    return projects
