import pandas as pd
import pymysql
import sqlite3

# ------------------------------
# LECTURA DESDE CSV
# ------------------------------
def leer_csv(ruta):
    return pd.read_csv(ruta)

def leer_excel(ruta):
    return pd.read_excel(ruta)

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

def detectar_columnas(df):
    columnas = {
        "hectareas": None,
        "temperatura": None,
        "lluvia": None,
        "toneladas": None,
        "año": None,
    }

    # Normalizar nombres de columnas
    df_cols = {col.lower(): col for col in df.columns}

    # Posibles variantes
    posibles = {
        "hectareas": ["hectareas", "hectáreas", "ha", "superficie", "area"],
        "temperatura": ["temperatura", "temp", "tmed", "media_temperatura"],
        "lluvia": ["lluvia", "precipitacion", "rain", "mm", "agua"],
        "toneladas": ["toneladas", "produccion", "kg", "output", "yield"],
        "año": ["año", "year", "fecha", "anio"],
    }

    # Buscar coincidencias
    for clave, variantes in posibles.items():
        for v in variantes:
            for col_norm, col_real in df_cols.items():
                if v in col_norm:
                    columnas[clave] = col_real

    return columnas
