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

    def ActualizarAnimacion(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.esta_moviendose:
            # Si el usuario se mueve, recorremos la lista de caminata de forma cíclica
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_caminando)
                self.sprite = self.animacion_caminando[self.indice_animacion]
                
                # Si camina hacia la izquierda, invertimos horizontalmente el sprite de caminata lateral
                if self.direccion_actual == "IZQUIERDA":
                    self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.tiempo_ultimo_frame = tiempo_actual
        else:
            # Si se queda quieto, volvemos a la dirección estática hacia donde miraba
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