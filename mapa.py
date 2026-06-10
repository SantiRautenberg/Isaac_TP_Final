# mapa.py
import pygame
import random
from base import Base

preset_obstaculos = [
    []
]

class Obstaculo(Base):
    def __init__(self, x, y, ancho, alto, color=(100, 100, 100)):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def actualizar(self, pantalla, *args):
        pass
    
    
class Mapa(Base):
    def __init__(self):
        super().__init__(0, 0)
        self.pisos = {}
        self.piso_actual = None

        self.crear_mapa()

    def crear_mapa(self):
        self.pisos[1] = Piso(1)
        self.pisos[2] = Piso(2)
        self.pisos[3] = Piso(3)

        self.piso_actual = self.pisos[1]

    def cambiar_piso(self, numero_piso):
        if numero_piso in self.pisos:
            self.piso_actual = self.pisos[numero_piso]

    def cambiar_sala(self, nombre_sala):
        if self.piso_actual is not None:
            self.piso_actual.cambiar_sala(nombre_sala)

    def dibujar(self, pantalla):
        if self.piso_actual is not None:
            self.piso_actual.dibujar(pantalla)

    def actualizar(self, pantalla, *args):
        if self.piso_actual is not None:
            self.piso_actual.actualizar(pantalla, *args)

    def colision(self, rect_jugador):
        if self.piso_actual is not None:
            return self.piso_actual.colision(rect_jugador)

        return False


class Piso(Base):
    def __init__(self, numero):
        super().__init__(0, 0)
        self.numero = numero
        self.salas = {}
        self.sala_actual = None

        self.crear_piso()

    def crear_piso(self):
        self.salas["comun_1"] = self.crear_sala_comun("comun_1")
        self.salas["comun_2"] = self.crear_sala_comun("comun_2")
        self.salas["comun_3"] = self.crear_sala_comun("comun_3")
        self.salas["comun_4"] = self.crear_sala_comun("comun_4")

        self.salas["tesoro"] = Sala("tesoro", tipo="tesoro", color_fondo=(45, 40, 20))
        self.salas["boss"] = Sala("boss", tipo="jefe", color_fondo=(45, 20, 20))
        self.sala_actual = self.salas["comun_1"]

    def crear_sala_comun(self, nombre):
        sala = Sala(nombre, tipo="comun", color_fondo=(35, 30, 35))
    
        sala.agregar_obstaculo(Obstaculo(200, 200, 100, 50))
        sala.agregar_obstaculo(Obstaculo(400, 300, 80, 80))
        return sala

    def cambiar_sala(self, nombre_sala):
        if nombre_sala in self.salas:
            self.sala_actual = self.salas[nombre_sala]

    def dibujar(self, pantalla):
        if self.sala_actual is not None:
            self.sala_actual.dibujar(pantalla)

    def actualizar(self, pantalla, *args):
        if self.sala_actual is not None:
            self.sala_actual.actualizar(pantalla, *args)

    def colision(self, rect_jugador):
        if self.sala_actual is not None:
            return self.sala_actual.colision(rect_jugador)

        return False

class Sala(Base):
    def __init__(self, nombre, tipo="comun", color_fondo=(35, 30, 35)):
        super().__init__(0, 0)
        self.nombre = nombre
        self.tipo = tipo
        self.color_fondo = color_fondo
        self.obstaculos = []

    def agregar_obstaculo(self, obstaculo):
        self.obstaculos.append(obstaculo)

    def dibujar(self, pantalla):
        pantalla.fill(self.color_fondo)

        for obstaculo in self.obstaculos:
            obstaculo.dibujar(pantalla)

    def actualizar(self, pantalla, *args):
        for obstaculo in self.obstaculos:
            obstaculo.actualizar(pantalla, *args)

    def colision(self, rect_jugador):
        for obstaculo in self.obstaculos:
            if rect_jugador.colliderect(obstaculo.rect):
                return True
        return False
