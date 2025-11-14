import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib

from CargarDatos import leer_csv, leer_mariadb, leer_sqlite

app = Flask(__name__)
modelo = joblib.load("modelo_IA.pkl")


# Crear carpeta static si no existe
if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/upload", methods=["POST"])
def upload():
    archivo = request.files["archivo"]
    ruta = os.path.join("uploads", archivo.filename)
    archivo.save(ruta)

    # Detectar tipo de archivo
    if archivo.filename.endswith(".csv"):
        df = fuente.leer_csv(ruta)

    elif archivo.filename.endswith(".xlsx") or archivo.filename.endswith(".xls"):
        df = fuente.leer_excel(ruta)

    else:
        return "Formato no compatible"

    # Guardar DataFrame para entrenamiento
    df.to_csv("cosechas.csv", index=False)

    return "Archivo subido correctamente. Ahora puedes entrenar la IA."

@app.route("/train", methods=["POST"])
def train():
    import subprocess
    proceso = subprocess.run(["python", "entrenar_modelo.py"], capture_output=True, text=True)
    return f"<pre>{proceso.stdout}</pre>"

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

        # Cargar datos ya entrenados
        df = pd.read_csv("cosechas.csv")

        # Gráfico
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

        # ------------------------------
        # PREDICCIÓN
        # ------------------------------
        entrada = np.array([[hect, temp, lluv]])
        prediccion = round(float(modelo.predict(entrada)[0]), 2)

        # ------------------------------
        # GRÁFICO
        # ------------------------------
        plt.figure(figsize=(6, 4))
        plt.plot(df["ano"], df["toneladas"], marker="o", color="blue")
        plt.scatter(df["ano"].max() + 1, prediccion, color="red", s=100)
        plt.xlabel("Año")
        plt.ylabel("Toneladas")
        plt.tight_layout()

        grafico = "static/grafico.png"
        plt.savefig(grafico)
        plt.close()

    return render_template("index.html", prediccion=prediccion, grafico=grafico)



if __name__ == "__main__":
    app.run(debug=True)
