from constants import *
import random
import pygame
from json import *


# Crear la matriz
def crear_tablero(celda:dict, cantidad_filas, cantidad_columnas, cantidad_bombas):
    tablero = inicializar_matriz(celda, cantidad_filas, cantidad_columnas)
    colocar_minas(tablero, cantidad_filas, cantidad_columnas, cantidad_bombas)
    calcular_minas_adyacentes(tablero, cantidad_filas, cantidad_columnas)
    return tablero

def inicializar_matriz(celda: dict, cantidad_filas, cantidad_columnas)->list:
    matriz = []
    for i in range(cantidad_filas):
        fila = []
        for j in range(cantidad_columnas):
            fila.append(celda.copy())
        matriz.append(fila)
    return matriz


# A. Desarrollar una función que realice la creación dinámica de una matriz de 8 filas por 8
# columnas. En la misma se deberá incluir:
#  Menos uno (-1): Si hay una mina en la coordenada de la matriz
#  Cero (0): Si no hay una mina en la coordenada de la matriz, ni minas contiguas.
def inicializar_matriz_ceros(cantidad_filas, cantidad_columnas)->list:
    matriz = []
    for i in range(cantidad_filas):
        fila = []
        for j in range(cantidad_columnas):
            fila.append(0)
        matriz.append(fila)
    return matriz

# Crear matriz dinámica con -1 y 0
def crear_matriz_dinamica(tablero, cantidad_filas, cantidad_columnas):
    matriz = inicializar_matriz_ceros(cantidad_filas, cantidad_columnas)
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            if tablero[y][x]["hay_mina"]:
                matriz[y][x] = -1
            elif tablero[y][x]["minas_adyacentes"] == 0:
                matriz[y][x] = 0
    return matriz

def colocar_minas(tablero, cantidad_filas, cantidad_columnas, cantidad_minas):
    minas_colocadas = 0
    while minas_colocadas < cantidad_minas:
        x = random.randint(0, cantidad_columnas - 1)
        y = random.randint(0, cantidad_filas - 1)
        if not tablero[y][x]["hay_mina"]:
            tablero[y][x].update({"hay_mina": True})
            minas_colocadas += 1

# B. Desarrollar una función que verifique cada elemento de la matriz y realice la siguiente
# modificación en cada cero (0) que encuentre si se cumple alguna de las siguientes condiciones:
def calcular_minas_adyacentes(tablero, cantidad_filas, cantidad_columnas):
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            if tablero[y][x]["hay_mina"]:
                for desplazamiento_fila in range(-1, 2):
                    for desplazamiento_columna in range(-1, 2):
                        fila_vecina = y + desplazamiento_fila
                        columna_vecina = x + desplazamiento_columna
                        if 0 <= fila_vecina < cantidad_filas and 0 <= columna_vecina < cantidad_columnas:
                            if not tablero[fila_vecina][columna_vecina]["hay_mina"]:
                                tablero[fila_vecina][columna_vecina]["minas_adyacentes"] += 1



# Modificar ceros en la matriz según las minas contiguas
def modificar_ceros(matriz, tablero, cantidad_filas, cantidad_columnas):
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            if matriz[y][x] == 0 and not tablero[y][x]["hay_mina"]:
                conteo_adyacente = tablero[y][x]["minas_adyacentes"]
                if conteo_adyacente > 0:
                    matriz[y][x] = conteo_adyacente

def calcular_vacios(tablero, fila , columna, contador_puntaje, cantidad_filas, cantidad_columnas):
    if fila < 0 or fila >= cantidad_filas:
        return

    if columna < 0 or columna >= cantidad_columnas:
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
            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                continue
            fila_vecina = fila + desplazamiento_fila
            columna_vecina = columna + desplazamiento_columna
            calcular_vacios(tablero, fila_vecina, columna_vecina, contador_puntaje, cantidad_filas, cantidad_columnas)
    return contador_puntaje


# Función para dibujar el tablero
def dibujar_tablero(tablero, pantalla, final, cantidad_filas, cantidad_columnas):
    imagen_celda = pygame.image.load("./assets/celda.png")
    imagen_celda = pygame.transform.scale(imagen_celda, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_bandera = pygame.image.load("./assets/flag.png")
    imagen_marcador = pygame.transform.scale(imagen_bandera, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_mina = pygame.image.load("./assets/bomba.png")
    imagen_bomba = pygame.transform.scale(imagen_mina, (TAMAÑO_CELDA, TAMAÑO_CELDA))


    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            celda = tablero[y][x]
            rect = pygame.Rect(x * TAMAÑO_CELDA, y * TAMAÑO_CELDA + 50, TAMAÑO_CELDA, TAMAÑO_CELDA)  # Desplazar el tablero hacia abajo
            if final:
                celda["revelada"] = True
                celda["flag"] = False
            if celda["revelada"] and not celda["flag"]:
                pygame.draw.rect(pantalla, FONDO_CELDA, rect)
                if celda["hay_mina"]:
                    pantalla.blit(imagen_bomba, rect.topleft)
                elif celda["minas_adyacentes"] > 0:
                    fuente = pygame.font.Font(None, 36)
                    color = BLANCO
                    if celda["minas_adyacentes"] == 2:
                        color = VERDE
                    elif celda["minas_adyacentes"] == 3:
                        color = ROJO
                    elif celda["minas_adyacentes"] == 4:
                        color = AMARILLO
                    elif celda["minas_adyacentes"] == 5:
                        color = ROSA
                    elif celda["minas_adyacentes"] == 6:
                        color = VIOLETA
                    elif celda["minas_adyacentes"] == 1:
                        color = AZUL
                    elif celda["minas_adyacentes"] == 7:
                        color = CELESTE
                    texto = fuente.render(str(celda["minas_adyacentes"]), True, color)
                    texto_center = texto.get_rect(center=rect.center)
                    pantalla.blit(texto, texto_center)
            elif celda["flag"]:
                pantalla.blit(imagen_celda, rect.topleft)
                pantalla.blit(imagen_marcador, rect.topleft)
            else:
                pantalla.blit(imagen_celda, rect.topleft)

            pygame.draw.rect(pantalla, NEGRO, rect, 1)

# Función para dibujar el botón "Reiniciar"
def dibujar_boton_reiniciar(pantalla):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render("Reiniciar", True, NEGRO)
    rect = texto.get_rect(center=(55, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)
    return rect

def verificar_juego_ganado(tablero, cantidad_filas, cantidad_columnas, cantidad_minas):
    resultado = False
    contador_minas = 0
    for i in range(cantidad_filas):
        for j in range(cantidad_columnas):
            if (tablero[i][j]["flag"] == False and tablero[i][j]["hay_mina"] == True) or (tablero[i][j]["revelada"] == False and tablero[i][j]["hay_mina"] == False):
                resultado = False
                break
            if tablero[i][j]["flag"] == True and tablero[i][j]["hay_mina"] == True:
                contador_minas += 1
            if contador_minas == cantidad_minas:
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
    jugadores = []
    for jugador in puntajes:
        if len(puntajes) >= 1:
            jugadores.append(jugador)
    def obtener_puntaje(jugadores):
        return jugadores["puntaje"]

    ordenados = sorted(jugadores, key=obtener_puntaje, reverse=True)
    return ordenados

def mostrar_puntajes(pantalla, path_archivo_puntajes):
    imagen_fondo = pygame.image.load("./assets/back.jpg")
    puntajes = cargar_archivo_json(path_archivo_puntajes)
    mejores_puntajes = obtener_mejores_puntajes(puntajes)
    fuente_titulo = pygame.font.Font("./assets/fonts/04b_25__.ttf", 40)
    fuente = pygame.font.Font("./assets/fonts/04b_25__.ttf", 30)
    run =True
    while run:
        pantalla.blit(imagen_fondo, (0, 0))

        # Crear el recuadro opaco en el centro
        ancho_recuadro = ANCHO // 1.2
        alto_recuadro = ALTO // 1.2
        x_recuadro = (ANCHO - ancho_recuadro) // 2
        y_recuadro = (ALTO - alto_recuadro) // 2

        recuadro = pygame.Surface((ancho_recuadro, alto_recuadro))
        recuadro.set_alpha(180)  # Nivel de opacidad (0 es completamente transparente, 255 es sólido)
        recuadro.fill((0, 0, 50))  # Color del recuadro (azul oscuro)
        pantalla.blit(recuadro, (x_recuadro, y_recuadro))

        # Dibujar título
        texto = fuente_titulo.render("** Mejores Puntajes **", True, BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO // 2, 100))
        pantalla.blit(texto, rect_texto)

        # Dibujar botón "Volver"
        texto_volver = fuente.render("Volver", True, BLANCO)
        boton_volver = texto_volver.get_rect(center=(110, 35))

        # Dibujar fondo del botón
        fondo_rect = pygame.Rect(
            boton_volver.left - 10, boton_volver.top - 10, boton_volver.width + 20, boton_volver.height + 20
        )

        # Detectar hover
        mouse_pos = pygame.mouse.get_pos()
        hover = fondo_rect.collidepoint(mouse_pos)

        # Colores según hover
        if hover:
            color_fondo = (30, 30, 80)
            color_borde = BLANCO
        else:
            color_fondo = (20, 20, 60)
            color_borde = NEGRO

        pygame.draw.rect(pantalla, color_fondo, fondo_rect)
        pygame.draw.rect(pantalla, color_borde, fondo_rect, 2)

        # Dibujar texto del botón
        pantalla.blit(texto_volver, boton_volver)

        if mejores_puntajes:
            alto_nombres = 50
            i = 1
            for jugador in mejores_puntajes:
                texto_jugador = fuente.render(f"{i}. {jugador["nombre"]}: {jugador["puntaje"]} puntos", True, BLANCO)
                rect_nombre = texto_jugador.get_rect(center=(ANCHO // 2, ALTO // 4 + alto_nombres))
                alto_nombres += 30
                pantalla.blit(texto_jugador, rect_nombre)
                i += 1
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
                    main(pantalla)
                    run = False
    return None

def pantalla_ingreso_nombre(contador_puntaje):
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    imagen_fondo = pygame.image.load("./assets/back.jpg")
    nombre_ingresado = ""
    fuente = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_titulo = pygame.font.Font("./assets/fonts/04b_25__.ttf", 40)
    jugadores = cargar_archivo_json(PATH_ARCHIVO_PUNTAJES)
    corriendo = True
    while corriendo:
        pantalla.blit(imagen_fondo, (0, 0))

        # Crear el recuadro opaco en el centro
        ancho_recuadro = ANCHO // 1.2
        alto_recuadro = ALTO // 1.2
        x_recuadro = (ANCHO - ancho_recuadro) // 2
        y_recuadro = (ALTO - alto_recuadro) // 2

        recuadro = pygame.Surface((ancho_recuadro, alto_recuadro))
        recuadro.set_alpha(180)  # Nivel de opacidad (0 es completamente transparente, 255 es sólido)
        recuadro.fill((0, 0, 50))  # Color del recuadro (azul oscuro)
        pantalla.blit(recuadro, (x_recuadro, y_recuadro))

        # Dibujar título
        texto = fuente_titulo.render("¡¡Ganaste!!", True, BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO // 2, 100))
        pantalla.blit(texto, rect_texto)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jugadores.append({"nombre": nombre_ingresado, "puntaje": contador_puntaje})
                    guardar_archivo_json(PATH_ARCHIVO_PUNTAJES, jugadores)
                    mostrar_puntajes(pantalla, PATH_ARCHIVO_PUNTAJES)
                    corriendo = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    nombre_ingresado += evento.unicode

        # Dibujar pantalla de ingreso de nombre
        texto = fuente.render("Ingresa tu nombre, y para finalizar apreta ENTER:", True, BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO // 2, 250))
        pantalla.blit(texto, rect_texto)

        # Mostrar nombre ingresado
        nombre_usuario = fuente_titulo.render(nombre_ingresado, True, BLANCO)
        rect_nombre = nombre_usuario.get_rect(center=(ANCHO // 2, 290))
        pantalla.blit(nombre_usuario, rect_nombre)

        pygame.display.flip()

def iniciar_juego(celda, pantalla, indice_nivel:int):
    if indice_nivel == 1:
        cantidad_filas = 16
        cantidad_columnas = 16
        cantidad_bombas = 40
        ancho_nivel = ANCHO
        alto_nivel = ALTO
    elif indice_nivel == 2:
        cantidad_filas = 16
        cantidad_columnas = 30
        cantidad_bombas = 100
        ancho_nivel = ANCHO * 1.9
        alto_nivel = ALTO +110
    else:
        cantidad_filas = 8
        cantidad_columnas = 8
        cantidad_bombas = 10
        ancho_nivel = ANCHO // 2 + 50
        alto_nivel = ALTO // 2 + 50
    pantalla = pygame.display.set_mode((ancho_nivel, alto_nivel))
    tablero = crear_tablero(celda, cantidad_filas, cantidad_columnas, cantidad_bombas)
    matriz_dinamica = crear_matriz_dinamica(tablero, cantidad_filas, cantidad_columnas)
    modificar_ceros(matriz_dinamica, tablero, cantidad_filas, cantidad_columnas)
    final = False
    contador_puntaje = 0000
    corriendo = True
    boton_rect = dibujar_boton_reiniciar(pantalla)
    actualizar_pantalla = True
    juego_ganado = False
    while corriendo:
        if not juego_ganado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                    pygame.quit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    if evento.button == 1 and boton_rect.collidepoint(evento.pos):
                        tablero = crear_tablero(celda, cantidad_filas, cantidad_columnas, cantidad_bombas)
                        matriz_dinamica = crear_matriz_dinamica(tablero, cantidad_filas, cantidad_columnas)
                        modificar_ceros(matriz_dinamica, tablero, cantidad_filas, cantidad_columnas)
                        final = False
                        contador_puntaje = 0000
                        actualizar_pantalla = True

                    else:
                        columna, fila = x // TAMAÑO_CELDA, (y - 50) // TAMAÑO_CELDA
                        if 0 <= fila < cantidad_filas and 0 <= columna < cantidad_columnas:
                            if evento.button == 1:
                                if not tablero[fila][columna]["revelada"] and not tablero[fila][columna]["flag"]:
                                    if tablero[fila][columna]["hay_mina"]:
                                        final = True
                                    else:
                                        if tablero[fila][columna]["minas_adyacentes"] == 0:
                                            contador_puntaje = calcular_vacios(tablero, fila, columna, contador_puntaje, cantidad_filas, cantidad_columnas)
                                        else:
                                            tablero[fila][columna]["revelada"] = True
                                            contador_puntaje += 1
                                    actualizar_pantalla = True

                            elif evento.button == 3:
                                if not tablero[fila][columna]["revelada"]:
                                    tablero[fila][columna]["flag"] = not tablero[fila][columna]["flag"]
                                    actualizar_pantalla = True
                    juego_ganado = verificar_juego_ganado(tablero, cantidad_filas, cantidad_columnas, cantidad_bombas)
        else:
            pantalla_ingreso_nombre(contador_puntaje)
            corriendo = False

        if actualizar_pantalla:
            pantalla.fill(FONDO)
            dibujar_boton_reiniciar(pantalla)
            puntaje(pantalla, contador_puntaje, ancho_nivel)
            dibujar_tablero(tablero, pantalla, final, cantidad_filas, cantidad_columnas)

            pygame.display.flip()
            actualizar_pantalla = False


def puntaje(pantalla, contador_puntaje, ancho):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render(f"Puntaje: {str(contador_puntaje).zfill(4)}", True, NEGRO)
    rect = texto.get_rect(center=(ancho - 60, 25))
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
    imagen_fondo = pygame.image.load("./assets/back.jpg")
    run = True
    niveles = ["Facil", "Medio", "Dificil"]
    indice_nivel = 0
    while run:
        pantalla.blit(imagen_fondo, (0, 0))
        font = pygame.font.Font("./assets/fonts/04b_25__.ttf", 100)
        font_menu_buttons = pygame.font.Font("./assets/fonts/04b_25__.ttf", 30)

        game_name = font.render("Buscaminas", True, BLANCO)
        text_rect = game_name.get_rect(center=(ANCHO/2, ALTO/8))
        pantalla.blit(game_name, text_rect)

        botones = [
            {"texto": "Jugar", "pos": (ANCHO // 5, ALTO // 2+ 100)},
            {"texto": f"Nivel: {niveles[indice_nivel]}", "pos": (ANCHO // 5, ALTO // 2 + 160)},
            {"texto": "Ver Puntajes", "pos": (ANCHO // 5, ALTO // 2 + 220)},
            {"texto": "Salir", "pos": (ANCHO // 5, ALTO // 2 + 280)},
        ]
        botones_rect = []

        for boton in botones:
            texto_renderizado = font_menu_buttons.render(boton["texto"], True, BLANCO)
            texto_rect = texto_renderizado.get_rect(center=boton["pos"])

            # Dibujar fondo del botón
            fondo_rect = pygame.Rect(
                texto_rect.left - 10, texto_rect.top - 10, texto_rect.width + 20, texto_rect.height + 20
            )

            # Detectar hover
            mouse_pos = pygame.mouse.get_pos()
            hover = fondo_rect.collidepoint(mouse_pos)

            # Colores según hover
            color_fondo = (30, 30, 80) if hover else (20, 20, 60)
            color_borde = BLANCO if hover else NEGRO

            pygame.draw.rect(pantalla, color_fondo, fondo_rect)
            pygame.draw.rect(pantalla, color_borde, fondo_rect, 2)

            # Dibujar texto del botón
            pantalla.blit(texto_renderizado, texto_rect)
            botones_rect.append(fondo_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botones_rect[0].collidepoint(evento.pos):
                    run = False
                    iniciar_juego(celda,pantalla, indice_nivel)
                elif botones_rect[1].collidepoint(evento.pos):
                    indice_nivel = (indice_nivel + 1) % len(niveles)
                elif botones_rect[2].collidepoint(evento.pos):
                    run = False
                    mostrar_puntajes(pantalla, PATH_ARCHIVO_PUNTAJES)
                elif botones_rect[3].collidepoint(evento.pos):
                    run = False
                    pygame.quit()
            pygame.display.flip()

