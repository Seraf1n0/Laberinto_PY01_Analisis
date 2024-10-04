from flask import Flask, render_template, send_file, request
from laberinto.laberinto import Laberinto
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

matrizG = None

@app.route('/')
def index(laberinto = None, mensajeDeError = None):
    global matrizG
    if(laberinto is None):
        
        lab = Laberinto(10, 10)  # Laberinto 10x10
        matrizG = lab
        #Ya no hace falta mandarlo a crear la matriz, él solito lo hace
        # Prueba para normalización
        matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
        print("Laberinto es none")
        return render_template('index.html', matriz=matriz, tamanio=lab.altura, mensajeError = False)  # Pasa la matriz al template
        
    else:
        #Tendría que mandarle el laberinto cargado
        print("Laberinto no es none")
        if(mensajeDeError is not None):
            print("Mensaje de error no es none")
            #Tengo que mostrar el mensaje de error
            lab = Laberinto(10, 10)  # Laberinto 10x10
            matrizG = lab
            matriz = lab.obtenerMatriz()  
            return render_template('index.html', matriz=matriz, tamanio=lab.altura, mensajeError = True)  # Pasa la matriz al template
        else:  
            #Tendría que imprimir el mensaje de errorsS
            print("Mensaje de error none")
            matrizG = laberinto
            matriz = laberinto.obtenerMatriz()
            return render_template('index.html', matriz=matriz, tamanio=laberinto.altura, mensajeError = False)  # Pasa la matriz al template
        
    
    

@app.route('/guardarLaberinto', methods=['POST'])
def guardarLaberinto():
    print("Llegué a guardarsh")
    global matrizG
    matrizG.guardarEnArchivo("C:/Users/Dylan/Documents/Laberinto_PY01_Analisis/laberintoPruebaMediaNoche.txt")
    print("Guardé la matriz")
    return send_file("C:/Users/Dylan/Documents/Laberinto_PY01_Analisis/laberintoPruebaMediaNoche.txt", as_attachment=True)
    
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

