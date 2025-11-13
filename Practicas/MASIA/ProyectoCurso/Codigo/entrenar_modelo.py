import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

data = pd.read_csv("cosechas.csv")

X = data[["hectareas", "temperatura_media", "lluvia_mm"]]
y = data["toneladas"]

modelo = LinearRegression()
modelo.fit(X, y)

joblib.dump(modelo, "modelo_IA.pkl")

pred = modelo.predict(X)
print("Modelo entrenado correctamente.")
print("R²:", round(r2_score(y, pred), 4))
print("MAE:", round(mean_absolute_error(y, pred), 2))
