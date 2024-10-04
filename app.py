from flask import Flask, render_template, send_file, request
from laberinto.laberinto import Laberinto
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

matrizG = None

@app.route('/')
def index(laberinto = None):
    global matrizG
    if(laberinto is None):
        
        lab = Laberinto(10, 10)  # Laberinto 10x10
        matrizG = lab
        #Ya no hace falta mandarlo a crear la matriz, él solito lo hace
        # Prueba para normalización
        matriz = lab.obtenerMatriz()  # Obtiene la matriz del laberinto
        print("Laberinto es none")
        return render_template('index.html', matriz=matriz)  # Pasa la matriz al template
        
    else:
        #Tendría que mandarle el laberinto cargado
        print("Laberinto no es none")       
        matrizG = laberinto
        matriz = laberinto.obtenerMatriz()
        return render_template('index.html', matriz=matriz)  # Pasa la matriz al template
        
    
    

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
        return "No file selected"
    
    # Eliminar todos los archivos existentes en la carpeta
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            return f"Error deleting file {filename}: {e}"

    # Guardar el nuevo archivo
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)    
        #Filepath tiene la ruta que ocupo para cargarlo
        matrizLocal = Laberinto(1,1, str(filepath))
        
        return index(matrizLocal)
        #return f"File {file.filename} uploaded successfully!"



if __name__ == '__main__':
    app.run(debug=True)

