#--------------librerias-----------------
import random
import pygame
import os
#----------------------------------------
ANCHO = 32
ALTO = 32


class Jugador:
    def __init__(self, nombre, vida, vel_movimiento, daño, proyectil, rango, x, y):
        self.nombre = nombre
        self.vida = vida
        self.vel_movimiento = vel_movimiento
        self.daño = daño
        self.proyectil = proyectil
        self.rango = rango
        self.x = x
        self.y = y
        # Escala para el sprite del jugador
        self.escala_ancho = 100
        self.escala_alto = 100

        ruta = os.path.join(os.path.dirname(__file__), "isaac_base_sprite.png")
        self.sprite_sheet = pygame.image.load(ruta).convert_alpha()
        
        # Elimina el color negro del sprite
        self.sprite_sheet.set_colorkey((0, 0, 0))
        
        # Extract frames for character directions and scale them
        self.sprites_direcciones = {
            "ABAJO":     self.obtener_y_escalar_cuadro((112, 103, 76, 85)),
            "ARRIBA":    self.obtener_y_escalar_cuadro((518, 103, 76, 85)),
            "IZQUIERDA": self.obtener_y_escalar_cuadro((518, 335, 76, 85)),
            "DERECHA":   self.obtener_y_escalar_cuadro((733, 335, 76, 85))
        }
        # Secuencia de animación de movimiento
        self.animacion_caminando = [
            self.obtener_y_escalar_cuadro((449, 634, 76, 85)),
            self.obtener_y_escalar_cuadro((574, 634, 76, 85)),
            self.obtener_y_escalar_cuadro((699, 634, 76, 85)),
            self.obtener_y_escalar_cuadro((824, 634, 76, 85))
        ]
        
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 150  # Milisegundos entre cada cuadro
        
        # Asignar frame por defecto inicial
        self.sprite = self.sprites_direcciones[self.direccion_actual]
        
        def obtener_y_escalar_cuadro(self, tupla_coordenadas):
            cuadro = self.sprite_sheet.subsurface(tupla_coordenadas)
            return pygame.transform.scale(cuadro, (self.escala_ancho, self.escala_alto))

    def ActualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            # Si se mueve, itera cíclicamente por las animaciones de movimiento
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_caminando)
                self.sprite = self.animacion_caminando[self.indice_animacion]
                self.tiempo_ultimo_frame = tiempo_actual
        else:
            # Si está quieto, muestra el sprite estático correspondiente
            self.sprite = self.sprites_direcciones[self.direccion_actual]

    def Moverse(self, keys):  
        self.esta_moviendose = False

        if keys[pygame.K_a]: # Izquierda
            self.x -= self.vel_movimiento
            self.direccion_actual = "IZQUIERDA"
            self.esta_moviendose = True
        if keys[pygame.K_d]: # Derecha
            self.x += self.vel_movimiento
            self.direccion_actual = "DERECHA"
            self.esta_moviendose = True
        if keys[pygame.K_w]: # Arriba
            self.y -= self.vel_movimiento
            self.direccion_actual = "ARRIBA"
            self.esta_moviendose = True
        if keys[pygame.K_s]: # Abajo
            self.y += self.vel_movimiento
            self.direccion_actual = "ABAJO"
            self.esta_moviendose = True

        # Actualizamos qué frame debe mostrarse en base a lo ocurrido arriba
        self.ActualizarAnimacion()
        
    def Dibujo(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))