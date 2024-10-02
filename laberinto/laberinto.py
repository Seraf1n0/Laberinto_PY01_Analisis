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
        for fila in self.matriz:
            print(" ".join(["P" if celda.visitado else "X" for celda in fila]))
            
    """
    Resolución del laberinto utilizando los valores de cada una de las celdas.
    Entradas: Coordenadas de inicio
    Post-condición: La matriz asociada será marcada con el camino.
    """
    def resolverLaberinto(self, filaActual, columnaActual):
        # Verificar si hemos llegado a la salida (n-1, n-1)
        if filaActual == self.altura - 1 and columnaActual == self.ancho - 1:
            self.matriz[filaActual][columnaActual].valor = "2"  # Marcamos la salida
            return True

        # Marcamos la celda actual como visitada para no regresar
        self.matriz[filaActual][columnaActual].visitado = True

        # Movimientos en cada una de las direcciones utulizando el diccionario de direcciones
        for direccion in self.direcciones:
            siguienteFila = filaActual + self.modificarDireccion[direccion]['fila']
            siguienteColumna = columnaActual + self.modificarDireccion[direccion]['columna']

            # Validar si podemos movernos en esa dirección (que haya un camino y no esté fuera de los límites), que haya camino y que no haya sido visitado
            if (0 <= siguienteFila < self.altura and 0 <= siguienteColumna < self.ancho and self.matriz[filaActual][columnaActual].caminos[direccion]['camino'] and not self.matriz[siguienteFila][siguienteColumna].visitado):

                # Backtracking: Si no puedo moverme a ninguna dirección retroceso desmarcando el visitado de la celda actual
                if self.resolverLaberinto(siguienteFila, siguienteColumna):
                    return True

        # Marcado y retroceso
        self.matriz[filaActual][columnaActual].visitado = False
        return False
         
    def obtenerMatriz(self):
        return self.matriz