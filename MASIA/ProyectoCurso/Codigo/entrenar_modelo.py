import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import CargarDatos as fuente    # ← IMPORT OBLIGATORIO

# ----------------------------------------
# SELECCIONAR FUENTE DE DATOS
# ----------------------------------------

# CSV
data = fuente.leer_csv("cosechas.csv")

# MySQL
# data = fuente.leer_mysql("localhost", "root", "1234", "masia", "cosechas")

# MariaDB
# data = fuente.leer_mariadb("localhost", "root", "1234", "masia", "cosechas")

# SQLite
# data = fuente.leer_sqlite("basedatos.db", "cosechas")

# SQLAlchemy universal
# data = fuente.leer_sqlalchemy("postgresql://user:pass@localhost/db", "SELECT * FROM cosechas")

# ----------------------------------------

X = data[["hectareas", "temperatura_media", "lluvia_mm"]]
y = data["toneladas"]

modelo = LinearRegression()
modelo.fit(X, y)

joblib.dump(modelo, "modelo_IA.pkl")

pred = modelo.predict(X)
print("Modelo entrenado correctamente.")
print("R²:", round(r2_score(y, pred), 4))
print("MAE:", round(mean_absolute_error(y, pred), 2))
