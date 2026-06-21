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
from audio import AudioManager

# Variables de colores 
color_boton = (236, 220, 220)
color_boton_borde = (140, 124, 128)
color_texto = (92, 44, 52)
color_fondo = (20, 15, 15)
color_interaccion_boton = (195, 189, 180)

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
        self.fondo_menu = None
        self.rect_btn_iniciar = pygame.Rect(0, 0, 0, 0)
        self.rect_btn_salir = pygame.Rect(0, 0, 0, 0)
        
        # Variables para el fade out
        self.fading = False
        self.fade_alpha = 0

    def inicializar(self):
        self.manager.audio_manager.reproducir_musica("musica_menu.mp3", volumen=0.2)
        ruta_img = os.path.join(os.path.dirname(__file__), "imagenes", "menu", "menu_inicial.png")
        if os.path.exists(ruta_img):
            self.fondo_menu = pygame.image.load(ruta_img).convert_alpha()

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_btn_iniciar.collidepoint(pos_mouse) and not self.fading:
                    self.fading = True
                    AudioManager.stop_music()
                    AudioManager.play_sfx("iniciar_juego")
                elif self.rect_btn_salir.collidepoint(pos_mouse) and not self.fading:
                    pygame.quit()
                    sys.exit()

        # Agregue un fade out del menu al iniciar la partida
        if self.fading:
            self.fade_alpha += 300 * time_delta
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.manager.cambiar_escena(EscenaJuego(self.manager))
                return

        # Regulamos la iluminacion de los botones con el mouse
        pos_mouse = pygame.mouse.get_pos()

    def dibujar(self):
        self.manager.pantalla.fill((color_fondo))

        if self.fondo_menu:
            self.manager.pantalla.blit(self.fondo_menu, (0, 0))

        if os.path.exists(self.manager.ruta_fuente):
            fuente_menu = pygame.font.Font(self.manager.ruta_fuente, 20)
            fuente_titulo = pygame.font.Font(self.manager.ruta_fuente, 23)
        else:
            fuente_menu = pygame.font.SysFont("sans", 16, bold=True)
            fuente_titulo = pygame.font.SysFont("sans", 24, bold=True)

        # Cartel de presentacion rotado a -5° 
        surf_titulo = fuente_titulo.render("ISAAC ARGENTO v0.2", True, (color_texto))
        surf_titulo_rotada = pygame.transform.rotate(surf_titulo, -5)
        self.manager.pantalla.blit(surf_titulo_rotada, (295, 195))

        # Botones
        ancho_b, alto_b = 180, 40
        pos_mouse = pygame.mouse.get_pos()

        # Determinación de color dinámico para el botón JUGAR
        if self.rect_btn_iniciar.collidepoint(pos_mouse):
            color_fondo_jugar = color_interaccion_boton
        else:
            color_fondo_jugar = color_boton

        # Determinación de color dinámico para el botón SALIR
        if self.rect_btn_salir.collidepoint(pos_mouse):
            color_fondo_salir = color_interaccion_boton
        else:
            color_fondo_salir = color_boton

        # Botón superior: JUGAR
        surf_btn1 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn1, (color_fondo_jugar), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn1, (color_boton_borde), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn1 = fuente_menu.render("JUGAR", True, (color_texto))
        surf_btn1.blit(texto_btn1, texto_btn1.get_rect(center=(ancho_b // 2, alto_b // 2)))

        # Botón inferior: SALIR
        surf_btn2 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn2, (color_fondo_salir), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn2, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn2 = fuente_menu.render("SALIR", True, (color_texto))
        surf_btn2.blit(texto_btn2, texto_btn2.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn1_rotado = pygame.transform.rotate(surf_btn1, -5)
        surf_btn2_rotado = pygame.transform.rotate(surf_btn2, -5)

        # ----------------- CALIBRACIÓN VERTICAL INDEPENDIENTE -----------------
        pos_b1_x, pos_b1_y = 305, 330 
        pos_b2_x, pos_b2_y = 313, 410  

        # hitbox del boton ajustadas
        self.rect_btn_iniciar = surf_btn1_rotado.get_rect(topleft=(pos_b1_x, pos_b1_y))
        self.rect_btn_salir = surf_btn2_rotado.get_rect(topleft=(pos_b2_x, pos_b2_y))

        self.manager.pantalla.blit(surf_btn1_rotado, (pos_b1_x, pos_b1_y))
        self.manager.pantalla.blit(surf_btn2_rotado, (pos_b2_x, pos_b2_y))

        # Agregue un fade out del menu
        if self.fade_alpha > 0:
            surf_fade = pygame.Surface(self.manager.resolucion)
            surf_fade.fill((0, 0, 0))
            surf_fade.set_alpha(int(self.fade_alpha))
            self.manager.pantalla.blit(surf_fade, (0, 0))


# =====================[ESCENA: PARTIDA JUGABLE]======================================
class EscenaJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.jugador = Jugador(200, 200)
        self.mapa = Mapa()
        self.balas_jugador = []
        self.balas_enemigos = []
        self.delay_disparo = 500
        self.ultimo_disparo = 0

        # Reseteamos el puntaje global al iniciar una nueva partida
        Estadisticas.puntaje_final = 0

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente, self.manager.alto_hud)
        AudioManager.play_music("musica_fondo.mp3", volumen=0.05)
        
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
            self.balas_jugador.append(bala)
            self.jugador.direccion_actual = "DERECHA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_LEFT] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x, self.jugador.y + 25, -1, 0, daño=self.jugador.get_daño())
            self.balas_jugador.append(bala)
            self.jugador.direccion_actual = "IZQUIERDA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_UP] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y, 0, -1, daño=self.jugador.get_daño())
            self.balas_jugador.append(bala)
            self.jugador.direccion_actual = "ARRIBA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_DOWN] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y + 50, 0, 1, daño=self.jugador.get_daño())
            self.balas_jugador.append(bala)
            self.jugador.direccion_actual = "ABAJO"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        self.jugador.actualizar(self.manager.pantalla, keys, self.mapa)
        self.mapa.actualizar(self.manager.pantalla, self.jugador, self.balas_enemigos)

        # Control de choques de las lagrimas
        for bala in self.balas_jugador[:]:
            bala.actualizar(self.manager.pantalla)
            rect_bala = pygame.Rect(bala.x, bala.y, 12, 12)
            bala_eliminada = False

            # ======================================
            # COLISIÓN BALA VS ENEMIGOS
            # ======================================
            sala_actual = self.mapa.piso_actual.sala_actual

            for enemigo in sala_actual.enemigos[:]:
                if rect_bala.colliderect(enemigo.rect):

                    enemigo.recibir_dano(bala.daño)
                    Estadisticas.sumar_balas_efectivas()

                    AudioManager.play_sfx("lagrima_impacto")

                    if bala in self.balas_jugador:
                        self.balas_jugador.remove(bala)
                    bala_eliminada = True

                    # enemigo muerto
                    if enemigo.vida <= 0:
                        Estadisticas.sumar_enemigos_asesinados("Mosca")
                        sala_actual.enemigos.remove(enemigo)

                    break

            if bala_eliminada:
                continue

            # ======================================
            # COLISIÓN CON PAREDES
            # ======================================
            if self.mapa.colision(rect_bala):

                if bala in self.balas_jugador:
                    self.balas_jugador.remove(bala)
                AudioManager.play_sfx("lagrima_impacto")

            # ======================================
            # FUERA DE PANTALLA
            # ======================================
            elif bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:

                if bala in self.balas_jugador:
                    self.balas_jugador.remove(bala)

        self.revisar_cambio_sala()


        for bala in self.balas_enemigos[:]:
            bala.actualizar(self.manager.pantalla)
            rect_bala = pygame.Rect(bala.x, bala.y, 12, 12)
            # choque contra jugador
            if rect_bala.colliderect(self.jugador.rect):
               self.jugador.recibirDaño(bala.daño)
               Estadisticas.sumar_balas_enemigo_impactadas()
               self.balas_enemigos.remove(bala)
            # choque con paredes
            elif self.mapa.colision(rect_bala):
                self.balas_enemigos.remove(bala)
            # fuera de pantalla
            elif bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:
                self.balas_enemigos.remove(bala)
        self.revisar_cambio_sala()

    def dibujar(self):
        subsuperficie_juego = self.manager.pantalla.subsurface((0, self.manager.alto_hud, 800, 600))
        self.mapa.dibujar(subsuperficie_juego)
        self.jugador.dibujar(subsuperficie_juego)

        for bala in self.balas_jugador:
            bala.dibujar(subsuperficie_juego)

        for bala in self.balas_enemigos:
            bala.dibujar(subsuperficie_juego)

        self.interfaz.dibujar_hud_juego(self.manager.pantalla, self.jugador, self.mapa)


# =====================[ESCENA: FIN DEL JUEGO]=======================================
class EscenaFinJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.fondo_endgame = None
        self.rect_btn_reiniciar = pygame.Rect(0, 0, 0, 0)
        self.rect_btn_salir = pygame.Rect(0, 0, 0, 0)
        
        # Variables para el fade out
        self.fading = False
        self.fade_alpha = 0

    def inicializar(self):
        AudioManager.stop_music()
        ruta_img = os.path.join(os.path.dirname(__file__), "imagenes", "menu", "menu_endgame.png")
        if os.path.exists(ruta_img):
            self.fondo_endgame = pygame.image.load(ruta_img).convert_alpha()

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_btn_reiniciar.collidepoint(pos_mouse) and not self.fading:
                    self.fading = True
                    AudioManager.stop_music()
                    AudioManager.play_sfx("jugar_de_nuevo")
                elif self.rect_btn_salir.collidepoint(pos_mouse) and not self.fading:
                    pygame.quit()
                    sys.exit()

        # Agregue un fade out del menu al reiniciar la partida
        if self.fading:
            self.fade_alpha += 300 * time_delta
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.manager.cambiar_escena(EscenaJuego(self.manager))
                return

    def dibujar(self):
        self.manager.pantalla.fill((20, 15, 15))

        if self.fondo_endgame:
            self.manager.pantalla.blit(self.fondo_endgame, (0, 0))

        if os.path.exists(self.manager.ruta_fuente):
            fuente_fin = pygame.font.Font(self.manager.ruta_fuente, 20)
        else:
            fuente_fin = pygame.font.SysFont("sans", 18, bold=True)

        # Subsuperficie para puntos
        surf_puntos = fuente_fin.render(str(Estadisticas.puntaje_final), True, (color_texto))
        surf_puntos_rotada = pygame.transform.rotate(surf_puntos, -5)
        self.manager.pantalla.blit(surf_puntos_rotada, (355, 455))

        # Botones
        ancho_b, alto_b = 180, 40
        pos_mouse = pygame.mouse.get_pos()

        # Determinación de color dinámico para el botón de reiniciar (Fin del juego)
        if self.rect_btn_reiniciar.collidepoint(pos_mouse):
            color_fondo_reiniciar = color_interaccion_boton
        else:
            color_fondo_reiniciar = color_boton

        # Determinación de color dinámico para el botón de salir (Fin del juego)
        if self.rect_btn_salir.collidepoint(pos_mouse):
            color_fondo_salir_fin = color_interaccion_boton
        else:
            color_fondo_salir_fin = color_boton

        # Botón izquierdo: Jugar nuevamente
        surf_btn1 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn1, (color_fondo_reiniciar), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn1, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn1 = fuente_fin.render("Volver a Jugar", True, (color_texto))
        surf_btn1.blit(texto_btn1, texto_btn1.get_rect(center=(ancho_b // 2, alto_b // 2)))

        # Botón derecho: Salir del juego
        surf_btn2 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn2, (color_fondo_salir_fin), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn2, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn2 = fuente_fin.render("Salir del juego", True, (color_texto))
        surf_btn2.blit(texto_btn2, texto_btn2.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn1_rotado = pygame.transform.rotate(surf_btn1, -5)
        surf_btn2_rotado = pygame.transform.rotate(surf_btn2, -5)

        # Posicionamiento ajustado con la hoja 
        pos_b1_x, pos_b1_y = 175, 489
        pos_b2_x, pos_b2_y = 370, 507

        # hitbox del boton ajustadas
        self.rect_btn_reiniciar = surf_btn1_rotado.get_rect(topleft=(pos_b1_x, pos_b1_y))
        self.rect_btn_salir = surf_btn2_rotado.get_rect(topleft=(pos_b2_x, pos_b2_y))

        self.manager.pantalla.blit(surf_btn1_rotado, (pos_b1_x, pos_b1_y))
        self.manager.pantalla.blit(surf_btn2_rotado, (pos_b2_x, pos_b2_y))

        # Agregue un fade out del menu
        if self.fade_alpha > 0:
            surf_fade = pygame.Surface(self.manager.resolucion)
            surf_fade.fill((0, 0, 0))
            surf_fade.set_alpha(int(self.fade_alpha))
            self.manager.pantalla.blit(surf_fade, (0, 0))