# personaje.py
from base import Base # Importa clase abstracta
import pygame
import os


class Jugador(Base):
    
    def __init__(self, nombre, vida, vel_movimiento, daño, proyectil, rango, x, y):
        super().__init__(x, y)
        self.nombre = nombre
        self.__vida = vida
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

        # Inicialización de las listas de animación unificadas
        self.animacion_horizontal = []
        self.animacion_arriba = []
        self.animacion_abajo = []
        
        # -------------------- CORRECCIÓN: CARGA INDIVIDUAL POR CARPETAS --------------------
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
        self.velocidad_animacion = 130  # ms de cada paso

        # sprite por defecto (Sprite de mirar hacia abajo)
        self.sprite = self.sprites_direcciones[self.direccion_actual]
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

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

            # Control del reloj: Avanza el índice de la animación según la lista activa
            if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(animacion_activa)
                self.tiempo_ultimo_frame = tiempo_actual
            
            # Se ejecuta en cada frame del juego 
            self.sprite = animacion_activa[self.indice_animacion]
                
            # Como tu tira por defecto mira a la izquierda, aplicamos flip al ir a la DERECHA
            if self.direccion_actual == "DERECHA":
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            # Si se queda quieto, vuelve al sprite estático de su dirección
            self.sprite = self.sprites_direcciones[self.direccion_actual]
            
        self.rect = pygame.Rect(self.x, self.y, self.dimensiones[0], self.dimensiones[1])

    # Encapsulamiento

    # Getter para stats
    def get_vida(self):
        return self.__vida
    
    # Setter con validación para recibirDaño
    def set_vida(self, valor):
        self.__vida -= valor
        if self.__vida<0:
            self.__vida=0
        return self.__vida
    
    def recibirDaño(self, valor):
        self.set_vida(valor)

    def moverse(self, keys, mapa):
        self.esta_moviendose = False
        dx = 0
        dy = 0

        # 1. CAPTURA DE INTENCIÓN DE MOVIMIENTO
        if keys[pygame.K_a]:
            dx = -self.vel_movimiento
        elif keys[pygame.K_d]:
            dx = self.vel_movimiento

        if keys[pygame.K_w]:
            dy = -self.vel_movimiento
        elif keys[pygame.K_s]:
            dy = self.vel_movimiento

        # 2. PROCESAMIENTO LOGICO DE DIRECCIÓN Y ANIMACIÓN
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
                        
        # 3. PRUEBA DE COLISIONES Y ACTUALIZACIÓN DE COORDENADAS FISICAS
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

        # Sincronizamos los cambios de coordenadas con los gráficos del personaje
        self.actualizarAnimacion()
 
    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))

    def actualizar(self, pantalla, keys, mapa):
        self.Moverse(keys, mapa)