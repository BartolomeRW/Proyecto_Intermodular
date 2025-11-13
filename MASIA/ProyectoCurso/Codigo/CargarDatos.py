import pandas as pd
from sqlalchemy import create_engine

def leer_csv(ruta):
    return pd.read_csv(ruta)


# ----------------------------
# LECTOR MYSQL
# ----------------------------
def leer_mysql(host, user, password, database, tabla):
    url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)

    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, engine)
    return df


# ----------------------------
# LECTOR MARIADB
# ----------------------------
def leer_mariadb(host, user, password, database, tabla):
    url = f"mariadb+mariadbconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)

    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, engine)
    return df


# ----------------------------
# LECTOR SQLITE
# ----------------------------
def leer_sqlite(ruta_sqlite, tabla):
    url = f"sqlite:///{ruta_sqlite}"
    engine = create_engine(url)

    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, engine)
    return df


# ----------------------------
# LECTOR SQLALCHEMY
# ----------------------------
def leer_sqlalchemy(url, tabla):
    engine = create_engine(url)

    query = f"SELECT * FROM {tabla}"
    df = pd.read_sql(query, engine)
    return df
