import pandas as pd
import pymysql
import sqlite3

# ------------------------------
# LECTURA DESDE CSV
# ------------------------------
def leer_csv(ruta):
    return pd.read_csv(ruta)


# ------------------------------
# LECTURA DESDE MYSQL / MARIADB
# ------------------------------
def leer_mariadb(host, user, password, database, tabla):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
    conn.close()
    return df


# ------------------------------
# LECTURA DESDE SQLITE
# ------------------------------
def leer_sqlite(ruta_sqlite, tabla):
    conn = sqlite3.connect(ruta_sqlite)
    df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
    conn.close()
    return df
