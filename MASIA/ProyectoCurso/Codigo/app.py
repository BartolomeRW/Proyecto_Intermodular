import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from flask import Flask, render_template, request
import CargarDatos as fuente  # Import correcto

app = Flask(__name__)

# Cargar modelo entrenado
if os.path.exists("modelo_IA.pkl"):
    modelo = joblib.load("modelo_IA.pkl")
else:
    modelo = None


# ==============================
#   SUBIR ARCHIVO CSV / EXCEL
# ==============================
@app.route("/upload", methods=["POST"])
def upload():
    archivo = request.files["archivo"]

    # Ruta donde se guardará el archivo subido
    ruta = os.path.join("UPLOADS", archivo.filename)
    archivo.save(ruta)

    # Detectar si es CSV o Excel
    if archivo.filename.endswith(".csv"):
        df = fuente.leer_csv(ruta)

    elif archivo.filename.endswith(".xlsx") or archivo.filename.endswith(".xls"):
        df = fuente.leer_excel(ruta)

    else:
        return "Formato no compatible. Solo CSV o Excel."

    # Guardar para que la IA pueda entrenar
    df.to_csv("cosechas.csv", index=False)

    return "Archivo subido correctamente. Ahora puedes reentrenar la IA."


# ==============================
#   REENTRENAR IA DESDE LA WEB
# ==============================
@app.route("/train", methods=["POST"])
def train():
    import subprocess

    # Ejecutar script de entrenamiento y capturar salida
    proceso = subprocess.run(["python", "entrenar_modelo.py"],
                             capture_output=True, text=True)

    return f"<pre>{proceso.stdout}</pre>"


# ==============================
#      PREDICCIÓN + GRÁFICO
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():
    prediccion = None
    grafico = None

    global modelo

    if request.method == "POST":

        if modelo is None:
            return "No hay modelo cargado. Sube un archivo y reentrena."

        try:
            hect = float(request.form["hectareas"])
            temp = float(request.form["temperatura"])
            lluv = float(request.form["lluvia"])
        except:
            return "Error: Debes introducir valores numéricos."

        # Crear entrada para la IA
        entrada = np.array([[hect, temp, lluv]])
        prediccion = round(modelo.predict(entrada)[0], 2)

        # ======= GENERAR GRÁFICO =======
        df = pd.read_csv("cosechas.csv")

        # Detectar columnas automáticamente
        cols = fuente.detectar_columnas(df)

        col_anio = cols["año"]
        col_ton = cols["toneladas"]

        if col_anio is None or col_ton is None:
            return "Error: No se detectaron las columnas de Año o Producción."

        # Crear carpeta static si no existe
        if not os.path.exists("static"):
            os.makedirs("static")

        # Gráfico dinámico agrícola
        plt.figure(figsize=(6, 4))
        plt.plot(df[col_anio], df[col_ton], marker="o")
        plt.scatter(df[col_anio].max() + 1, prediccion, color="red")
        plt.title("Predicción de producción agrícola")
        plt.xlabel("Año")
        plt.ylabel("Toneladas")
        plt.tight_layout()

        grafico = "static/grafico.png"
        plt.savefig(grafico)
        plt.close()

    return render_template("index.html", prediccion=prediccion, grafico=grafico)


# ==============================
#          INICIAR APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
