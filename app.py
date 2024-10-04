from flask import Flask, render_template
from laberinto.laberinto import Laberinto

app = Flask(__name__)

@app.route('/')
def index():
    lab = Laberinto(7, 7)  # Laberinto 10x10
    lab.reiniciarVisitados()
    # Prueba de solución por resolución backtracking
    lab.resolverLaberinto(0, 0)
    lab.imprimirLaberinto()
    lab.mostrarSolucion()
    matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
    return render_template('index.html', matriz=matriz)  # Pasa la matriz al template

if __name__ == '__main__':
    app.run(debug=True)