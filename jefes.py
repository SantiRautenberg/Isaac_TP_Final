#jefes.py
import pygame
import math
from enemigo import Enemigo
from bala_enemigo import BalaEnemigo


class JefeBase(Enemigo):
    def __init__(self, x, y, velocidad, vida, daño, color):
        super().__init__(x, y, velocidad, vida, daño)

        self.ancho = 80
        self.alto = 80
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.vida_maxima = vida
        self.color = color

    def dibujar_barra_vida(self, pantalla):
        ancho_barra = 375
        alto_barra = 20
        x = 200
        y = 550

        porcentaje = max(0, self.vida / self.vida_maxima)

        pygame.draw.rect(pantalla, (40, 40, 40), (x, y, ancho_barra, alto_barra))
        pygame.draw.rect(pantalla, (180, 30, 30), (x, y, ancho_barra * porcentaje, alto_barra))
        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho_barra, alto_barra), 2)

    def dibujar(self, pantalla):
        centro_x = int(self.x + self.ancho / 2)
        centro_y = int(self.y + self.alto / 2)

        pygame.draw.circle(pantalla, self.color, (centro_x, centro_y), 40)
        pygame.draw.circle(pantalla, (40, 0, 0), (centro_x, centro_y), 15)
        self.dibujar_barra_vida(pantalla)


class JefePiso1(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=1.4, vida=14, daño=2, color=(180, 40, 40))

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None):   
        self.seguir_jugador(jugador)
        self.colision_con_jugador(jugador)


class JefePiso2(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=2, vida=18, daño=2, color=(150, 60, 180))

        self.direccion_x = 1
        self.direccion_y = 1
        self.cooldown_invocar = 2200
        self.ultimo_invocado = 0

    def mover_por_sala(self):
        self.x += self.velocidad * self.direccion_x
        self.y += self.velocidad * self.direccion_y

        if self.x <= 40 or self.x + self.ancho >= 760:
            self.direccion_x *= -1

        if self.y <= 80 or self.y + self.alto >= 620:
            self.direccion_y *= -1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def invocar_enemigo(self, lista_enemigos):
        if lista_enemigos is None:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_invocado < self.cooldown_invocar:
            return

        enemigo = Enemigo(self.x + 20, self.y + 20, velocidad=2, vida=2, daño=1)
        lista_enemigos.append(enemigo)

        self.ultimo_invocado = tiempo_actual

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None):
        self.mover_por_sala()
        self.invocar_enemigo(lista_enemigos)
        self.colision_con_jugador(jugador)


class JefePiso3(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=1, vida=22, daño=2, color=(40, 40, 190))

        self.cooldown_disparo = 900
        self.ultimo_disparo = 0

    def disparar(self, jugador, lista_balas):
        if lista_balas is None:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_disparo < self.cooldown_disparo:
            return

        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            return

        dx /= distancia
        dy /= distancia

        bala = BalaEnemigo(
            self.x + self.ancho / 2,
            self.y + self.alto / 2,
            dx,
            dy,
            daño=self.daño
        )

        lista_balas.append(bala)
        self.ultimo_disparo = tiempo_actual

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None):
        self.disparar(jugador, lista_balas)
        self.colision_con_jugador(jugador)