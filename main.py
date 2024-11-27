from lib import *

# Inicializa Pygame
pygame.init()
pygame.display.set_caption("Buscaminas")

# Cargar sonido de canción
pygame.mixer.music.load("./assets/music.mp3")
pygame.mixer.music.play(-1)


main()
