from constants import *
import random
import pygame
import os

# Crear la matriz
def crear_tablero(celda:dict):
    tablero = inicializar_matriz(celda)
    colocar_minas(tablero)
    calcular_minas_adyacentes(tablero)
    return tablero

def inicializar_matriz(celda: dict)->list:
    matriz = []
    for i in range(CANTIDAD_FILAS):
        fila = []
        for j in range(CANTIDAD_COLUMNAS):
            fila.append(celda.copy())
        matriz.append(fila)
    return matriz


# Colocar minas aleatoriamente
def colocar_minas(tablero):
    minas_colocadas = 0
    while minas_colocadas < CANTIDAD_MINAS:
        x = random.randint(0, CANTIDAD_COLUMNAS - 1)
        y = random.randint(0, CANTIDAD_FILAS - 1)
        if not tablero[y][x]["hay_mina"]:
            tablero[y][x].update({"hay_mina": True})
            minas_colocadas += 1

# Calcular minas adyacentes
def calcular_minas_adyacentes(tablero):
    for y in range(CANTIDAD_FILAS):
        for x in range(CANTIDAD_COLUMNAS):
            if tablero[y][x]["hay_mina"]:
                for desplazamiento_fila in range(-1, 2):
                    for desplazamiento_columna in range(-1, 2):
                        fila_vecina = y + desplazamiento_fila
                        columna_vecina = x + desplazamiento_columna
                        if 0 <= fila_vecina < CANTIDAD_FILAS and 0 <= columna_vecina < CANTIDAD_COLUMNAS:
                            if not tablero[fila_vecina][columna_vecina]["hay_mina"]:
                                tablero[fila_vecina][columna_vecina]["minas_adyacentes"] += 1

def inicializar_matriz_ceros()->list:
    matriz = []
    for i in range(CANTIDAD_FILAS):
        fila = []
        for j in range(CANTIDAD_COLUMNAS):
            fila.append(0)
        matriz.append(fila)
    return matriz

# Crear matriz dinámica con -1 y 0
def crear_matriz_dinamica(tablero):
    matriz = inicializar_matriz_ceros()
    for y in range(CANTIDAD_FILAS):
        for x in range(CANTIDAD_COLUMNAS):
            if tablero[y][x]["hay_mina"]:
                matriz[y][x] = -1
            elif tablero[y][x]["minas_adyacentes"] == 0:
                matriz[y][x] = 0
    return matriz

# Modificar ceros en la matriz según las minas contiguas
def modificar_ceros(matriz, tablero):
    for y in range(CANTIDAD_FILAS):
        for x in range(CANTIDAD_COLUMNAS):
            if matriz[y][x] == 0 and not tablero[y][x]["hay_mina"]:
                conteo_adyacente = tablero[y][x]["minas_adyacentes"]
                if conteo_adyacente > 0:
                    matriz[y][x] = conteo_adyacente

def calcular_vacios(tablero, fila , columna):
    if not (0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ):
        return
    celda_actual = tablero[fila][columna]

    if celda_actual["revelada"] or celda_actual["hay_mina"] or celda_actual["flag"]:
        return
    celda_actual["revelada"] = True
    if celda_actual["minas_adyacentes"] > 0:
        return
    for desplazamiento_fila in range(-1, 2):
        for desplazamiento_columna in range(-1, 2):
            # Saltar la misma celda
            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                continue
            fila_vecina = fila + desplazamiento_fila
            columna_vecina = columna + desplazamiento_columna
            calcular_vacios(tablero, fila_vecina, columna_vecina)


# Función para dibujar el tablero
def dibujar_tablero(tablero, pantalla, final):
    imagen_bandera = pygame.image.load("./assets/flag.png")
    imagen_marcador = pygame.transform.scale(imagen_bandera, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_mina = pygame.image.load("./assets/bomba.png")
    imagen_bomba = pygame.transform.scale(imagen_mina, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    for y in range(CANTIDAD_FILAS):
        for x in range(CANTIDAD_COLUMNAS):
            celda = tablero[y][x]
            rect = pygame.Rect(x * TAMAÑO_CELDA, y * TAMAÑO_CELDA + 50, TAMAÑO_CELDA, TAMAÑO_CELDA)  # Desplazar el tablero hacia abajo
            if final:
                celda["revelada"] = True
                celda["flag"] = False
            if celda["revelada"] and not celda["flag"]:
                pygame.draw.rect(pantalla, BLANCO, rect)
                if celda["hay_mina"]:
                    pygame.draw.circle(pantalla, ROJO, rect.center, TAMAÑO_CELDA // 4)
                    pantalla.blit(imagen_bomba, rect.topleft)
                elif celda["minas_adyacentes"] > 0:
                    fuente = pygame.font.Font(None, 36)
                    texto = fuente.render(str(celda["minas_adyacentes"]), True, NEGRO)
                    pantalla.blit(texto, rect.topleft)
                # elif celda["minas_adyacentes"] == 0:
                #     calcular_vacios(tablero, y, x)
            elif celda["flag"]:
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
def pantalla_inicio(pantalla)->str:
    imagen_fondo = pygame.image.load("./assets/background.jpeg").convert()
    run = True
    retorno = ""
    while run:
        pantalla.blit(imagen_fondo, (0, 0))
        fuente = pygame.font.Font(None, 48)

        # Botones
        boton_jugar = fuente.render("Jugar", True, NEGRO)
        boton_nivel = fuente.render("Nivel", True, NEGRO)
        boton_puntajes = fuente.render("Ver Puntajes", True, NEGRO)
        boton_salir = fuente.render("Salir", True, NEGRO)

        boton_juego = pantalla.blit(boton_jugar, (ANCHO // 2 - boton_jugar.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(boton_nivel, (ANCHO // 2 - boton_nivel.get_width() // 2, ALTO // 2 - 20))
        pantalla.blit(boton_puntajes, (ANCHO // 2 - boton_puntajes.get_width() // 2, ALTO // 2 + 20))
        button_quit = pantalla.blit(boton_salir, (ANCHO // 2 - boton_salir.get_width() // 2, ALTO // 2 + 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                retorno = "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if button_quit.collidepoint(evento.pos):
                    run = False
                    retorno = "salir"
                elif boton_juego.collidepoint(evento.pos):
                    run = False
                    retorno = "jugar"


            pygame.display.flip()
    return retorno

def guardar_puntaje(ARCHIVO_PUNTAJES,nombre, puntaje):
    """
    Guarda el nombre del usuario y su puntaje en el archivo.
    """
    with open(ARCHIVO_PUNTAJES, "a") as archivo:
        archivo.write(f"{nombre},{puntaje}\n")

def obtener_mejores_puntajes(ARCHIVO_PUNTAJES):
    """
    Obtiene los tres mejores puntajes ordenados de mayor a menor.
    """
    if not os.path.exists(ARCHIVO_PUNTAJES):
        return []

    with open(ARCHIVO_PUNTAJES, "r") as archivo:
        puntajes = []
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) == 2:
                nombre, puntaje = datos
                puntajes.append((nombre, int(puntaje)))

    # Ordena los puntajes de mayor a menor
    puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)

    # Retornar los tres mejores
    return puntajes_ordenados[:3]

def mostrar_puntajes():
    """
    Muestra los tres mejores puntajes.
    """
    mejores_puntajes = obtener_mejores_puntajes()
    if mejores_puntajes:
        print("\n** Mejores Puntajes **")
        for i, (nombre, puntaje) in enumerate(mejores_puntajes, start=1):
            print(f"{i}. {nombre}: {puntaje} puntos")
    else:
        print("\nNo hay puntajes registrados aún.")

    input("\nPresiona Enter para volver al menú principal.")


def iniciar_juego(celda, pantalla):
    tablero = crear_tablero(celda)
    matriz_dinamica = crear_matriz_dinamica(tablero)
    modificar_ceros(matriz_dinamica, tablero)
    final = False
    contador_puntaje = 0000
    corriendo = True
    boton_rect = dibujar_boton_reiniciar(pantalla)
    actualizar_pantalla = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if evento.button == 1 and boton_rect.collidepoint(evento.pos):
                    tablero = crear_tablero(celda)
                    matriz_dinamica = crear_matriz_dinamica(tablero)
                    modificar_ceros(matriz_dinamica, tablero)
                    final = False
                    contador_puntaje = 0000
                    actualizar_pantalla = True

                else:
                    columna, fila = x // TAMAÑO_CELDA, (y - 50) // TAMAÑO_CELDA
                    if 0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ:
                        if evento.button == 1:
                            if not tablero[fila][columna]["revelada"] and not tablero[fila][columna]["flag"]:
                                if tablero[fila][columna]["hay_mina"]:
                                    final = True
                                else:
                                    contador_puntaje += 1
                                    if tablero[fila][columna]["minas_adyacentes"] == 0:
                                        calcular_vacios(tablero, fila, columna)
                                    else:
                                        tablero[fila][columna]["revelada"] = True
                                actualizar_pantalla = True

                        elif evento.button == 3:
                            if not tablero[fila][columna]["revelada"]:
                                tablero[fila][columna]["flag"] = not tablero[fila][columna]["flag"]
                                actualizar_pantalla = True

        if actualizar_pantalla:
            pantalla.fill(NEGRO)
            dibujar_boton_reiniciar(pantalla)
            puntaje(pantalla, contador_puntaje)
            dibujar_tablero(tablero, pantalla, final)
            pygame.display.flip()
            actualizar_pantalla = False

def puntaje(pantalla, contador_puntaje):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render(f"Puntaje: {str(contador_puntaje).zfill(4)}", True, NEGRO)
    rect = texto.get_rect(center=(ANCHO - 60, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)
    return None

# Función principal del juego
def main(pantalla):
    celda = {
        "hay_mina": False,
        "revelada": False,
        "flag": False,
        "minas_adyacentes": 0
    }
    seleccion_inicio = pantalla_inicio(pantalla)
    match seleccion_inicio:
        case "salir":
            pygame.quit()
        case "jugar":
            iniciar_juego(celda,pantalla)
        case _:
            print("error")

    # ARCHIVO_PUNTAJES = "puntajes.txt"
    #

