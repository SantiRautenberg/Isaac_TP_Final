# escenas.py
import pygame
import pygame_gui
import os
import sys
from personaje import Jugador
from bala import Bala
from mapa import Mapa
from interfaz import Interfaz
from estadistica import Estadisticas

class SceneManager:
    def __init__(self, pantalla, resolucion, audio_manager, ui_manager, ruta_themes, ruta_fuente, alto_hud=75):
        self.pantalla = pantalla
        self.resolucion = resolucion
        self.audio_manager = audio_manager
        self.ui_manager = ui_manager
        self.ruta_themes = ruta_themes
        self.ruta_fuente = ruta_fuente
        self.alto_hud = alto_hud
        self.escena_actual = None

    def cambiar_escena(self, nueva_escena):
        self.escena_actual = nueva_escena
        self.escena_actual.inicializar()

    def actualizar(self, time_delta, tiempo_actual, keys):
        if self.escena_actual:
            self.escena_actual.actualizar(time_delta, tiempo_actual, keys)

    def dibujar(self):
        if self.escena_actual:
            self.escena_actual.dibujar()


# =====================[ESCENA: MENÚ PRINCIPAL]=======================================
class EscenaMenu:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.interfaz = None

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente, self.manager.alto_hud)
        self.interfaz.crear_menu_inicio()
        self.manager.audio_manager.reproducir_musica("musica_menu.mp3", volumen=0.2)

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.USEREVENT and hasattr(evento, 'user_type') and evento.user_type == pygame_gui.UI_BUTTON_PRESSED or evento.type == pygame.USEREVENT + 1:
                try:
                    if evento.ui_element == self.interfaz.boton_iniciar:
                        self.manager.audio_manager.detener_musica()
                        self.interfaz.destruir_menu_inicio()
                        self.manager.cambiar_escena(EscenaJuego(self.manager))
                    elif evento.ui_element == self.interfaz.boton_salir:
                        pygame.quit()
                        sys.exit()
                except AttributeError:
                    pass

            self.interfaz.manager.process_events(evento)
        self.interfaz.manager.update(time_delta)

    def dibujar(self):
        self.manager.pantalla.fill((20, 20, 30))
        self.interfaz.manager.draw_ui(self.manager.pantalla)


# =====================[ESCENA: PARTIDA JUGABLE]======================================
class EscenaJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.jugador = Jugador(200, 200)
        self.mapa = Mapa()
        self.balas = []
        self.delay_disparo = 500
        self.ultimo_disparo = 0

        # Reseteamos el puntaje global al iniciar una nueva partida
        Estadisticas.puntaje_final = 0

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente, self.manager.alto_hud)

    def revisar_cambio_sala(self):
        ancho_canvas = 800
        alto_canvas = 600
        margen = 15

        if self.jugador.rect.left <= 10:
            if 225 <= self.jugador.rect.centery <= 375 and self.mapa.cambiar_sala_por_direccion("IZQUIERDA"):
                self.jugador.x = ancho_canvas - self.jugador.dimensiones[0] - margen
            else:
                self.jugador.x = 10
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.right >= ancho_canvas:
            if 225 <= self.jugador.rect.centery <= 375 and self.mapa.cambiar_sala_por_direccion("DERECHA"):
                self.jugador.x = margen
            else:
                self.jugador.x = ancho_canvas - self.jugador.dimensiones[0]
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.top <= 0:
            if 325 <= self.jugador.rect.centerx <= 475 and self.mapa.cambiar_sala_por_direccion("ARRIBA"):
                self.jugador.y = alto_canvas - self.jugador.dimensiones[1] - margen
            else:
                self.jugador.y = 0
            self.jugador.rect.y = self.jugador.y

        elif self.jugador.rect.bottom >= alto_canvas:
            if 325 <= self.jugador.rect.centerx <= 475 and self.mapa.cambiar_sala_por_direccion("ABAJO"):
                self.jugador.y = margen
            else:
                self.jugador.y = alto_canvas - self.jugador.dimensiones[1]
            self.jugador.rect.y = self.jugador.y

    def actualizar(self, time_delta, tiempo_actual, keys):
        # Si Isaac se queda sin salud, salta a la pantalla de Game Over
        if self.jugador.get_vida() <= 0:
            self.manager.cambiar_escena(EscenaFinJuego(self.manager))
            return

        if keys[pygame.K_1]: self.mapa.cambiar_sala("comun_1")
        if keys[pygame.K_2]: self.mapa.cambiar_sala("comun_2")
        if keys[pygame.K_3]: self.mapa.cambiar_sala("tesoro")
        if keys[pygame.K_4]: self.mapa.cambiar_sala("boss")

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.manager.cambiar_escena(EscenaMenu(self.manager))
                return

        if keys[pygame.K_RIGHT] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 50, self.jugador.y + 25, 1, 0, daño=self.jugador.get_daño())
            self.balas.append(bala)
            self.jugador.direccion_actual = "DERECHA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_LEFT] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x, self.jugador.y + 25, -1, 0, daño=self.jugador.get_daño())
            self.balas.append(bala)
            self.jugador.direccion_actual = "IZQUIERDA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_UP] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y, 0, -1, daño=self.jugador.get_daño())
            self.balas.append(bala)
            self.jugador.direccion_actual = "ARRIBA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_DOWN] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y + 50, 0, 1, daño=self.jugador.get_daño())
            self.balas.append(bala)
            self.jugador.direccion_actual = "ABAJO"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        self.jugador.actualizar(self.manager.pantalla, keys, self.mapa)
        self.mapa.actualizar(self.manager.pantalla, self.jugador, self.balas)

        for bala in self.balas[:]:
            bala.actualizar(self.manager.pantalla)
            if bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:
                self.balas.remove(bala)

        self.revisar_cambio_sala()

    def dibujar(self):
        subsuperficie_juego = self.manager.pantalla.subsurface((0, self.manager.alto_hud, 800, 600))
        self.mapa.dibujar(subsuperficie_juego)
        self.jugador.dibujar(subsuperficie_juego)

        for bala in self.balas:
            bala.dibujar(subsuperficie_juego)

        self.interfaz.dibujar_hud_juego(self.manager.pantalla, self.jugador, self.mapa)


# =====================[ESCENA: FIN DEL JUEGO]=======================================
class EscenaFinJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.interfaz = None

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente, self.manager.alto_hud)
        self.interfaz.crear_pantalla_fin()
        self.manager.audio_manager.detener_musica()

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.USEREVENT and hasattr(evento, 'user_type') and evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                try:
                    if evento.ui_element == self.interfaz.boton_reiniciar:
                        self.interfaz.destruir_pantalla_fin()
                        self.manager.cambiar_escena(EscenaJuego(self.manager))

                    elif evento.ui_element == self.interfaz.boton_salir_fin:
                        pygame.quit()
                        sys.exit()
                except AttributeError:
                    pass

            self.interfaz.manager.process_events(evento)
        self.interfaz.manager.update(time_delta)

    def dibujar(self):
        self.manager.pantalla.fill((20, 10, 10))
        self.interfaz.manager.draw_ui(self.manager.pantalla)
