# mapa.py
import pygame
import random
import os

from base import Base
from enemigo import Enemigo, EnemigoDisparador
from jefes import JefePiso1, JefePiso2, JefePiso3
from audio import AudioManager

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TAM_ROCA = 60


# ============================================================
# FUNCIONES PARA LIMPIAR FONDO DE SPRITES SIN CONGELAR EL JUEGO
# ============================================================

def quitar_fondo_por_esquinas(superficie, tolerancia=55):
    superficie = superficie.convert_alpha()

    ancho = superficie.get_width()
    alto = superficie.get_height()

    colores_fondo = [
        superficie.get_at((0, 0))[:3],
        superficie.get_at((ancho - 1, 0))[:3],
        superficie.get_at((0, alto - 1))[:3],
        superficie.get_at((ancho - 1, alto - 1))[:3],
    ]

    for x in range(ancho):
        for y in range(alto):
            r, g, b, a = superficie.get_at((x, y))

            if a == 0:
                continue

            # Borra blancos/grises claros del fondo cuadriculado
            es_claro = r > 205 and g > 205 and b > 205

            # Borra colores parecidos a las esquinas
            es_fondo = False
            for fr, fg, fb in colores_fondo:
                if (
                    abs(r - fr) <= tolerancia and
                    abs(g - fg) <= tolerancia and
                    abs(b - fb) <= tolerancia
                ):
                    es_fondo = True
                    break

            if es_claro or es_fondo:
                superficie.set_at((x, y), (r, g, b, 0))

    return superficie


def recortar_a_contenido(superficie):
    superficie = superficie.convert_alpha()
    rect = superficie.get_bounding_rect()

    if rect.width == 0 or rect.height == 0:
        return superficie

    return superficie.subsurface(rect).copy()


def limpiar_sprite(superficie, tamanio_final, tolerancia=55):
    superficie = superficie.convert_alpha()

    superficie = pygame.transform.scale(superficie, tamanio_final)
    superficie = quitar_fondo_por_esquinas(superficie, tolerancia)
    superficie = recortar_a_contenido(superficie)
    superficie = pygame.transform.scale(superficie, tamanio_final)

    return superficie


# ============================================================
# TEXTURAS DEL MAPA
# ============================================================

class TexturasMapa:
    def __init__(self):
        ruta_mapa = os.path.join(os.path.dirname(__file__), "imagenes", "mapa")
        self.sala_tutorial = self.cargar_imagen(os.path.join(ruta_mapa, "basement_guia.png"))
        ruta_sala_comun = os.path.join(ruta_mapa, "sala_comun.png")

        self.sala_comun = self.cargar_imagen(ruta_sala_comun)

        self.puertas_sheet = self.cargar_imagen(os.path.join(ruta_mapa, "puertas_0.png"))
        self.roca = self.cargar_imagen(os.path.join(ruta_mapa, "roca_0.png"))
        self.trampilla_cerrada = self.cargar_imagen(os.path.join(ruta_mapa, "escotilla_cerrada.png"))
        self.trampilla_abierta = self.cargar_imagen(os.path.join(ruta_mapa, "escotilla_abierta.png"))

        self.sala_tutorial_fondo = None
        self.sala_comun_fondo = None

        self.puertas = {
            "ARRIBA": None,
            "ABAJO": None,
            "IZQUIERDA": None,
            "DERECHA": None
        }

        if self.roca is not None:
            self.roca = limpiar_sprite(self.roca, (TAM_ROCA, TAM_ROCA), tolerancia=60)

        if self.trampilla_cerrada is not None:
            self.trampilla_cerrada = limpiar_sprite(
                self.trampilla_cerrada,
                (90, 90),
                tolerancia=60
            )

        if self.trampilla_abierta is not None:
            self.trampilla_abierta = limpiar_sprite(
                self.trampilla_abierta,
                (120, 120),
                tolerancia=60
            )

        self.preparar_texturas()

    def cargar_imagen(self, ruta, tamanio=None):
        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()

            if tamanio is not None:
                imagen = pygame.transform.scale(imagen, tamanio)

            return imagen

        print(f"[Aviso] No se encontró la imagen: {ruta}")
        return None

    def preparar_texturas(self):
        if self.sala_tutorial is not None:
            self.sala_tutorial_fondo = pygame.transform.scale(
                self.sala_tutorial,
                (ANCHO_PANTALLA, ALTO_PANTALLA)
            )

        if self.sala_comun is not None:
            self.sala_comun_fondo = pygame.transform.scale(
                self.sala_comun,
                (ANCHO_PANTALLA, ALTO_PANTALLA)
            )

        self.preparar_puertas()

    def recortar_relativo(self, imagen, rx, ry, rw, rh, tamanio_final):
        ancho = imagen.get_width()
        alto = imagen.get_height()

        rect = pygame.Rect(
            int(ancho * rx),
            int(alto * ry),
            int(ancho * rw),
            int(alto * rh)
        )

        recorte = imagen.subsurface(rect).copy()

        recorte = limpiar_sprite(
            recorte,
            tamanio_final,
            tolerancia=65
        )

        return recorte

    def preparar_puertas(self):
        self.puertas = {
            "ARRIBA": None,
            "ABAJO": None,
            "IZQUIERDA": None,
            "DERECHA": None
        }

        if self.puertas_sheet is None:
            return

        self.puertas["ARRIBA"] = self.recortar_relativo(
            self.puertas_sheet,
            0.27, 0.03, 0.46, 0.28,
            (150, 90)
        )

        self.puertas["ABAJO"] = self.recortar_relativo(
            self.puertas_sheet,
            0.28, 0.68, 0.46, 0.28,
            (150, 90)
        )

        self.puertas["IZQUIERDA"] = self.recortar_relativo(
            self.puertas_sheet,
            0.04, 0.32, 0.25, 0.38,
            (90, 150)
        )

        self.puertas["DERECHA"] = self.recortar_relativo(
            self.puertas_sheet,
            0.72, 0.32, 0.25, 0.38,
            (90, 150)
        )


# ============================================================
# TRAMPILLA / ESCOTILLA PARA CAMBIO DE PISO
# ============================================================

class Trampilla(Base):
    def __init__(self, x, y, imagen_cerrada, imagen_abierta):
        super().__init__(x, y)

        self.imagen_cerrada = imagen_cerrada
        self.imagen_abierta = imagen_abierta

        self.visible = False
        self.abierta = False

        self.imagen_actual = self.imagen_cerrada

        if self.imagen_actual is not None:
            self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, 90, 90)

    def abrir(self):
        self.visible = True
        self.abierta = True
        self.imagen_actual = self.imagen_abierta

        if self.imagen_actual is not None:
            self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y))
        
        AudioManager.play_sfx("trampilla_abierta")

    def cerrar(self):
        self.visible = True
        self.abierta = False
        self.imagen_actual = self.imagen_cerrada

        if self.imagen_actual is not None:
            self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y))

    def dibujar(self, pantalla):
        if self.visible and self.imagen_actual is not None:
            pantalla.blit(self.imagen_actual, (self.x, self.y))

    def actualizar(self, pantalla, *args):
        pass


# ============================================================
# OBSTÁCULOS
# ============================================================

class Obstaculo(Base):
    def __init__(self, x, y, ancho, alto, color=(100, 100, 100), imagen=None):
        super().__init__(x, y)

        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.imagen = imagen

    def dibujar(self, pantalla):
        if self.imagen is not None:
            self.dibujar_rocas_en_mosaico(pantalla)
        else:
            pygame.draw.rect(pantalla, self.color, self.rect)

    def dibujar_rocas_en_mosaico(self, pantalla):
        for y in range(self.rect.y, self.rect.y + self.rect.height, TAM_ROCA):
            for x in range(self.rect.x, self.rect.x + self.rect.width, TAM_ROCA):
                pantalla.blit(self.imagen, (x, y))

    def actualizar(self, pantalla, *args):
        pass


# ============================================================
# SALA
# ============================================================

class Sala(Base):
    def __init__(self, nombre, tipo="comun", color_fondo=(35, 30, 35), texturas=None):
        super().__init__(0, 0)

        self.nombre = nombre
        self.tipo = tipo
        self.color_fondo = color_fondo
        self.texturas = texturas

        self.obstaculos = []
        self.enemigos = []
        self.conexiones = {}

        self.trampilla = None

        # variables para el delay de enemigos comunes
        self.enemigos_guardados = []
        self.tiempo_inicio_spawn = 0
        self.timer_spawn_listo = False

        # variables para el jefe
        self.jefe_guardado = None
        self.tiempo_entrada = 0

        if self.tipo == "boss" and self.texturas is not None:
            self.trampilla = Trampilla(
                340,
                240,
                self.texturas.trampilla_cerrada,
                self.texturas.trampilla_abierta
            )

    def conectar(self, direccion, nombre_sala):
        self.conexiones[direccion] = nombre_sala

    def agregar_obstaculo(self, obstaculo):
        self.obstaculos.append(obstaculo)

    def agregar_enemigo(self, enemigo):
        self.enemigos.append(enemigo)

    def dibujar_fondo(self, pantalla):
        if self.tipo == "tutorial":
            if self.texturas is not None and self.texturas.sala_tutorial_fondo is not None:
                pantalla.blit(self.texturas.sala_tutorial_fondo, (0, 0))
            else:
                pantalla.fill(self.color_fondo)
        else:
            if self.texturas is not None and self.texturas.sala_comun_fondo is not None:
                pantalla.blit(self.texturas.sala_comun_fondo, (0, 0))
            else:
                pantalla.fill(self.color_fondo)

        self.dibujar_puertas(pantalla)

    def dibujar_puertas(self, pantalla):
        for direccion in self.conexiones:
            self.dibujar_puerta(pantalla, direccion)

    def dibujar_puerta(self, pantalla, direccion):
        if self.texturas is None:
            return

        puerta = self.texturas.puertas.get(direccion)

        if puerta is None:
            return

        if direccion == "ARRIBA":
            x = ANCHO_PANTALLA // 2 - puerta.get_width() // 2
            y = 5

        elif direccion == "ABAJO":
            x = ANCHO_PANTALLA // 2 - puerta.get_width() // 2
            y = ALTO_PANTALLA - puerta.get_height() - 5

        elif direccion == "IZQUIERDA":
            x = 5
            y = ALTO_PANTALLA // 2 - puerta.get_height() // 2

        elif direccion == "DERECHA":
            x = ANCHO_PANTALLA - puerta.get_width() - 5
            y = ALTO_PANTALLA // 2 - puerta.get_height() // 2

        else:
            return

        pantalla.blit(puerta, (x, y))

    def dibujar(self, pantalla):
        self.dibujar_fondo(pantalla)

        for obstaculo in self.obstaculos:
            obstaculo.dibujar(pantalla)

        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)

        if self.trampilla is not None:
            self.trampilla.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, lista_balas=None):
        for obstaculo in self.obstaculos:
            obstaculo.actualizar(pantalla)

        if jugador is not None:
            for enemigo in self.enemigos[:]:
                if isinstance(enemigo, EnemigoDisparador):
                    enemigo.actualizar(jugador, lista_balas)
                else:
                    enemigo.actualizar(jugador, lista_balas, self.enemigos)

                if enemigo.vida <= 0:
                    self.enemigos.remove(enemigo)

        # Si es sala boss y ya no quedan enemigos, aparece la trampilla abierta
        if self.tipo == "boss" and self.trampilla is not None:
            # checkeamos que el jefe ya haya spawneado de la lista de espera
            if self.jefe_guardado is None and len(self.enemigos) == 0:
                if not self.trampilla.abierta:
                    self.trampilla.abrir()

    def al_entrar(self, tiempo_actual):
        for enemigo in self.enemigos:
            enemigo.resetear_delay(tiempo_actual)

    def colision(self, rect_jugador):
        for obstaculo in self.obstaculos:
            if rect_jugador.colliderect(obstaculo.rect):
                return True

        return False

    def jugador_en_trampilla(self, rect_jugador):
        if self.trampilla is None:
            return False

        if not self.trampilla.visible:
            return False

        if not self.trampilla.abierta:
            return False

        return rect_jugador.colliderect(self.trampilla.rect)


# ============================================================
# PRESETS DE SALAS
# ============================================================

presets_salas_comunes = [
    {
        "nombre": "linea_rocas",
        "obstaculos": [
            (200, 250, 120, 60),
            (430, 310, 120, 120),
        ],
        "enemigos": [
            (600, 150, "normal"),
            (400, 350, "disparador"),
        ]
    },
    {
        "nombre": "bloques_2x2",
        "obstaculos": [
            (200, 200, 120, 120),
            (500, 300, 120, 120),
        ],
        "enemigos": [
            (400, 250, "disparador"),
        ]
    },
    {
        "nombre": "bloques_en_fila",
        "obstaculos": [
            (180, 250, 240, 60),
            (500, 250, 120, 120),
        ],
        "enemigos": [
            (400, 350, "normal"),
            (600, 180, "disparador"),
        ]
    },
]


# ============================================================
# PISO
# ============================================================

class Piso(Base):
    def __init__(self, numero, texturas):
        super().__init__(0, 0)

        self.numero = numero
        self.texturas = texturas

        self.salas = {}
        self.sala_actual = None
        self.posiciones_salas = {}

        self.crear_piso()

    def crear_piso(self):
        # Piso 1 empieza con sala tutorial
        if self.numero == 1:
            self.salas["comun_1"] = Sala(
                "comun_1",
                tipo="tutorial",
                color_fondo=(35, 30, 35),
                texturas=self.texturas
            )
        else:
            self.salas["comun_1"] = self.crear_sala_comun("comun_1")

        self.salas["comun_2"] = self.crear_sala_comun("comun_2")
        self.salas["comun_3"] = self.crear_sala_comun("comun_3")
        self.salas["comun_4"] = self.crear_sala_comun("comun_4")

        # Sala tesoro sin enemigos ni obstáculos
        self.salas["tesoro"] = Sala(
            "tesoro",
            tipo="tesoro",
            color_fondo=(45, 40, 20),
            texturas=self.texturas
        )

        # Sala boss
        self.salas["boss"] = Sala(
            "boss",
            tipo="boss",
            color_fondo=(45, 20, 20),
            texturas=self.texturas
        )
        self.salas["boss"].jefe_guardado = self.crear_jefe_del_piso()
        self.salas["boss"].tiempo_entrada = 0

        self.generar_conexiones_aleatorias()

        self.sala_actual = self.salas["comun_1"]

    def generar_conexiones_aleatorias(self):
        direcciones = {
            "ARRIBA": (0, -1),
            "ABAJO": (0, 1),
            "IZQUIERDA": (-1, 0),
            "DERECHA": (1, 0)
        }

        coords = [(0, 0)]

        while len(coords) < 6:
            origen = random.choice(coords)
            opciones = list(direcciones.values())
            random.shuffle(opciones)

            for dx, dy in opciones:
                nueva = (origen[0] + dx, origen[1] + dy)

                if nueva not in coords:
                    coords.append(nueva)
                    break

        inicio = (0, 0)
        posibles_especiales = [coord for coord in coords if coord != inicio]

        coord_boss = max(
            posibles_especiales,
            key=lambda coord: abs(coord[0] - inicio[0]) + abs(coord[1] - inicio[1])
        )

        posibles_tesoro = [
            coord for coord in posibles_especiales
            if coord != coord_boss
        ]
        coord_tesoro = random.choice(posibles_tesoro)

        coords_comunes = [
            coord for coord in coords
            if coord not in (inicio, coord_boss, coord_tesoro)
        ]
        random.shuffle(coords_comunes)

        coord_a_sala = {
            inicio: "comun_1",
            coord_boss: "boss",
            coord_tesoro: "tesoro"
        }

        nombres_comunes = ["comun_2", "comun_3", "comun_4"]

        for nombre, coord in zip(nombres_comunes, coords_comunes):
            coord_a_sala[coord] = nombre

        self.posiciones_salas = {
            nombre: coord
            for coord, nombre in coord_a_sala.items()
        }

        for coord, nombre_sala in coord_a_sala.items():
            sala = self.salas[nombre_sala]

            for direccion, (dx, dy) in direcciones.items():
                vecina = (coord[0] + dx, coord[1] + dy)

                if vecina in coord_a_sala:
                    sala.conectar(direccion, coord_a_sala[vecina])

    def crear_jefe_del_piso(self):
        if self.numero == 1:
            return JefePiso1(360, 250)

        if self.numero == 2:
            return JefePiso2(360, 250)

        if self.numero == 3:
            return JefePiso3(360, 250)

        return JefePiso1(360, 250)

    def crear_sala_comun(self, nombre):
        sala = Sala(
            nombre,
            tipo="comun",
            color_fondo=(35, 30, 35),
            texturas=self.texturas
        )

        preset = random.choice(presets_salas_comunes)

        for x, y, ancho, alto in preset["obstaculos"]:
            sala.agregar_obstaculo(
                Obstaculo(
                    x,
                    y,
                    ancho,
                    alto,
                    imagen=self.texturas.roca
                )
            )

        for datos_enemigo in preset["enemigos"]:
            x = datos_enemigo[0]
            y = datos_enemigo[1]

            tipo = "normal"

            if len(datos_enemigo) >= 3:
                tipo = datos_enemigo[2]

            if tipo == "disparador":
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
            
            # Delay de spawn de enemigos con sonido
            if len(self.sala_actual.enemigos) > 0 and not self.sala_actual.timer_spawn_listo:
                self.sala_actual.enemigos_guardados = self.sala_actual.enemigos
                self.sala_actual.enemigos = []
                self.sala_actual.tiempo_inicio_spawn = pygame.time.get_ticks()
            
            # Sonido de cierre de puertas
            if self.sala_actual.tipo == "boss" and self.sala_actual.jefe_guardado is not None:
                if self.sala_actual.tiempo_entrada == 0:
                    self.sala_actual.tiempo_entrada = pygame.time.get_ticks()
                    AudioManager.play_sfx("spawn_jefe")

        tiempo_actual = pygame.time.get_ticks()
        for enemigo in self.sala_actual.enemigos:
            enemigo.tiempo_spawn = tiempo_actual 
            enemigo.resetear_delay()           
        print(
            "Sala actual:",
            self.sala_actual.nombre,
            "- tipo:",
            self.sala_actual.tipo,
            "- obstaculos:",
            len(self.sala_actual.obstaculos),
            "- enemigos:",
            len(self.sala_actual.enemigos))

    def cambiar_sala_por_direccion(self, direccion):
        if self.sala_actual is None:
            return False

        if direccion in self.sala_actual.conexiones:
            nombre_siguiente = self.sala_actual.conexiones[direccion]
            self.cambiar_sala(nombre_siguiente)
            return True

        return False

    def dibujar(self, pantalla):
        if self.sala_actual is not None:
            self.sala_actual.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, balas=None):
        if self.sala_actual is not None:
            # Los enemigos se spawnean al 0.5 segundo
            if len(self.sala_actual.enemigos_guardados) > 0:
                if pygame.time.get_ticks() - self.sala_actual.tiempo_inicio_spawn >= 500:
                    AudioManager.play_sfx("spawn_enemigos")
                    self.sala_actual.enemigos = self.sala_actual.enemigos_guardados
                    self.sala_actual.enemigos_guardados = []
                    self.sala_actual.timer_spawn_listo = True

            # Se spawnea el jefe 1 sec despues
            if self.sala_actual.tipo == "boss" and self.sala_actual.jefe_guardado is not None:
                if pygame.time.get_ticks() - self.sala_actual.tiempo_entrada >= 1000:
                    AudioManager.play_sfx("spawn_enemigos")
                    self.sala_actual.agregar_enemigo(self.sala_actual.jefe_guardado)
                    self.sala_actual.jefe_guardado = None

            self.sala_actual.actualizar(pantalla, jugador, balas)

    def colision(self, rect_jugador):
        if self.sala_actual is not None:
            return self.sala_actual.colision(rect_jugador)
        return False

    def jugador_en_trampilla(self, rect_jugador):
        if self.sala_actual is not None:
            return self.sala_actual.jugador_en_trampilla(rect_jugador)
        return False


# ============================================================
# MAPA
# ============================================================

class Mapa(Base):
    def __init__(self):
        super().__init__(0, 0)

        self.texturas = TexturasMapa()

        self.pisos = {}
        self.piso_actual = None

        self.crear_mapa()

    def crear_mapa(self):
        self.pisos[1] = Piso(1, self.texturas)
        self.pisos[2] = Piso(2, self.texturas)
        self.pisos[3] = Piso(3, self.texturas)

        self.piso_actual = self.pisos[1]

    def cambiar_piso(self, numero_piso):
        if numero_piso in self.pisos:
            self.piso_actual = self.pisos[numero_piso]
            print("Piso actual:", numero_piso)

    def pasar_siguiente_piso(self):
        numero_actual = self.obtener_numero_piso_actual()
        siguiente = numero_actual + 1

        if siguiente in self.pisos:
            self.cambiar_piso(siguiente)
            return True

        return False

    def obtener_numero_piso_actual(self):
        if self.piso_actual is not None:
            return self.piso_actual.numero

        return 1

    def cambiar_sala(self, nombre_sala):
        if self.piso_actual is not None:
            self.piso_actual.cambiar_sala(nombre_sala)

    def cambiar_sala_por_direccion(self, direccion):
        if self.piso_actual is not None:
            return self.piso_actual.cambiar_sala_por_direccion(direccion)

        return False

    def dibujar(self, pantalla):
        if self.piso_actual is not None:
            self.piso_actual.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, balas=None):
        if self.piso_actual is not None:
            self.piso_actual.actualizar(pantalla, jugador, balas)

    def colision(self, rect_jugador):
        if self.piso_actual is not None:
            return self.piso_actual.colision(rect_jugador)

        return False

    def jugador_en_trampilla(self, rect_jugador):
        if self.piso_actual is not None:
            return self.piso_actual.jugador_en_trampilla(rect_jugador)

        return False
