from flask import Flask, render_template
from laberinto.laberinto import Laberinto

app = Flask(__name__)

@app.route('/')
def index():
    lab = Laberinto(3, 3)  # Laberinto 10x10
    #Ya no hace falta mandarlo a crear la matriz, él solito lo hace
    # Prueba para normalización
    lab.normalizarLaberinto()
    lab.imprimirNormalizado()
    matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
    return render_template('index.html', matriz=matriz)  # Pasa la matriz al template

if __name__ == '__main__':
    app.run(debug=True)