# mapa.py
import pygame
import random
import os
from base import Base
from audio import AudioManager
from enemigo import Enemigo, EnemigoDisparador

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TAM_ROCA = 60

# =====================[FUNCIONES DE LIMPIEZA DE SPRITES]=============================
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
            if a == 0: continue
            es_claro = r > 205 and g > 205 and b > 205
            es_fondo = False
            for fr, fg, fb in colores_fondo:
                if abs(r - fr) <= tolerancia and abs(g - fg) <= tolerancia and abs(b - fb) <= tolerancia:
                    es_fondo = True
                    break
            if es_claro or es_fondo:
                superficie.set_at((x, y), (r, g, b, 0))
    return superficie

def recortar_a_contenido(superficie):
    superficie = superficie.convert_alpha()
    rect = superficie.get_bounding_rect()
    if rect.width == 0 or rect.height == 0: return superficie
    return superficie.subsurface(rect).copy()

def limpiar_sprite(superficie, tamanio_final, tolerancia=55):
    superficie = superficie.convert_alpha()
    superficie = pygame.transform.scale(superficie, tamanio_final)
    superficie = quitar_fondo_por_esquinas(superficie, tolerancia)
    superficie = recortar_a_contenido(superficie)
    superficie = pygame.transform.scale(superficie, tamanio_final)
    return superficie

# =====================[TEXTURAS DEL MAPA]============================================
class TexturasMapa:
    def __init__(self):
        ruta_mapa = os.path.join(os.path.dirname(__file__), "imagenes", "mapa")
        self.sala_tutorial = self.cargar_imagen(os.path.join(ruta_mapa, "basement_guia.png"))
        self.sala_comun = self.cargar_imagen(os.path.join(ruta_mapa, "sala_comun.png"))
        self.puertas_sheet = self.cargar_imagen(os.path.join(ruta_mapa, "puertas_0.png"))
        self.roca = self.cargar_imagen(os.path.join(ruta_mapa, "roca_0.png"))
        self.trampilla_cerrada = self.cargar_imagen(os.path.join(ruta_mapa, "escotilla_cerrada.png"))
        self.trampilla_abierta = self.cargar_imagen(os.path.join(ruta_mapa, "escotilla_abierta.png"))

        self.sala_tutorial_fondo = None
        self.sala_comun_fondo = None
        self.puertas = {"ARRIBA": None, "ABAJO": None, "IZQUIERDA": None, "DERECHA": None}

        if self.roca is not None:
            self.roca = limpiar_sprite(self.roca, (TAM_ROCA, TAM_ROCA), tolerancia=60)
        if self.trampilla_cerrada is not None:
            self.trampilla_cerrada = limpiar_sprite(self.trampilla_cerrada, (90, 90), tolerancia=60)
        if self.trampilla_abierta is not None:
            self.trampilla_abierta = limpiar_sprite(self.trampilla_abierta, (120, 120), tolerancia=60)
        self.preparar_texturas()

    def cargar_imagen(self, ruta, tamanio=None):
        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            if tamanio is not None: imagen = pygame.transform.scale(imagen, tamanio)
            return imagen
        return None

    def preparar_texturas(self):
        if self.sala_tutorial is not None:
            self.sala_tutorial_fondo = pygame.transform.scale(self.sala_tutorial, (ANCHO_PANTALLA, ALTO_PANTALLA))
        if self.sala_comun is not None:
            self.sala_comun_fondo = pygame.transform.scale(self.sala_comun, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.preparar_puertas()

    def recortar_relativo(self, imagen, rx, ry, rw, rh, tamanio_final):
        ancho, alto = imagen.get_width(), imagen.get_height()
        rect = pygame.Rect(int(ancho * rx), int(alto * ry), int(ancho * rw), int(alto * rh))
        recorte = imagen.subsurface(rect).copy()
        return limpiar_sprite(recorte, tamanio_final, tolerancia=65)

    def preparar_puertas(self):
        if self.puertas_sheet is None: return
        self.puertas["ARRIBA"] = self.recortar_relativo(self.puertas_sheet, 0.27, 0.03, 0.46, 0.28, (150, 90))
        self.puertas["ABAJO"] = self.recortar_relativo(self.puertas_sheet, 0.28, 0.68, 0.46, 0.28, (150, 90))
        self.puertas["IZQUIERDA"] = self.recortar_relativo(self.puertas_sheet, 0.04, 0.32, 0.25, 0.38, (90, 150))
        self.puertas["DERECHA"] = self.recortar_relativo(self.puertas_sheet, 0.72, 0.32, 0.25, 0.38, (90, 150))

# =====================[ENTIDAD: TRAMPILLA]===========================================
class Trampilla(Base):
    def __init__(self, x, y, imagen_cerrada, imagen_abierta):
        super().__init__(x, y)
        self.imagen_cerrada = imagen_cerrada
        self.imagen_abierta = imagen_abierta
        self.visible = False
        self.abierta = False
        self.imagen_actual = self.imagen_cerrada
        self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y)) if self.imagen_actual else pygame.Rect(self.x, self.y, 90, 90)

    def abrir(self):
        self.visible, self.abierta = True, True
        self.imagen_actual = self.imagen_abierta
        if self.imagen_actual: self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y))

    def cerrar(self):
        self.visible, self.abierta = True, False
        self.imagen_actual = self.imagen_cerrada
        if self.imagen_actual: self.rect = self.imagen_actual.get_rect(topleft=(self.x, self.y))

    def dibujar(self, pantalla):
        if self.visible and self.imagen_actual: pantalla.blit(self.imagen_actual, (self.x, self.y))

    def actualizar(self, pantalla, *args): pass

# =====================[ENTIDAD: OBSTÁCULO / ROCA]====================================
class Obstaculo(Base):
    def __init__(self, x, y, ancho, alto, color=(100, 100, 100), imagen=None):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.imagen = imagen

    def dibujar(self, pantalla):
        if self.imagen is not None:
            for y in range(self.rect.y, self.rect.y + self.rect.height, TAM_ROCA):
                for x in range(self.rect.x, self.rect.x + self.rect.width, TAM_ROCA):
                    pantalla.blit(self.imagen, (x, y))
        else:
            pygame.draw.rect(pantalla, self.color, self.rect)

    def actualizar(self, pantalla, *args): pass

# =====================[CLASE: SALA JUGABLE]==========================================
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

        if self.tipo == "boss" and self.texturas is not None:
            self.trampilla = Trampilla(340, 240, self.texturas.trampilla_cerrada, self.texturas.trampilla_abierta)

    def conectar(self, direccion, nombre_sala): self.conexiones[direccion] = nombre_sala
    def agregar_obstaculo(self, obstaculo): self.obstaculos.append(obstaculo)
    def agregar_enemigo(self, enemigo): self.enemigos.append(enemigo)

    def dibujar_fondo(self, pantalla):
        if self.tipo == "tutorial" and self.texturas and self.texturas.sala_tutorial_fondo:
            pantalla.blit(self.texturas.sala_tutorial_fondo, (0, 0))
        elif self.texturas and self.texturas.sala_comun_fondo:
            pantalla.blit(self.texturas.sala_comun_fondo, (0, 0))
        else:
            pantalla.fill(self.color_fondo)
        for direccion in self.conexiones:
            puerta = self.texturas.puertas.get(direccion) if self.texturas else None
            if puerta:
                if direccion == "ARRIBA":    x, y = ANCHO_PANTALLA // 2 - puerta.get_width() // 2, 5
                elif direccion == "ABAJO":  x, y = ANCHO_PANTALLA // 2 - puerta.get_width() // 2, ALTO_PANTALLA - puerta.get_height() - 5
                elif direccion == "IZQUIERDA": x, y = 5, ALTO_PANTALLA // 2 - puerta.get_height() // 2
                elif direccion == "DERECHA":   x, y = ANCHO_PANTALLA - puerta.get_width() - 5, ALTO_PANTALLA // 2 - puerta.get_height() // 2
                pantalla.blit(puerta, (x, y))

    def dibujar(self, pantalla):
        self.dibujar_fondo(pantalla)
        for obs in self.obstaculos: obs.dibujar(pantalla)
        for ene in self.enemigos: ene.dibujar(pantalla)
        if self.trampilla: self.trampilla.dibujar(pantalla)

    def actualizar(self, pantalla, jugador=None, lista_balas=None):
        for obs in self.obstaculos: obs.actualizar(pantalla)
        if jugador is not None:
            for ene in self.enemigos[:]:
                ene.actualizar(jugador, lista_balas)
                if ene.vida <= 0:
                    self.enemigos.remove(ene)
                    AudioManager.play_sfx("muerte_enemigo")
        if self.tipo == "boss" and self.trampilla and len(self.enemigos) == 0:
            self.trampilla.abrir()

    def colision(self, rect_jugador):
        
        for obstaculo in self.obstaculos:
            if rect_jugador.colliderect(obstaculo.rect):
                return True

        # Límite físico contra las paredes de la textura de fondo (60 píxeles de grosor)
        grosor_pared = 60

        if rect_jugador.left < grosor_pared:
            if "IZQUIERDA" in self.conexiones and 225 <= rect_jugador.centery <= 375: pass
            else: return True

        if rect_jugador.right > ANCHO_PANTALLA - grosor_pared:
            if "DERECHA" in self.conexiones and 225 <= rect_jugador.centery <= 375: pass
            else: return True

        if rect_jugador.top < grosor_pared:
            if "ARRIBA" in self.conexiones and 325 <= rect_jugador.centerx <= 475: pass
            else: return True

        if rect_jugador.bottom > ALTO_PANTALLA - grosor_pared:
            if "ABAJO" in self.conexiones and 325 <= rect_jugador.centerx <= 475: pass
            else: return True

        return False

    def jugador_en_trampilla(self, rect_jugador):
        return self.trampilla.visible and self.trampilla.abierta and rect_jugador.colliderect(self.trampilla.rect) if self.trampilla else False

# =====================[PRESETS DE SALAS COMUNES]====================================
presets_salas_comunes = [
    {"nombre": "linea_rocas", "obstaculos": [(200, 250, 120, 60), (430, 310, 120, 120)], "enemigos": [(600, 150, "normal"), (400, 350, "disparador")]},
    {"nombre": "bloques_2x2", "obstaculos": [(200, 200, 120, 120), (500, 300, 120, 120)], "enemigos": [(400, 250, "disparador")]},
    {"nombre": "bloques_en_fila", "obstaculos": [(180, 250, 240, 60), (500, 250, 120, 120)], "enemigos": [(400, 350, "normal"), (600, 180, "disparador")]}
]

# =====================[CLASE: PISO COMPLETO]=========================================
class Piso(Base):
    def __init__(self, numero, textTextures):
        super().__init__(0, 0)
        self.numero, self.texturas, self.salas, self.sala_actual = numero, textTextures, {}, None
        self.crear_piso()

    def crear_piso(self):
        if self.numero == 1: self.salas["comun_1"] = Sala("comun_1", tipo="tutorial", texturas=self.texturas)
        else: self.salas["comun_1"] = self.crear_sala_comun("comun_1")
        self.salas["comun_2"] = self.crear_sala_comun("comun_2")
        self.salas["comun_3"] = self.crear_sala_comun("comun_3")
        self.salas["comun_4"] = self.crear_sala_comun("comun_4")
        self.salas["tesoro"] = Sala("tesoro", tipo="tesoro", color_fondo=(45, 40, 20), texturas=self.texturas)
        self.salas["boss"] = Sala("boss", tipo="boss", color_fondo=(45, 20, 20), texturas=self.texturas)
        self.salas["boss"].agregar_enemigo(Enemigo(400, 250, 1, 10, 1))

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
        sala = Sala(nombre, tipo="comun", texturas=self.texturas)
        preset = random.choice(presets_salas_comunes)
        for x, y, ancho, alto in preset["obstaculos"]:
            sala.agregar_obstaculo(Obstaculo(x, y, ancho, alto, imagen=self.texturas.roca))
        for datos in preset["enemigos"]:
            x, y, tipo = datos[0], datos[1], datos[2] if len(datos) >= 3 else "normal"
            sala.agregar_enemigo(EnemigoDisparador(x, y) if tipo == "disparador" else Enemigo(x, y))
        return sala

    def cambiar_sala(self, nombre_sala):
        if nombre_sala in self.salas: self.sala_actual = self.salas[nombre_sala]

    def cambiar_sala_por_direccion(self, direccion):
        if self.sala_actual and direccion in self.sala_actual.conexiones:
            self.cambiar_sala(self.sala_actual.conexiones[direccion])
            return True
        return False

    def dibujar(self, pantalla):
        if self.sala_actual: self.sala_actual.dibujar(pantalla)
    def actualizar(self, pantalla, jugador=None, balas=None):
        if self.sala_actual: self.sala_actual.actualizar(pantalla, jugador, balas)
    def colision(self, rect_jugador):
        return self.sala_actual.colision(rect_jugador) if self.sala_actual else False
    def jugador_en_trampilla(self, rect_jugador):
        return self.sala_actual.jugador_en_trampilla(rect_jugador) if self.sala_actual else False

# =====================[CLASE: ADMINISTRADOR GENERAL DEL MAPA]========================
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
        if numero_piso in self.pisos: self.piso_actual = self.pisos[numero_piso]
    def cambiar_sala(self, nombre_sala):
        if self.piso_actual: self.piso_actual.cambiar_sala(nombre_sala)
    def cambiar_sala_por_direccion(self, direccion):
        return self.piso_actual.cambiar_sala_por_direccion(direccion) if self.piso_actual else False
    def dibujar(self, pantalla):
        if self.piso_actual: self.piso_actual.dibujar(pantalla)
    def actualizar(self, pantalla, jugador=None, balas=None):
        if self.piso_actual: self.piso_actual.actualizar(pantalla, jugador, balas)

   
    def colision(self, rect_jugador):
        return self.piso_actual.colision(rect_jugador) if self.piso_actual else False
    def jugador_en_trampilla(self, rect_jugador):
        return self.piso_actual.jugador_en_trampilla(rect_jugador) if self.piso_actual else False