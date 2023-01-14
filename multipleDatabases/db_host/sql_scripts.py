import pandas as pd
from sqlalchemy import create_engine, inspect
import db_configs
import os

"""
Manual:

1) Добавить файл с утечкой до 1-2Гб
2) Убедиться, что есть подключение к базе (см. README)
3) Если есть ошибка кодировки, то поменять на cp1251/utf-8  
"""

def get_file_path(filename: str):
    return os.path.abspath(f'{filename}.txt')

def leak_to_db(filename: str):
    """
    :return: создает таблицу в базе данных с заданной утечкой
    """
    try:
        engine, connection = db_configs.mssql_config()
        df = pd.read_csv(get_file_path(filename), encoding='cp1251', sep=';')
        df_sql_version = df.to_sql(f'{filename} leak', connection, index=False)
        return 1
    except:
        return "Execution error! Check manual"

