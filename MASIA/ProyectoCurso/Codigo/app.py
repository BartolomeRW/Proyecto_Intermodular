from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import joblib

# Import correcto de funciones personalizadas
from CargarDatos import (
    leer_csv,
    leer_mysql,
    leer_mariadb,
    leer_sqlite,
    leer_sqlalchemy
)

app = Flask(__name__)
modelo = joblib.load("modelo_IA.pkl")


@app.route("/", methods=["GET", "POST"])
def index():
    prediccion = None
    grafico = None

    if request.method == "POST":

        # ---------------------------
        # CAPTURAR DATOS DEL FORM
        # ---------------------------
        origen = request.form.get("origen")
        hect = float(request.form["hectareas"])
        temp = float(request.form["temperatura"])
        lluv = float(request.form["lluvia"])

        # ---------------------------
        # SELECCIÓN DE ORIGEN
        # ---------------------------
        if origen == "mysql":
            df = leer_mysql(
                host="localhost",
                user="root",
                password="1234",          # tu contraseña de MySQL
                database="produccion_agricola",
                tabla="cosechas"
            )

        elif origen == "mariadb":
            df = leer_mariadb("localhost", "root", "1234", "produccion_agricola", "cosechas")

        elif origen == "sqlite":
            df = leer_sqlite("basedatos.db", "cosechas")

        else:   # CSV por defecto
            df = leer_csv("cosechas.csv")

        # ---------------------------
        # PREDICCIÓN DEL MODELO
        # ---------------------------
        entrada = np.array([[hect, temp, lluv]])
        prediccion = round(modelo.predict(entrada)[0], 2)

        # ---------------------------
        # GENERAR GRÁFICO
        # ---------------------------
        if not os.path.exists("static"):
            os.makedirs("static")

        plt.figure(figsize=(6, 4))
        plt.plot(df["ano"], df["toneladas"], marker="o")
        plt.scatter(2026, prediccion, color="red")

        plt.title("Predicción de producción")
        plt.xlabel("Año")
        plt.ylabel("Toneladas")
        plt.tight_layout()

        grafico = "static/grafico.png"
        plt.savefig(grafico)
        plt.close()

    return render_template("index.html", prediccion=prediccion, grafico=grafico)


if __name__ == "__main__":
    app.run(debug=True)
