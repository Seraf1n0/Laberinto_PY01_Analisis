import random
import copy
import os
from collections import deque
import heapq

"""
Nombre de la clase: ElementoLaberinto
Cantidad de métodos: 1 (Constructor unicamente)
Función: Este será el objeto que se aloje en cada posición de la matriz que contenga el laberinto.
Contiene un diccionario con los puntos cardinales (norte, sur, este, oeste) y un valor booleano para indicar si en esa dirección hay pared o camino.
Además guarda el valor de la casilla en la que se estaba anteriormente antes de llegar a esta y si ya se había visitado previamente.
"""
class ElementoLaberinto:
    def __init__(self):
        self.valor = 1
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
"""
Nombre de la clase: Laberinto
Cantidad de métodos: 11
Función: Generar el laberinto de forma aleatoria con el tamaño indicado.
         Guardarlo en un archivo y cargarlo.
         Resolverlo utilizando el método que se indique.
"""
class Laberinto:
    def __init__(self, altura, ancho, rutaArchivo=None) :
        #Poniendo atributos de instancia
        if(rutaArchivo is None): #No se proporciona la ruta del archivo, entonces hay que crear la matriz de 0
            self.ancho = ancho
            self.altura = altura
            self.matriz = []
            self.solucion = []
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
            self.solucion = []
            self.direcciones = ['n', 's', 'e', 'o'] #norte, sur, este, oeste
            self.modificarDireccion = {
                'n': {'fila': -1, 'columna': 0,'opuesto':'s'},
                's': {'fila': 1, 'columna': 0,'opuesto':'n'},
                'e': {'fila': 0, 'columna': 1,'opuesto':'o'},
                'o': {'fila': 0, 'columna': -1,'opuesto':'e'}
            }

            #Para cargar la matriz
            if(self.leerLaberintoDeArchivo(rutaArchivo)):
                self.laberintoCargado = True

                self.cantidadCeldas = self.ancho * self.altura
            else:
                #No se cargó el laberinto
                self.laberintoCargado = False

    """
    Se genera una matriz del tamaño indicado en el constructor. Cada posición contiene un objeto del tipo ElementoLaberinto
    Entradas: ninguna
    Post-condición: Ahora la matriz contendrá los elementos necesarios para poder generar el laberinto aleatorio
    """
    def generarMatriz(self):
        #Primero genero una matriz con 1's indicando las paredes
        self.matriz = [[ElementoLaberinto() for _ in range(self.ancho)] for _ in range(self.altura)] #Aquí creo listas independientes y no referencian a una misma
        
        elemento = self.matriz[self.altura-1][0]
        elemento.valor = "0"
        self.matriz[self.altura-1][0] = elemento

        return self.generarLaberinto()
    
    """
    Se genera el laberinto de forma aleatoria por medio de un algoritmo de backtraking que recorre todas las casillas y derriba
    los muros entre en la posición que se encuentre y la siguiente a la que quiera moverse en una dirección elegida de forma aleatoria. Esto es lo que permite
    que siempre se genere un laberinto diferente al anterior.
    Pre-condiciones: Se debe de haber ejecutado el método generarMatriz previamente para que esta ya se encuentre llena con el objeto ElementoLaberinto
    Entradas: Ninguna
    Post-condición: El laberinto ya se encontrará generado y listo para utilizarse
    """
    def generarLaberinto(self):
        #Tiene que ser recursivo
        fila = self.altura - 1
        columna = 0
        self.matriz[self.altura-1][0].posicionAnteriorColumna = 1 #Para que el anterior de la primera casilla no sea None
        self.matriz[self.altura-1][0].posicionAnteriorFila = 0
        completado = False
        moverse = False
        ciclos = 0
        maximoCiclos = 0


        while not completado:
            moverse = False
            #Pongo en las visitadas la posición actual
            if(fila is None or columna is None):
                #Vuelvo a generar otro laberinto
                self.celdasVisitadas = 1
                self.matriz = []
                return self.generarMatriz
            
            self.matriz[fila][columna].visitado = True

            #Ahora voy con lo del número de loops para darle aletoriedad
            if(ciclos > maximoCiclos):
                random.shuffle(self.direcciones)
                maximoCiclos = round(random.random() * (self.altura / 8))
                ciclos = 0
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

                        self.celdasVisitadas += 1
                        moverse = True
                        break

            #Al salir del for verifico si me moví, en caso contrario me muevo a la casilla anterior
            if not moverse:
                if(self.matriz[fila][columna].posicionAnteriorFila is not None and self.matriz[fila][columna].posicionAnteriorColumna is not None):
                    fila = self.matriz[fila][columna].posicionAnteriorFila #Pongo la fila anterior
                    columna = self.matriz[fila][columna].posicionAnteriorColumna  #Pongo la columna anterior 
                else:
                    self.celdasVisitadas = 1
                    self.matriz = []
                    return self.generarMatriz()
                    
            if(self.celdasVisitadas == self.cantidadCeldas):
                completado = True
       
    """
    Método que imprime el laberinto en consola. De uso para el desarrollo
    Entradas: Ninguna
    Post-condición: Se muestra el laberinto en la consola
    """
    def imprimirLaberinto(self):
        for fila in self.matriz:
            print(" ".join(["P" if celda.valor == 3 else "X" for celda in fila]))

    """
    Resolución del laberinto utilizando los valores de cada una de las celdas.
    Entradas: Coordenadas de inicio
    Post-condición: La matriz asociada será marcada con el camino.
    """
    def resolverLaberinto(self, filaActual, columnaActual):
        # Condición de parada de recursión, para saber si se ha llegado a la salida
        if filaActual == (1 - 1) and columnaActual == self.ancho - 1:
            self.matriz[filaActual][columnaActual].valor = 3  # La salida forma parte de la solución
            self.solucion.append((filaActual, columnaActual))  # Almacenamos la salida en la solución
            return True

        # Se marca la celda como visitada (no sirve tanto) y se agrega a la solución.
        self.matriz[filaActual][columnaActual].visitado = True
        self.matriz[filaActual][columnaActual].valor = 3  # Se marca como parte de la solución
        self.solucion.append((filaActual, columnaActual))  # Se agrega a la solución actual

        # Se probará cada direccion de la celda
        for direccion in self.direcciones:
            siguienteFila = filaActual + self.modificarDireccion[direccion]['fila']
            siguienteColumna = columnaActual + self.modificarDireccion[direccion]['columna']

            # Vemos si en la siguiente celda (usando direcciones) es posible seguir
            if (0 <= siguienteFila < self.altura and 0 <= siguienteColumna < self.ancho 
                and self.matriz[filaActual][columnaActual].caminos[direccion]['camino'] 
                and not self.matriz[siguienteFila][siguienteColumna].visitado):
                
                # Backtracking usando la casilla siguiente
                if self.resolverLaberinto(siguienteFila, siguienteColumna):
                    return True


        # En el caso de no haber posibilidad de moverse a alguna dirección entonces retrocedemos
        self.matriz[filaActual][columnaActual].valor = 4  # Retroceso
        self.solucion.pop()  # Eliminar la celda actual de la solución
        return False

    def resolverLaberintoAStar(self, filaInicio, columnaInicio):
        # Cola de prioridad para los nodos abiertos
        cola_abierta = []
        heapq.heappush(cola_abierta, (0, (filaInicio, columnaInicio)))  # (costo total, coordenadas)
        
        # Diccionarios para costos y predecesores
        g_costs = { (filaInicio, columnaInicio): 0 }
        h_costs = { (filaInicio, columnaInicio): self.heuristica(filaInicio, columnaInicio) }
        predecesor = { (filaInicio, columnaInicio): None }
        
        while cola_abierta:
            # se saca el nodo de costo bajo
            costo_total, (filaActual, columnaActual) = heapq.heappop(cola_abierta)

            # Condición de parada se llego al final
            if filaActual == (1 - 1) and columnaActual == self.ancho - 1:
                self.solucion = []
                while (filaActual, columnaActual) is not None:
                    self.solucion.append((filaActual, columnaActual))
                    filaActual, columnaActual = predecesor.get((filaActual, columnaActual), (None, None))
                self.solucion.reverse()  # Invertir para que el camino esté en orden (FIFO)
                return True

            # Añadir a la lista de cerrados
            for direccion in self.direcciones:
                siguienteFila = filaActual + self.modificarDireccion[direccion]['fila']
                siguienteColumna = columnaActual + self.modificarDireccion[direccion]['columna']

                # Validar si podemos movernos en esa dirección
                if (0 <= siguienteFila < self.altura and 0 <= siguienteColumna < self.ancho 
                    and self.matriz[filaActual][columnaActual].caminos[direccion]['camino']):
                    
                    g_nuevo = g_costs[(filaActual, columnaActual)] + 1 

                    if (siguienteFila, siguienteColumna) not in g_costs or g_nuevo < g_costs[(siguienteFila, siguienteColumna)]:
                        g_costs[(siguienteFila, siguienteColumna)] = g_nuevo
                        h_costs[(siguienteFila, siguienteColumna)] = self.heuristica(siguienteFila, siguienteColumna)
                        f_nuevo = g_nuevo + h_costs[(siguienteFila, siguienteColumna)]
                        predecesor[(siguienteFila, siguienteColumna)] = (filaActual, columnaActual)

                        # Añadir el nuevo nodo a la cola abierta si no está ya presente
                        heapq.heappush(cola_abierta, (f_nuevo, (siguienteFila, siguienteColumna)))

        return False  # No hay solución

    def heuristica(self, fila, columna):
        return abs(fila - (self.altura - 1)) + abs(columna - (self.ancho - 1))

    """
    Este método será para reiniciar el booleano que indica si la casilla se ha visitado anteriormente.
    El algoritmo para generar el laberinto deja a todas las casillas como visitadas, entonces este método reinicia este valor
    para que este atributo se pueda utilizar en los algoritmos para resolver el laberinto.
    Pre-condición: Se debe de haber ejecutado el método generarMatriz previamente porque sino esta se encontrará vacía
    Post-condición: Ahora el valor del atributo visitado en cada elemento de la matriz es False
    """
    def reiniciarVisitados (self):
        for i in range(self.altura):
            for j in range(self.ancho):
                self.matriz[i][j].visitado = False # Reiniciar como 
                self.matriz[i][j].valor = 1

    def actualizarLaberinto(self, paso):
        x, y = paso  # El paso es una coordenada (x, y) en la matriz dentro de la lista de solucion
        self.matriz[x][y].valor = 3

    """
    Este método imprime la solución que se encuentra para el laberinto
    Pre-condiciones: Se debe de haber ejecutado el método generarMatriz previamente porque sino esta se encontrará vacía
                     Se debe de haber ejecutado el método resolverLaberinto previamente para que la lista con la solución no se encuentre vacía
    Entrada: Ninguna
    Salida: Se imprime el dato en la consola
    """
    def mostrarSolucion(self):
        print("Solución encontrada, paso a paso:")
        for paso, (fila, columna) in enumerate(self.solucion):
            print(f"Paso {paso + 1}: Coordenada (Fila {fila}, Columna {columna})")

    """
    Este método permite guardar en un archivo .txt el laberinto generado.
    Escribe una validación para utilizar al momento de cargar el laberinto en la primera línea, luego la cantidad de 
    filas y columnas. Finalmente escribe el diccionario con las direcciones de la casilla en las cuales tiene pared o camino
    Entrada: nombreArchivo. Es el que se le designará al resultado de ejeuctar la función.
    Pre-condición: Se debe de haber ejecutado el método generarMatriz previamente porque sino esta se encontrará vacía
    Post-condición: Se genera un archivo con el laberinto que puede ser utilizado en el método leerLaberintoDeArchivo
    """
    def guardarEnArchivo(self, nombreArchivo):

        #Abro el archivo en modo w para que borre el anterior en caso de existir y evitar problemas
        archivo = open(nombreArchivo, mode='w') #encoding="utf-8", 
        #Ahora tendría que iterar para escribir todo
        lineaInicio = "Laberinto\n"+ str(self.altura) + "," + str(self.ancho) + "\n"
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
    Este método permite interpretar el contenido de un archivo .txt para cargar el laberinto.
    Pre-condiciones: Se debe ejecutar previamente el método generarMatriz para que la matriz no se encuentre vacía.
                     Se debe haber ejecutado previamente el método guardarEnArchivo para tener un archivo válido de laberinto, de lo contrario
                     no se cargará el laberinto.
    Entrada: rutaArchivo. Es la ruta donde está alojado el archivo que se intentará cargar
    Post-condición: Ahora el atributo matriz de esta clase contendrá el laberinto cargado del archivo en caso de ser este uno válido generado previamente por la aplicación
    """
    def leerLaberintoDeArchivo(self, rutaArchivo):
        if os.path.exists(rutaArchivo):
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
                                return False #No es un archivo apto para leer
                            primeraLinea = False
                        else:
                            #Después de la primera línea tengo que leer la cantidad de filas y columnas
                            if(lineaDimensiones):
                                listaDimensiones = linea.rstrip('\n').split(",")
                                self.altura, self.ancho = int(listaDimensiones[0]), int(listaDimensiones[1]) #Filas, columnas
                                self.matriz = [[ElementoLaberinto() for _ in range(self.ancho)] for _ in range(self.altura)]
                                lineaDimensiones = False
                            else:
                                #Ya tocaría leer todas las demás líneas
                            
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
                                        
                                if(listaParedes[7] == "True"):
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
                    return True

            else:
                return False #El archivo no tenía líneas para leer
        else:
            return False

    """
    Este método permite contar la cantidad de líneas que contiene un archivo. 
    Entrada: rutaArchivo. Ruta del archivo que se leerá
    Salida: Se retorna la cantidad de líneas que contiene el archivo
    """
    def totalLineasArchivo(self, rutaArchivo):
        contador = 0
        archivo = open(rutaArchivo, mode="r")
        #contenido = archivo.read()
        listaLineas = archivo.readlines()
        for linea in listaLineas:
            contador += 1
        return contador

    """
    Método para obtener la matriz.
    Entrada: ninguna
    Salida: Se retorna el atributo matriz de esta clase
    """
    def obtenerMatriz(self):
        return self.matriz
    
