import pandas as pd
from sqlalchemy import inspect, text
import  db_configs
import os
"""
Manual:

1) Добавить файл с утечкой до 1-2Гб
2) Убедиться, что есть подключение к базе (см. README)
3) Если есть ошибка кодировки, то поменять на cp1251/utf-8  
"""


def get_file_path(filename):
    return os.path.abspath(f'{filename}')


def leak_to_db(file):
    """
    :return: создает таблицу в базе данных с заданной утечкой
    """
    try:
        engine, connection = db_configs.mssql_config()
        tmp_file = open("new_leak.txt", "w")
        decoded_file = file.read().decode('cp1251')
        for row in decoded_file:
            tmp_file.write(row)
        df = pd.read_csv(get_file_path("new_leak.txt"), encoding='cp1251', sep=';')
        df_sql_version = df.to_sql(f'{file}_leak', connection, index=False)
        os.remove("new_leak.txt")
        return "Successfully uploaded"
    except:
        return "Execution error"


def get_table_names(engine):
    """
    :param engine: движок для подключения к базе данных (хранит все доступные имена таблиц)
    :return: список имен таблиц
    """
    try:
        inspector = inspect(engine)
        table_names_list = inspector.get_table_names()
        return table_names_list
    except:
        return "engine error! unable to get table names"


def get_column_names(engine, table_name: str):
    """
    :param engine: движок для подключения к базе данных (хранит все доступные имена таблиц)
    :param table_name: имя заданной таблицы
    :return: возвращает список имен столбцов
    """
    tables = get_table_names(engine=engine)
    for item_name in tables:
        if item_name == table_name:
            with engine.connect() as connection:
                result = connection.execute(text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS"
                                                       f" WHERE TABLE_NAME = '{item_name}'"
                                                       f" ORDER BY ORDINAL_POSITION")).fetchall()
                column_names = []
                for item_1 in result:
                    for item in item_1:
                        column_names.append(item)
                return column_names


