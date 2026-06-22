# audio.py
import pygame
import os
import random

class AudioManager:

    # Propiedad de clase para implementar el acceso global optimizado
    instancia = None

    def __init__(self, ruta_sonidos_ignore=None):
        # ESCUDO DE AUDIO: Forzamos la inicialización explícita del hardware de sonido
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # PORTABILIDAD ABSOLUTA: Autocalculamos la ubicación real del proyecto
        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        self.ruta_sonidos = os.path.join(ruta_raiz, "sonidos")

        # Registramos tus nuevas subcarpetas organizacionales
        self.subcarpetas = ["", "enemigos", "juego", "jugador"]

        # -----------------DICCIONARIO DE EFECTOS (SFX)-----------------
        self.sonidos_sfx = {
            "disparo": self._cargar_variaciones_sfx("lagrima_disparo", 3, "mp3"),
            "daño_isaac": self._cargar_variaciones_sfx("daño", 3, "wav"),
            "muerte_isaac": self._cargar_variaciones_sfx("muerte", 3, "wav"),
            "muerte_enemigo": self._cargar_sfx("muerte.wav"),
            "lagrima_impacto": self._cargar_sfx("lagrima_impacto.mp3"),
            "jugar_de_nuevo": self._cargar_sfx("jugar_de_nuevo.mp3"),
            "iniciar_juego": self._cargar_sfx("iniciar_juego.wav"),
            "trampilla_abierta": self._cargar_sfx("trampilla_abierta.mp3"),
            "spawn_jefe": self._cargar_sfx("boss_spawn.mp3"),
            "spawn_enemigos": self._cargar_sfx("sala_spawn_enemigos.mp3")
        }

        # Ajustamos volúmenes iniciales para los efectos de sonido
        for valor in self.sonidos_sfx.values():
            if isinstance(valor, list):
                for sfx in valor:
                    if sfx: sfx.set_volume(0.15)
            elif valor:
                valor.set_volume(0.15)

        # Guardamos la referencia de la instancia activa de forma estática
        AudioManager.instancia = self

    def _buscar_en_subcarpetas(self, nombre_archivo):
        for subcarpeta in self.subcarpetas:
            ruta_intento = os.path.join(self.ruta_sonidos, subcarpeta, nombre_archivo)
            if os.path.exists(ruta_intento):
                return ruta_intento
        return None

    def _cargar_sfx(self, nombre_archivo):
        ruta_completa = self._buscar_en_subcarpetas(nombre_archivo)
        if ruta_completa:
            return pygame.mixer.Sound(ruta_completa)
        return None

    def _cargar_variaciones_sfx(self, nombre_base, cantidad, extension):
        lista_sonidos = []
        for i in range(1, cantidad + 1):
            nombre_archivo = f"{nombre_base}_{i}.{extension}"
            ruta_completa = self._buscar_en_subcarpetas(nombre_archivo)

            if not ruta_completa and nombre_base == "lagrima_disparo" and i == 3:
                ruta_completa = self._buscar_en_subcarpetas("lagrima disparo_3.mp3")

            if ruta_completa:
                lista_sonidos.append(pygame.mixer.Sound(ruta_completa))
        return lista_sonidos if lista_sonidos else None

    # =====================[METODOS DE CONTROL]==========================================
    def reproducir_musica(self, nombre_archivo, volumen=0.2, bucle=-1):
        archivo_completo = self._buscar_en_subcarpetas(nombre_archivo)
        if archivo_completo:
            try:
                pygame.mixer.music.load(archivo_completo)
                pygame.mixer.music.set_volume(volumen)
                pygame.mixer.music.play(bucle)
            except pygame.error as e:
                print(f"[Error Mixer] No se pudo reproducir el archivo de audio: {e}")

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_sfx(self, nombre_sfx):
        valor = self.sonidos_sfx.get(nombre_sfx)
        if valor:
            if isinstance(valor, list):
                random.choice(valor).play()
            else:
                valor.play()

    # ---------- MÉTODOS ESTÁTICOS GLOBALES ----------
    @classmethod
    def play_sfx(cls, nombre_sfx):
        if cls.instancia:
            cls.instancia.reproducir_sfx(nombre_sfx)

    @classmethod
    def play_music(cls, nombre_archivo, volumen=0.2, bucle=-1):
        if cls.instancia:
            cls.instancia.reproducir_musica(nombre_archivo, volumen, bucle)

    @classmethod
    def stop_music(cls):
        if cls.instancia:
            cls.instancia.detener_musica()