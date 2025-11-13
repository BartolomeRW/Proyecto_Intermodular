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

def leer_mariadb(host, user, password, database, tabla):
    url = f"mysql+mariadbconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url, echo=False)

    with engine.connect() as conn:
        query = f"SELECT * FROM {tabla}"
        return pd.read_sql(query, conn)

def leer_sqlite(ruta_sqlite, tabla):
    url = f"sqlite:///{ruta_sqlite}"
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def leer_sqlalchemy(url, tabla):
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
