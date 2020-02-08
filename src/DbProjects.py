import psycopg2 as pg
import psycopg2.extensions
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Postgre():
    sql_create = '''
        CREATE TABLE employees
        (
            id serial PRIMARY KEY,
            fio text NOT NULL UNIQUE
        );
        
        CREATE TABLE projects
        (
            id serial PRIMARY KEY,
            title text NOT NULL,
            manager_id integer NOT NULL,
            date_plan date NOT NULL,
            date_fact date NOT NULL,
            FOREIGN KEY (manager_id) REFERENCES employees (id)
        );
        
        CREATE TABLE work_list
        (
            project_id integer NOT NULL,
            employee_id integer NOT NULL,
            days_plan integer,
            days_fact integer,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        );
    '''
    sql_clear = '''
        TRUNCATE TABLE projects RESTART IDENTITY CASCADE;
        TRUNCATE TABLE employees RESTART IDENTITY CASCADE;
    '''
    sql_get_rating = '''
        SELECT emp.id AS "ID",emp.fio AS "ФИО", sd_r.SD AS "Среднеквадратическое отклонение от плана"
        FROM
        (
            SELECT SQRT(AVG(POWER((COALESCE(days_fact, 0) - COALESCE(days_plan, 0)), 2))) AS SD,
            employee_id
            FROM work_list 
            GROUP BY employee_id
        ) AS sd_r
        INNER JOIN employees AS emp
        ON sd_r.employee_id = emp.id
        ORDER BY SD
    '''

    def __init__(self, database, user, password, host='localhost', port='5432'):
        '''

        :param database: Database name
        :param user: Login
        :param password: Password
        :param host: Address server
        '''
        self._connection = None
        self._connection_data = {'database': database,
                                 'user': user,
                                 'password': password,
                                 'host': host,
                                 'port': port}
        self._connection = pg.connect(database=database, user=user, password=password, host=host, port=port)

    def create_database(self, dbname):
        '''
        Creates a database with the necessary tables to work with

        :param dbname: Database name
        '''
        self._connection_data['database'] = dbname
        self._connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = self._connection.cursor()
        cursor.execute('create database ' + dbname)
        self._connection.close()
        self._connection = pg.connect(
            dbname=dbname,
            user=self._connection_data['user'],
            password=self._connection_data['password'],
            host=self._connection_data['host'],
            port=self._connection_data['port']
        )
        cursor = self._connection.cursor()
        cursor.execute(self.sql_create)
        self._connection.commit()
        cursor.close()

    def clear_data(self):
        '''
        Cleans all the tables

        '''
        cursor = self._connection.cursor()
        cursor.execute(self.sql_clear)
        self._connection.commit()
        cursor.close()

    def add_project(self, project):
        '''
        Adds project information to the database

        :param project: dict. with project information
        '''
        none_to_null = lambda x: x if x is not None else 'null'
        self._connection.autocommit = False
        cursor = self._connection.cursor()
        if cursor is not None:
            try:
                cursor.execute(
                    "INSERT INTO employees(fio)"
                    "VALUES {}"
                    "ON CONFLICT (fio)"
                    "DO NOTHING;".format(', '.join(["('{}')".format(x['fio']) for x in project['employees']]))
                )
                cursor.execute(
                    "INSERT INTO projects(title, manager_id, date_plan, date_fact)"
                    "VALUES "
                    "("
                    "   '{}',"
                    "   (SELECT id FROM employees WHERE fio = '{}'),"
                    "   '{}'::date,"
                    "   '{}'::date"
                    ") RETURNING id".format(project['title'],
                                            project['manager_fio'],
                                            project['date_plan'],
                                            project['date_fact'])
                )

                last_project_id = cursor.fetchone()[0]

                for emp in project['employees']:
                    cursor.execute(
                        "INSERT INTO work_list(project_id, employee_id, days_plan, days_fact)"
                        "VALUES "
                        "("
                        "   {},"
                        "   (SELECT id FROM employees WHERE fio = '{}'),"
                        "   {},"
                        "   {}"
                        ")".format(last_project_id,
                                   emp['fio'],
                                   none_to_null(emp['days_plan']),
                                   none_to_null(emp['days_fact']))
                    )
                self._connection.commit()
            except pg.DatabaseError as err:
                print(err)
                self._connection.rollback()
            finally:
                cursor.close()

    def get_variance_rating(self):
        '''

        :return: List of employees sorted by standard deviation from the set plan
        '''
        cursor = self._connection.cursor()
        cursor.execute(self.sql_get_rating)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __del__(self):
        if self._connection is not None:
            self._connection.close()
