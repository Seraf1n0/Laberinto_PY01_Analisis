from flask import Flask, render_template, send_file, request, jsonify
from laberinto.laberinto import Laberinto
import os


app = Flask(__name__)
"""
Esto es para crear y guardar el directorio donde se almacenan los archivos que carga el usuario con el mapa
"""
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Variable global que puede servir
matrizG = None

"""
Función principal para ejecutar la interfaz.
Tiene dos parámetros que pueden ser none, en caso de ser indicados es para alterar la interfaz
El parámetro laberinto se utiliza para que no genere uno nuevo, sino que ponga en la interfaz el que le mando
El parámetro mensajeDeError se usa cuando intento cargar un archivo como laberinto pero no cumple las condiciones necesarias para ser leído por el programa
"""
@app.route('/')
def index(laberinto = None, mensajeDeError = None):
    global matrizG
    if(laberinto is None):
        
        lab = Laberinto(10, 10)  # Laberinto 10x10
        matrizG = lab
        #Ya no hace falta mandarlo a crear la matriz, él solito lo hace
        # Prueba para normalización
        matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
        return render_template('index.html', matriz=matriz, tamanio=lab.altura, mensajeError = False)  # Pasa la matriz al template
        
    else:
        if(mensajeDeError is not None):
            #Tengo que mostrar el mensaje de error
            lab = Laberinto(10, 10)  # Laberinto 10x10 predeterminado
            matrizG = lab
            matriz = lab.obtenerMatriz()
            matrizG.matriz[matrizG.altura-1][0].valor = 5
            matrizG.matriz[0][matrizG.ancho-1].valor = 2  
            return render_template('index.html', matriz=matriz, tamanio=lab.altura, mensajeError = True)  # Pasa la matriz al template
        else:  
            #Tendría que imprimir el mensaje de errors
            matrizG = laberinto
            matriz = laberinto.obtenerMatriz()
            matrizG.matriz[matrizG.altura-1][0].valor = 5
            matrizG.matriz[0][matrizG.ancho-1].valor = 2
            return render_template('index.html', matriz=matriz, tamanio=laberinto.altura, mensajeError = False)  # Pasa la matriz al template
        
    
@app.route('/resolverLaberinto', methods=['POST'])
def resolverLaberinto():
    global matrizG
    algoritmo = request.form.get('algoritmo')

    matrizG.reiniciarVisitados()# Reiniciar valores para resolver el laberinto

    if algoritmo == "backtracking":
        matrizG.resolverLaberinto(matrizG.altura - 1, 0)
    else:
        matrizG.resolverLaberintoAStar(matrizG.altura - 1, 0)

    pasos = matrizG.solucion

    matrizG.reiniciarVisitados()

    for paso in pasos:
        matrizG.actualizarLaberinto(paso)  # Cambiará los valores de las celdas correspondientes a 3
    
    # Marcamos la casilla de inicio y final:
    matrizG.matriz[matrizG.altura-1][0].valor = 5
    matrizG.matriz[0][matrizG.ancho-1].valor = 2

    return index(matrizG)


"""
Esta función se ejecuta cuando se presiona el botón Guadar Laberinto en la interfaz.
Toma la matriz y ejecuta el método que permite guardar el laberinto.
El archivo lo pone en la carpeta preparando que se encuentra en el directorio del proyecto. Antes de guardarlo borra todos los anteriores para que solo quede el últio generado.
Luego el archivo se descarga en la interfaz.
"""
@app.route('/guardarLaberinto', methods=['POST'])
def guardarLaberinto():
    
    global matrizG
    base_dir = os.path.dirname(os.path.abspath(__file__))
       
    save_dir = os.path.join(base_dir, 'preparando')
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    file_path = os.path.join(save_dir, 'laberinto.txt')
    file_path = file_path.replace("\\", "/")

    matrizG.guardarEnArchivo(file_path)
    return send_file(file_path, as_attachment=True)


"""
Esta función se ejecuta cuando se presiona el botón Subir. Previamente debe haberse seleccionado el archivo a cargar.
Se eliminan todos los archivos que se encuentren en la carpeta uploads y luego se agrega el nuevo archivo generado por el método en la clase Laberinto
"""
@app.route('/upload', methods=['POST'])
def upload_file():
 
    if 'file' not in request.files:
        return "El archivo no se encuentra entre los solicitados"
    
    file = request.files['file']

    if file.filename == '':
        return index(1, True) #Por si no ha seleccionado aún
    
    # Eliminar todos los archivos existentes en la carpeta
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("Removiendo: " + str(file_path))
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            return f"Error borrando archivo {filename}: {e}"

    
    # Guardar el nuevo archivo
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print("Insertando: " + str(filepath))
        print(filepath)
        filepath = str(filepath)
        filepath = filepath.replace("\\", "/")
        print(filepath)
        #Filepath tiene la ruta que ocupo para cargarlo
        matrizLocal = Laberinto(10,10, filepath)
        if(matrizLocal.laberintoCargado):
            return index(matrizLocal)
        else:
            #Hago el return pero con el parámetro para que me muestre el mensaje de error
            return index(matrizLocal, True)


"""
Esta función se ejecuta al momento de presionar el botón de Generar Laberinto en la interfaz.
Se toma el valor que se encuentra en el spinbox con el tamaño del laberinto y se crea este.
Luego se envía a la interfaz para que se cargue
"""
@app.route('/generarLaberinto', methods=['POST'])
def generarLaberinto():
    tamano = request.form.get('tamanoLaberinto', type=int) #Con esto obtengo la selección del spinbox
    matriz = Laberinto(tamano,tamano)
    #Ahora tendría que cargarlo en la vista
    return index(matriz)

if __name__ == '__main__':
    app.run(debug=True)

