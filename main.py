# main.py
import pygame
import pygame_gui
import os
from audio import AudioManager
import escenas

# Ajustes graficos: 
resolucion = (800, 720) 


pygame.init()
pygame.display.set_caption("Isaac TP Final")


pantalla = pygame.display.set_mode(resolucion)
reloj = pygame.time.Clock()
Ejecutando = True

ruta_base = os.path.dirname(__file__)
ruta_sonidos = os.path.join(ruta_base, "sonidos")
ruta_themes = os.path.join(ruta_base, "config", "theme.json")
ruta_fuente = os.path.join(ruta_base, "fuentes", "fuente_isaac.ttf")
ruta_icono = os.path.join(ruta_base, "imagenes", "menu", "icono.png")

audio_manager = AudioManager(ruta_sonidos)
ui_manager = pygame_gui.UIManager(resolucion)

if os.path.exists(ruta_fuente):
    ui_manager.add_font_paths(font_name="fuente_isaac.ttf", regular_path=ruta_fuente)
    if os.path.exists(ruta_themes):
        ui_manager.get_theme().load_theme(ruta_themes)
        

if os.path.exists(ruta_icono):
    icono = pygame.image.load(ruta_icono).convert_alpha()
    pygame.display.set_icon(icono)
    

scene_manager = escenas.SceneManager(pantalla, resolucion, audio_manager, ui_manager, ruta_themes, ruta_fuente)
scene_manager.cambiar_escena(escenas.EscenaMenu(scene_manager))

while Ejecutando:
    time_delta = reloj.tick(60) / 1000.0
    tiempo_actual = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    scene_manager.actualizar(time_delta, tiempo_actual, keys)
    scene_manager.dibujar()
    pygame.display.flip()

pygame.quit()   