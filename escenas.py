# escenas.py
import pygame
import pygame_gui
import os
import sys
import json
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
    def __init__(self, pantalla, resolucion, audio_manager, ui_manager, ruta_themes, ruta_fuente, alto_hud=120):
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
        self.rect_btn_puntajes = pygame.Rect(0, 0, 0, 0)
        self.rect_btn_salir = pygame.Rect(0, 0, 0, 0)

        # Variables para el fade out
        self.fading = False
        self.fade_alpha = 0

    def inicializar(self):
        AudioManager.play_music("musica_menu.mp3", volumen=0.2)
        ruta_img = os.path.join(os.path.dirname(__file__), "imagenes", "menu", "menu_inicial.png")
        if os.path.exists(ruta_img):
            imagen_original = pygame.image.load(ruta_img).convert_alpha()
            self.fondo_menu = pygame.transform.scale(imagen_original, self.manager.resolucion)

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
                elif self.rect_btn_puntajes.collidepoint(pos_mouse) and not self.fading:
                    AudioManager.play_sfx("lagrima_impacto")
                    self.manager.cambiar_escena(EscenaPuntajes(self.manager))
                    return
                elif self.rect_btn_salir.collidepoint(pos_mouse) and not self.fading:
                    pygame.quit()
                    sys.exit()

        if self.fading:
            self.fade_alpha += 300 * time_delta
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.manager.cambiar_escena(EscenaJuego(self.manager))
                return

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

        surf_titulo = fuente_titulo.render("ISAAC ARGENTO v0.2", True, (color_texto))
        surf_titulo_rotada = pygame.transform.rotate(surf_titulo, -5)
        self.manager.pantalla.blit(surf_titulo_rotada, (295, 195))

        ancho_b, alto_b = 180, 40
        pos_mouse = pygame.mouse.get_pos()

        # Cambios estéticos reactivos al pasar el mouse por encima
        color_fondo_jugar = color_interaccion_boton if self.rect_btn_iniciar.collidepoint(pos_mouse) else color_boton
        color_fondo_puntajes = color_interaccion_boton if self.rect_btn_puntajes.collidepoint(pos_mouse) else color_boton
        color_fondo_salir = color_interaccion_boton if self.rect_btn_salir.collidepoint(pos_mouse) else color_boton

        # Botón 1: JUGAR
        surf_btn1 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn1, color_fondo_jugar, (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn1, color_boton_borde, (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn1 = fuente_menu.render("JUGAR", True, color_texto)
        surf_btn1.blit(texto_btn1, texto_btn1.get_rect(center=(ancho_b // 2, alto_b // 2)))

        # Botón 2: PUNTAJES
        surf_btn_p = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn_p, color_fondo_puntajes, (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn_p, color_boton_borde, (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn_p = fuente_menu.render("TOP 3 PUNTAJES", True, color_texto)
        surf_btn_p.blit(texto_btn_p, texto_btn_p.get_rect(center=(ancho_b // 2, alto_b // 2)))

        # Botón 3: SALIR
        surf_btn2 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn2, color_fondo_salir, (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn2, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn2 = fuente_menu.render("SALIR", True, color_texto)
        surf_btn2.blit(texto_btn2, texto_btn2.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn1_rotado = pygame.transform.rotate(surf_btn1, -5)
        surf_btn_p_rotado = pygame.transform.rotate(surf_btn_p, -5)
        surf_btn2_rotado = pygame.transform.rotate(surf_btn2, -5)

        pos_b1_x, pos_b1_y = 300, 310
        pos_bp_x, pos_bp_y = 308, 385
        pos_b2_x, pos_b2_y = 316, 460

        self.rect_btn_iniciar = surf_btn1_rotado.get_rect(topleft=(pos_b1_x, pos_b1_y))
        self.rect_btn_puntajes = surf_btn_p_rotado.get_rect(topleft=(pos_bp_x, pos_bp_y))
        self.rect_btn_salir = surf_btn2_rotado.get_rect(topleft=(pos_b2_x, pos_b2_y))

        self.manager.pantalla.blit(surf_btn1_rotado, (pos_b1_x, pos_b1_y))
        self.manager.pantalla.blit(surf_btn_p_rotado, (pos_bp_x, pos_bp_y))
        self.manager.pantalla.blit(surf_btn2_rotado, (pos_b2_x, pos_b2_y))

        if self.fade_alpha > 0:
            surf_fade = pygame.Surface(self.manager.resolucion)
            surf_fade.fill((0, 0, 0))
            surf_fade.set_alpha(int(self.fade_alpha))
            self.manager.pantalla.blit(surf_fade, (0, 0))

# =====================[ESCENA: TOP 3 PUNTAJES]=======================================
class EscenaPuntajes:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.rect_btn_volver = pygame.Rect(0, 0, 0, 0)
        self.lista_top_3 = []

    def inicializar(self):
        self.lista_top_3 = []
        ruta_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registro_partidas.json")
        if not os.path.exists(ruta_json):
            ruta_json = "registro_partidas.json"

        if os.path.exists(ruta_json):
            try:
                if os.path.getsize(ruta_json) > 0:
                    with open(ruta_json, "r", encoding="utf-8") as f:
                        datos = json.load(f)

                        # Procesamos el diccionario estructurado por marcas de tiempo
                        if isinstance(datos, dict):
                            puntajes = []
                            for info_partida in datos.values():
                                if isinstance(info_partida, dict) and "Puntaje" in info_partida:
                                    puntajes.append(int(info_partida["Puntaje"]))

                            puntajes.sort(reverse=True)
                            self.lista_top_3 = puntajes[:3]
            except Exception as e:
                print(f"[Error Leaderboard] Archivo vacío o estructura JSON inválida: {e}")

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Soporte para volver al menú con la tecla ESC
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.manager.cambiar_escena(EscenaMenu(self.manager))
                return

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_btn_volver.collidepoint(pos_mouse):
                    AudioManager.play_sfx("lagrima_impacto")
                    self.manager.cambiar_escena(EscenaMenu(self.manager))
                    return

    def dibujar(self):
        self.manager.pantalla.fill(color_boton)

        if os.path.exists(self.manager.ruta_fuente):
            fuente_titulo = pygame.font.Font(self.manager.ruta_fuente, 24)
            fuente_ranking = pygame.font.Font(self.manager.ruta_fuente, 20)
        else:
            fuente_titulo = pygame.font.SysFont("sans", 26, bold=True)
            fuente_ranking = pygame.font.SysFont("sans", 20, bold=True)

        surf_titulo = fuente_titulo.render("TOP 3 MEJORES PUNTAJES", True, color_texto)
        self.manager.pantalla.blit(surf_titulo, surf_titulo.get_rect(center=(400, 150)))

        y_puesto = 250
        etiquetas_podio = ["1° LUGAR:  ", "2° LUGAR:  ", "3° LUGAR:  "]

        # Dimensiones de las cajas individuales de puntuación
        ancho_caja, alto_caja = 340, 46
        colores_podio_claros = [(180, 135, 10), (95, 95, 95), (135, 85, 30)] # Oro, Plata y Bronce

        for i in range(3):
            if i < len(self.lista_top_3):
                texto_linea = f"{etiquetas_podio[i]}{self.lista_top_3[i]} PTS"
            else:
                texto_linea = f"{etiquetas_podio[i]}---"

            rect_caja = pygame.Rect(0, 0, ancho_caja, alto_caja)
            rect_caja.center = (400, y_puesto)

            pygame.draw.rect(self.manager.pantalla, (236, 220, 220), rect_caja, border_radius=4)
            pygame.draw.rect(self.manager.pantalla, color_boton_borde, rect_caja, 2, border_radius=4)

            # 4. Renderizamos y bliteamos el texto centrado exactamente adentro del recuadro
            surf_linea = fuente_ranking.render(texto_linea, True, colores_podio_claros[i])
            self.manager.pantalla.blit(surf_linea, surf_linea.get_rect(center=rect_caja.center))

            y_puesto += 65


        # Botón Volver
        ancho_b, alto_b = 180, 40
        pos_mouse = pygame.mouse.get_pos()
        color_btn_actual = color_interaccion_boton if self.rect_btn_volver.collidepoint(pos_mouse) else color_boton

        surf_btn = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn, color_btn_actual, (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn, color_boton_borde, (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn = fuente_ranking.render("VOLVER", True, color_texto)
        surf_btn.blit(texto_btn, texto_btn.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn_rotado = pygame.transform.rotate(surf_btn, 0)
        pos_x, pos_y = 310, 520
        self.rect_btn_volver = surf_btn_rotado.get_rect(topleft=(pos_x, pos_y))
        self.manager.pantalla.blit(surf_btn_rotado, (pos_x, pos_y))


# =====================[ESCENA: PARTIDA JUGABLE]======================================
class EscenaJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.jugador = Jugador(200, 200)
        self.mapa = Mapa()
        self.balas_jugador = [] # Corregido: Nombre unificado para evitar AttributeErrors
        self.balas_enemigos = []
        self.ultimo_disparo = 0

        # Variables de control para las transiciones entre pisos
        self.fading_piso = False
        self.fade_alpha_piso = 0

        Estadisticas.puntaje_final = 0

    def inicializar(self):
        AudioManager.stop_music()
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente, self.manager.alto_hud)
        AudioManager.play_music("musica_fondo.mp3", volumen=0.1)

    def sala_actual_limpia(self):
        if self.mapa.piso_actual and self.mapa.piso_actual.sala_actual:
            return len(self.mapa.piso_actual.sala_actual.enemigos) == 0
        return True

    def revisar_cambio_sala(self):
        ancho_canvas = 800
        alto_canvas = 600
        margen = 15
        puede_salir = self.sala_actual_limpia()

        if self.fading_piso:
            return

        if self.jugador.rect.left <= 10:
            if puede_salir and 225 <= self.jugador.rect.centery <= 375 and self.mapa.cambiar_sala_por_direccion("IZQUIERDA"):
                self.jugador.x = ancho_canvas - self.jugador.dimensiones[0] - margen
            else:
                self.jugador.x = 10
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.right >= ancho_canvas:
            if puede_salir and 225 <= self.jugador.rect.centery <= 375 and self.mapa.cambiar_sala_por_direccion("DERECHA"):
                self.jugador.x = margen
            else:
                self.jugador.x = ancho_canvas - self.jugador.dimensiones[0]
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.top <= 0:
            if puede_salir and 325 <= self.jugador.rect.centerx <= 475 and self.mapa.cambiar_sala_por_direccion("ARRIBA"):
                self.jugador.y = alto_canvas - self.jugador.dimensiones[1] - margen
            else:
                self.jugador.y = 0
            self.jugador.rect.y = self.jugador.y

        elif self.jugador.rect.bottom >= alto_canvas:
            if puede_salir and 325 <= self.jugador.rect.centerx <= 475 and self.mapa.cambiar_sala_por_direccion("ABAJO"):
                self.jugador.y = margen
            else:
                self.jugador.y = alto_canvas - self.jugador.dimensiones[1]
            self.jugador.rect.y = self.jugador.y

    def actualizar(self, time_delta, tiempo_actual, keys):
        if self.jugador.get_vida() <= 0:
            Estadisticas.puntaje_final = Estadisticas.calcular_puntaje(self.jugador)
            self.manager.cambiar_escena(EscenaFinJuego(self.manager))
            return

        if not self.fading_piso:
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

        if not self.fading_piso:
            if keys[pygame.K_RIGHT] and tiempo_actual - self.ultimo_disparo > self.jugador.get_delay_disparo():
                bala = Bala(self.jugador.x + 50, self.jugador.y + 25, 1, 0, daño=self.jugador.get_daño())
                self.balas_jugador.append(bala)
                self.jugador.direccion_actual = "DERECHA"
                AudioManager.play_sfx("disparo")
                self.ultimo_disparo = tiempo_actual
                Estadisticas.sumar_balas_disparadas()

            elif keys[pygame.K_LEFT] and tiempo_actual - self.ultimo_disparo > self.jugador.get_delay_disparo():
                bala = Bala(self.jugador.x, self.jugador.y + 25, -1, 0, daño=self.jugador.get_daño())
                self.balas_jugador.append(bala)
                self.jugador.direccion_actual = "IZQUIERDA"
                AudioManager.play_sfx("disparo")
                self.ultimo_disparo = tiempo_actual
                Estadisticas.sumar_balas_disparadas()

            elif keys[pygame.K_UP] and tiempo_actual - self.ultimo_disparo > self.jugador.get_delay_disparo():
                bala = Bala(self.jugador.x + 25, self.jugador.y, 0, -1, daño=self.jugador.get_daño())
                self.balas_jugador.append(bala)
                self.jugador.direccion_actual = "ARRIBA"
                AudioManager.play_sfx("disparo")
                self.ultimo_disparo = tiempo_actual
                Estadisticas.sumar_balas_disparadas()

            elif keys[pygame.K_DOWN] and tiempo_actual - self.ultimo_disparo > self.jugador.get_delay_disparo():
                bala = Bala(self.jugador.x + 25, self.jugador.y + 50, 0, 1, daño=self.jugador.get_daño())
                self.balas_jugador.append(bala)
                self.jugador.direccion_actual = "ABAJO"
                AudioManager.play_sfx("disparo")
                self.ultimo_disparo = tiempo_actual
                Estadisticas.sumar_balas_disparadas()

            self.jugador.actualizar(self.manager.pantalla, keys, self.mapa)

        self.mapa.actualizar(self.manager.pantalla, self.jugador, self.balas_enemigos)

        # Control de choques de las lagrimas del jugador
        for bala in self.balas_jugador[:]:
            bala.actualizar(self.manager.pantalla)
            rect_bala = pygame.Rect(bala.x, bala.y, 12, 12)
            bala_eliminada = False

            sala_actual = self.mapa.piso_actual.sala_actual

            for enemigo in sala_actual.enemigos[:]:
                if rect_bala.colliderect(enemigo.rect):
                    enemigo.recibir_dano(bala.daño)
                    Estadisticas.sumar_balas_efectivas()
                    AudioManager.play_sfx("lagrima_impacto")

                    if bala in self.balas_jugador:
                        self.balas_jugador.remove(bala)
                    bala_eliminada = True
                    break

            if bala_eliminada:
                continue

            if self.mapa.colision(rect_bala):
                if bala in self.balas_jugador:
                    self.balas_jugador.remove(bala)
                AudioManager.play_sfx("lagrima_impacto")
            elif bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:
                if bala in self.balas_jugador:
                    self.balas_jugador.remove(bala)

        # Control de choques de las balas enemigas
        for bala in self.balas_enemigos[:]:
            bala.actualizar(self.manager.pantalla)
            rect_bala = pygame.Rect(bala.x, bala.y, 12, 12)

            if rect_bala.colliderect(self.jugador.rect):
                self.jugador.recibirDaño(bala.daño)
                Estadisticas.sumar_balas_enemigo_impactadas()
                self.balas_enemigos.remove(bala)
            elif self.mapa.colision(rect_bala):
                self.balas_enemigos.remove(bala)
            elif bala.x < 0 or bala.x > 800 or bala.y < 0 or bala.y > 600:
                self.balas_enemigos.remove(bala)

        # Transición de Piso con Fade Out y Validación de Victoria
        if self.mapa.jugador_en_trampilla(self.jugador.rect) and not self.fading_piso:
            self.fading_piso = True
            self.fade_alpha_piso = 0

        if self.fading_piso:
            self.fade_alpha_piso += 320 * time_delta
            if self.fade_alpha_piso >= 255:
                self.fade_alpha_piso = 255

                numero_piso_actual = self.mapa.obtener_numero_piso_actual()

                if numero_piso_actual == 3:
                    Estadisticas.puntaje_final = Estadisticas.calcular_puntaje(self.jugador)
                    self.manager.cambiar_escena(EscenaFinJuego(self.manager))
                    return
                else:
                    self.mapa.pasar_siguiente_piso()
                    AudioManager.play_music("musica_fondo.mp3", volumen=0.1)
                    self.jugador.x = 200
                    self.jugador.y = 200
                    self.jugador.rect.x = self.jugador.x
                    self.jugador.rect.y = self.jugador.y

                    self.balas_jugador.clear()
                    self.balas_enemigos.clear()

                    self.fading_piso = False
                    self.fade_alpha_piso = 0

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

        if self.fade_alpha_piso > 0:
            surf_fade = pygame.Surface(self.manager.resolucion)
            surf_fade.fill((0, 0, 0))
            surf_fade.set_alpha(int(self.fade_alpha_piso))
            self.manager.pantalla.blit(surf_fade, (0, 0))


# =====================[ESCENA: FIN DEL JUEGO]=======================================
class EscenaFinJuego:
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.fondo_endgame = None
        self.rect_btn_reiniciar = pygame.Rect(0, 0, 0, 0)
        self.rect_btn_salir = pygame.Rect(0, 0, 0, 0)

        self.fading = False
        self.fade_alpha = 0

    def inicializar(self):
        AudioManager.stop_music()
        ruta_img = os.path.join(os.path.dirname(__file__), "imagenes", "menu", "menu_endgame.png")
        if os.path.exists(ruta_img):
            imagen_original = pygame.image.load(ruta_img).convert_alpha()
            self.fondo_endgame = pygame.transform.scale(imagen_original, self.manager.resolucion)

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

        surf_puntos = fuente_fin.render(str(Estadisticas.puntaje_final), True, (color_texto))
        surf_puntos_rotada = pygame.transform.rotate(surf_puntos, -5)
        self.manager.pantalla.blit(surf_puntos_rotada, (355, 485))

        ancho_b, alto_b = 180, 40
        pos_mouse = pygame.mouse.get_pos()

        if self.rect_btn_reiniciar.collidepoint(pos_mouse):
            color_fondo_reiniciar = color_interaccion_boton
        else:
            color_fondo_reiniciar = color_boton

        if self.rect_btn_salir.collidepoint(pos_mouse):
            color_fondo_salir_fin = color_interaccion_boton
        else:
            color_fondo_salir_fin = color_boton

        surf_btn1 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn1, (color_fondo_reiniciar), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn1, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn1 = fuente_fin.render("Volver a Jugar", True, (color_texto))
        surf_btn1.blit(texto_btn1, texto_btn1.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn2 = pygame.Surface((ancho_b, alto_b), pygame.SRCALPHA)
        pygame.draw.rect(surf_btn2, (color_fondo_salir_fin), (0, 0, ancho_b, alto_b), border_radius=3)
        pygame.draw.rect(surf_btn2, (140, 124, 128), (0, 0, ancho_b, alto_b), 2, border_radius=3)
        texto_btn2 = fuente_fin.render("Salir del juego", True, (color_texto))
        surf_btn2.blit(texto_btn2, texto_btn2.get_rect(center=(ancho_b // 2, alto_b // 2)))

        surf_btn1_rotado = pygame.transform.rotate(surf_btn1, -5)
        surf_btn2_rotado = pygame.transform.rotate(surf_btn2, -5)

        pos_b1_x, pos_b1_y = 175, 547
        pos_b2_x, pos_b2_y = 370, 567

        self.rect_btn_reiniciar = surf_btn1_rotado.get_rect(topleft=(pos_b1_x, pos_b1_y))
        self.rect_btn_salir = surf_btn2_rotado.get_rect(topleft=(pos_b2_x, pos_b2_y))

        self.manager.pantalla.blit(surf_btn1_rotado, (pos_b1_x, pos_b1_y))
        self.manager.pantalla.blit(surf_btn2_rotado, (pos_b2_x, pos_b2_y))

        if self.fade_alpha > 0:
            surf_fade = pygame.Surface(self.manager.resolucion)
            surf_fade.fill((0, 0, 0))
            surf_fade.set_alpha(int(self.fade_alpha))
            self.manager.pantalla.blit(surf_fade, (0, 0))
