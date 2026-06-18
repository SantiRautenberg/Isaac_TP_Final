# mapa.py
import pygame
import random
from base import Base
from enemigo import Enemigo, EnemigoDisparador

presets_salas_comunes = [
    {
        "nombre": "bloques_centro",
        "obstaculos": [
            (200, 200, 100, 50),
            (400, 300, 80, 80)
        ],
        "enemigos": [
            (600, 150),
            (600, 450),
            (600, 350)
        ]
    },
    {
        "nombre": "pasillo_horizontal",
        "obstaculos": [
            (180, 260, 160, 50),
            (460, 260, 160, 50)
        ],
        "enemigos": [
            (300, 150),
            (500, 450),
            (300, 450)
        ]
    },
    {
        "nombre": "cuatro_piedras",
        "obstaculos": [
            (180, 160, 80, 80),
            (540, 160, 80, 80),
            (180, 360, 80, 80),
            (540, 360, 80, 80)
        ],
        "enemigos": [
            (400, 180),
            (400, 420),
            (400, 310)
        ]
    },
    {
        "nombre": "sala_limpia_con_enemigos",
        "obstaculos": [],
        "enemigos": [
            (250, 250),
            (550, 350),
            (350, 150)
        ]
    }
]

class Obstaculo(Base):
    def __init__(self, x, y, ancho, alto, color=(100, 100, 100)):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def actualizar(self, pantalla, *args):
        pass
    
    
class Mapa(Base):
    def __init__(self):
        super().__init__(0, 0)
        self.pisos = {}
        self.piso_actual = None

        self.crear_mapa()

    def crear_mapa(self):
        self.pisos[1] = Piso(1)
        self.pisos[2] = Piso(2)
        self.pisos[3] = Piso(3)

        self.piso_actual = self.pisos[1]

    def cambiar_piso(self, numero_piso):
        if numero_piso in self.pisos:
            self.piso_actual = self.pisos[numero_piso]

    def cambiar_sala(self, nombre_sala):
        if self.piso_actual is not None:
            self.piso_actual.cambiar_sala(nombre_sala)

    def dibujar(self, pantalla):
        if self.piso_actual is not None:
            self.piso_actual.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, lista_balas=None):
        if self.piso_actual is not None:
          self.piso_actual.actualizar(
            pantalla,
            jugador,
            lista_balas
         )

    def colision(self, rect_jugador):
        if self.piso_actual is not None:
            return self.piso_actual.colision(rect_jugador)
        return False
    
    def cambiar_sala_por_direccion(self, direccion):
        if self.piso_actual is not None:
            return self.piso_actual.cambiar_sala_por_direccion(direccion)
        return False

class Piso(Base):
    def __init__(self, numero):
        super().__init__(0, 0)
        self.numero = numero
        self.salas = {}
        self.sala_actual = None

        self.crear_piso()

    def crear_piso(self):
        self.salas["comun_1"] = self.crear_sala_comun("comun_1")
        self.salas["comun_2"] = self.crear_sala_comun("comun_2")
        self.salas["comun_3"] = self.crear_sala_comun("comun_3")
        self.salas["comun_4"] = self.crear_sala_comun("comun_4")

        self.salas["tesoro"] = Sala("tesoro", tipo="tesoro", color_fondo=(45, 40, 20))
        self.salas["boss"] = Sala("boss", tipo="boss", color_fondo=(45, 20, 20))

        # =====================[CONEXIONES ENTRE SALAS]=====================

        self.salas["comun_1"].conectar("DERECHA", "comun_2")
        self.salas["comun_1"].conectar("ABAJO", "comun_3")
        self.salas["comun_2"].conectar("IZQUIERDA", "comun_1")
        self.salas["comun_2"].conectar("DERECHA", "tesoro")
        self.salas["comun_3"].conectar("ARRIBA", "comun_1")
        self.salas["comun_3"].conectar("DERECHA", "comun_4")
        self.salas["comun_4"].conectar("IZQUIERDA", "comun_3")
        self.salas["comun_4"].conectar("DERECHA", "boss")
        self.salas["tesoro"].conectar("IZQUIERDA", "comun_2")
        self.salas["boss"].conectar("IZQUIERDA", "comun_4")

 
        self.sala_actual = self.salas["comun_1"]

    def crear_sala_comun(self, nombre):
        sala = Sala(nombre, tipo="comun", color_fondo=(35, 30, 35))

        preset = random.choice(presets_salas_comunes)

        for x, y, ancho, alto in preset["obstaculos"]:
            sala.agregar_obstaculo(
                Obstaculo(x, y, ancho, alto)
            )

        for i, (x, y) in enumerate(preset["enemigos"]):

            if i == 0:
              sala.agregar_enemigo(
              EnemigoDisparador(x, y)
             )
            else:
              sala.agregar_enemigo(
              Enemigo(x, y)
             )

        return sala
    def cambiar_sala(self, nombre_sala):
        if nombre_sala in self.salas:
            self.sala_actual = self.salas[nombre_sala]

    def dibujar(self, pantalla):
        if self.sala_actual is not None:
            self.sala_actual.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, lista_balas=None):
        self.sala_actual.actualizar(
             pantalla,
             jugador,
             lista_balas
            )

    def colision(self, rect_jugador):
        if self.sala_actual is not None:
            return self.sala_actual.colision(rect_jugador)
        return False

    def cambiar_sala_por_direccion(self, direccion):
        if self.sala_actual is None:
            return False

        if direccion in self.sala_actual.conexiones:
            nombre_siguiente = self.sala_actual.conexiones[direccion]
            self.sala_actual = self.salas[nombre_siguiente]
            return True
        return False

class Sala(Base):
    def __init__(self, nombre, tipo="comun", color_fondo=(35, 30, 35)):
        super().__init__(0, 0)
        self.nombre = nombre
        self.tipo = tipo
        self.color_fondo = color_fondo
        self.obstaculos = []
        self.enemigos = []
        self.conexiones = {}

    def conectar(self, direccion, nombre_sala):
        self.conexiones[direccion] = nombre_sala

    def agregar_obstaculo(self, obstaculo):
        self.obstaculos.append(obstaculo)

    def agregar_enemigo(self, enemigo):
        self.enemigos.append(enemigo)

    def dibujar(self, pantalla):
        pantalla.fill(self.color_fondo)

        for obstaculo in self.obstaculos:
            obstaculo.dibujar(pantalla)

        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, lista_balas=None):
        if jugador is not None:
            for enemigo in self.enemigos:

              if lista_balas is not None:
                enemigo.actualizar(jugador, lista_balas)
              else:
                enemigo.actualizar(jugador)

    def colision(self, rect_jugador):
        for obstaculo in self.obstaculos:
            if rect_jugador.colliderect(obstaculo.rect):
                return True
        return False
