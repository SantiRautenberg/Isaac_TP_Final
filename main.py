import pygame
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo
from mapa import Mapa

pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla = pygame.display.set_mode((800, 600))
reloj = pygame.time.Clock()

#----------------sets_del_personaje------------------------
jugador = Jugador("Isaac", 3, 5, 1, None, 100, 100, 100)
mapa = Mapa()
balas = []
#----------------------------------------------------------

#-------------------sets_de_enemigos-----------------------
enemigos = [
    Enemigo(400, 300),
    Enemigo(200, 150)
]

#------------------LISTA GENERAL---------------------------
entidades = [jugador] + enemigos + balas
#----------------------------------------------------------

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
        
    tiempo_actual = pygame.time.get_ticks()

    #=====================[sets_teclas_disparo]==========================================
    if keys[pygame.K_RIGHT] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x + 50, jugador.y + 50, 1, 0)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "DERECHA" # Fuerza a mirar al lado del disparo
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_LEFT] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x + 50, jugador.y + 50, -1, 0)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "IZQUIERDA"
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_UP] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x, jugador.y, 0, -1)
        balas.append(bala)
        entidades.append(bala)
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x, jugador.y, 0, 1)
        balas.append(bala)
        entidades.append(bala)
        ultimo_disparo = tiempo_actual
        
    #-------------------- DICCIONARIO ARGUMENTOS --------------------
    # Para usar en actualizar
    dic_args = {
        Jugador: [pantalla, keys, mapa],
        Enemigo: [pantalla, jugador],
        Bala: [pantalla]
    }
   
    # LIMPIADOR DE LA PANTALLA
    mapa.actualizar(pantalla)
    mapa.dibujar(pantalla)
    
    #-------------------- ACTUALIZA LISTA GENERAL --------------------
    for entidad in entidades[:]:

        args = dic_args[type(entidad)]
        entidad.actualizar(*args)

        # Eliminar balas que salen de la pantalla
        if isinstance(entidad,Bala):
            if entidad.x < 0 or entidad.x > 800 or entidad.y < 0 or entidad.y > 600:
                # Sincronizo ambas listas, mantengo balas para otras funciones
                balas.remove(entidad)
                entidades.remove(entidad)

    pygame.display.flip()

pygame.quit()