#main del juego
import pygame
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo


pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla    = pygame.display.set_mode((800,600))
reloj       = pygame.time.Clock()

#----------------sets_del_personaje------------------------
jugador = Jugador("Isaac",3,5,1,None,100,100,100)
balas   =[]
#----------------------------------------------------------

#-------------------sets_de_enemigos-----------------------
enemigos = [
    Enemigo(400, 300),
    Enemigo(200, 150)
]
#----------------------------------------------------------

Ejecutando =  True
#--------------Variables de disparo para generar delay-----------------------------
delay_disparo = 500
ultimo_disparo = 0
#----------------------------------------------------------------------------------
while Ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Ejecutando = False
    
    keys = pygame.key.get_pressed()
    jugador.Moverse(keys)
        
    tiempo_actual = pygame.time.get_ticks()
    
    for enemigo in enemigos:
        enemigo.seguir_jugador(jugador)
        enemigo.colision_con_jugador(jugador)

#=====================[sets_teclas_disparo]==========================================
    if keys[pygame.K_RIGHT] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, 1, 0))
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_LEFT] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, -1, 0))
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_UP] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, 0, -1))
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, 0, 1))
        ultimo_disparo = tiempo_actual
    #================================================================================
    pantalla.fill((0,0,0)) 
    jugador.Dibujo(pantalla)
    
    
    
    
    #-------------------muestreo_pantalla-------------------------------
    for bala in balas:
        bala.Trayectoria()
        bala.Dibujar(pantalla)
        
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)
    pygame.display.flip()
    #-------------------------------------------------------------------  

pygame.quit()


    
    

 