# enemigo.py
from base import Base
from bala_enemigo import BalaEnemigo
import pygame
import math
import os

class Enemigo(Base):
    def __init__(self, x, y, velocidad=2, vida=5, daño=1):
        super().__init__(x, y)

        self.velocidad = velocidad
        self.vida = vida
        self.daño = daño

        self.delay_entrada = 1000
        self.tiempo_spawn = pygame.time.get_ticks()

        self.ancho = 40
        self.alto = 40
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        self.cooldown_daño = 700
        self.ultimo_hit = 0

        self.dimensiones = (60, 70)

        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.join(ruta_raiz, "imagenes", "enemigos", "perseguidor")

        # Carga secuencial de los frames independientes
        self.anim_frente = []
        for i in range(1, 4):
            ruta = os.path.join(ruta_carpeta, f"ene_perseguidor_{i}.png")
            if os.path.exists(ruta):
                self.anim_frente.append(pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), self.dimensiones))

        self.anim_espalda = []
        for i in range(1, 3):
            ruta = os.path.join(ruta_carpeta, f"ene_perseguidor_espalda_{i}.png")
            if os.path.exists(ruta):
                self.anim_espalda.append(pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), self.dimensiones))

        # --- Variables de control para la animacion ---
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 130 # ms de cada paso

        # Sprite por defecto por si las moscas
        self.sprite = self.anim_frente[0] if self.anim_frente else None

    def puede_actuar(self):
        tiempo_actual = pygame.time.get_ticks()
        return tiempo_actual - self.tiempo_spawn >= self.delay_entrada

    def resetear_delay(self):
        self.tiempo_spawn = pygame.time.get_ticks()

    def seguir_jugador(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        # Logica de persecucion
        if distancia != 0:
            dx /= distancia
            dy /= distancia

            self.x += dx * self.velocidad
            self.y += dy * self.velocidad

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            # Cambiamos la direccion visual según el eje vertical
            if dy < 0:
                self.direccion_actual = "ARRIBA"
            else:
                self.direccion_actual = "ABAJO"

            self.esta_moviendose = True
        else:
            self.esta_moviendose = False

    def actualizar_animacion(self):
        tiempo_actual = pygame.time.get_ticks()

        # Seleccionamos la lista segun corresponda
        if self.direccion_actual == "ARRIBA" and self.anim_espalda:
            anim_activa = self.anim_espalda
        elif self.anim_frente:
            anim_activa = self.anim_frente
        else:
            return

        if self.esta_moviendose:
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(anim_activa)
                self.tiempo_ultimo_frame = tiempo_actual
            
            # ajustamos el indice por las dudas si cambia de animacion
            self.indice_animacion = self.indice_animacion % len(anim_activa)
            self.sprite = anim_activa[self.indice_animacion]
        else:
            self.sprite = anim_activa[0]

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

    def recibir_dano(self, cantidad):
        self.vida -= cantidad

    def esta_muerto(self):
       return self.vida <= 0

    def dibujar(self, pantalla):
        if self.sprite:
            pantalla.blit(self.sprite, (self.x - (self.dimensiones[0] - self.ancho) // 2, self.y - (self.dimensiones[1] - self.alto)))
        else:
            centro_x = int(self.x + self.ancho / 2)
            centro_y = int(self.y + self.alto / 2)
            pygame.draw.circle(pantalla, (200, 50, 50), (centro_x, centro_y), 20)
            pygame.draw.circle(pantalla, (120, 0, 0), (centro_x, centro_y), 9)

    def actualizar(self, jugador, *args):
        # Espera antes de activarse
        if not self.puede_actuar():
            return
        self.seguir_jugador(jugador)
        self.colision_con_jugador(jugador)
        self.actualizar_animacion()


class EnemigoDisparador(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=0, vida=3, daño=1)

        self.cooldown_disparo = 1500
        self.ultimo_disparo = 0

        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta_disp = os.path.join(ruta_raiz, "imagenes", "enemigos", "disparador")
        
        if not os.path.exists(ruta_carpeta_disp):
            ruta_carpeta_disp = os.path.join(ruta_raiz, "imagenes", "enemigo", "disparador")

        self.anim_frente = []
        for i in range(1, 2):
            ruta = os.path.join(ruta_carpeta_disp, f"ene_disparador_{i}.png")
            if os.path.exists(ruta):
                self.anim_frente.append(pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), self.dimensiones))

        self.anim_espalda = []
        ruta_esp = os.path.join(ruta_carpeta_disp, "ene_disparador_espalda_1.png")
        if os.path.exists(ruta_esp):
            self.anim_espalda.append(pygame.transform.scale(pygame.image.load(ruta_esp).convert_alpha(), self.dimensiones))

        # Sprite inicial
        self.sprite = self.anim_frente[0] if self.anim_frente else None

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

        bala = BalaEnemigo(
            self.x + self.ancho / 2,
            self.y + self.alto / 2,
            dx,
            dy,
            daño=self.daño
        )

        lista_balas.append(bala)
        self.ultimo_disparo = tiempo_actual

        print("ENEMIGO DISPARÓ")

    def actualizar_animacion_disparador(self, jugador):
        tiempo_actual = pygame.time.get_ticks()

        # Cambiamos orientacion segun la posicion de isaac
        if jugador.y < self.y:
            self.direccion_actual = "ARRIBA"
        else:
            self.direccion_actual = "ABAJO"

        # Seteamos el frame que corresponde
        if self.direccion_actual == "ARRIBA" and self.anim_espalda:
            self.sprite = self.anim_espalda[0]
        elif self.anim_frente:
            if tiempo_actual - self.ultimo_disparo < 250 and len(self.anim_frente) > 1:
                self.sprite = self.anim_frente[1]
            else:
                self.sprite = self.anim_frente[0]

    def actualizar(self, jugador, lista_balas=None):
        # Espera antes de activarse
        if not self.puede_actuar():
            return 
        self.colision_con_jugador(jugador)
        self.disparar(jugador, lista_balas)
        self.actualizar_animacion_disparador(jugador)

    def dibujar(self, pantalla):
        if self.sprite:
            pantalla.blit(self.sprite, (self.x - (self.dimensiones[0] - self.ancho) // 2, self.y - (self.dimensiones[1] - self.alto)))
        else:
            centro_x = int(self.x + self.ancho / 2)
            centro_y = int(self.y + self.alto / 2)
            pygame.draw.circle(pantalla, (50, 50, 200), (centro_x, centro_y), 20)
            pygame.draw.circle(pantalla, (20, 20, 120), (centro_x, centro_y), 9)