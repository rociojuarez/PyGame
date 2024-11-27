from typing import Tuple

from constants import *
import random
import pygame
from json import *


def crear_tablero(celda:dict, cantidad_filas:int, cantidad_columnas:int, cantidad_bombas:int)->list:
    '''
    Funcion que crea el tablero del juego, inicializa la matriz con las celdas, coloca las minas y calcula las minas adyacentes.
    :param celda: Recibe el diccionario de la celda.
    :param cantidad_filas: Recibe la cantidad de filas del tablero dependiendo el nivel seleccionado.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero dependiendo el nivel seleccionado.
    :param cantidad_bombas: Recibe la cantidad de minas del tablero dependiendo el nivel seleccionado.
    :return: Retorna una matriz con el tablero creado.
    '''
    tablero = inicializar_matriz(celda, cantidad_filas, cantidad_columnas)
    colocar_minas(tablero, cantidad_filas, cantidad_columnas, cantidad_bombas)
    calcular_minas_adyacentes(tablero, cantidad_filas, cantidad_columnas)
    return tablero

def inicializar_matriz(celda: dict, cantidad_filas:int, cantidad_columnas:int)->list:
    '''
    Funcion que inicializa la matriz poniendo en cada posicion un diccionario que representa una celda del juego.
    :param celda: Recibe el diccionario de la celda.
    :param cantidad_filas: Recibe la cantidad de filas de la matriz a inicializar dependiendo el nivel seleccionado.
    :param cantidad_columnas: Recibe la cantidad de columnas de la matriz a inicializar dependiendo el nivel seleccionado.
    :return: Retorna la matriz inicializada.
    '''
    matriz = []
    for i in range(cantidad_filas):
        fila = []
        for j in range(cantidad_columnas):
            fila.append(celda.copy())
        matriz.append(fila)
    return matriz


def inicializar_matriz_ceros(cantidad_filas:int, cantidad_columnas:int)->list:
    '''
    Funcion que inicializa una matriz con las dimensiones pasadas por parametro y llena de ceros.
    :param cantidad_filas: Recibe la cantidad de filas de la matriz a inicializar.
    :param cantidad_columnas: Recibe la cantidad de columnas de la matriz a inicializar.
    :return: Retorna la matriz inicializada con 0.
    '''
    matriz = []
    for i in range(cantidad_filas):
        fila = []
        for j in range(cantidad_columnas):
            fila.append(0)
        matriz.append(fila)
    return matriz

def crear_matriz_dinamica(tablero:list[dict], cantidad_filas:int, cantidad_columnas:int)->list:
    '''
    Funcion que crea una matriz y luego si en esa posicion en el tablero hay una mina le coloca -1, si no se encuentran minas adyacentes le coloca 0.
    :param tablero: Recibe el tablero con las minas colocadas.
    :param cantidad_filas: Recibe la cantidad de filas del tablero.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero.
    :return: Retorna la matriz dinamica con las minas (-1) y los ceros.
    '''
    matriz = inicializar_matriz_ceros(cantidad_filas, cantidad_columnas)
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            if tablero[y][x]["hay_mina"]:
                matriz[y][x] = -1
            elif tablero[y][x]["minas_adyacentes"] == 0:
                matriz[y][x] = 0
    return matriz

def colocar_minas(tablero:list[dict], cantidad_filas:int, cantidad_columnas:int, cantidad_minas:int)->None:
    '''
    Funcion que coloca las minas en el tablero de manera aleatoria.
    :param tablero: Recibe el tablero sin minas con las celdas.
    :param cantidad_filas: Recibe la cantidad de filas del tablero.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero.
    :param cantidad_minas: Recibe la cantidad de minas seleccionadas dependiendo del nivel.
    :return: Retorna None.
    '''
    minas_colocadas = 0
    while minas_colocadas < cantidad_minas:
        x = random.randint(0, cantidad_columnas - 1)
        y = random.randint(0, cantidad_filas - 1)
        if not tablero[y][x]["hay_mina"]:
            tablero[y][x].update({"hay_mina": True})
            minas_colocadas += 1

def calcular_minas_adyacentes(tablero:list[dict], cantidad_filas:int, cantidad_columnas:int)->None:
    '''
    Funcion que calcula las minas adyacentes a cada celda del tablero y coloca el valor en "minas_adyacentes" de cada celda.
    :param tablero: Recibe el tablero con las minas colocadas.
    :param cantidad_filas: Recibe la cantidad de filas del tablero.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero.
    :return: retorna None
    '''
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



def modificar_ceros(matriz:list, tablero:list[dict], cantidad_filas:int, cantidad_columnas:int)->None:
    '''
    Funcion que recibe la matriz dinamica y el tablero con las minas colocadas y modifica los ceros por los valores de las minas adyacentes.
    :param matriz: Recibe la matriz dinamica con las minas y los ceros.
    :param tablero: Recibe el tablero para guiarse de las minas adyacentes.
    :param cantidad_filas: Recibe la cantidad de filas del tablero.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero.
    :return: No retorna nada nada, solo modifica la matriz dinamica.
    '''
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            if matriz[y][x] == 0 and not tablero[y][x]["hay_mina"]:
                conteo_adyacente = tablero[y][x]["minas_adyacentes"]
                if conteo_adyacente > 0:
                    matriz[y][x] = conteo_adyacente

def calcular_vacios(tablero:list[dict], fila:int , columna:int, contador_puntaje:int, cantidad_filas:int, cantidad_columnas:int)->int:
    '''
    Funcion que calcula los espacios vacios alrededor de una celda y los revela recursivamente.
    :param tablero: recibe el tablero del juego
    :param fila: Recibe la fila de la celda a revisar
    :param columna: Recibe la columna de la celda a revisar
    :param contador_puntaje: Recibe el puntaje actual del juego
    :param cantidad_filas: Recibe la cantidad de filas del tablero
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero
    :return: Retorna el puntaje actualizado
    '''
    if fila >= 0 and fila < cantidad_filas:
        if columna >= 0 and columna < cantidad_columnas:
            celda_actual = tablero[fila][columna]
            if not celda_actual["revelada"] and not celda_actual["hay_mina"] and not celda_actual["flag"]:
                celda_actual["revelada"] = True
                contador_puntaje += 1
                if celda_actual["minas_adyacentes"] == 0:
                    for desplazamiento_fila in range(-1, 2):
                        for desplazamiento_columna in range(-1, 2):
                            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                                continue
                            fila_vecina = fila + desplazamiento_fila
                            columna_vecina = columna + desplazamiento_columna
                            calcular_vacios(tablero, fila_vecina, columna_vecina, contador_puntaje, cantidad_filas, cantidad_columnas)
    return contador_puntaje


def dibujar_tablero(tablero:list[dict], pantalla:pygame.Surface, final:bool, cantidad_filas:int, cantidad_columnas:int)->None:
    '''
    Funcion que dibuja el tablero en la pantalla, mostrando las celdas reveladas, las banderas y las minas.
    :param tablero: recibe la matriz "tablero" del juego
    :param pantalla: Recibe la pantalla donde se va a renderizar el tablero.
    :param final: Recibe un booleano que indica si el juego finalizó (solo si el jugador perdió).
    :param cantidad_filas: Recibe la cantidad de filas del tablero
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero
    :return: Retorna None
    '''
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

def dibujar_boton_reiniciar(pantalla:pygame.Surface)->pygame.Rect:
    '''
    Funcion que crea y dibuja el boton para reiniciar el juego
    :param pantalla: Recibe por parametro la pantalla donde se va a renderizar el boton.
    :return: Retorna el rectangulo donde se va a encontrar el boton.
    '''
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render("Reiniciar", True, NEGRO)
    rect = texto.get_rect(center=(55, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))
    pantalla.blit(texto, rect)
    return rect

def verificar_juego_ganado(tablero:list[dict], cantidad_filas:int, cantidad_columnas:int, cantidad_minas:int)->bool:
    '''
    Funcion que recorre el tablero para verificar si se gano el juego, contando las banderas y fijandose que no quede ninguna mina sin marcar.
    :param tablero: Recibe el tablero del juego
    :param cantidad_filas: Recibe la cantidad de filas del tablero para poder recorrerlo.
    :param cantidad_columnas: Recibe la cantidad de columnas del tablero para poder recorrerlo.
    :param cantidad_minas: Recibe la cantidad de minas que tiene el tablero, depende de la dificultad seleccionada.
    :return: Retorna True cuando el juego se ganó, sino retorna False
    '''
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
    '''
    Funcion que guarda una lista en un archivo json.
    :param ruta: Recibe el path donde guardar el archivo.
    :param lista: Recibe la lista a guardar en el archivo.
    :return: Retorna None
    '''
    with open(ruta, "w") as archivo:
        dump(lista, archivo, indent=4)

def cargar_archivo_json(ruta:str)->list:
    '''
    Funcion que carga un archivo json y lo retorna como una lista.
    :param ruta: Recibe el path donde buscar el archivo para leerlo.
    :return: Retorna el archivo leido como una lista.
    '''
    with open(ruta, "r") as archivo:
        datos = load(archivo)
    return datos

def obtener_puntaje(jugadores:list)->int:
    '''
    Funcion que obtiene el puntaje de un jugador (funciona como key para el metodo sorted).
    :param jugadores: Recibe la lista de jugadores para obtener el puntaje.
    :return: Retorna el puntaje del jugador.
    '''
    return jugadores["puntaje"]

def obtener_mejores_puntajes(puntajes:list)->list:
    '''
    Funcion que acomoda una lista de jugadores y solo deja los mejores 10 acomodandolos de mayor a menor.
    :param puntajes:Recibe la lista de jugadores para chequear los puntajes a ordenar.
    :return:Retorna la lista de jugadores ordenada de mayor a menor.
    '''
    jugadores = []
    for jugador in puntajes:
        if len(puntajes) >= 1:
            jugadores.append(jugador)

    ordenados = sorted(jugadores, key=obtener_puntaje, reverse=True)
    return ordenados[:10]

def mostrar_puntajes(pantalla:pygame.Surface, path_archivo_puntajes:str)->str:
    '''
    Funcion que genera y muestra la pantalla con los 10 mejores puntajes del juego.
    :param pantalla: Recibe la pantalla donde se va a renderizar la pantalla de puntajes.
    :param path_archivo_puntajes: Recibe el path del archivo donde se guardan los puntajes.
    :return: Retorna el nombre de la pantalla a la que quiere dirigirse.
    '''
    imagen_fondo = pygame.image.load("./assets/back.jpg")
    puntajes = cargar_archivo_json(path_archivo_puntajes)
    mejores_puntajes = obtener_mejores_puntajes(puntajes)
    fuente_titulo = pygame.font.Font("./assets/fonts/04b_25__.ttf", 40)
    fuente = pygame.font.Font("./assets/fonts/04b_25__.ttf", 30)
    run =True
    pantalla_retorno = "menu"
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
            texto = fuente.render("No hay puntajes registrados", True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(texto, rect_texto)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pantalla_retorno = "salir"
                run = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_retorno = "menu"
                    run = False
    pygame.display.flip()
    return pantalla_retorno

def pantalla_ingreso_nombre(contador_puntaje:int)->None:
    '''
    Funcion que muestra la pantalla de ingreso de nombre cuando se gana el juego y te envia a la pantalla donde muestra los mejores puntajes.
    :param contador_puntaje: Recibe por parametro el puntaje del jugador
    :return: No retorna nada
    '''
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

def iniciar_juego(celda:dict,  indice_nivel:int)->None:
    '''
    Funcion que inicia el juego, setea el tablero dependiendo del nivel elegido en la pantalla de inicio y lleva el contador de puntaje del juego.
    :param celda: Recibe el diccionario de la celda.
    :param indice_nivel: Recibe el indice del nivel seleccionado, siendo 0 Facil, 1 Medio y 2 Dificil.
    :return: No retorna nada
    '''
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


def puntaje(pantalla:pygame.Surface, contador_puntaje:int, ancho:int)->None:
    '''
    Funcion que muestra el puntaje actual del juego en la pantalla.
    :param pantalla: Recibe la pantalla donde se va a renderizar el puntaje.
    :param contador_puntaje: Recibe el puntaje actual del juego a mostrar.
    :param ancho: Recibe el ancho de la pantalla para ajustar el puntaje.
    :return: Retorna None
    '''
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render(f"Puntaje: {str(contador_puntaje).zfill(4)}", True, NEGRO)
    rect = texto.get_rect(center=(ancho - 60, 25))
    pygame.draw.rect(pantalla, GRIS, rect.inflate(20, 10))  # Fondo del botón
    pantalla.blit(texto, rect)
    return None

def mostrar_menu(pantalla:pygame.Surface) ->Tuple[str, int]:
    '''
    Funcion que crea y muestra el menu principal del juego
    :param pantalla: Recibe por parametro la pantalla
    :return: Retorna una tupla con la pantalla a la que quiere dirigirse el jugador y el indice de nivel que seteo previamente.
    '''
    pantalla_retorno = "salir"
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

            if hover:
                color_borde = BLANCO
            else:
                color_borde = NEGRO

            pygame.draw.rect(pantalla, color_fondo, fondo_rect)
            pygame.draw.rect(pantalla, color_borde, fondo_rect, 2)

            # Dibujar texto del botón
            pantalla.blit(texto_renderizado, texto_rect)
            botones_rect.append(fondo_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                pantalla_retorno = "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botones_rect[0].collidepoint(evento.pos):
                    run = False
                    pantalla_retorno = "jugar"
                elif botones_rect[1].collidepoint(evento.pos):
                    indice_nivel = (indice_nivel + 1) % len(niveles)
                elif botones_rect[2].collidepoint(evento.pos):
                    run = False
                    pantalla_retorno = "puntajes"
                elif botones_rect[3].collidepoint(evento.pos):
                    run = False
                    pantalla_retorno = "salir"
        pygame.display.flip()
    return pantalla_retorno, indice_nivel

def main()->None:
    '''
    Funcion principal del juego, crea la pantalla con el ANCHO y ALTO definido por constante,
    Define el diccionario de las celdas y maneja el flujo entre diferentes pantallas.
    :return: No retorna nada.
    '''
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pantalla_actual = "menu"
    indice_nivel = 0
    celda = {
        "hay_mina": False,
        "revelada": False,
        "flag": False,
        "minas_adyacentes": 0
    }
    while pantalla_actual != "salir":
        if pantalla_actual == "menu":
            respuesta = mostrar_menu(pantalla)
            pantalla_actual, indice_nivel = respuesta
        elif pantalla_actual == "jugar":
            iniciar_juego(celda, indice_nivel)
            pantalla_actual = "menu"
        elif pantalla_actual == "puntajes":
            pantalla_actual = mostrar_puntajes(pantalla, PATH_ARCHIVO_PUNTAJES)
    pygame.quit()


