import random
import copy

#De momento aquí para evitarme el errorsh
class ElementoLaberinto:
    def __init__(self):
        self.valor = "1"
        self.visitado = False
        self.posicionAnteriorFila = None 
        self.posicionAnteriorColumna = None 

class Laberinto:
    def __init__(self, altura, ancho) :
        #Poniendo atributos de instancia
        self.ancho = ancho
        self.altura = altura
        self.matriz = []
        self.direcciones = ['n', 's', 'e', 'o'] #norte, sur, este, oeste
        self.modificarDireccion = {
            'n': {'fila': -1, 'columna': 0, 'opuestoFila': 1, 'opuestoColumna':0},
            's': {'fila': 1, 'columna': 0, 'opuestoFila':-1, 'opuestoColumna':0},
            'e': {'fila': 0, 'columna': 1, 'opuestoFila':0, 'opuestoColumna':-1},
            'o': {'fila': 0, 'columna': -1, 'opuestoFila':0, 'opuestoColumna':1}
        }
        self.cantidadCeldas = ancho * altura
        self.celdasVisitadas = 0


    def generarMatriz(self):
        #Primero genero una matriz con 1's indicando las paredes
        self.matriz = [[ElementoLaberinto() for _ in range(self.ancho)] for _ in range(self.altura)] #Aquí creo listas independientes y no referencian a una misma
        
        elemento = self.matriz[self.altura-1][0]
        elemento.valor = "0"
        self.matriz[self.altura-1][0] = elemento

        print("Primera impresión")
        self.imprimirLaberinto()
        print("==============================")

        return self.generarLaberinto(self.altura-1, 0, 0,1)
    
    def generarLaberinto(self, fila, columna, ciclos, maximoCiclos):
        #Tiene que ser recursivo
        #Pongo en las visitadas la posición actual
        self.matriz[fila][columna].visitado = True

        moverse = False

        #Ahora voy con lo del número de loops para darle aletoriedad
        if(ciclos > maximoCiclos):
            random.shuffle(self.direcciones)
            maximoCiclos = round(random.random() * (self.altura / 8))
        
        #Ciclo para decidir el movimiento
        for direccion in self.direcciones:
            siguienteFila, siguienteColumna = fila + self.modificarDireccion[direccion]['fila'], columna +self.modificarDireccion[direccion]['columna']  #Me muevo a la siguiente posición
            #Verifico si me puedo mover a la siguiente posición (Que no se salga del mapa)
            if(siguienteFila < self.altura and siguienteFila >= 0 and siguienteColumna < self.ancho and siguienteColumna >= 0):
                #Verifico que la celda no haya sido visitada previamente
                if not (self.matriz[siguienteFila][siguienteColumna].visitado):
                    #Pongo la actual como 0 para indicar camino
                    self.matriz[fila][columna].valor = "0"
                    #Pongo la siguiente dirección como parte del camino
                    self.matriz[siguienteFila][siguienteColumna].valor = "0"
                    #También marco la dirección opuesta a la siguiente columna como camino
                    #self.matriz[self.modificarDireccion[direccion]['opuestoFila']] #Dirección va sin comillas por ser la variable del for
                    #En la siguiente celda pongo como anterior la actual
                    self.matriz[siguienteFila][siguienteColumna].posicionAnteriorFila = fila
                    self.matriz[siguienteFila][siguienteColumna].posicionAnteriorColumna = columna


                    #Imprimo el laberinto para ver el progreso
                    print("==============================")
                    self.imprimirLaberinto()
                    print("==============================")

                    #Llamada recursiva a la función. Ahora la fila y la columnna actual son siguienteFila y siguienteColumna+
                    self.celdasVisitadas += 1
                    return self.generarLaberinto(siguienteFila, siguienteColumna, ciclos +1, maximoCiclos)


        #Si llego a este punto es porque no me moví
        #Voy a intentar detener la recursión usando la verificación de si ya visité todas las celdas
       
        if(self.matriz[fila][columna].posicionAnteriorFila is not None and self.matriz[fila][columna].posicionAnteriorColumna is not None):
            #Vuelvo a ejecutar pero me devuelvo de fila
            return self.generarLaberinto(self.matriz[fila][columna].posicionAnteriorFila, self.matriz[fila][columna].posicionAnteriorColumna, ciclos +1, maximoCiclos)
        
        if(self.celdasVisitadas == self.cantidadCeldas):
            return
        #Si no, me tengo que mover a la celda anterior
    def imprimirLaberinto(self):
        lista = []
        for i in range(len(self.matriz)):
            for j in range(self.ancho):
                lista += self.matriz[i][j].valor
            print(lista)
            lista = []
            
prueba = Laberinto(5,5)
prueba.generarMatriz()



