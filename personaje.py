# personaje.py
from base import Base # Importa clase abstracta
import pygame
import os


class Jugador(Base):
    
    def __init__(self, nombre, vida, vel_movimiento, daño, proyectil, rango, x, y):
        super().__init__(x, y)
        self.nombre = nombre
        self.vida = vida
        self.vel_movimiento = vel_movimiento
        self.daño = daño
        self.proyectil = proyectil
        self.rango = rango

        # Escalado uniforme para todos los sprites del personaje
        self.dimensiones = (75, 75)

        # Ruta
        ruta_carpeta = os.path.join(os.path.dirname(__file__), "imagenes", "jugador") # Obtiene la ruta del directorio actual

        # Los sprites para cada direccion se guardan por separado
        self.sprites_direcciones = {
            "ABAJO":     pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_frente.png")).convert_alpha(), self.dimensiones),
            "ARRIBA":    pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_atras.png")).convert_alpha(), self.dimensiones),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_izq.png")).convert_alpha(), self.dimensiones),
            "DERECHA":   pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_der.png")).convert_alpha(), self.dimensiones)
        }

        # La animacion de movimiento se guarda en un archivo con los 4 frames
        anim_caminar = pygame.image.load(os.path.join(ruta_carpeta, "isaac_caminando.png")).convert_alpha()
        anim_caminar_arriba = pygame.image.load(os.path.join(ruta_carpeta, "isaac_caminando_arriba.png")).convert_alpha()
        anim_caminar_abajo = pygame.image.load(os.path.join(ruta_carpeta, "isaac_caminando_abajo.png")).convert_alpha()
        
        # Como las imagenes de animacion miden distinto, se toma la medida para cada una
        ancho_h, alto_h = anim_caminar.get_width(), anim_caminar.get_height()
        ancho_cuadro_h = ancho_h // 4

        ancho_up, alto_up = anim_caminar_arriba.get_width(), anim_caminar_arriba.get_height()
        ancho_cuadro_up = ancho_up // 4

        ancho_down, alto_down = anim_caminar_abajo.get_width(), anim_caminar_abajo.get_height()
        ancho_cuadro_down = ancho_down // 4

        self.animacion_horizontal = []
        self.animacion_arriba = []
        self.animacion_abajo = []
        
        for i in range(4):
            # Tira Horizontal 
            sub_cuadro_horizontal = anim_caminar.subsurface((i * ancho_cuadro_h, 0, ancho_cuadro_h, alto_h))
            self.animacion_horizontal.append(pygame.transform.scale(sub_cuadro_horizontal, self.dimensiones))
            
            # Tira Vertical Arriba
            sub_cuadro_arriba = anim_caminar_arriba.subsurface((i * ancho_cuadro_up, 0, ancho_cuadro_up, alto_up))
            self.animacion_arriba.append(pygame.transform.scale(sub_cuadro_arriba, self.dimensiones))
            
            # Tira Vertical Abajo
            sub_cuadro_abajo = anim_caminar_abajo.subsurface((i * ancho_cuadro_down, 0, ancho_cuadro_down, alto_down))
            self.animacion_abajo.append(pygame.transform.scale(sub_cuadro_abajo, self.dimensiones))
            
        # --- Variables de control para los estados y el tiempo ---
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 130  # ms de cada paso

        # sprite por defecto (Sprite de mirar hacia abajo)
        self.sprite = self.sprites_direcciones[self.direccion_actual]
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    def actualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            # Seleccionamos la lista de animación que corresponde según el estado de dirección
            if self.direccion_actual in ["DERECHA", "IZQUIERDA"]:
                animacion_activa = self.animacion_horizontal
            elif self.direccion_actual == "ARRIBA":
                animacion_activa = self.animacion_arriba
            else:  # ABAJO
                animacion_activa = self.animacion_abajo

            # Control del reloj: Avanza el índice de la animación según la lista activa
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(animacion_activa)
                self.tiempo_ultimo_frame = tiempo_actual
            
            # Se ejecuta en cada frame del juego 
            self.sprite = animacion_activa[self.indice_animacion]
                
            # Si el jugador se mueve hacia la derecha, invertimos la tira de animaciones 
            if self.direccion_actual == "DERECHA":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            # Si se queda quieto, vuelve al sprite estático de su dirección
            self.sprite = self.sprites_direcciones[self.direccion_actual]
            
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    def Moverse(self, keys, mapa):
        self.esta_moviendose = False

        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx = -self.vel_movimiento
        elif keys[pygame.K_d]:
            dx = self.vel_movimiento

        if keys[pygame.K_w]:
            dy = -self.vel_movimiento
        elif keys[pygame.K_s]:
            dy = self.vel_movimiento

        if dx != 0 or dy != 0:
            self.esta_moviendose = True
       
            # Logica de control de prioridad de movimiento 
            if abs(dy) >= abs(dx) and dy != 0:
                if dy < 0:
                    self.direccion_actual = "ARRIBA"
                else:
                    self.direccion_actual = "ABAJO"
            elif abs(dx) > abs(dy) and dx != 0:
                if dx < 0:
                    self.direccion_actual = "IZQUIERDA"
                else:
                    self.direccion_actual = "DERECHA"
                        
        # Probar movimiento en X
        nuevo_rect = self.rect.copy()
        nuevo_rect.x += dx
        if not mapa.colision(nuevo_rect):
            self.x += dx
            self.rect.x = self.x

        # Probar movimiento en Y
        nuevo_rect = self.rect.copy()
        nuevo_rect.y += dy
        if not mapa.colision(nuevo_rect):
            self.y += dy
            self.rect.y = self.y

        self.actualizarAnimacion()
 
    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))

    def actualizar(self, pantalla, keys, mapa):
        self.Moverse(keys, mapa)