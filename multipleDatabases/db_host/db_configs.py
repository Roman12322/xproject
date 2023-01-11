from sqlalchemy import create_engine, inspect
import pandas as pd
import json
"""
В данном файле описаны конфиги для подключения к базам данных
"""

def mssql_config():
    """
    :return: admin's config + connection string for database mssql server 2012
    """
    #config settings
    HOST_NAME = 'mssql'
    USER = 'db_admin'
    PASSWORD = '2002'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    DATABASE = 'AdventureWorks2019'
    SERVER = 'HEEN'
    connection_URL = f"{HOST_NAME}://{USER}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}"
    mssql_engine = create_engine(connection_URL)
    mssql_connection = mssql_engine.connect()
    return mssql_engine, mssql_connection