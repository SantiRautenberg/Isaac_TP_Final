# audio.py
import pygame
import os
import random

class AudioManager:

    # Propiedad de clase para implementar el acceso global optimizado
    instancia = None

    def __init__(self, ruta_sonidos_ignore=None):
        # HARDWARE REINFORCE: Forzamos un reinicio limpio del mixer cerrando defaults defectuosos
        # Usamos un buffer de 2048 para darle espacio al sistema operativo de procesar MP3s sin enmudecer
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            print("[Audio] Mezclador de Pygame reiniciado con éxito (Buffer: 2048).")
        except Exception as e:
            print(f"[Audio Error] No se pudo activar el hardware de sonido: {e}")

        # PORTABILIDAD ABSOLUTA: Autocalculamos la ubicación real del proyecto
        ruta_raiz = os.path.dirname(os.path.abspath(__file__))
        self.ruta_sonidos = os.path.join(ruta_raiz, "sonidos")
        print(f"[Audio] Buscando recursos en la ruta raíz: {self.ruta_sonidos}")

        # Registramos tus subcarpetas organizacionales (añadimos música y menú por si acaso)
        self.subcarpetas = ["", "enemigos", "juego", "jugador", "musica", "menu"]

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
                    if sfx: sfx.set_volume(0.30) # Subimos sfx a 30%
            elif valor:
                valor.set_volume(0.30)

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
            try:
                return pygame.mixer.Sound(ruta_completa)
            except Exception:
                pass
        else:
            print(f"[Audio Aviso] Archivo SFX no encontrado: '{nombre_archivo}'")
        return None

    def _cargar_variaciones_sfx(self, nombre_base, cantidad, extension):
        lista_sonidos = []
        for i in range(1, cantidad + 1):
            nombre_archivo = f"{nombre_base}_{i}.{extension}"
            ruta_completa = self._buscar_en_subcarpetas(nombre_archivo)

            if not ruta_completa and nombre_base == "lagrima_disparo" and i == 3:
                ruta_completa = self._buscar_en_subcarpetas("lagrima disparo_3.mp3")

            if ruta_completa:
                try:
                    lista_sonidos.append(pygame.mixer.Sound(ruta_completa))
                except Exception:
                    pass
        return lista_sonidos if lista_sonidos else None

    # =====================[METODOS DE CONTROL]==========================================
    def reproducir_musica(self, nombre_archivo, volumen=0.4, bucle=-1):
        archivo_completo = self._buscar_en_subcarpetas(nombre_archivo)

        if not archivo_completo:
            print(f"[Audio Alerta] ¡MÚSICA NO ENCONTRADA! El archivo '{nombre_archivo}' no existe.")
            return

        try:
            pygame.mixer.music.load(archivo_completo)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(bucle)
            print(f"[Audio] Reproduciendo música de fondo: {nombre_archivo}")
        except Exception as e:
            print(f"[Audio Error] No se pudo reproducir la música '{nombre_archivo}': {e}")

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_sfx(self, nombre_sfx):
        valor = self.sonidos_sfx.get(nombre_sfx)
        if valor:
            if isinstance(valor, list):
                random.choice(valor).play()
            else:
                valor.play()

    # ---------- MÉTODOS ESTÁTICOS GLOBALES AUTO-INICIALIZABLES ----------
    @classmethod
    def play_music(cls, nombre_archivo, volumen=0.4, bucle=-1):
        if cls.instancia is None:
            cls()
        if cls.instancia:
            cls.instancia.reproducir_musica(nombre_archivo, volumen, bucle)

    @classmethod
    def play_sfx(cls, nombre_sfx):
        if cls.instancia is None:
            cls()
        if cls.instancia:
            cls.instancia.reproducir_sfx(nombre_sfx)

    @classmethod
    def stop_music(cls):
        if cls.instancia is None:
            cls()
        if cls.instancia:
            cls.instancia.detener_musica()