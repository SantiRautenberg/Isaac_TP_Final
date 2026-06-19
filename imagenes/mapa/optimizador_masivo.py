# optimizador_masivo.py
import pygame
import os

# Inicializamos los módulos de pygame
pygame.init()

# CORRECCIÓN DE MOTOR: Creamos una pantalla invisible en memoria para habilitar convert_alpha()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# ----------------- CONFIGURACIÓN DE RUTAS Y REGLAS -----------------
ruta_base = os.path.dirname(__file__)
ruta_mapa = os.path.join(ruta_base, "imagenes", "mapa")

# Sistema de contingencia: Si el script se ejecuta dentro de la misma carpeta de assets
if not os.path.exists(ruta_mapa):
    ruta_mapa = ruta_base 

# Reglas automáticas: Vinculamos una palabra clave del nombre al tamaño ideal del juego
reglas_resolucion = {
    "sala": (800, 600),
    "guia": (800, 600),
    "basement": (800, 600),
    "roca": (60, 60),
    "cerrada": (90, 90),
    "abierta": (120, 120),
    "puerta": (1024, 1024)
}

print(f"=== Iniciando optimización masiva en: {ruta_mapa} ===")

# =====================[BUCLE DE PROCESAMIENTO]======================================
for nombre_archivo in os.listdir(ruta_mapa):
    # Filtramos para procesar únicamente archivos con extensiones de imagen válidas
    if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
        ruta_completa = os.path.join(ruta_mapa, nombre_archivo)
        
        # Buscamos de forma dinámica si el nombre coincide con alguna de nuestras reglas
        resolucion_ideal = None
        for clave, res in reglas_resolucion.items():
            if clave in nombre_archivo.lower():
                resolucion_ideal = res
                break # Rompemos el bucle interno al encontrar la primera coincidencia
        
        # Si la imagen no coincide con ninguna palabra clave, la omitimos de forma segura
        if resolucion_ideal is None:
            print(f"[Aviso] Se omitió '{nombre_archivo}' porque no coincide con ninguna palabra clave conocida.")
            continue
            
        try:
            # 1. Cargamos la imagen original de alta resolución
            imagen_original = pygame.image.load(ruta_completa).convert_alpha()
            
            # 2. Aplicamos smoothscale para un reescalado suave de alta calidad (evita pixelado duro)
            imagen_optimizada = pygame.transform.smoothscale(imagen_original, resolucion_ideal)
            
            # 3. Guardamos la nueva imagen optimizada reemplazando la pesada en el disco
            pygame.image.save(imagen_optimizada, ruta_completa)
            print(f"[Éxito] '{nombre_archivo}' optimizado correctamente a {resolucion_ideal}")
            
        except Exception as e:
            print(f"[Error] No se pudo procesar el archivo '{nombre_archivo}': {e}")

print("=== Optimización masiva finalizada con éxito ===")
pygame.quit()