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
    def __init__(self, altura, ancho) :
        #Poniendo atributos de instancia
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

prueba = Laberinto(5,5)
prueba.generarMatriz()

a = prueba.guardarEnArchivo("C:/Users/Dylan/Documents/Laberinto_PY01_Analisis/Laberinto-Dylan/Prueba.txt")
