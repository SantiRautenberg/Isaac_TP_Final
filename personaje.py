# personaje.py
from base import Base
from estadistica import Estadisticas
from audio import AudioManager
import pygame
import os

inventario = {}

class Jugador(Base):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nombre = "Isaac"
        self.__vida = 6
        self.__vida_max = 6
        self.__vel_movimiento = 4
        self.__daño = 1
        self.__delay_disparo = 500
        self.proyectil = None
        self.rango = 100
        self.__vivo = True

        # Escalado uniforme para todos los sprites del personaje
        self.dimensiones = (60, 60)

        # Ruta
        ruta_carpeta = os.path.join(os.path.dirname(__file__), "imagenes", "jugador")

        # Los sprites para cada direccion se guardan por separado
        self.sprites_direcciones = {
            "ABAJO":     pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_frente.png")).convert_alpha(), self.dimensiones),
            "ARRIBA":    pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_atras.png")).convert_alpha(), self.dimensiones),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_izq.png")).convert_alpha(), self.dimensiones),
            "DERECHA":   pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_der.png")).convert_alpha(), self.dimensiones)
        }

        # Inicialización de las listas de animación unificadas
        self.animacion_horizontal = []
        self.animacion_arriba = []
        self.animacion_abajo = []

        # Recorremos del 0 al 3 para cargar secuencialmente cada frame independiente de las 3 carpetas
        for i in range(4):
            # 1. Carga de animación horizontal (Caminata Base)
            ruta_frame_h = os.path.join(ruta_carpeta, "anim_base", f"{i}.png")
            img_h = pygame.image.load(ruta_frame_h).convert_alpha()
            self.animacion_horizontal.append(pygame.transform.scale(img_h, self.dimensiones))

            # 2. Carga de animación hacia arriba
            ruta_frame_up = os.path.join(ruta_carpeta, "anim_arriba", f"{i}.png")
            img_up = pygame.image.load(ruta_frame_up).convert_alpha()
            self.animacion_arriba.append(pygame.transform.scale(img_up, self.dimensiones))

            # 3. Carga de animación hacia abajo
            ruta_frame_down = os.path.join(ruta_carpeta, "anim_abajo", f"{i}.png")
            img_down = pygame.image.load(ruta_frame_down).convert_alpha()
            self.animacion_abajo.append(pygame.transform.scale(img_down, self.dimensiones))

        # --- Variables de control para los estados y el tiempo ---
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 110  # ms de cada paso

        # sprite por defecto (Sprite de mirar hacia abajo)
        self.sprite = self.sprites_direcciones[self.direccion_actual]
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

        # cargamos el estado inicial de las estadisticas
        Estadisticas.cargar_estado_inicial(self)

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

            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(animacion_activa)
                self.tiempo_ultimo_frame = tiempo_actual

            # Se ejecuta en cada frame del juego
            self.sprite = animacion_activa[self.indice_animacion]

            # La tira por defecto de movimiento mira a la izquierda, la invertimos para la derecha
            if self.direccion_actual == "DERECHA":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            # Si se queda quieto, vuelve al sprite estático de su dirección
            self.sprite = self.sprites_direcciones[self.direccion_actual]

        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    # ------------ Encapsulamiento ------------
    def get_vida(self):
        return self.__vida

    def get_vida_max(self):
        return self.__vida_max

    def set_vida_max(self, valor):
        self.__vida_max = valor
        # controlamos topes de vida maxima por items
        if self.__vida_max > 10:
            self.__vida_max = 10
        if self.__vida_max <= 0:
            self.__vida_max = 1

        # si la vida actual supera al nuevo maximo se recorta
        if self.__vida > self.__vida_max:
            self.__vida = self.__vida_max

    def get_velMovimiento(self):
        return self.__vel_movimiento

    def get_daño(self):
        return self.__daño

    def get_delay_disparo(self):
        return self.__delay_disparo

    def set_delay_disparo(self, valor):
        self.__delay_disparo = valor
        if self.__delay_disparo < 100:
            self.__delay_disparo = 100

    def get_estado(self):
        return self.__vivo

    def set_vida(self, valor):
        self.__vida = valor
        if self.__vida < 0:
            self.__vida = 0
        if self.__vida == 0:
            self.morir()
        if self.__vida >= self.__vida_max:
            self.__vida = self.__vida_max

    def set_velMovimiento(self, valor):
        self.__vel_movimiento += valor
        if self.__vel_movimiento <= 0:
            self.__vel_movimiento = 1

    def set_daño(self, valor):
        self.__daño += valor
        if self.__daño <= 0:
            self.__daño = 1

    # ------------ Métodos del personaje ------------
    def recibirDaño(self,cantidad):
        self.recibir_daño(cantidad)

    def recibir_daño(self, cantidad):
        daño_recibido = self.__vida - cantidad
        self.set_vida(daño_recibido)
        Estadisticas.sumar_daño_recibido(cantidad)
        AudioManager.play_sfx("daño_isaac")

    def morir(self):
        self.__vivo = False

    # funciones extras para interactuar con items.py
    def curar(self, cantidad):
        curacion = self.__vida + cantidad
        self.set_vida(curacion)
        self.set_vida_max(curacion)

    def curacion_completa(self):
        self.set_vida(self.__vida_max)

    def añadir_contenedor(self, cantidad):
        self.set_vida_max(self.__vida_max + cantidad)

    def reducir_vida_maxima(self, cantidad):
        self.set_vida_max(self.__vida_max - cantidad)

    def aumentar_daño(self, cantidad):
        aumento_daño = self.__daño + cantidad
        self.set_daño(aumento_daño)

    def reducir_daño(self, cantidad):
        reduccion_daño = self.__daño - cantidad
        self.set_daño(reduccion_daño)

    def aumentar_velocidad(self, cantidad):
        aumento_vm = self.__vel_movimiento + cantidad
        self.set_velMovimiento(aumento_vm)

    def reducir_velocidad(self, cantidad):
        reduccion_vm = self.__vel_movimiento - cantidad
        self.set_velMovimiento(reduccion_vm)

    # Otras funciones del personaje

    def moverse(self, keys, mapa):
        self.esta_moviendose = False
        dx = 0
        dy = 0

        # Logica de movimiento
        if keys[pygame.K_a]:
            dx = -self.__vel_movimiento
        elif keys[pygame.K_d]:
            dx = self.__vel_movimiento

        if keys[pygame.K_w]:
            dy = -self.__vel_movimiento
        elif keys[pygame.K_s]:
            dy = self.__vel_movimiento

        if dx != 0 or dy != 0:
            self.esta_moviendose = True

            # Lógica de control de prioridad para determinar la dirección visual de Isaac
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

        # Control de colisiones
        # Probar movimiento simulado en el eje X
        nuevo_rect = self.rect.copy()
        nuevo_rect.x += dx
        if not mapa.colision(nuevo_rect):
            self.x += dx
            self.rect.x = self.x

        # Probar movimiento simulado en el eje Y
        nuevo_rect = self.rect.copy()
        nuevo_rect.y += dy
        if not mapa.colision(nuevo_rect):
            self.y += dy
            self.rect.y = self.y

        self.actualizarAnimacion()

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))

    def actualizar(self, pantalla, keys, mapa):
        self.moverse(keys, mapa)
