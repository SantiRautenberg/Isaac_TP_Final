import pygame
import pygame_gui
# Importar las clases desde sus respectivos archivos
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo

resolucion = (800, 600)  # Resolución de la pantalla

# Inicializamos el juego y el gestor de interfaces
pygame.init()
pygame.display.set_caption("Isaac TP Final")
manager = pygame_gui.UIManager((resolucion))

# instancio la pantalla, el jugador y el clock
pantalla = pygame.display.set_mode((resolucion))
reloj = pygame.time.Clock()
Ejecutando = True

# ----------------sets_del_personaje------------------------
jugador = Jugador("Isaac", 3, 5, 1, None, 100, 100, 100)
balas = []
# -------------------sets_de_enemigos-----------------------
enemigos = [Enemigo(400, 300), Enemigo(200, 150)]
# ------------------LISTA GENERAL---------------------------
entidades = [jugador] + enemigos + balas
# --------------Variables de disparo para generar delay-----------------------------
delay_disparo = 500
ultimo_disparo = 0
# ----------------------------------------------------------------------------------
while Ejecutando:
    time_delta = reloj.tick(60) / 1000.0
    tiempo_actual = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    
    pantalla.fill((45, 55, 32))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Ejecutando = False
        manager.process_events(evento)
        
    manager.update(time_delta)

    jugador.moverse(keys)

    for enemigo in enemigos:
        enemigo.seguir_jugador(jugador)
        enemigo.colision_con_jugador(jugador)
        
# =====================[sets_teclas_disparo]==========================================
    if keys[pygame.K_RIGHT] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x + 50, jugador.y + 50, 1, 0)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "DERECHA"  # Fuerza a mirar al lado del disparo
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
        jugador.direccion_actual = "ARRIBA"
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x, jugador.y, 0, 1)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "ABAJO"
        ultimo_disparo = tiempo_actual

#-------------------- DICCIONARIO ARGUMENTOS --------------------
    # Para usar en actualizar
    dic_args = {Jugador: [pantalla, keys],
                Enemigo: [pantalla, jugador],
                Bala: [pantalla]
                }
#-------------------- ACTUALIZA LISTA GENERAL --------------------
# Dibuja todas las entidades en pantalla por polimorfismo
    for entidad in entidades[:]:
        # Obtengo argumentos
        args = dic_args[type(entidad)]
        entidad.actualizar(*args)
        entidad.dibujar(pantalla)
        if isinstance(entidad, Bala):
            if entidad.x < 0 or entidad.x > 800 or entidad.y < 0 or entidad.y > 600:
                if entidad in balas:
                    balas.remove(entidad)
                entidades.remove(entidad)
                
    # Renderiza UI después de actualizar para que esté por encima de todo
    manager.draw_ui(pantalla)
    pygame.display.flip()

pygame.quit()
