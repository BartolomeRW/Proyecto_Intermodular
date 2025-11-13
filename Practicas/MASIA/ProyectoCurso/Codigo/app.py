from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from flask import Flask, render_template, request
import joblib
import CargarDatos as fuente   # Import correcto

app = Flask(__name__)
modelo = joblib.load("modelo_IA.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediccion = None
    grafico = None

    if request.method == "POST":
        hect = float(request.form["hectareas"])
        temp = float(request.form["temperatura"])
        lluv = float(request.form["lluvia"])

        entrada = np.array([[hect, temp, lluv]])
        prediccion = round(modelo.predict(entrada)[0], 2)

        # -------------------------------------
        # SELECCIONAR FUENTE DE DATOS PARA LA WEB
        # -------------------------------------

        # -------------------------------------
        # SELECCIONAR FUENTE DE DATOS PARA LA WEB
        # -------------------------------------

        origen = request.form.get("origen")

        if origen == "csv":
            df = fuente.leer_csv("cosechas.csv")

        elif origen == "mysql":
            df = fuente.leer_mysql("localhost", "root", "1234", "masia", "cosechas")

        elif origen == "mariadb":
            df = fuente.leer_mariadb("localhost", "root", "1234", "masia", "cosechas")

        elif origen == "sqlite":
            df = fuente.leer_sqlite("basedatos.db", "cosechas")

        elif origen == "sqlalchemy":
            df = fuente.leer_sqlalchemy(
                "postgresql://user:pass@localhost/db",
                "SELECT * FROM cosechas"
            )

        else:
            df = fuente.leer_csv("cosechas.csv")   # fallback

        # CSV
        df = fuente.leer_csv("cosechas.csv")

        # MySQL
        # df = fuente.leer_mysql("localhost", "root", "1234", "masia", "cosechas")

        # MariaDB
        # df = fuente.leer_mariadb("localhost", "root", "1234", "masia", "cosechas")

        # SQLite
        # df = fuente.leer_sqlite("basedatos.db", "cosechas")

        # SQLAlchemy
        # df = fuente.leer_sqlalchemy("postgresql://user:pass@localhost/db", "SELECT * FROM cosechas")

        # -------------------------------------

        if not os.path.exists("static"):
            os.makedirs("static")

        plt.figure(figsize=(6, 4))
        plt.plot(df["anio"], df["toneladas"], marker="o")
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

fuente.guardar_prediccion(origen, {
    "hectareas": hect,
    "temperatura": temp,
    "lluvia": lluv,
    "prediccion": prediccion
})
