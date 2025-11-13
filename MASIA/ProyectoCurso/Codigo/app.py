from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import joblib

from CargarDatos import (
    leer_csv,
    leer_mysql,
    leer_mariadb,
    leer_sqlite,
    leer_sqlalchemy
)

app = Flask(__name__)
modelo = joblib.load("modelo_IA.pkl")

# Crear carpeta static si no existe
if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/", methods=["GET", "POST"])
def index():
    prediccion = None
    grafico = None

    if request.method == "POST":

        origen = request.form.get("origen")
        hect = float(request.form["hectareas"])
        temp = float(request.form["temperatura"])
        lluv = float(request.form["lluvia"])

        # ORIGEN DE DATOS
        if origen == "mysql":
            df = leer_mysql(
                host="localhost",
                user="root",
                password="1234",
                database="produccion_agricola",
                tabla="cosechas"
            )

        elif origen == "mariadb":
            df = leer_mariadb("localhost", "root", "1234", "produccion_agricola", "cosechas")

        elif origen == "sqlite":
            df = leer_sqlite("basedatos.db", "cosechas")

        elif origen == "sqlalchemy":
            df = leer_sqlalchemy(
                "postgresql://usuario:pass@localhost/basedatos",
                "SELECT * FROM cosechas"
            )

        else:
            df = leer_csv("cosechas.csv")

        # PREDICCIÓN
        entrada = np.array([[hect, temp, lluv]])
        prediccion = round(float(modelo.predict(entrada)[0]), 2)

        # GRÁFICO
        plt.figure(figsize=(6, 4))
        plt.plot(df["ano"], df["toneladas"], marker="o", color="blue")
        plt.scatter(2026, prediccion, color="red", s=100)

        plt.title("Predicción de producción agrícola")