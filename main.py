import pygame
from personaje import Jugador
from bala import Bala


pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla = pygame.display.set_mode((800, 600))
reloj = pygame.time.Clock()

jugador = Jugador("Isaac", 3, 5, 1, None, 100, 100, 100)
balas = []

Ejecutando = True
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

    if keys[pygame.K_RIGHT] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x + 50, jugador.y + 50, 1, 0))
        jugador.direccion_actual = "DERECHA" # Fuerza a mirar al lado del disparo
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_LEFT] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x + 50, jugador.y + 50, -1, 0))
        jugador.direccion_actual = "IZQUIERDA"
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_UP] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, 0, -1))
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
        balas.append(Bala(jugador.x, jugador.y, 0, 1))
        ultimo_disparo = tiempo_actual
        
    # LIMPIADOR DE LA PANTALLA
    pantalla.fill((45, 55, 32))
    
    for bala in balas[:]:
        bala.Trayectoria()
        bala.Dibujar(pantalla)
        # Eliminar balas que salen de la pantalla
        if bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:
            balas.remove(bala)
            
    jugador.Dibujo(pantalla)
    pygame.display.flip()
        
pygame.quit()