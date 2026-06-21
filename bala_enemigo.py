# bala_enemigo.py
from bala import Bala
from estadistica import Estadisticas
import pygame

class BalaEnemigo(Bala):

    def __init__(self, x, y, dire_x, dire_y, daño=1):
        super().__init__(x, y, dire_x, dire_y, daño)

        # Stats propias
        self.bala_vel = 8
        self.daño = daño

        # Estadísticas separadas
        Estadisticas.sumar_balas_enemigo_disparadas()

    def dibujar(self, pantalla):
        rojo_base = (220, 60, 60)
        rojo_oscuro = (120, 20, 20)

        pygame.draw.circle(pantalla, rojo_base, (int(self.x), int(self.y)), 10)
        pygame.draw.circle(pantalla, rojo_oscuro, (int(self.x - 2), int(self.y - 2)), 3)