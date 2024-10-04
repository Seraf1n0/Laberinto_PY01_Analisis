from flask import Flask, render_template
from laberinto.laberinto import Laberinto

app = Flask(__name__)

@app.route('/')
def index():
    lab = Laberinto(7, 7)  # Laberinto 10x10
    # Prueba para normalización
    matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
    lab.resolverLaberinto(0, 0)
    lab.mostrarSolucion()
    return render_template('index.html', matriz=matriz)  # Pasa la matriz al template

if __name__ == '__main__':
    app.run(debug=True)