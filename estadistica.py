# estadistica
from datetime import datetime, timedelta
import pygame
import json
import os

# Decorador para guardar datos de partidas en un archivo json.
def registros(func):
    def wrapper(*args,**kwargs):
        print("Guardando datos de la partida...")

        datos= func(*args,**kwargs)
        archivo = "registro_partidas.json"
        clave = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") 
        partidas = {} 

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
        partidas[clave] = datos

        # Guarda el diccionario actualizado
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(partidas, f, ensure_ascii=False, indent=4)
        except (PermissionError, OSError, TypeError) as e: 
            print(f"[ERROR EN ESCRITURA] {e}")
        except Exception as e: 
            print(f"[ERROR INESPERADO EN ESCRITURA] {e}")
        else:
            print(f"Datos guardados con éxito en '{archivo}'.")
        finally:
            print("Proceso de escritura finalizado.")

        # Se imprime al final de la lectura/escritura del archivo
        print("Proceso de guardado de datos de partida finalizado.")

        return datos
    return wrapper

class Estadisticas:
    
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

    items_obtenidos = 0
    detalle_items = {}

    balas_disparadas = 0
    balas_efectivas = 0

    # Contadores de enemigos
    enemigos_instanciados = 0
    enemigos_asesinados = 0
    boss_derrotados = 0

    balas_enemigo_disparadas = 0
    balas_enemigo_impactadas = 0

    #---------- Métodos de estado del jugador ----------
    @classmethod
    def cargar_estado_inicial(cls, jugador):            # Se llama al instanciar el personaje
        cls.tiempo_inicio = pygame.time.get_ticks()
        cls.vida_inicial = jugador.get_vida()
        cls.daño_base = jugador.get_daño()
        cls.vm_inicial = jugador.get_velMovimiento()

    @classmethod
    def cargar_estado_final(cls, jugador):              
        cls.tiempo_fin = pygame.time.get_ticks()
        cls.duracion_partida = cls.calcular_duracion()
        cls.jugador_vivo = jugador.get_estado()
        cls.vida_final = jugador.get_vida()
        cls.daño_final = jugador.get_daño()
        cls.vm_final = jugador.get_velMovimiento()
        if cls.jugador_vivo==False:
            cls.resultado = "derrota"
        else:
            cls.resultado = "victoria"

    @classmethod
    def calcular_duracion(cls):
        duracion = round(((cls.tiempo_fin - cls.tiempo_inicio) / 1000),2) # segundos
        cls.duracion_partida = str(timedelta(seconds=duracion)) # para formato h:m:s.ms
        return cls.duracion_partida
    
    @classmethod
    def calcular_puntaje(cls, jugador):   # Se llama al finalizar la partida (victoria/derrota)
        cls.cargar_estado_final(jugador)

        # ---------- CÁLCULO DE PUNTAJE ----------
        puntaje_base = cls.vida_final + (cls.enemigos_asesinados*5 + cls.boss_derrotados*10) - cls.total_daño_recibido

        # porcentaje de efectividad de balas
        efectividad_balas = float(cls.balas_efectivas / cls.balas_disparadas) if cls.balas_disparadas>0 else 0

        # bonificación por precisión
        puntaje_base += efectividad_balas * 100  # porcentaje como puntos
        
        # bonificación por ítems
        if cls.items_obtenidos>0:
            puntaje_base *= float(cls.items_obtenidos / 100)
        
        # bonificación/penalización por resultado
        if cls.resultado == "victoria":
            puntaje_base *= 1.2
        else:
            puntaje_base *= 0.8

        cls.puntaje_final = max(0,int(puntaje_base)) # asegura que el puntaje no sea negativo y sea entero

        # Llamo a los otros métodos finales
        cls.resumen_partida_testeo()
        cls.registro_partida()

        return cls.puntaje_final
    
    #---------- Métodos para los contadores ----------
    @classmethod
    def sumar_daño_recibido(cls, valor):
        cls.total_daño_recibido += valor
    
    @classmethod
    def sumar_enemigos_instanciados(cls):
        cls.enemigos_instanciados += 1
        
    @classmethod
    def sumar_enemigos_asesinados(cls):
        cls.enemigos_asesinados += 1

    @classmethod
    def sumar_boss_derrotados(cls):
        cls.boss_derrotados += 1

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

    @classmethod
    def sumar_balas_enemigo_disparadas(cls):
        cls.balas_enemigo_disparadas += 1

    @classmethod
    def sumar_balas_enemigo_impactadas(cls):
        cls.balas_enemigo_impactadas += 1

    @classmethod
    def resumen_partida_testeo(cls):
        stats_fin = {
            "Estadísticas jugador":
            {   
                "Jugador vivo": cls.jugador_vivo,
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
                "Total enemigos asesinados": cls.enemigos_asesinados + cls.boss_derrotados,
                "Boss derrotados": cls.boss_derrotados,
                "Total balas disparadas": cls.balas_disparadas,
                "Balas efectivas": cls.balas_efectivas,
            },
            "Estadísticas ítems":
            {
                "Ítems obtenidos": cls.items_obtenidos,
                "Detalle de ítems": cls.detalle_items
            }
        }
        print(stats_fin) #para testear
        return stats_fin
    
    # ---------- Método para registro con decorador ----------
    @classmethod
    @registros
    def registro_partida(cls):
        datos_partida = { 
            "Resultado": cls.resultado,
            "Duración": cls.duracion_partida,
            "Puntaje": cls.puntaje_final             
        }
        print(datos_partida)
        return datos_partida
