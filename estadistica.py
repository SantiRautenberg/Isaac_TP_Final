from datetime import datetime, timedelta
import pygame
import json
import os

#Decorador para guardar estadísticas en un archivo json.
def registros(func):
    def wrapper(*args,**kwargs):
        print("Guardando estadísticas de la partida...")

        dict_stats = func(*args,**kwargs)
        archivo = "registro_partidas_isaac_argento.json"
        clave = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")    # clave de partida
        partidas = {} # Inicio un diccionario vacío

        # Si existe el archivo reasigna a partidas el diccionario guardado
        if os.path.exists(archivo):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    partidas = json.load(f)
            except (json.JSONDecodeError, PermissionError, OSError) as e:
                print(f"[ERROR EN LECTURA] {e}")
            except Exception as e:
                print(f"[ERROR INESPERADO EN LECTURA] {e}")
            else:
                print("Archivo leído correctamente.")
            finally:
                print("Proceso de lectura finalizado.")

        # Guarda la partida actual
        partidas[clave] = dict_stats

        # Guarda el diccionario actualizado
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(partidas, f, ensure_ascii=False, indent=4)
        except (PermissionError, OSError, TypeError) as e: 
            print(f"[ERROR EN ESCRITURA] {e}")
        except Exception as e: 
            print(f"[ERROR INESPERADO EN ESCRITURA] {e}")
        else:
            print(f"Estadísticas guardadas con éxito en '{archivo}'.")
        finally:
            print("Proceso de escritura finalizado.")

        # Se imprime al final de la lectura/escritura del archivo
        print("Proceso de guardado de estadísticas finalizado.")

        return dict_stats
    return wrapper

class Estadisticas:

    nombre_jugador = "Isaac"        # Si hubiese otros personajes habría que obtenerlo con un getter
    
    # Estado inicial del jugador
    tiempo_inicio = None
    vida_inicial = None
    daño_base = None
    vm_inicial = None

    # Estado final del jugador
    tiempo_fin = None
    duracion_partida = None
    resultado = None
    jugador_vivo = None # recibe un booleano (vivo o muerto)
    vida_final = None
    daño_final = None
    vm_final = None

    # Contadores del personaje, ítems y balas
    total_daño_recibido = 0
    puntaje_final = 0

    items_obtenidos = 0 # mejorar y/o poner directamente el inventario con un diccionario
    detalle_items = {}

    balas_disparadas = 0
    balas_efectivas = 0

    # Contadores de enemigos
    enemigos_instanciados = 0
    detalle_instanciados = {"Mosca": 0} # mejorar con los de cada sala

    enemigos_asesinados = 0
    detalle_asesinados = {"Mosca": 0} #acá van los nombres de los enemigos como clave y como valor arranca en 0

    #---------- Métodos de estado del jugador ----------
    @classmethod
    def cargar_estado_inicial(cls, jugador):            # Se llama al instanciar el personaje
        cls.tiempo_inicio = pygame.time.get_ticks()
        cls.vida_inicial = jugador.get_vida()
        cls.daño_base = jugador.get_daño()
        cls.vm_inicial = jugador.get_velMovimiento()

    @classmethod
    def cargar_estado_final(cls, jugador, estado):              
        cls.tiempo_fin = pygame.time.get_ticks()
        cls.duracion_partida = cls.calcular_duracion()
        cls.resultado = estado # victoria, derrota o abandono
        cls.jugador_vivo = jugador.get_estado()
        cls.vida_final = jugador.get_vida()
        cls.daño_final = jugador.get_daño()
        cls.vm_final = jugador.get_velMovimiento()

    @classmethod
    def calcular_duracion(cls):
        duracion = round(((cls.tiempo_fin - cls.tiempo_inicio) / 1000),2) # segundos
        duracion_td = str(timedelta(seconds=duracion)) # para formato h:m:s.ms
        return duracion_td
    
    #---------- Métodos para los contadores ----------
    @classmethod
    def sumar_daño_recibido(cls, valor):
        cls.total_daño_recibido += valor
    
    @classmethod
    def calcular_puntaje(cls, jugador, estado):     # Se llama al finalizar la partida (victoria, derrota, esc)
        cls.cargar_estado_final(jugador, estado)
        puntaje_base = cls.vida_final + cls.balas_efectivas + (cls.enemigos_asesinados * 10) - cls.total_daño_recibido
        # porcentajes de efectividad
        efectividad_balas = cls.balas_efectivas / cls.balas_disparadas if cls.balas_disparadas>0 else 0
        efectividad_asesinatos = cls.enemigos_asesinados / cls.enemigos_instanciados if cls.enemigos_instanciados>0 else 0
        # bonificación por precisión
        puntaje_base += efectividad_balas * 100  # porcentaje como puntos
        # bonificación por efectividad en asesinatos
        puntaje_base += efectividad_asesinatos * 100
        # bonificación por ítem
        if cls.items_obtenidos == 1:
            puntaje_base *= 1.25
        # bonificación/penalización por resultado
        if cls.resultado == "victoria":
            puntaje_final = puntaje_base * 2
        elif cls.resultado == "derrota":
            puntaje_final = puntaje_base
        else:
            puntaje_final = puntaje_base / 2
        return max(0,int(puntaje_final)) # asegura que el puntaje no sea negativo y sea entero
    
    @classmethod
    def sumar_enemigos_instanciados(cls,nombre):
        cls.enemigos_instanciados += 1
        cls.detalle_instanciados[nombre] += 1
        
    @classmethod
    def sumar_enemigos_asesinados(cls,nombre):
        cls.enemigos_asesinados += 1
        cls.detalle_asesinados[nombre] += 1

    @classmethod
    def sumar_balas_disparadas(cls):
        cls.balas_disparadas += 1

    @classmethod
    def sumar_balas_efectivas(cls):
        cls.balas_efectivas += 1

    @classmethod
    def sumar_items_obtenidos(cls,nombre):
        cls.items_obtenidos += 1
        cls.detalle_items[nombre] += 1

    # ---------- Método para registro con decorador ----------
    @classmethod
    @registros
    def resumen_partida(cls):
        stats_fin = {
            "Estadísticas jugador":
            {   
                "Nombre": cls.nombre_jugador,
                "Jugador vivo": cls.estado_final,
                "Vida inicial": cls.vida_inicial,
                "Vida final": cls.vida_final,
                "Daño base": cls.daño_base,
                "Daño final": cls.daño_final,
                "Velocidad de movimiento inicial": cls.vm_inicial,
                "Velocidad de movimiento final": cls.vm_final,
                "Total daño recibido": cls.total_daño_recibido,
                "Duración partida": cls.duracion_partida, # es un str
                "Puntaje final": cls.puntaje_final,
                "Resultado": cls.resultado,
            },
            "Estadísticas asesinatos":
            {
                "Total enemigos": cls.enemigos_instanciados,
                "Detalle de enemigos": cls.detalle_instanciados,
                "Total enemigos asesinados": cls.enemigos_asesinados,
                "Detalles de asesinatos": cls.detalle_asesinados,
                "Total balas disparadas": cls.balas_disparadas,
                "Balas efectivas": cls.balas_efectivas,
            },
            "Estadísticas ítems":
            {
                "Ítems obtenidos": cls.items_obtenidos,
                "Detalle de ítems": cls.detalle_items
            }
        }
        return stats_fin
    