# personaje.py
from base import Base # Importa clase abstracta
import pygame
import os


class Jugador(Base):
    
    def __init__(self, nombre, vida, vel_movimiento, daño, proyectil, rango, x, y):
        super().__init__(x, y)
        self.nombre = nombre
        self.vida = vida
        self.vel_movimiento = vel_movimiento
        self.daño = daño
        self.proyectil = proyectil
        self.rango = rango

        # Escalado uniforme para todos los sprites del personaje
        self.dimensiones = (75, 75)

        # Ruta
        ruta_carpeta = os.path.join(os.path.dirname(__file__), "imagenes", "jugador") # Obtiene la ruta del directorio actual

        # Los sprites para cada direccion se guardan por separado
        self.sprites_direcciones = {
            "ABAJO":     pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_frente.png")).convert_alpha(), self.dimensiones),
            "ARRIBA":    pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_atras.png")).convert_alpha(), self.dimensiones),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_izq.png")).convert_alpha(), self.dimensiones),
            "DERECHA":   pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "isaac_der.png")).convert_alpha(), self.dimensiones)
        }

        # La animacion de movimiento se guarda en un archivo con los 4 frames
        anim_caminar = pygame.image.load(os.path.join(ruta_carpeta, "isaac_caminando.png")).convert_alpha()
        ancho_tira = anim_caminar.get_width()
        alto_tira = anim_caminar.get_height()
        ancho_cuadro = ancho_tira // 4  # Se divide en los 4 cuadros horizontales

        self.animacion_caminando = []
        for i in range(4):
            # Recortamos cada frame de la tira horizontal
            sub_cuadro = anim_caminar.subsurface((i * ancho_cuadro, 0, ancho_cuadro, alto_tira))
            # Lo escalamos a nuestras dimensiones de juego y lo guardamos
            self.animacion_caminando.append(pygame.transform.scale(sub_cuadro, self.dimensiones))

        # --- Variables de control para los estados y el tiempo ---
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 130  # ms de cada paso

        # sprite por defecto (Sprite de mirar hacia abajo)
        self.sprite = self.sprites_direcciones[self.direccion_actual]
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    def actualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_caminando)
                self.tiempo_ultimo_frame = tiempo_actual
            
            # Se ejecuta en cada frame del juego 
            self.sprite = self.animacion_caminando[self.indice_animacion]
                
            # Si camina hacia la izquierda, invertimos horizontalmente el cuadro actual
            if self.direccion_actual == "DERECHA": #ahora si camina a la derecha
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            # Si se queda quieto, vuelve al sprite estático de su dirección
            self.sprite = self.sprites_direcciones[self.direccion_actual]
            self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    def Moverse(self, keys, mapa):
        self.esta_moviendose = False

        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx = -self.vel_movimiento
            self.direccion_actual = "IZQUIERDA"
            self.esta_moviendose = True
        elif keys[pygame.K_d]:
            dx = self.vel_movimiento
            self.direccion_actual = "DERECHA"
            self.esta_moviendose = True

        if keys[pygame.K_w]:
            dy = -self.vel_movimiento
            self.direccion_actual = "ARRIBA"
            self.esta_moviendose = True
        elif keys[pygame.K_s]:
            dy = self.vel_movimiento
            self.direccion_actual = "ABAJO"
            self.esta_moviendose = True

        # Probar movimiento en X
        nuevo_rect = self.rect.copy()
        nuevo_rect.x += dx

        if not mapa.colision(nuevo_rect):
            self.x += dx
            self.rect.x = self.x

        # Probar movimiento en Y
        nuevo_rect = self.rect.copy()
        nuevo_rect.y += dy

        if not mapa.colision(nuevo_rect):
            self.y += dy
            self.rect.y = self.y

        self.actualizarAnimacion()
 
    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))

    def actualizar(self, pantalla, keys, mapa):
        self.Moverse(keys, mapa)


    
