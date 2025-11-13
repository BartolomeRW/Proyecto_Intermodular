import os
print("CargarDatos.py cargado desde:", os.path.abspath(__file__))

import pandas as pd
from sqlalchemy import create_engine

def leer_csv(ruta):
    return pd.read_csv(ruta)

def leer_mysql(host, user, password, database, tabla):
    url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

import mysql.connector
import pandas as pd

def leer_mariadb(host, user, password, database, tabla):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def leer_sqlite(ruta_sqlite, tabla):
    import sqlite3
    conn = sqlite3.connect(ruta_sqlite)
    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

from sqlalchemy import create_engine

def leer_sqlalchemy(url, query):
    engine = create_engine(url)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
