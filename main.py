#main del juego
import pygame
from personaje import Jugador
from bala import Bala



pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla    = pygame.display.set_mode((800,600))
reloj       = pygame.time.Clock()

jugador = Jugador("Isaac",3,5,1,None,100,100,100)
balas   =[]

Ejecutando =  True

while Ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Ejecutando = False
    
    keys = pygame.key.get_pressed()
    jugador.Moverse(keys)
    
    if keys[pygame.K_RIGHT]:
        balas.append(Bala(jugador.x,jugador.y,1,0))
    
    pantalla.fill((0,0,0)) 
    jugador.Dibujo(pantalla)
    
    for bala in balas:
        bala.Trayectoria()
        bala.Dibujar(pantalla)
    pygame.display.flip()
        

pygame.quit()


    
    

 