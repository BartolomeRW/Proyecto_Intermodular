import pandas as pd
from sqlalchemy import create_engine

def leer_csv(ruta):
    return pd.read_csv(ruta)

def leer_mysql(host, user, password, database, tabla):
    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(url, echo=False)
    with engine.connect() as conn:
        return pd.read_sql(f"SELECT * FROM {tabla}", conn)

def leer_mariadb(host, user, password, database, tabla):
    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(url, echo=False)
    with engine.connect() as conn:
        return pd.read_sql(f"SELECT * FROM {tabla}", conn)

def leer_sqlite(ruta_sqlite, tabla):
    url = f"sqlite:///{ruta_sqlite}"
    engine = create_engine(url)
    return pd.read_sql(f"SELECT * FROM {tabla}", engine)

def leer_sqlalchemy(url, query):
    engine = create_engine(url)
    return pd.read_sql(query, engine)
