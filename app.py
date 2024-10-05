from flask import Flask, render_template, send_file, request
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
        #Tendría que mandarle el laberinto cargado
        if(mensajeDeError is not None):
            #Tengo que mostrar el mensaje de error
            lab = Laberinto(10, 10)  # Laberinto 10x10
            matrizG = lab
            matriz = lab.obtenerMatriz()  
            return render_template('index.html', matriz=matriz, tamanio=lab.altura, mensajeError = True)  # Pasa la matriz al template
        else:  
            #Tendría que imprimir el mensaje de errors
            matrizG = laberinto
            matriz = laberinto.obtenerMatriz()
            return render_template('index.html', matriz=matriz, tamanio=laberinto.altura, mensajeError = False)  # Pasa la matriz al template
        
    
    

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
    
@app.route('/upload', methods=['POST'])
def upload_file():
 
    if 'file' not in request.files:
        return "No file part in the request"
    
    file = request.files['file']
    
    

    if file.filename == '':
        return index(1, True)
    
    # Eliminar todos los archivos existentes en la carpeta
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("Removiendo: " + str(file_path))
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            return f"Error deleting file {filename}: {e}"

    
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

@app.route('/generarLaberinto', methods=['POST'])
def generarLaberinto():
    tamano = request.form.get('tamanoLaberinto', type=int) #Con esto obtengo la selección del spinbox
    matriz = Laberinto(tamano,tamano)
    #Ahora tendría que cargarlo en la vista
    return index(matriz)

if __name__ == '__main__':
    app.run(debug=True)

