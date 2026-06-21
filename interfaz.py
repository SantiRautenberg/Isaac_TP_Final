# interfaz.py
import pygame
import pygame_gui
import os
from estadistica import Estadisticas

class Interfaz:
    def __init__(self, resolucion, manager_ui, ruta_fuente, alto_hud=100):
        # ----------------- PARAMETRIZACIÓN INICIAL -----------------
        self.resolucion = resolucion
        self.ruta_fuente = ruta_fuente
        self.manager = manager_ui
        self.alto_hud = alto_hud

        # Elementos del menú principal
        self.label_titulo = None
        self.boton_iniciar = None
        self.boton_salir = None

        # Elementos de la pantalla de fin del juego
        self.label_placeholder = None
        self.label_puntaje = None
        self.boton_reiniciar = None
        self.boton_salir_fin = None

    def dibujar_hud_juego(self, pantalla, jugador, mapa):
        # Base del HUD
        pygame.draw.rect(pantalla, (15, 15, 20), (0, 0, self.resolucion[0], self.alto_hud))
        pygame.draw.rect(pantalla, (60, 60, 65), (0, self.alto_hud - 2, self.resolucion[0], 2))

        # Salud dinamica
        vida_actual = jugador.get_vida()
        max_contenedores = 3
        pos_x_corazon = 50
        pos_y_corazon = self.alto_hud // 2 - 5

        for i in range(max_contenedores):
            limite_vida_corazon = (i + 1) * 2

            if vida_actual >= limite_vida_corazon:
                pygame.draw.circle(pantalla, (220, 40, 40), (pos_x_corazon, pos_y_corazon), 8)
                pygame.draw.circle(pantalla, (220, 40, 40), (pos_x_corazon + 10, pos_y_corazon), 8)
                pygame.draw.polygon(pantalla, (220, 40, 40), [(pos_x_corazon - 8, pos_y_corazon + 2), (pos_x_corazon + 18, pos_y_corazon + 2), (pos_x_corazon + 5, pos_y_corazon + 14)])

            elif vida_actual == limite_vida_corazon - 1:
                pygame.draw.circle(pantalla, (220, 40, 40), (pos_x_corazon, pos_y_corazon), 8)
                pygame.draw.polygon(pantalla, (220, 40, 40), [(pos_x_corazon - 8, pos_y_corazon + 2), (pos_x_corazon + 5, pos_y_corazon + 2), (pos_x_corazon + 5, pos_y_corazon + 14)])
                pygame.draw.circle(pantalla, (40, 40, 45), (pos_x_corazon + 10, pos_y_corazon), 8)
                pygame.draw.circle(pantalla, (140, 40, 40), (pos_x_corazon + 10, pos_y_corazon), 8, 1)

            else:
                pygame.draw.circle(pantalla, (30, 30, 35), (pos_x_corazon, pos_y_corazon), 8)
                pygame.draw.circle(pantalla, (30, 30, 35), (pos_x_corazon + 10, pos_y_corazon), 8)
                pygame.draw.polygon(pantalla, (30, 30, 35), [(pos_x_corazon - 8, pos_y_corazon + 2), (pos_x_corazon + 18, pos_y_corazon + 2), (pos_x_corazon + 5, pos_y_corazon + 14)])
                pygame.draw.circle(pantalla, (150, 40, 40), (pos_x_corazon, pos_y_corazon), 8, 1)
                pygame.draw.circle(pantalla, (150, 40, 40), (pos_x_corazon + 10, pos_y_corazon), 8, 1)

            pos_x_corazon += 35

        # Presentacion del puntaje en tiempo real
        if os.path.exists(self.ruta_fuente):
            fuente_hud = pygame.font.Font(self.ruta_fuente, 16)
        else:
            fuente_hud = pygame.font.SysFont("sans", 16, bold=True)

        texto_score = fuente_hud.render(f"PUNTAJE: {Estadisticas.puntaje_final}", True, (240, 240, 245))
        pantalla.blit(texto_score, (260, self.alto_hud // 2 - 10))

        # Minimapa
        piso_actual = mapa.piso_actual

        if piso_actual and hasattr(piso_actual, "posiciones_salas"):
            posiciones_mapa = piso_actual.posiciones_salas

            if not posiciones_mapa:
                return

            tile_ancho = 26
            tile_alto = 19
            separacion_x = 38
            separacion_y = 28

            min_x = min(pos[0] for pos in posiciones_mapa.values())
            max_x = max(pos[0] for pos in posiciones_mapa.values())
            min_y = min(pos[1] for pos in posiciones_mapa.values())
            max_y = max(pos[1] for pos in posiciones_mapa.values())

            ancho_minimapa = (max_x - min_x) * separacion_x + tile_ancho
            alto_minimapa = (max_y - min_y) * separacion_y + tile_alto

            start_x = self.resolucion[0] - ancho_minimapa - 35
            start_y = (self.alto_hud - alto_minimapa) // 2 

            if start_y < 6:
                start_y = 6

            for nombre_sala, sala in piso_actual.salas.items():
                if nombre_sala in posiciones_mapa:
                    gx, gy = posiciones_mapa[nombre_sala]
                    gx -= min_x
                    gy -= min_y

                    centro_origen_x = start_x + (gx * 38) + 13
                    centro_origen_y = start_y + (gy * 28) + 9

                    for direccion, destino in sala.conexiones.items():
                        if destino in posiciones_mapa:
                            dgx, dgy = posiciones_mapa[destino]
                            dgx -= min_x
                            dgy -= min_y

                            centro_destino_x = start_x + (dgx * 38) + 13
                            centro_destino_y = start_y + (dgy * 28) + 9
                            pygame.draw.line(pantalla, (90, 90, 95), (centro_origen_x, centro_origen_y), (centro_destino_x, centro_destino_y), 3)

            for nombre_sala, sala in piso_actual.salas.items():
                if nombre_sala in posiciones_mapa:
                    grid_x, grid_y = posiciones_mapa[nombre_sala]
                    grid_x -= min_x
                    grid_y -= min_y

                    bx = start_x + (grid_x * 38)
                    by = start_y + (grid_y * 28)

                    if sala.tipo == "tesoro":
                        color_bloque = (212, 175, 55)
                    elif sala.tipo == "boss":
                        color_bloque = (180, 30, 30)
                    else:
                        color_bloque = (65, 65, 70)

                    if piso_actual.sala_actual and piso_actual.sala_actual.nombre == nombre_sala:
                        color_bloque = (245, 245, 250)

                    pygame.draw.rect(pantalla, color_bloque, (bx, by, 26, 19))
                    pygame.draw.rect(pantalla, (10, 10, 15), (bx, by, 26, 19), 1)    
