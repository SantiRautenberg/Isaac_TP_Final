# escenas.py
import pygame
import pygame_gui
import os
import sys
# Importar las clases desde sus respectivos archivos
from personaje import Jugador
from bala import Bala
from enemigo import Enemigo
from mapa import Mapa
from interfaz import Interfaz

class SceneManager:
    
    def __init__(self, pantalla, resolucion, audio_manager, ui_manager, ruta_themes, ruta_fuente):
        self.pantalla = pantalla
        self.resolucion = resolucion
        self.audio_manager = audio_manager
        self.ui_manager = ui_manager  # Guardamos el manager global compartido
        self.ruta_themes = ruta_themes
        self.ruta_fuente = ruta_fuente
        
        # Escena activa actual
        self.escena_actual = None

    # =====================[CONTROL DE TRANSICIONES]======================================
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
        # Instanciamos el Menu con el manager
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente)
        self.interfaz.crear_menu_inicio()
        # Reproducir música de menú
        self.manager.audio_manager.reproducir_musica("musica_menu.mp3", volumen=0.2)

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Botones del Menu
            if evento.type == pygame.USEREVENT and hasattr(evento, 'user_type') and evento.user_type == pygame_gui.UI_BUTTON_PRESSED or evento.type == pygame.USEREVENT + 1:
                try:
                    if evento.ui_element == self.interfaz.boton_iniciar:
                        self.manager.audio_manager.detener_musica()
                        self.interfaz.destruir_menu_inicio()
                        self.manager.cambiar_escena(EscenaJuego(self.manager))

                    elif evento.ui_element == self.interfaz.boton_pruebas:
                        self.interfaz.destruir_menu_inicio()
                        self.manager.cambiar_escena(EntornoPruebas(self.manager))

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

# =====================[ESCENA: ENTORNO DE PRUEBAS HUD]===============================
class EntornoPruebas:
    
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        self.interfaz = None

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente)
        self.interfaz.crear_entorno_pruebas()

    def actualizar(self, time_delta, tiempo_actual, keys):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.USEREVENT and hasattr(evento, 'ui_element'):
                if evento.ui_element == self.interfaz.boton_volver:
                    self.interfaz.boton_volver.kill()
                    # Regreso limpio a la clase EscenaMenu
                    self.manager.cambiar_escena(EscenaMenu(self.manager))
                    
            self.interfaz.manager.process_events(evento)
            
        self.interfaz.manager.update(time_delta)

    def dibujar(self):
        self.manager.pantalla.fill((40, 40, 45))
        self.interfaz.dibujar_prototipo_hud(self.manager.pantalla)
        self.interfaz.manager.draw_ui(self.manager.pantalla)


# =====================[ESCENA: PARTIDA JUGABLE]======================================
class EscenaJuego:
    
    def __init__(self, manager_escenas):
        self.manager = manager_escenas
        
        # ----------------sets_del_personaje------------------------
        self.jugador = Jugador("Isaac", 3, 5, 1, None, 100, 100, 100)
        self.mapa = Mapa()
        self.balas = []
        # -------------------sets_de_enemigos-----------------------
        self.enemigos = [Enemigo(400, 300), Enemigo(200, 150)]
        # ------------------LISTA GENERAL---------------------------
        self.entidades = [self.jugador] + self.enemigos + self.balas
        # --------------Variables de disparo para generar delay-----------------------------
        self.delay_disparo = 500
        self.ultimo_disparo = 0

    def inicializar(self):
        self.interfaz = Interfaz(self.manager.resolucion, self.manager.ui_manager, self.manager.ruta_fuente)

    def revisar_cambio_sala(self):
        ancho_pantalla, alto_pantalla = self.manager.resolucion
        margen = 10

        if self.jugador.rect.left <= 0:
            if self.mapa.cambiar_sala_por_direccion("IZQUIERDA"):
                self.jugador.x = ancho_pantalla - self.jugador.dimensiones[0] - margen
            else:
                self.jugador.x = 0
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.right >= ancho_pantalla:
            if self.mapa.cambiar_sala_por_direccion("DERECHA"):
                self.jugador.x = margen
            else:
                self.jugador.x = ancho_pantalla - self.jugador.dimensiones[0]
            self.jugador.rect.x = self.jugador.x

        elif self.jugador.rect.top <= 0:
            if self.mapa.cambiar_sala_por_direccion("ARRIBA"):
                self.jugador.y = alto_pantalla - self.jugador.dimensiones[1] - margen
            else:
                self.jugador.y = 0
            self.jugador.rect.y = self.jugador.y

        elif self.jugador.rect.bottom >= alto_pantalla:
            if self.mapa.cambiar_sala_por_direccion("ABAJO"):
                self.jugador.y = margen
            else:
                self.jugador.y = alto_pantalla - self.jugador.dimensiones[1]
            self.jugador.rect.y = self.jugador.y

    def actualizar(self, time_delta, tiempo_actual, keys):
        # =====================[TEST CAMBIO DE SALAS/PISOS]=====================
        if keys[pygame.K_1]: self.mapa.cambiar_sala("comun_1")
        if keys[pygame.K_2]: self.mapa.cambiar_sala("comun_2")
        if keys[pygame.K_3]: self.mapa.cambiar_sala("tesoro")
        if keys[pygame.K_4]: self.mapa.cambiar_sala("boss")
        
        # Procesamos los eventos de la ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.interfaz.manager.process_events(evento)
            
        self.interfaz.manager.update(time_delta)
        
        # =====================[sets_teclas_disparo]==========================================
        if keys[pygame.K_RIGHT] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 50, self.jugador.y + 50, 1, 0)
            self.balas.append(bala)
            self.entidades.append(bala)
            self.jugador.direccion_actual = "DERECHA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_LEFT] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 50, self.jugador.y + 50, -1, 0)
            self.balas.append(bala)
            self.entidades.append(bala)
            self.jugador.direccion_actual = "IZQUIERDA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_UP] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y, 0, -1)
            self.balas.append(bala)
            self.entidades.append(bala)
            self.jugador.direccion_actual = "ARRIBA"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        elif keys[pygame.K_DOWN] and tiempo_actual - self.ultimo_disparo > self.delay_disparo:
            bala = Bala(self.jugador.x + 25, self.jugador.y + 50, 0, 1)
            self.balas.append(bala)
            self.entidades.append(bala)
            self.jugador.direccion_actual = "ABAJO"
            self.manager.audio_manager.reproducir_sfx("disparo")
            self.ultimo_disparo = tiempo_actual

        # Actualizamos el mapa
        self.mapa.actualizar(self.manager.pantalla)
        
        # -------------------- CORRECCIÓN DE MOVIMIENTO DIRECTO --------------------
        self.jugador.actualizar(self.manager.pantalla, keys, self.mapa)

        #-------------------- ACTUALIZA EL RESTO DE ENTIDADES --------------------
        # Corremos el bucle polimórfico solo para los enemigos y las balas
        for entidad in self.entidades[:]:
            if isinstance(entidad, Enemigo):
                entidad.actualizar(self.manager.pantalla, self.jugador)
            elif isinstance(entidad, Bala):
                entidad.actualizar(self.manager.pantalla)
                # Limpieza para las balas
                if entidad.x < 0 or entidad.x > 800 or entidad.y < 0 or entidad.y > 600:
                    if entidad in self.balas:
                        self.balas.remove(entidad)
                    if entidad in self.entidades:
                        self.entidades.remove(entidad)

        self.revisar_cambio_sala()

    def dibujar(self):
        self.mapa.dibujar(self.manager.pantalla)
        for entidad in self.entidades:
            entidad.dibujar(self.manager.pantalla)
        self.interfaz.manager.draw_ui(self.manager.pantalla)