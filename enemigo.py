# enemigo.py
from base import Base
from bala import Bala
import pygame
import math


class Enemigo(Base):
    def __init__(self, x, y, velocidad=2, vida=3, daño=1):
        super().__init__(x, y)

        self.velocidad = velocidad
        self.vida = vida
        self.daño = daño

        self.ancho = 40
        self.alto = 40
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        self.cooldown_daño = 700
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

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def hacer_daño_al_jugador(self, jugador):
        if hasattr(jugador, "get_vida") and jugador.get_vida() <= 0:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_hit < self.cooldown_daño:
            return

        if hasattr(jugador, "recibirDaño"):
            jugador.recibirDaño(self.daño)

        elif hasattr(jugador, "recibir_daño"):
            jugador.recibir_daño(self.daño)

        elif hasattr(jugador, "set_vida") and hasattr(jugador, "get_vida"):
            nueva_vida = max(0, jugador.get_vida() - self.daño)
            jugador.set_vida(nueva_vida)

        else:
            print("El jugador no tiene método para recibir daño")

        self.ultimo_hit = tiempo_actual

        if hasattr(jugador, "get_vida"):
            print("ENEMIGO HIZO DAÑO. Vida jugador:", jugador.get_vida())

    def colision_con_jugador(self, jugador):
        if hasattr(jugador, "rect"):
            if self.rect.colliderect(jugador.rect):
                self.hacer_daño_al_jugador(jugador)

    def dibujar(self, pantalla):
        centro_x = int(self.x + self.ancho / 2)
        centro_y = int(self.y + self.alto / 2)

        pygame.draw.circle(pantalla, (200, 50, 50), (centro_x, centro_y), 20)
        pygame.draw.circle(pantalla, (120, 0, 0), (centro_x, centro_y), 9)

    def actualizar(self, jugador, *args):
        self.seguir_jugador(jugador)
        self.colision_con_jugador(jugador)


class EnemigoDisparador(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=0, vida=5, daño=1)

        self.cooldown_disparo = 1500
        self.ultimo_disparo = 0

    def disparar(self, jugador, lista_balas):
        if lista_balas is None:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_disparo <= self.cooldown_disparo:
            return

        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            return

        dx /= distancia
        dy /= distancia

        bala = Bala(
            self.x + self.ancho / 2,
            self.y + self.alto / 2,
            dx,
            dy,
            daño=self.daño
        )

        lista_balas.append(bala)
        self.ultimo_disparo = tiempo_actual

        print("ENEMIGO DISPARÓ")

    def actualizar(self, jugador, lista_balas=None):
        self.colision_con_jugador(jugador)
        self.disparar(jugador, lista_balas)

    def dibujar(self, pantalla):
        centro_x = int(self.x + self.ancho / 2)
        centro_y = int(self.y + self.alto / 2)

        pygame.draw.circle(pantalla, (50, 50, 200), (centro_x, centro_y), 20)
        pygame.draw.circle(pantalla, (20, 20, 120), (centro_x, centro_y), 9)