from base import Base
import pygame
import math

class Bala(Base):

    def __init__(self, x, y, dire_x, dire_Y):
        super().__init__(x, y)
        self.dire_x = dire_x
        self.dire_Y = dire_Y
        self.bala_vel = 10
        self.daño = 1
        self.radio_colision = 15

    def trayectoria(self):
     self.x += self.dire_x * self.bala_vel
     self.y += self.dire_Y * self.bala_vel

    def colision_jugador(self, jugador):

     distancia = math.hypot(
        self.x - jugador.x,
        self.y - jugador.y
     )

     if distancia < self.radio_colision:
        jugador.recibirDaño(self.daño)
        return True

     return False

    def dibujar(self, pantalla):
       verde_base = (80, 200, 120)
       verde_oscuro = (40, 120, 70)

       pygame.draw.circle( pantalla, verde_base,(int(self.x), int(self.y)),10)

       pygame.draw.circle(pantalla,verde_oscuro,(int(self.x - 2), int(self.y - 2)),3)

       pygame.draw.circle(pantalla,(200, 255, 200),(int(self.x + 2), int(self.y + 2)),2)

    def actualizar(self, pantalla, *args):
        self.trayectoria()
