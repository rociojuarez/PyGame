import pygame
import sys
from lib import *

# Inicializa Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas")

# Cargar imagen de fondo y sonido
pygame.mixer.music.load("./assets/music.mp3")
pygame.mixer.music.play(-1)  # Repetir la música


if __name__ == "__main__":
    main(pantalla)
