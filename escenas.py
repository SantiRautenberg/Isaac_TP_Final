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
        self.fondo_endgame = None
        self.rect_btn_reiniciar = pygame.Rect(0, 0, 0, 0)
        self.rect_btn_salir = pygame.Rect(0, 0, 0, 0)

    def inicializar(self):
        self.manager.audio_manager.detener_musica()
        # NUEVA RUTA SOLICITADA: imagenes -> menu -> endgame screen.png
        ruta_img = os.path.join(os.path.dirname(__file__), "imagenes", "menu", "endgame screen.png")
        if os.path.exists(ruta_img):
            self.fondo_endgame = pygame.image.load(ruta_img).convert_alpha()

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_btn_reiniciar.collidepoint(pos_mouse):
                    self.manager.cambiar_escena(EscenaJuego(self.manager))
                    return
                elif self.rect_btn_salir.collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()

    def dibujar(self):
        self.manager.pantalla.fill((20, 15, 15))
        y_offset = (self.manager.resolucion[1] - 600) // 2

        if self.fondo_endgame:
            self.manager.pantalla.blit(self.fondo_endgame, (0, y_offset))

        if os.path.exists(self.manager.ruta_fuente):
            fuente_fin = pygame.font.Font(self.manager.ruta_fuente, 20)
        else:
            fuente_fin = pygame.font.SysFont("sans", 20, bold=True)

        # Renderizamos e inclinamos 6° horarios (-6) el valor numérico del puntaje al lado de la palabra
        surf_puntos = fuente_fin.render(str(Estadisticas.puntaje_final), True, (75, 75, 75))
        surf_puntos_rotada = pygame.transform.rotate(surf_puntos, -6)
        self.manager.pantalla.blit(surf_puntos_rotada, (380, y_offset + 410))

        # Construcción de los botones interactivos e inclinados a -6°
        ancho_b, alto_b = 210, 45

        # Botón izquierdo: Jugar nuevamente
        surf_btn1 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn1, (116, 172, 223), (0, 0, ancho_b, alto_b), border_radius=4)
        pygame.draw.rect(surf_btn1, (255, 255, 255), (0, 0, ancho_b, alto_b), 2, border_radius=4)
        texto_btn1 = fuente_fin.render("Jugar nuevamente", True, (10, 20, 40))
        surf_btn1.blit(texto_btn1, texto_btn1.get_rect(center=(ancho_b // 2, alto_b // 2)))

        # Botón derecho: Salir del juego
        surf_btn2 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn2, (116, 172, 223), (0, 0, ancho_b, alto_b), border_radius=4)
        pygame.draw.rect(surf_btn2, (255, 255, 255), (0, 0, ancho_b, alto_b), 2, border_radius=4)
        texto_btn2 = fuente_fin.render("Salir del juego", True, (10, 20, 40))
        surf_btn2.blit(texto_btn2, texto_btn2.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn1_rotado = pygame.transform.rotate(surf_btn1, -6)
        surf_btn2_rotado = pygame.transform.rotate(surf_btn2, -6)

        # Posicionamiento calibrado según la pendiente de la hoja arrugada
        pos_b1_x, pos_b1_y = 175, y_offset + 490
        pos_b2_x, pos_b2_y = 415, y_offset + 515

        # Almacenamos las hitboxes rotadas expandidas para colisiones perfectas de mouse
        self.rect_btn_reiniciar = surf_btn1_rotado.get_rect(topleft=(pos_b1_x, pos_b1_y))
        self.rect_btn_salir = surf_btn2_rotado.get_rect(topleft=(pos_b2_x, pos_b2_y))

        self.manager.pantalla.blit(surf_btn1_rotado, (pos_b1_x, pos_b1_y))
        self.manager.pantalla.blit(surf_btn2_rotado, (pos_b2_x, pos_b2_y))