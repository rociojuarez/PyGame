import pygame
import random
import sys
from constants import *

# Inicializa Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas")

# Cargar imagen de fondo y sonido
imagen_fondo = pygame.image.load("./assets/background.jpeg").convert()
pygame.mixer.music.load("./assets/music.mp3")
pygame.mixer.music.play(-1)  # Repetir la música

# Clase para la celda
class Celda:
    def __init__(self):
        self.hay_mina = False
        self.revelada = False
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
# Función para dibujar el tablero
def dibujar_tablero(tablero):
    for y in range(TAMAÑO_MATRIZ):
        for x in range(TAMAÑO_MATRIZ):
            celda = tablero[y][x]
            rect = pygame.Rect(x * TAMAÑO_CELDA, y * TAMAÑO_CELDA + 50, TAMAÑO_CELDA, TAMAÑO_CELDA)  # Desplazar el tablero hacia abajo
            if celda.revelada:
                pygame.draw.rect(pantalla, BLANCO, rect)
                if celda.hay_mina:
                    pygame.draw.circle(pantalla, ROJO, rect.center, TAMAÑO_CELDA // 4)
                elif celda.minas_adyacentes > 0:
                    fuente = pygame.font.Font(None, 36)
                    texto = fuente.render(str(celda.minas_adyacentes), True, NEGRO)
                    pantalla.blit(texto, rect.topleft)
            else:
                pygame.draw.rect(pantalla, GRIS, rect)

            pygame.draw.rect(pantalla, NEGRO, rect, 1)

# Función para dibujar el botón "Reiniciar"
def dibujar_boton_reiniciar():
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Reiniciar", True, NEGRO)
    rect = texto.get_rect(center=(ANCHO // 2, 25))  # Botón centrado en la parte superior
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)
    return rect

# Pantalla de inicio
def pantalla_inicio():
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
        pantalla.blit(boton_salir, (ANCHO // 2 - boton_salir.get_width() // 2, ALTO // 2 + 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos

                # Verifica si se hace clic en el botón "Jugar"
                if (ANCHO // 2 - boton_jugar.get_width() // 2 < mouse_x < ANCHO // 2 + boton_jugar.get_width() // 2) and \
                        (ALTO // 2 - 60 < mouse_y < ALTO // 2 - 60 + boton_jugar.get_height()):
                    return  # Inicia el juego

        pygame.display.flip()

# Función principal del juego
def main():
    pantalla_inicio()  # Llama a la pantalla de inicio
    tablero = crear_tablero()
    matriz_dinamica = crear_matriz_dinamica(tablero)
    modificar_ceros(matriz_dinamica, tablero)


    # Función principal del juego

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Verificar si se hace clic en el botón "Reiniciar"
                boton_rect = dibujar_boton_reiniciar()
                if boton_rect.collidepoint(evento.pos):
                    tablero = crear_tablero()  # Reiniciar el tablero
                    continue  # Volver a la parte superior del bucle

                # Verificar si se hace clic en una celda
                columna, fila = x // TAMAÑO_CELDA, (y - 50) // TAMAÑO_CELDA  # Ajustar la fila
                if 0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ:
                    if not tablero[fila][columna].revelada:
                        tablero[fila][columna].revelada = True
                        if tablero[fila][columna].hay_mina:
                            print("¡Perdiste!")
                            pygame.quit()
                            sys.exit()

        pantalla.fill(NEGRO)
        dibujar_boton_reiniciar()
        dibujar_tablero(tablero)
        pygame.display.flip()

if __name__ == "__main__":
    main()
