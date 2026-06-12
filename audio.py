# audio.py
import pygame
import os

class AudioManager:
    
    def __init__(self, ruta_sonidos):
        # Guardamos la ruta base de los efectos y música
        self.ruta_sonidos = ruta_sonidos
        
        # -----------------DICCIONARIO DE EFECTOS (SFX)-----------------
        # Cargamos los archivos de sonido una sola vez en memoria
        self.sonidos_sfx = {
            "disparo": pygame.mixer.Sound(os.path.join(ruta_sonidos, "disparo.wav")) if os.path.exists(os.path.join(ruta_sonidos, "disparo.wav")) else None,
            "daño_isaac": pygame.mixer.Sound(os.path.join(ruta_sonidos, "daño.wav")) if os.path.exists(os.path.join(ruta_sonidos, "daño.wav")) else None,
            "muerte_enemigo": pygame.mixer.Sound(os.path.join(ruta_sonidos, "muerte.wav")) if os.path.exists(os.path.join(ruta_sonidos, "muerte.wav")) else None
        }
        
        # Ajustamos volúmenes iniciales para los efectos de sonido
        for sfx in self.sonidos_sfx.values():
            if sfx:
                sfx.set_volume(0.4)

    # =====================[METODOS DE CONTROL]==========================================
    def reproducir_musica(self, nombre_archivo, volumen=0.2, bucle=-1):
        """Maneja el flujo de la música de fondo (BGM)."""
        archivo_completo = os.path.join(self.ruta_sonidos, nombre_archivo)
        if os.path.exists(archivo_completo):
            pygame.mixer.music.load(archivo_completo)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(bucle)
        else:
            print(f"[Aviso Audio] No se encontró la música: {archivo_completo}")

    def detener_musica(self):
        """Frena la música de fondo en transiciones como menús o pantallas."""
        pygame.mixer.music.stop()

    def reproducir_sfx(self, nombre_sfx):
        """Reproduce un efecto de sonido instantáneo (SFX) mediante canales libres."""
        sonido = self.sonidos_sfx.get(nombre_sfx)
        if sonido:
            sonido.play()