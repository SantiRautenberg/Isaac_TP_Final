import pygame
import pygame_gui
import os
import sys
# Importar las clases desde sus respectivos archivos
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo

resolucion = (800, 600)  # Resolución de la pantalla

# Inicializamos el juego y el gestor de interfaces
pygame.init()
pygame.display.set_caption("Isaac TP Final")
manager = pygame_gui.UIManager((resolucion))

# instancio la pantalla, el jugador y el reloj
pantalla = pygame.display.set_mode((resolucion))
reloj = pygame.time.Clock()
Ejecutando = True

# ----------------- RUTAS DE ASSETS ----------------
ruta_base = os.path.dirname(__file__)
ruta_imagenes = os.path.join(ruta_base, "imagenes", "jugador")
ruta_sonidos = os.path.join(ruta_base, "sonidos")

# -----------------sets_de_audio_y_menu---------------------
en_menu = True  # Estado inicial que determina el bucle activo
archivo_audio = os.path.join(ruta_sonidos, "musica_menu.mp3")

# Valida y carga la música de fondo en bucle para el menú desde la carpeta sonidos
if os.path.exists(archivo_audio):
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
else:
    print(f"[Aviso] No se encontró el archivo de audio en: {archivo_audio}")

# -----------------CREACION COMPONENTES UI------------------
titulo_texto = "ISAAC ARGENTO v0.1"
label_titulo = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((resolucion[0] // 2 - 200, 100), (400, 50)),
    text=titulo_texto,
    manager=manager
)

# Botones principales
boton_iniciar = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((resolucion[0] // 2 - 100, 250), (200, 50)),
    text="Iniciar juego",
    manager=manager
)

boton_salir = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((resolucion[0] // 2 - 100, 330), (200, 50)),
    text="Salir del juego",
    manager=manager
)

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


# =====================[BUCLE PRINCIPAL DEL MENU]===================================
while en_menu:
    time_delta = reloj.tick(60) / 1000.0
    pantalla.fill((20, 20, 30)) # Fondo oscuro espacial para la UI de inicio

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verifica si se toco un boton
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == boton_iniciar:
                pygame.mixer.music.stop()
                # Los botones hay que matarlos para liberar la memoria
                label_titulo.kill()
                boton_iniciar.kill()
                boton_salir.kill()
                en_menu = False # Rompe el ciclo del menú y permite el paso al juego

            elif evento.ui_element == boton_salir:
                pygame.quit()
                sys.exit()
        manager.process_events(evento)

    manager.update(time_delta)
    manager.draw_ui(pantalla)
    pygame.display.flip()

# =====================[BUCLE PRINCIPAL DE LA PARTIDA]==============================
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
        jugador.direccion_actual = "IZQUIERDA"  # Fuerza a mirar al lado del disparo
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_UP] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x, jugador.y, 0, -1)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "ARRIBA"  # Fuerza a mirar al lado del disparo
        ultimo_disparo = tiempo_actual

    elif keys[pygame.K_DOWN] and tiempo_actual - ultimo_disparo > delay_disparo:
        bala = Bala(jugador.x, jugador.y, 0, 1)
        balas.append(bala)
        entidades.append(bala)
        jugador.direccion_actual = "ABAJO"  # Fuerza a mirar al lado del disparo
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