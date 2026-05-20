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
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento == pygame.QUIT:
            Ejecutando = False
    
    
    keys = pygame.key.get_pressed()
    jugador.Moverse(keys)
    
    pantalla.fill((0,0,0))
    jugador.Dibujo(pantalla)
    pygame.display.flip()
        

pygame.quit()

#commit de muestra
    
    

 