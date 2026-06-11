from base import Base # Importa clase abstracta base
import pygame
import math

class Enemigo(Base):
    def __init__(self, x, y, velocidad=2, vida=3, daño=1):
        super().__init__(x, y) # Delega a la clase base
        self.velocidad = velocidad 
        self.vida = vida
        self.daño = daño
        self.radio_colision = 20
        self.cooldown_daño = 500  # milisegundos
        self.ultimo_hit = 0

    def seguir_jugador(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            dx /= distancia
            dy /= distancia

            self.x += dx * self.velocidad
            self.y += dy * self.velocidad

    def colision_con_jugador(self, jugador):
        distancia = math.hypot(self.x - jugador.x, self.y - jugador.y)

        if distancia < self.radio_colision:
            tiempo_actual = pygame.time.get_ticks()

            if tiempo_actual - self.ultimo_hit > self.cooldown_daño:
                jugador.recibirDaño(self.daño)
                self.ultimo_hit = tiempo_actual

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (200, 50, 50), (int(self.x), int(self.y)), 15)
        pygame.draw.circle(pantalla, (120, 0, 0), (int(self.x), int(self.y)), 7)

    def actualizar(self, jugador):
        self.seguir_jugador(jugador)
        self.colision_con_jugador(jugador)


    
    
