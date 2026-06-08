import pygame
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo

# MAIN SIN LISTA BALAS !

pygame.init()
#instancio la pantalla, el jugador y el clock

pantalla = pygame.display.set_mode((800, 600))
reloj = pygame.time.Clock()

#----------------sets_del_personaje------------------------
jugador = Jugador("Isaac", 3, 5, 1, None, 100, 100, 100)
#----------------------------------------------------------

#-------------------sets_de_enemigos-----------------------
enemigos = [
    Enemigo(400, 300),
    Enemigo(200, 150)
]
#------------------LISTA GENERAL---------------------------
# Concateno las listas para poder iterar luego
entidades = [jugador] + enemigos
#----------------------------------------------------------

Ejecutando = True
#--------------Variables de disparo para generar delay-----------------------------
delay_disparo = 500
ultimo_disparo = 0
try:
    while Ejecutando:

        reloj.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                Ejecutando = False
        
        keys = pygame.key.get_pressed()
            
        tiempo_actual = pygame.time.get_ticks()

        #=====================[sets_teclas_disparo]==========================================
        if keys[pygame.K_RIGHT] and tiempo_actual - ultimo_disparo > delay_disparo:
            entidades.append(Bala(jugador.x + 50, jugador.y + 50, 1, 0))
            jugador.direccion_actual = "DERECHA" # Fuerza a mirar al lado del disparo
            ultimo_disparo = tiempo_actual

        elif keys[pygame.K_LEFT] and tiempo_actual - ultimo_disparo > delay_disparo:
            entidades.append(Bala(jugador.x + 50, jugador.y + 50, -1, 0))
            jugador.direccion_actual = "IZQUIERDA"
            ultimo_disparo = tiempo_actual

        elif keys[pygame.K_UP] and tiempo_actual - ultimo_disparo > delay_disparo:
            entidades.append(Bala(jugador.x, jugador.y, 0, -1))
            ultimo_disparo = tiempo_actual

        elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
            entidades.append(Bala(jugador.x, jugador.y, 0, 1))
            ultimo_disparo = tiempo_actual

        #-------------------- DICCIONARIO ARGUMENTOS --------------------
        # Para usar en actualizar
        dic_args = {Jugador: [pantalla, keys],
                    Enemigo: [pantalla, jugador],
                    Bala: [pantalla]
                    }
            
        # LIMPIADOR DE LA PANTALLA
        pantalla.fill((45, 55, 32))
        
        #-------------------- ACTUALIZA LISTA GENERAL --------------------
        for entidad in entidades[:]:
            # Obtengo argumentos
            args = dic_args[type(entidad)]
            entidad.actualizar(*args)

            # Eliminar balas que salen de la pantalla
            if isinstance(entidad,Bala):
                if entidad.x < 0 or entidad.x > 800 or entidad.y < 0 or entidad.y > 600:
                    entidades.remove(entidad)

        pygame.display.flip()

except Exception as e:
    print(e)

finally:
    pygame.quit()