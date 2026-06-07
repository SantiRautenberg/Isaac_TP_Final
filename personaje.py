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

        # Escalado uniforme para todos los sprites del personaje
        self.dimensiones = (75, 75)

        # Ruta
        ruta_carpeta = os.path.dirname(__file__) + "/imagenes/jugador" # Obtiene la ruta del directorio actual

        # Los sprites para cada direccion se guardan por separado
        self.sprites_direcciones = {
            "ABAJO":     pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "abajo.png")).convert_alpha(), self.dimensiones),
            "ARRIBA":    pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "atras.png")).convert_alpha(), self.dimensiones),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "izquierda.png")).convert_alpha(), self.dimensiones),
            "DERECHA":   pygame.transform.scale(pygame.image.load(os.path.join(ruta_carpeta, "derecha.png")).convert_alpha(), self.dimensiones)
        }

        self.animacion_caminando_derecha = []
        self.animacion_caminando_izquierda = []

        for i in range(4):
            imagen = pygame.image.load(
                os.path.join(ruta_carpeta, f"caminar_{i}.png")
            ).convert_alpha()

            imagen = pygame.transform.scale(imagen, self.dimensiones)

            # Si tus caminar_0, caminar_1, etc. miran hacia la IZQUIERDA:
            self.animacion_caminando_izquierda.append(imagen)
            self.animacion_caminando_derecha.append(pygame.transform.flip(imagen, True, False))
#----------------------------------------------------------------------------------------------------
        # --- Variables de control para los estados y el tiempo ---
        self.direccion_actual = "ABAJO"
        self.esta_moviendose = False
        self.indice_animacion = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 130  # ms de cada paso

        # sprite por defecto (Sprite de mirar hacia abajo)
        self.sprite = self.sprites_direcciones[self.direccion_actual]

    def ActualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion += 1

                if self.direccion_actual == "IZQUIERDA":
                    animacion = self.animacion_caminando_izquierda
                elif self.direccion_actual == "DERECHA":
                    animacion = self.animacion_caminando_derecha
                else:
                    animacion = self.animacion_caminando_derecha

                self.indice_animacion = self.indice_animacion % len(animacion)
                self.sprite = animacion[self.indice_animacion]

                self.tiempo_ultimo_frame = tiempo_actual
        else:
            self.sprite = self.sprites_direcciones[self.direccion_actual]

    def Moverse(self, keys):
        # Reiniciamos el estado a Falso en cada frame. Solo cambia a Verdadero si toca una tecla.
        self.esta_moviendose = False

        if keys[pygame.K_a]:    # Izquierda
            self.x -= self.vel_movimiento
            self.direccion_actual = "IZQUIERDA"
            self.esta_moviendose = True
        elif keys[pygame.K_d]:  # Derecha
            self.x += self.vel_movimiento
            self.direccion_actual = "DERECHA"
            self.esta_moviendose = True
            
        if keys[pygame.K_w]:    # Arriba
            self.y -= self.vel_movimiento
            self.direccion_actual = "ARRIBA"
            self.esta_moviendose = True
        elif keys[pygame.K_s]:  # Abajo
            self.y += self.vel_movimiento
            self.direccion_actual = "ABAJO"
            self.esta_moviendose = True
        self.ActualizarAnimacion()
        
    def Dibujo(self, pantalla):
        # Renderiza el sprite para cada frame en la posición actual del jugador
        pantalla.blit(self.sprite, (self.x, self.y))