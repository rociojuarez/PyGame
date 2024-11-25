from constants import *
import random
import pygame
import os
from json import *

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

def calcular_vacios(tablero, fila , columna, contador_puntaje):
    if not (0 <= fila < TAMAÑO_MATRIZ and 0 <= columna < TAMAÑO_MATRIZ):
        return
    celda_actual = tablero[fila][columna]
    if celda_actual["revelada"] or celda_actual["hay_mina"] or celda_actual["flag"]:
        return
    celda_actual["revelada"] = True
    contador_puntaje += 1
    if celda_actual["minas_adyacentes"] > 0:
        return
    for desplazamiento_fila in range(-1, 2):
        for desplazamiento_columna in range(-1, 2):
            # Saltar la misma celda
            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                continue
            fila_vecina = fila + desplazamiento_fila
            columna_vecina = columna + desplazamiento_columna
            calcular_vacios(tablero, fila_vecina, columna_vecina, contador_puntaje)
    return contador_puntaje


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
    niveles = ["Fácil", "Medio", "Difícil"]
    indice_nivel = 0
    while run:
        pantalla.blit(imagen_fondo, (0, 0))
        fuente = pygame.font.Font(None, 48)

        # Botones
        boton_jugar = fuente.render("Jugar", True, BLANCO)
        boton_nivel = fuente.render(f"Nivel: {niveles[indice_nivel]}", True, BLANCO)
        boton_puntajes = fuente.render("Ver Puntajes", True, BLANCO)
        boton_salir = fuente.render("Salir", True, BLANCO)

        boton_juego = pantalla.blit(boton_jugar, (ANCHO // 2 - boton_jugar.get_width() // 2, ALTO // 2 - 60))
        seleccionador_niveles = pantalla.blit(boton_nivel, (ANCHO // 2 - boton_nivel.get_width() // 2, ALTO // 2 - 20))
        boton_pantalla_puntajes = pantalla.blit(boton_puntajes, (ANCHO // 2 - boton_puntajes.get_width() // 2, ALTO // 2 + 20))
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
                elif boton_pantalla_puntajes.collidepoint(evento.pos):
                    run = False
                    retorno = "puntajes"
                elif seleccionador_niveles.collidepoint(evento.pos):
                    indice_nivel = (indice_nivel + 1) % len(niveles)

            pygame.display.flip()
    return retorno

def verificar_juego_ganado(puntaje, tablero):
    resultado = False
    contador_minas = 0
    for i in range(CANTIDAD_FILAS):
        for j in range(CANTIDAD_COLUMNAS):
            if (tablero[i][j]["flag"] == False and tablero[i][j]["hay_mina"] == True) or (tablero[i][j]["revelada"] == False and tablero[i][j]["hay_mina"] == False):
                resultado = False
                break
            if tablero[i][j]["flag"] == True and tablero[i][j]["hay_mina"] == True:
                contador_minas += 1
            if contador_minas == CANTIDAD_MINAS:
                resultado = True
                break
    return resultado

def guardar_archivo_json(ruta:str, lista:list[dict])->None:
    with open(ruta, "w") as archivo:
        dump(lista, archivo, indent=4)

def cargar_archivo_json(ruta:str):
    with open(ruta, "r") as archivo:
        datos = load(archivo)
    return datos

def obtener_mejores_puntajes(puntajes):
    """
    Obtiene los tres mejores puntajes ordenados de mayor a menor.
    """
    jugadores = []
    for jugador in puntajes:
        print("len: ", len(puntajes), "jugador: ", jugador)
        if len(puntajes) >= 1:
            jugadores.append(jugador)
    print(jugadores)
    def obtener_puntaje(jugadores):
        return jugadores["puntaje"]

    ordenados = sorted(jugadores, key=obtener_puntaje, reverse=True)
    return ordenados

def mostrar_puntajes(pantalla, path_archivo_puntajes):
    puntajes = cargar_archivo_json(path_archivo_puntajes)
    mejores_puntajes = obtener_mejores_puntajes(puntajes)
    fuente = pygame.font.SysFont("Arial", 30, bold=True)
    run =True
    while run:
        # Dibujar fondo y elementos de la pantalla
        pantalla.fill(NEGRO)

        # Dibujar título
        texto = fuente.render("** Mejores Puntajes **", True, BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 150))
        pantalla.blit(texto, rect_texto)

        # Dibujar botón "Volver"
        texto_volver = fuente.render("<- Volver", True, BLANCO)
        boton_volver = pantalla.blit(
            texto_volver,
            (ANCHO // 2 - texto_volver.get_width() // 2, ALTO // 2 + 150))

        if mejores_puntajes:
            # Dibujar pantalla de ingreso de nombre
            alto_nombres = 50
            for i, jugador in enumerate(mejores_puntajes, start=1):
                print(f"{i}. {jugador["nombre"]}: {jugador["puntaje"]} puntos")
                texto_jugador = fuente.render(f"{i}. {jugador["nombre"]}: {jugador["puntaje"]} puntos", True, BLANCO)
                rect_nombre = texto_jugador.get_rect(center=(ANCHO // 2, ALTO // 2 + alto_nombres))
                alto_nombres += 30
                pantalla.blit(texto_jugador, rect_nombre)
        else:
            texto = fuente.render("No hay puntajes registrados*", True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(texto, rect_texto)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_inicio(pantalla)
                    run = False
    return None

def iniciar_juego(celda, pantalla):
    tablero = crear_tablero(celda)
    matriz_dinamica = crear_matriz_dinamica(tablero)
    modificar_ceros(matriz_dinamica, tablero)
    final = False
    contador_puntaje = 0000
    corriendo = True
    boton_rect = dibujar_boton_reiniciar(pantalla)
    actualizar_pantalla = True
    juego_ganado = False
    nombre_ingresado = ""
    fuente = pygame.font.SysFont("Arial", 30, bold=True)
    jugadores = cargar_archivo_json(PATH_ARCHIVO_PUNTAJES)
    while corriendo:
        if not juego_ganado:
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
                                        if tablero[fila][columna]["minas_adyacentes"] == 0:
                                            contador_puntaje = calcular_vacios(tablero, fila, columna, contador_puntaje)
                                            print("contador puntaje: ", contador_puntaje)
                                        else:
                                            tablero[fila][columna]["revelada"] = True
                                            contador_puntaje += 1
                                    actualizar_pantalla = True

                            elif evento.button == 3:
                                if not tablero[fila][columna]["revelada"]:
                                    tablero[fila][columna]["flag"] = not tablero[fila][columna]["flag"]
                                    actualizar_pantalla = True
                    juego_ganado = verificar_juego_ganado(contador_puntaje, tablero)
        else:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                    pygame.quit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        jugadores.append({"nombre": nombre_ingresado, "puntaje": contador_puntaje})# Finalizar ingreso del nombre
                        guardar_archivo_json(PATH_ARCHIVO_PUNTAJES, jugadores)
                        mostrar_puntajes(pantalla, PATH_ARCHIVO_PUNTAJES)
                        corriendo = False
                    elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        nombre_ingresado = nombre_ingresado[:-1]
                    else:  # Agregar nuevo carácter
                        nombre_ingresado += evento.unicode

            # Dibujar pantalla de ingreso de nombre
            pantalla.fill(NEGRO)
            texto = fuente.render("¡Ganaste! Ingresa tu nombre:", True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(texto, rect_texto)

            # Mostrar nombre ingresado
            nombre_usuario = fuente.render(nombre_ingresado, True, BLANCO)
            rect_nombre = nombre_usuario.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
            pantalla.blit(nombre_usuario, rect_nombre)

            pygame.display.flip()
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
        case "puntajes":
            mostrar_puntajes(pantalla, PATH_ARCHIVO_PUNTAJES)
        case _:
            print("error")

