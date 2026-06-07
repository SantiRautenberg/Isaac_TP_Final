# personaje.py
import pygame
import os


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

        self.dimensiones = (75, 75)

        ruta_carpeta = os.path.join(os.path.dirname(__file__), "imagenes", "jugador")

        self.sprites_direcciones = {
            "ABAJO": pygame.transform.scale(
                pygame.image.load(os.path.join(ruta_carpeta, "abajo.png")).convert_alpha(),
                self.dimensiones
            ),
            "ARRIBA": pygame.transform.scale(
                pygame.image.load(os.path.join(ruta_carpeta, "atras.png")).convert_alpha(),
                self.dimensiones
            ),
            "IZQUIERDA": pygame.transform.scale(
                pygame.image.load(os.path.join(ruta_carpeta, "izquierda.png")).convert_alpha(),
                self.dimensiones
            ),
            "DERECHA": pygame.transform.scale(
                pygame.image.load(os.path.join(ruta_carpeta, "derecha.png")).convert_alpha(),
                self.dimensiones
            )
        }

        self.animacion_caminando_derecha = []
        self.animacion_caminando_izquierda = []

        for i in range(4):
            imagen = pygame.image.load(
                os.path.join(ruta_carpeta, f"caminar_{i}.png")
            ).convert_alpha()

            imagen = pygame.transform.scale(imagen, self.dimensiones)

            self.animacion_caminando_izquierda.append(imagen)
            self.animacion_caminando_derecha.append(
                pygame.transform.flip(imagen, True, False)
            )

        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 130

        self.sprite = self.sprites_direcciones[self.direccion_actual]

    def ActualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            if self.direccion_actual == "IZQUIERDA":
                animacion = self.animacion_caminando_izquierda
            elif self.direccion_actual == "DERECHA":
                animacion = self.animacion_caminando_derecha
            else:
                animacion = self.animacion_caminando_derecha

            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(animacion)
                self.tiempo_ultimo_frame = tiempo_actual

            self.sprite = animacion[self.indice_animacion]
        else:
            self.sprite = self.sprites_direcciones[self.direccion_actual]

    def Moverse(self, keys):
        self.esta_moviendose = False

        if keys[pygame.K_a]:
            self.x -= self.vel_movimiento
            self.direccion_actual = "IZQUIERDA"
            self.esta_moviendose = True
        elif keys[pygame.K_d]:
            self.x += self.vel_movimiento
            self.direccion_actual = "DERECHA"
            self.esta_moviendose = True

        if keys[pygame.K_w]:
            self.y -= self.vel_movimiento
            self.direccion_actual = "ARRIBA"
            self.esta_moviendose = True
        elif keys[pygame.K_s]:
            self.y += self.vel_movimiento
            self.direccion_actual = "ABAJO"
            self.esta_moviendose = True

        self.ActualizarAnimacion()

    def Dibujo(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))