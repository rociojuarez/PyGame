from constants import *
import random
import pygame
import sys

# Clase para la celda
class Celda:
    def __init__(self):
        self.hay_mina = False
        self.revelada = False
        self.flag = False
        self.minas_adyacentes = 0

# Crear la matriz
def crear_tablero():
    tablero = [[Celda() for _ in range(TAMAÑO_MATRIZ)] for _ in range(TAMAÑO_MATRIZ)]
    colocar_minas(tablero)
    calcular_minas_adyacentes(tablero)
    return tablero

# Colocar minas aleatoriamente
def colocar_minas(tablero):
    minas_colocadas = 0
    while minas_colocadas < CANTIDAD_MINAS:
        x = random.randint(0, TAMAÑO_MATRIZ - 1)
        y = random.randint(0, TAMAÑO_MATRIZ - 1)
        if not tablero[y][x].hay_mina:
            tablero[y][x].hay_mina = True
            minas_colocadas += 1

# Calcular minas adyacentes
def calcular_minas_adyacentes(tablero):
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            if tablero[y][x].hay_mina:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if 0 <= x + dx < TAMAÑO_MATRIZ and 0 <= y + dy < TAMAÑO_MATRIZ:
                            if not tablero[y + dy][x + dx].hay_mina:
                                tablero[y + dy][x + dx].minas_adyacentes += 1

# Crear matriz dinámica con -1 y 0
def crear_matriz_dinamica(tablero):
    matriz = [[0 for _ in range(TAMAÑO_MATRIZ)] for _ in range(TAMAÑO_MATRIZ)]
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            if tablero[y][x].hay_mina:
                matriz[y][x] = -1
            elif tablero[y][x].minas_adyacentes == 0:
                matriz[y][x] = 0
            else:
                matriz[y][x] = tablero[y][x].minas_adyacentes
    return matriz

# Modificar ceros en la matriz según las minas contiguas
def modificar_ceros(matriz, tablero):
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            if matriz[y][x] == 0 and not tablero[y][x].hay_mina:
                conteo_adyacente = tablero[y][x].minas_adyacentes
                if conteo_adyacente > 0:
                    matriz[y][x] = conteo_adyacente

def calcular_vacios(tablero, fila , columna):
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            if 0 <= y < TAMAÑO_MATRIZ and 0 <= x < TAMAÑO_MATRIZ:
                if es_vecino(columna, fila, x, y):
                    if tablero[y][x].minas_adyacentes == 0 and tablero[y][x].hay_mina == False:
                        tablero[y][x].revelada = True
                    elif tablero[y][x].minas_adyacentes > 0 and tablero[y][x].hay_mina == False:
                        tablero[y][x].revelada = True

def es_vecino(columna, fila, columna2, fila2):
    return abs(columna - columna2) <= 1 and abs(fila - fila2) <= 1

# Función para dibujar el tablero
def dibujar_tablero(tablero, pantalla, final):
    imagen_bandera = pygame.image.load("./assets/flag.png")
    imagen_marcador = pygame.transform.scale(imagen_bandera, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_mina = pygame.image.load("./assets/bomba.png")
    imagen_bomba = pygame.transform.scale(imagen_mina, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            celda = tablero[y][x]
            rect = pygame.Rect(x * TAMAÑO_CELDA, y * TAMAÑO_CELDA + 50, TAMAÑO_CELDA, TAMAÑO_CELDA)  # Desplazar el tablero hacia abajo
            if final:
                celda.revelada = True
                celda.flag = False
            if celda.revelada and not celda.flag:
                pygame.draw.rect(pantalla, BLANCO, rect)
                if celda.hay_mina:
                    pygame.draw.circle(pantalla, ROJO, rect.center, TAMAÑO_CELDA // 4)
                    pantalla.blit(imagen_bomba, rect.topleft)
                elif celda.minas_adyacentes > 0:
                    fuente = pygame.font.Font(None, 36)
                    texto = fuente.render(str(celda.minas_adyacentes), True, NEGRO)
                    pantalla.blit(texto, rect.topleft)
                elif celda.minas_adyacentes == 0:
                    calcular_vacios(tablero, y, x)
            elif celda.flag:
                pantalla.blit(imagen_marcador, rect.topleft)
            else:
                pygame.draw.rect(pantalla, GRIS, rect)

            pygame.draw.rect(pantalla, NEGRO, rect, 1)

# Función para dibujar el botón "Reiniciar"
def dibujar_boton_reiniciar(pantalla):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render("Reiniciar", True, NEGRO)
    rect = texto.get_rect(center=(55, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)
    return rect

# Pantalla de inicio
def pantalla_inicio(pantalla):
    imagen_fondo = pygame.image.load("./assets/background.jpeg").convert()
    while True:
        pantalla.blit(imagen_fondo, (0, 0))
        fuente = pygame.font.Font(None, 48)

        # Botones
        boton_jugar = fuente.render("Jugar", True, NEGRO)
        boton_nivel = fuente.render("Nivel", True, NEGRO)
        boton_puntajes = fuente.render("Ver Puntajes", True, NEGRO)
        boton_salir = fuente.render("Salir", True, NEGRO)

        pantalla.blit(boton_jugar, (ANCHO // 2 - boton_jugar.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(boton_nivel, (ANCHO // 2 - boton_nivel.get_width() // 2, ALTO // 2 - 20))
        pantalla.blit(boton_puntajes, (ANCHO // 2 - boton_puntajes.get_width() // 2, ALTO // 2 + 20))
        button_quit = pantalla.blit(boton_salir, (ANCHO // 2 - boton_salir.get_width() // 2, ALTO // 2 + 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if button_quit.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
                else:
                    mouse_x, mouse_y = evento.pos

                    # Verifica si se hace clic en el botón "Jugar"
                    if (ANCHO // 2 - boton_jugar.get_width() // 2 < mouse_x < ANCHO // 2 + boton_jugar.get_width() // 2) and \
                            (ALTO // 2 - 60 < mouse_y < ALTO // 2 - 60 + boton_jugar.get_height()):
                        return  # Inicia el juego

            pygame.display.flip()

def puntaje(pantalla, contador_puntaje):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render(f"Puntaje: {contador_puntaje}", True, NEGRO)
    rect = texto.get_rect(center=(ANCHO - 60, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)



# Función principal del juego
def main(pantalla):
    pantalla_inicio(pantalla)  # Llama a la pantalla de inicio
    tablero = crear_tablero()
    matriz_dinamica = crear_matriz_dinamica(tablero)
    modificar_ceros(matriz_dinamica, tablero)
    final = False
    contador_puntaje = 0000

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if evento.button == 1:
                    # Verificar si se hace clic en el botón "Reiniciar"
                    boton_rect = dibujar_boton_reiniciar(pantalla)
                    if boton_rect.collidepoint(evento.pos):
                        final = False
                        tablero = crear_tablero()  # Reiniciar el tablero
                        continue  # Volver a la parte superior del bucle

                    # Verificar si se hace clic en una celda
                    columna, fila = x // TAMAÑO_CELDA, (y - 50) // TAMAÑO_CELDA  # Ajustar la fila
                    if 0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ:
                        if not tablero[fila][columna].revelada and not tablero[fila][columna].flag:
                            tablero[fila][columna].revelada = True
                            if tablero[fila][columna].hay_mina:
                                final = True
                            else:
                                contador_puntaje += 1

                elif evento.button == 3:
                    columna, fila = x // TAMAÑO_CELDA, (y - 50) // TAMAÑO_CELDA  # Ajustar la fila
                    if 0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ:
                        if not tablero[fila][columna].revelada and not tablero[fila][columna].flag:
                            tablero[fila][columna].flag = True
                        elif tablero[fila][columna].flag and not tablero[fila][columna].revelada:
                            tablero[fila][columna].flag = False


            pantalla.fill(NEGRO)
            dibujar_boton_reiniciar(pantalla)
            puntaje(pantalla, contador_puntaje)
            dibujar_tablero(tablero, pantalla, final)
            pygame.display.flip()
