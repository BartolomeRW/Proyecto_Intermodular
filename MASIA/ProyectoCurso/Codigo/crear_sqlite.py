import sqlite3
import pandas as pd

# Cargar CSV
df = pd.read_csv("cosechas.csv")

# Normalizar nombres
df.columns = df.columns.str.lower()

df.rename(columns={
    "temperatura_media": "temperatura",
    "lluvia_mm": "lluvia"
}, inplace=True)

# Crear base de datos SQLite
conn = sqlite3.connect("basedatos.db")

# Guardar tabla
df.to_sql("cosechas", conn, if_exists="replace", index=False)

conn.close()

print("Base de datos SQLite creada correctamente: basedatos.db")
