#main del juego
import pygame
from personaje import Jugador



pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla    = pygame.display.set_mode((800,600))
reloj       = pygame.time.Clock()

jugador = Jugador("Isaac",3,5,1,100,100)

Ejecutando =  True

while Ejecutando:
    pass

pygame.quit()
    
    

 