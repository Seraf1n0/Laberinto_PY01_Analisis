import random
import copy

#De momento aquí para evitarme el errorsh
class ElementoLaberinto:
    def __init__(self):
        self.valor = "1"
        self.visitado = False
        self.posicionAnteriorFila = None 
        self.posicionAnteriorColumna = None 
        #Con esto es que indico en cuales direcciones hay paredes y cuales caminos
        self.caminos = {
            'n':{'camino':False},
            's':{'camino':False},
            'e':{'camino':False},
            'o':{'camino':False}
        }

class Laberinto:
    def __init__(self, altura, ancho, rutaArchivo=None) :
        #Poniendo atributos de instancia

        if(rutaArchivo is None): #No se proporciona la ruta del archivo, entonces hay que crear la matriz de 0
            self.ancho = ancho
            self.altura = altura
            self.matriz = []
            self.direcciones = ['n', 's', 'e', 'o'] #norte, sur, este, oeste
            self.modificarDireccion = {
                'n': {'fila': -1, 'columna': 0,'opuesto':'s'},
                's': {'fila': 1, 'columna': 0,'opuesto':'n'},
                'e': {'fila': 0, 'columna': 1,'opuesto':'o'},
                'o': {'fila': 0, 'columna': -1,'opuesto':'e'}
            }
            self.cantidadCeldas = ancho * altura
            self.celdasVisitadas = 1
            self.generarMatriz() #Para generar la matriz aleatoria
        else:
            self.ancho = 0
            self.altura = 0
            self.matriz = []
            self.direcciones = ['n', 's', 'e', 'o'] #norte, sur, este, oeste
            self.modificarDireccion = {
                'n': {'fila': -1, 'columna': 0,'opuesto':'s'},
                's': {'fila': 1, 'columna': 0,'opuesto':'n'},
                'e': {'fila': 0, 'columna': 1,'opuesto':'o'},
                'o': {'fila': 0, 'columna': -1,'opuesto':'e'}
            }

            #Para cargar la matriz
            self.leerLaberintoDeArchivo(rutaArchivo)
            self.cantidadCeldas = self.ancho * self.altura

    def generarMatriz(self):
        #Primero genero una matriz con 1's indicando las paredes
        self.matriz = [[ElementoLaberinto() for _ in range(self.ancho)] for _ in range(self.altura)] #Aquí creo listas independientes y no referencian a una misma
        
        elemento = self.matriz[self.altura-1][0]
        elemento.valor = "0"
        self.matriz[self.altura-1][0] = elemento

        print("Primera impresión")
        self.imprimirLaberinto()
        print("==============================")

        return self.generarLaberinto()
    
    def generarLaberinto(self):
        #Tiene que ser recursivo
        completado = False
        moverse = False
        fila = self.altura-1
        columna = 0
        ciclos = 0
        maximoCiclos = 0

        while not completado:
            moverse = False
            #Pongo en las visitadas la posición actual
            self.matriz[fila][columna].visitado = True

            #Ahora voy con lo del número de loops para darle aletoriedad
            if(ciclos > maximoCiclos):
                random.shuffle(self.direcciones)
                maximoCiclos = round(random.random() * (self.altura / 8))
            ciclos +=1
            #Ciclo para decidir el movimiento
            for direccion in self.direcciones:
                siguienteFila, siguienteColumna = fila + self.modificarDireccion[direccion]['fila'], columna +self.modificarDireccion[direccion]['columna']  #Me muevo a la siguiente posición
                #Verifico si me puedo mover a la siguiente posición (Que no se salga del mapa)
                if(siguienteFila < self.altura and siguienteFila >= 0 and siguienteColumna < self.ancho and siguienteColumna >= 0):
                    #Verifico que la celda no haya sido visitada previamente
                    if not (self.matriz[siguienteFila][siguienteColumna].visitado):
                        #Me puedo mover al siguiente. Derribo la pared entre este y el actual
                        self.matriz[fila][columna].caminos[direccion]['camino'] = True #Se supone que con esto cambio el valor del diccionario para la pared actual

                        #En el próximo tengo que derribar la pared contraria a este
                        caracterOpuesto = self.modificarDireccion[direccion]['opuesto'] #Con esto obtengo el opuesto, este es el que cambio en el próximo
                        self.matriz[siguienteFila][siguienteColumna].caminos[caracterOpuesto]['camino'] = True

                        #Pongo en el anterior del próximo el actual
                        self.matriz[siguienteFila][siguienteColumna].posicionAnteriorFila = fila
                        self.matriz[siguienteFila][siguienteColumna].posicionAnteriorColumna = columna

                        #Modifico la fila actual para que sea a la que me moví
                        fila, columna =  siguienteFila, siguienteColumna

                        #Imprimo el laberinto para ver el progreso
                        print("==============================")
                        self.imprimirLaberinto()
                        print("==============================")

                        #Llamada recursiva a la función. Ahora la fila y la columnna actual son siguienteFila y siguienteColumna+
                        self.celdasVisitadas += 1
                        moverse = True
                        break

            #Al salir del for verifico si me moví, en caso contrario me muevo a la casilla anterior
            if not moverse:
                fila = self.matriz[fila][columna].posicionAnteriorFila #Pongo la fila anterior
                columna = self.matriz[fila][columna].posicionAnteriorColumna  #Pongo la columna anterior 
            
            if(self.celdasVisitadas == self.cantidadCeldas):
                completado = True
           

    def imprimirLaberinto(self):
        #Ahora la impresión es diferente, tengo que dibujar con rayas
        cadenaImprimir = ""
        direcciones = ['n', 's', 'e', 'o']
         
        for fila in range(self.altura):
            for columna in range(self.ancho):
                for direccion in direcciones:
                    #En todas las direcciones me fijo si hay o no camino
                    caminoDireccion = self.matriz[fila][columna].caminos[direccion]['camino'] #Sé si hay un camino en la dirección que estoy evaluando
                    if(direccion == 'o'):
                        if(caminoDireccion):
                            #Añado caracter
                            cadenaImprimir += "|"
                        #Si no simplemente no hago nada
                    if(direccion == 'n'):
                        if(caminoDireccion):
                            #Añado caracter arriba
                            cadenaImprimir += "─"
                    if(direccion == 's'):
                        cadenaImprimir += "_"
                    if(direccion == 'e'):
                        cadenaImprimir += " |"
            print(cadenaImprimir)
            cadenaImprimir = ""

    def guardarEnArchivo(self, nombreArchivo):
        #Abro el archivo en modo w para que borre el anterior en caso de existir y evitar problemas
        archivo = open(nombreArchivo, mode='w') #encoding="utf-8", 
        #Ahora tendría que iterar para escribir todo
        lineaInicio = "Laberinto\n"+str(self.altura) + "," + str(self.ancho) + "\n"
        archivo.write(lineaInicio)   #No olvidarme de escribir los saltos de línea
        
        for fila in range(self.altura):
            for columna in range(self.ancho):
                #Tendría que añadir una línea al archivo indicando lo que dice el diccionario
                booleanoN = self.matriz[fila][columna].caminos['n']['camino']
                booleanoS = self.matriz[fila][columna].caminos['s']['camino']
                booleanoE = self.matriz[fila][columna].caminos['e']['camino']
                booleanoO = self.matriz[fila][columna].caminos['o']['camino']
                lineaEscribir = "n," + str(booleanoN) + ",s," + str(booleanoS) + ",e," + str(booleanoE) + ",o," + str(booleanoO) 



                #If para añadir el salto de línea y que no me quede una vacía al final
                if(fila == (self.altura -1) and columna == (self.ancho -1)):
                    #Solo añado y no le pongo el salto de línea
                    archivo.write(lineaEscribir)
                else:
                    
                    #No es la última línea, le pongo el salto
                    lineaEscribir += "\n"
                    archivo.write(lineaEscribir)

        archivo.close()

        """
    Resolución del laberinto utilizando los valores de cada una de las celdas.
    Entradas: Coordenadas de inicio
    Post-condición: La matriz asociada será marcada con el camino.
    """
    def resolverLaberinto(self, filaActual, columnaActual):
        # Esta es la salida designada como salida (n-1, n-1)
        if (filaActual == self.altura - 1 and columnaActual == self.ancho - 1):
            self.matriz[filaActual][columnaActual].valor = "2"  # De momento se marca la salida con un "2"
            return True
        
        # Validamos que la casilla actual sea un camino (valor '0')
        if (self.matriz[filaActual][columnaActual].valor == "0"):
            # Marcamos el camino actual como parte de la solución
            self.matriz[filaActual][columnaActual].valor = "1" # Marcamos con un 1 temporal (para que sepa que no debe volver)

            #Movimiento en todas las direcciones
            for direccion in self.direcciones:
                siguienteFila = filaActual + self.modificarDireccion[direccion]['fila']
                siguienteColumna = columnaActual + self.modificarDireccion[direccion]['columna']

                # Validación para no salirse del rango de columnas y filas
                if (0 <= siguienteFila < self.altura and 0 <= siguienteColumna < self.ancho):
                    # Decisión del backtracking
                    if (self.resolverLaberinto(siguienteFila, siguienteColumna)):
                        return True
            # En el caso de que no se encuentre ninguna posible dirección entonces retrocedemos en una (marcando libre la celda actual)
            self.matriz[filaActual][columnaActual].valor = "0"
        
        return False

    def leerLaberintoDeArchivo(self, rutaArchivo):
        if(self.totalLineasArchivo(rutaArchivo) > 0):
            fila = 0
            columna = 0
            with open(rutaArchivo, 'r') as archivo:
                primeraLinea = True
                lineaDimensiones = True
                for linea in archivo:
                    if(primeraLinea):
                        #Estoy en la primera línea, verifico que el texto sea el correcto
                        if(linea.rstrip('\n') == "" or linea.rstrip('\n')  != "Laberinto"):
                            return False #No es un archivo apto para leersh
                        primeraLinea = False
                    else:
                        #Después de la primera línea tengo que leer la cantidad de filas y columnas
                        if(lineaDimensiones):
                            listaDimensiones = linea.rstrip('\n').split(",")
                            self.altura, self.ancho = int(listaDimensiones[0]), int(listaDimensiones[1]) #Filas, columnas
                            self.matriz = [[ElementoLaberinto() for _ in range(self.ancho)] for _ in range(self.altura)]
                            lineaDimensiones = False
                        else:
                            #Ya tocaría leersh todas las demás líneas
                        
                            listaParedes = linea.rstrip('\n').split(",")
                            #Tengo que poner los boleanos indicando las paredes
                            if(listaParedes[1] == "True"):
                                paredN = True
                            else:
                                paredN = False
                                
                            if(listaParedes[3] == "True"):
                                paredS = True
                            else:
                                paredS = False

                            if(listaParedes[5] == "True"):
                                paredE = True
                            else:
                                paredE = False
                                    
                            if(listaParedes[5] == "True"):
                                paredO = True
                            else:
                                paredO = False

                            #Ahora añado todos los valores al diccionario
                            self.matriz[fila][columna].caminos[listaParedes[0]]['camino'] = paredN
                            self.matriz[fila][columna].caminos[listaParedes[2]]['camino'] = paredS
                            self.matriz[fila][columna].caminos[listaParedes[4]]['camino'] = paredE
                            self.matriz[fila][columna].caminos[listaParedes[6]]['camino'] = paredO 
                            
                            columna += 1
                            if(columna == self.ancho):
                                columna = 0
                                fila +=1


        else:
            return False #El archivo no tenía líneas para leersh
    def totalLineasArchivo(self, rutaArchivo):
        contador = 0
        archivo = open(rutaArchivo, mode="r")
        #contenido = archivo.read()
        listaLineas = archivo.readlines()
        for linea in listaLineas:
            contador += 1
        return contador

    def obtenerMatriz (self): 
        return self.matriz

prueba = Laberinto(5,5)

a = prueba.guardarEnArchivo("Prueba.txt")
b = prueba.leerLaberintoDeArchivo("Prueba.txt")
    
