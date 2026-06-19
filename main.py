# main.py
import pygame
import pygame_gui
import os
import sys
from audio import AudioManager
import escenas  

# Definimos la resolución considerando los 600px fijos de la sala + 75px del HUD superior
resolucion = (800, 675)  

# Inicializamos el juego
pygame.init()
pygame.display.set_caption("Isaac TP Final")

# Instanciamos la pantalla expandida y el reloj
pantalla = pygame.display.set_mode(resolucion)
reloj = pygame.time.Clock()
Ejecutando = True

# ----------------- RUTAS DE ASSETS ----------------
ruta_base = os.path.dirname(__file__)
ruta_sonidos = os.path.join(ruta_base, "sonidos")
ruta_themes = os.path.join(ruta_base, "config", "theme.json")  # Configuración estética
ruta_fuente = os.path.join(ruta_base, "fuentes", "fuente_isaac.ttf")

# ----------------- INSTANCIAS DE MANAGERS EXTERNOS -----------------
audio_manager = AudioManager(ruta_sonidos)
ui_manager = pygame_gui.UIManager(resolucion)

# Cargamos la tipografía a usar
if os.path.exists(ruta_fuente):
    ui_manager.add_font_paths(font_name="fuente_isaac.ttf", regular_path=ruta_fuente)
    ui_manager.preload_fonts([
        {"name": "fuente_isaac.ttf", "size": 14}, 
        {"name": "fuente_isaac.ttf", "size": 16}
    ])
    if os.path.exists(ruta_themes):
        ui_manager.get_theme().load_theme(ruta_themes)

scene_manager = escenas.SceneManager(pantalla, resolucion, audio_manager, ui_manager, ruta_themes, ruta_fuente)
scene_manager.cambiar_escena(escenas.EscenaMenu(scene_manager))

# =====================[BUCLE ÚNICO DEL JUEGO]======================================
while Ejecutando:
    time_delta = reloj.tick(60) / 1000.0
    tiempo_actual = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    scene_manager.actualizar(time_delta, tiempo_actual, keys)
    scene_manager.dibujar()
    pygame.display.flip()

pygame.quit()