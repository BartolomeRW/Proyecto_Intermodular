from flask import Flask, render_template, request
import joblib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

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

        df = pd.read_csv("cosechas.csv")

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
