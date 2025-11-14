import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import CargarDatos as fuente

# Cargar datos
df = fuente.leer_csv("cosechas.csv")  # archivo subido

# Detectar columnas automáticamente
cols = fuente.detectar_columnas(df)

# Validación mínima
necesarias = ["hectareas", "temperatura", "lluvia", "toneladas"]
for col in necesarias:
    if cols[col] is None:
        raise Exception(f"No se encontró la columna necesaria: {col}")

# Preparar X e Y
X = df[[cols["hectareas"], cols["temperatura"], cols["lluvia"]]]
y = df[cols["toneladas"]]

# Entrenar modelo
modelo = LinearRegression()
modelo.fit(X, y)

joblib.dump(modelo, "modelo_IA.pkl")

# Evaluar
pred = modelo.predict(X)
print("Modelo entrenado correctamente.")
print("R²:", round(r2_score(y, pred), 4))
print("MAE:", round(mean_absolute_error(y, pred), 2))
