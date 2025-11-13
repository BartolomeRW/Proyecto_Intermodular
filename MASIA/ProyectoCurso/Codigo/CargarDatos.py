import pandas as pd
import sqlite3
import mysql.connector

# CSV
def leer_csv(ruta):
    return pd.read_csv(ruta)

# MYSQL / MARIADB
def leer_mariadb(host, user, password, database, tabla):
    try:
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

    except Exception as e:
        print("ERROR en MariaDB/MySQL:", e)
        return None

# SQLITE
def leer_sqlite(ruta_sqlite, tabla):
    try:
        conn = sqlite3.connect(ruta_sqlite)
        query = f"SELECT * FROM {tabla}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print("ERROR en SQLite:", e)
        return None