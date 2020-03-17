from time import sleep
from uuid import uuid4

import pyodbc

from .base import *

DB_DRIVER = 'ODBC Driver 17 for SQL Server'
DB_HOST = os.environ['MCR_MICROSOFT_COM_MSSQL_SERVER_HOST']
DB_PORT = os.environ['MCR_MICROSOFT_COM_MSSQL_SERVER_1433_TCP']
DB_USER = 'sa'
DB_PASSWORD = 'River@Credentials'
sleep(10)
db_connection = pyodbc.connect(f"DRIVER={DB_DRIVER};SERVER={DB_HOST},{DB_PORT};DATABASE=master;UID={DB_USER};PWD={DB_PASSWORD}", autocommit=True)
cursor = db_connection.cursor()
cursor.execute(
    """
     If(db_id(N'river') IS NULL)
    BEGIN
        CREATE DATABASE river
    END;
    """)

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'river',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TEST': {
            'NAME': 'river' + str(uuid4()),
        },
        'OPTIONS': {
            'driver': DB_DRIVER
        },
    }
}

INSTALLED_APPS += (
    'river.tests',
)

if django.get_version() >= '1.9.0':
    MIGRATION_MODULES = DisableMigrations()
