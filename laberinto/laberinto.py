import random
import copy

#De momento aquí para evitarme el errorsh
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
        fila = self.altura - 1
        columna = 0
        self.matriz[fila][columna].posicionAnteriorFila = fila
        self.matriz[fila][columna].posicionAnteriorColumna = columna

        completado = False
        moverse = False
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
        print("Terminé el laberinto")

    def imprimirLaberinto(self):
        for fila in self.matriz:
            print(" ".join(["P" if celda.visitado else "X" for celda in fila]))

    """
    Resolución del laberinto utilizando los valores de cada una de las celdas.
    Entradas: Coordenadas de inicio
    Post-condición: La matriz asociada será marcada con el camino.
    """
    def resolverLaberinto(self, filaActual, columnaActual):
        # Condición de parada de recursión, para saber si se ha llegado a la salida
        if self.matriz[filaActual][columnaActual] == 2:
            self.matriz[filaActual][columnaActual].valor = 0  # Marcamos la salida en la solución.
            return True

        # Se marca la celda como visitada (no sirve tanto) y con un numero que indique que por ese lado no puede irse.
        self.matriz[filaActual][columnaActual].visitado = True
        self.matriz[filaActual][columnaActual].valor = 0  # Marcamos el camino recorrido con un numero identificando un camino temporal de solución

        # Se probará cada direccion de la celda
        for direccion in self.direcciones:
            siguienteFila = filaActual + self.modificarDireccion[direccion]['fila']
            siguienteColumna = columnaActual + self.modificarDireccion[direccion]['columna']

            # Vemos si en la siguiente celda (usando direcciones) es posible seguir
            if (0 <= siguienteFila < self.altura and 0 <= siguienteColumna < self.ancho 
                and self.matriz[filaActual][columnaActual].caminos[direccion]['camino'] 
                and not self.matriz[siguienteFila][siguienteColumna].visitado):

                # Backtracking usando la casilla siguiente
                if self.resolver_laberinto(siguienteFila, siguienteColumna):
                    return True

        # En el caso de no haber posibilidad de moverse a alguna dirección entonces retrocedemos
        self.matriz[filaActual][columnaActual].visitado = False
        return False


    """
    Normalización de laberinto
    Utiliza la matriz asociada para normalizarla, en caso de estar rodeada de paredes entonces es una pared,
    y en caso de ser un camino es porque tiene alguna dirección abierta
    Post-condición: La matriz queda con valores 1, 0 y 2 para hacer más facil el analisis en la solución del algoritmo.
    """
    def normalizarLaberinto(self):
        for i in range(self.altura):
            for j in range(self.ancho):
                celda = self.matriz[i][j]
                
                # Por cada dirección vamos a ver si la celda tiene un camino
                esCamino = False
                for direccion in ['n', 's', 'e', 'o']:
                    if celda.caminos[direccion]['camino']:
                        esCamino = True
                        break

                if esCamino:
                    celda.valor = 0
                else:
                    celda.valor = 1

        # Salida, va a cambiar
        self.matriz[self.altura - 1][self.ancho - 1].valor = 2


    def imprimirNormalizado (self):
        for fila in self.matriz:
            print(' '.join([str(celda.valor) for celda in fila]))

    def guardarEnArchivo(self, nombreArchivo):
        #Abro el archivo en modo w para que borre el anterior en caso de existir y evitar problemas
        archivo = open(nombreArchivo, mode='w') #encoding="utf-8", 
        #Ahora tendría que iterar para escribir todo
        lineaInicio = str(self.altura) + "," + str(self.ancho) + "\n"
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

    def obtenerMatriz(self):
        return self.matriz
    
a = Laberinto(3,3)
a.normalizarLaberinto()