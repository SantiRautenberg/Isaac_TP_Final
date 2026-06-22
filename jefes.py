# jefes.py
import pygame
import math
import os
from enemigo import Enemigo
from bala_enemigo import BalaEnemigo


SPRITES_JEFES_CACHE = {}


def cargar_sprite_recortado(ruta, dimensiones):
    clave_cache = (ruta, dimensiones)

    if clave_cache in SPRITES_JEFES_CACHE:
        return SPRITES_JEFES_CACHE[clave_cache]

    imagen = pygame.image.load(ruta).convert_alpha()
    ancho = imagen.get_width()
    alto = imagen.get_height()

    esquinas = [
        imagen.get_at((0, 0)),
        imagen.get_at((ancho - 1, 0)),
        imagen.get_at((0, alto - 1)),
        imagen.get_at((ancho - 1, alto - 1)),
    ]
    limpiar_fondo_blanco = any(
        a > 0 and r > 220 and g > 220 and b > 220
        for r, g, b, a in esquinas
    )

    if limpiar_fondo_blanco:
        for x in range(ancho):
            for y in range(alto):
                r, g, b, a = imagen.get_at((x, y))

                if r > 220 and g > 220 and b > 220:
                    imagen.set_at((x, y), (r, g, b, 0))

    rect_contenido = imagen.get_bounding_rect()

    if rect_contenido.width > 0 and rect_contenido.height > 0:
        imagen = imagen.subsurface(rect_contenido).copy()

    imagen = pygame.transform.scale(imagen, dimensiones)
    SPRITES_JEFES_CACHE[clave_cache] = imagen

    return imagen


class JefeBase(Enemigo):
    def __init__(self, x, y, velocidad, vida, daño, color):
        super().__init__(x, y, velocidad, vida, daño)

        self.ancho = 90
        self.alto = 90
        self.dimensiones = (90, 90)
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

        pygame.draw.circle(pantalla, self.color, (centro_x, centro_y), self.ancho // 2)
        pygame.draw.circle(pantalla, (40, 0, 0), (centro_x, centro_y), self.ancho // 5)
        self.dibujar_barra_vida(pantalla)


class JefePiso1(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=1.4, vida=35, daño=2, color=(180, 40, 40))

        self.animaciones = {
            "ARRIBA": self.cargar_animacion(["boss_f_atras_1", "boss_f_atras_2", "boss_f_atras_3", "boss_f_atras_4"]),
            "ABAJO": self.cargar_animacion(["boss_f_adelante_1", "boss_f_adelante_2", "boss_f_adelante_3", "boss_f_adelante_4"]),
            "DERECHA": self.cargar_animacion([
                "boss_f_derecha_1", "boss_f_derecha_2", "boss_f_derecha_3", "boss_f_derecha_4",
                "boss_f_derecah_1", "boss_f_derecah_2", "boss_f_derecah_3", "boss_f_derecah_4",
            ]),
            "IZQUIERDA": self.cargar_animacion(["boss_f_izquierda_1", "boss_f_izquierda_2", "boss_f_izquierda_3", "boss_f_izquierda_4"]),
        }

        self.direccion_actual = "ABAJO"
        self.indice_animacion_jefe = 0
        self.tiempo_ultimo_frame_jefe = 0
        self.velocidad_animacion_jefe = 140
        self.sprite_jefe = self.obtener_sprite_actual()

    def obtener_carpeta_sprites(self):
        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        opciones = [
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "Piso_1"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "piso_1"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "jefe_piso_1"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes"),
        ]

        for ruta in opciones:
            if os.path.exists(ruta):
                return ruta

        return opciones[0]

    def cargar_animacion(self, nombres):
        carpeta = self.obtener_carpeta_sprites()
        animacion = []

        for nombre in nombres:
            ruta = os.path.join(carpeta, f"{nombre}.png")

            if os.path.exists(ruta):
                animacion.append(cargar_sprite_recortado(ruta, self.dimensiones))

        return animacion

    def obtener_sprite_actual(self):
        animacion = self.animaciones.get(self.direccion_actual, [])

        if not animacion:
            return None

        self.indice_animacion_jefe = self.indice_animacion_jefe % len(animacion)
        return animacion[self.indice_animacion_jefe]

    def actualizar_direccion(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y

        if abs(dx) > abs(dy):
            if dx > 0:
                self.direccion_actual = "DERECHA"
            else:
                self.direccion_actual = "IZQUIERDA"
        else:
            if dy > 0:
                self.direccion_actual = "ABAJO"
            else:
                self.direccion_actual = "ARRIBA"

    def actualizar_animacion_jefe(self):
        animacion = self.animaciones.get(self.direccion_actual, [])

        if not animacion:
            self.sprite_jefe = None
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_ultimo_frame_jefe > self.velocidad_animacion_jefe:
            self.indice_animacion_jefe = (self.indice_animacion_jefe + 1) % len(animacion)
            self.tiempo_ultimo_frame_jefe = tiempo_actual

        self.sprite_jefe = self.obtener_sprite_actual()

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None, obstaculos=None):
        if not self.puede_actuar():
            return

        self.actualizar_direccion(jugador)
        self.seguir_jugador(jugador, obstaculos)
        self.colision_con_jugador(jugador)
        self.actualizar_animacion_jefe()

    def dibujar(self, pantalla):
        if self.sprite_jefe:
            pantalla.blit(self.sprite_jefe, (self.x, self.y))
            self.dibujar_barra_vida(pantalla)
        else:
            super().dibujar(pantalla)


class JefePiso2(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=2, vida=55, daño=2, color=(150, 60, 180))

        self.direccion_x = 1
        self.direccion_y = 1
        self.cooldown_invocar = 2200
        self.ultimo_invocado = 0
        self.direccion_actual = "ABAJO"
        self.animaciones = {
            "ARRIBA": self.cargar_animacion(["boss_2_atras_1", "boss_2_atras_2", "boss_2_atras_3"]),
            "ABAJO": self.cargar_animacion(["boss_2_frente_1", "boss_2_frente_2", "boss_2_frente_3"]),
            "DERECHA": self.cargar_animacion(["boss_2_derecha_1", "boss_2_derecha_2", "boss_2_derecha_3"]),
            "IZQUIERDA": self.cargar_animacion(["boss_2_izquierda_1", "boss_2_izquierda_2", "boss_2_izquierda_3"]),
        }
        self.indice_animacion_jefe = 0
        self.tiempo_ultimo_frame_jefe = 0
        self.velocidad_animacion_jefe = 140
        self.sprite_jefe = self.obtener_sprite_actual()

    def obtener_carpeta_sprites(self):
        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        opciones = [
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "piso_2"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "Piso_2"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "jefe_piso_2"),
        ]

        for ruta in opciones:
            if os.path.exists(ruta):
                return ruta

        return opciones[0]

    def cargar_animacion(self, nombres):
        carpeta = self.obtener_carpeta_sprites()
        animacion = []

        for nombre in nombres:
            ruta = os.path.join(carpeta, f"{nombre}.png")

            if os.path.exists(ruta):
                animacion.append(cargar_sprite_recortado(ruta, self.dimensiones))

        return animacion

    def obtener_sprite_actual(self):
        animacion = self.animaciones.get(self.direccion_actual, [])

        if not animacion:
            return None

        self.indice_animacion_jefe = self.indice_animacion_jefe % len(animacion)
        return animacion[self.indice_animacion_jefe]

    def actualizar_direccion_animacion(self):
        if abs(self.direccion_x) > abs(self.direccion_y):
            if self.direccion_x > 0:
                self.direccion_actual = "DERECHA"
            else:
                self.direccion_actual = "IZQUIERDA"
        else:
            if self.direccion_y > 0:
                self.direccion_actual = "ABAJO"
            else:
                self.direccion_actual = "ARRIBA"

    def actualizar_animacion_jefe(self):
        animacion = self.animaciones.get(self.direccion_actual, [])

        if not animacion:
            self.sprite_jefe = None
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_ultimo_frame_jefe > self.velocidad_animacion_jefe:
            self.indice_animacion_jefe = (self.indice_animacion_jefe + 1) % len(animacion)
            self.tiempo_ultimo_frame_jefe = tiempo_actual

        self.sprite_jefe = self.obtener_sprite_actual()

    def mover_por_sala(self):
        self.x += self.velocidad * self.direccion_x
        self.y += self.velocidad * self.direccion_y

        if self.x <= 40 or self.x + self.ancho >= 760:
            self.direccion_x *= -1

        if self.y <= 80 or self.y + self.alto >= 620:
            self.direccion_y *= -1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.actualizar_direccion_animacion()

    def invocar_enemigo(self, lista_enemigos):
        if lista_enemigos is None:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_invocado < self.cooldown_invocar:
            return

        enemigo = Enemigo(self.x + 20, self.y + 20, velocidad=2, vida=2, daño=1)
        lista_enemigos.append(enemigo)

        self.ultimo_invocado = tiempo_actual

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None, obstaculos=None):
        self.mover_por_sala()
        self.invocar_enemigo(lista_enemigos)
        self.colision_con_jugador(jugador)
        self.actualizar_animacion_jefe()

    def dibujar(self, pantalla):
        if self.sprite_jefe:
            pantalla.blit(self.sprite_jefe, (self.x, self.y))
            self.dibujar_barra_vida(pantalla)
        else:
            super().dibujar(pantalla)


class JefePiso3(JefeBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=1, vida=80, daño=2, color=(40, 40, 190))

        self.cooldown_disparo = 550
        self.ultimo_disparo = 0
        self.direccion_actual = "ABAJO"
        self.animaciones = {
            "ARRIBA": self.cargar_animacion(["boss_3_atras_1"]),
            "ABAJO": self.cargar_animacion(["boss_3_frente_1"]),
            "DERECHA": self.cargar_animacion(["boss_3_derecha_1"]),
            "IZQUIERDA": self.cargar_animacion(["boss_3_izquierda_1", "boss_3_izquierda_!"]),
        }
        self.sprite_jefe = self.obtener_sprite_actual()

    def obtener_carpeta_sprites(self):
        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        opciones = [
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "piso_3"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "Piso_3"),
            os.path.join(ruta_raiz, "imagenes", "enemigos", "jefes", "jefe_piso_3"),
        ]

        for ruta in opciones:
            if os.path.exists(ruta):
                return ruta

        return opciones[0]

    def cargar_animacion(self, nombres):
        carpeta = self.obtener_carpeta_sprites()
        animacion = []

        for nombre in nombres:
            ruta = os.path.join(carpeta, f"{nombre}.png")

            if os.path.exists(ruta):
                animacion.append(cargar_sprite_recortado(ruta, self.dimensiones))

        return animacion

    def obtener_sprite_actual(self):
        animacion = self.animaciones.get(self.direccion_actual, [])

        if not animacion:
            return None

        return animacion[0]

    def actualizar_direccion(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y

        if abs(dx) > abs(dy):
            if dx > 0:
                self.direccion_actual = "DERECHA"
            else:
                self.direccion_actual = "IZQUIERDA"
        else:
            if dy > 0:
                self.direccion_actual = "ABAJO"
            else:
                self.direccion_actual = "ARRIBA"

        self.sprite_jefe = self.obtener_sprite_actual()

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

    def actualizar(self, jugador, lista_balas=None, lista_enemigos=None, obstaculos=None):
        self.actualizar_direccion(jugador)
        self.disparar(jugador, lista_balas)
        self.colision_con_jugador(jugador)

    def dibujar(self, pantalla):
        if self.sprite_jefe:
            pantalla.blit(self.sprite_jefe, (self.x, self.y))
            self.dibujar_barra_vida(pantalla)
        else:
            super().dibujar(pantalla)

