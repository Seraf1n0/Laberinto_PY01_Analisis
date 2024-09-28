import random

class Laberinto:
    """Inicializa un laberinto según las filas y columnas que se requiera por el usuario"""
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)] # Se llenar de 0s cada una

    """Genera un laberinto aleatorio con paredes y caminos, pero hay que cambiar el enfoque de generación"""
    def generar_laberinto(self):
        # 0 será camino, 1 será pared (diseño de laberinto)
        for i in range(self.filas):
            for j in range(self.columnas):
                if random.random() < 0.3:  # Probabilidad de ser una pared
                    self.matriz[i][j] = 1
                else:
                    self.matriz[i][j] = 0

        # Estos serían los puntos de entrada y salida
        self.matriz[0][0] = 0
        self.matriz[self.filas-1][self.columnas-1] = 0

    """Imprime el laberinto en consola"""
    def mostrar_laberinto(self):
        for fila in self.matriz:
            print(" ".join(str(celda) for celda in fila))

    """Retorna la matriz del laberinto"""
    def obtener_matriz(self):
        return self.matriz