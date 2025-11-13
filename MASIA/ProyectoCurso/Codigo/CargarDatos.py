import pandas as pd
from sqlalchemy import create_engine

def leer_csv(ruta):
    return pd.read_csv(ruta)

# ----------------------------
# MYSQL
# ----------------------------
def leer_mysql(host, user, password, database, tabla):
    url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# ----------------------------
# MARIADB
# ----------------------------
def leer_mariadb(host, user, password, database, tabla):
    url = f"mariadb+mariadbconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# ----------------------------
# SQLITE
# ----------------------------
def leer_sqlite(ruta_sqlite, tabla):
    url = f"sqlite:///{ruta_sqlite}"
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# ----------------------------
# SQLALCHEMY (GENÉRICO)
# ----------------------------
def leer_sqlalchemy(url, tabla):
    engine = create_engine(url)
    query = f"SELECT * FROM {tabla}"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
