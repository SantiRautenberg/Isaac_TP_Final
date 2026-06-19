import json

#Decorador para guardar estadísticas en un archivo json.

# se puede mejorar para guardar varias partidas con un try/except incluido
def registros(func):
    def wrapper(*args,**kwargs):
        print("Guardando estadísticas...")
        stats_finales = func(*args,**kwargs)
        try: #arreglar esta parte
            with open("registro_estadisticas.json", "w", encoding="utf-8") as f:
                json.dump(stats_finales, f, ensure_ascii=False,indent=4)
        except Exception as e: 
            print()
        print("Estadísticas guardadas con éxito en 'registro_estadisticas.json'")
        return stats_finales
    return wrapper


class Estadisticas:
    
    # Estado inicial del jugador
    nombre_jugador = "Isaac"        # Si hubiese otros personajes habría que obtenerlo con un getter
    jugador_vivo = None
    vida_inicial = None
    daño_base = None
    vm_inicial = None

    # Estado final del jugador
    jugador_vivo = None # recibe un booleano (vivo o muerto)
    vida_final = None
    daño_final = None
    vm_final = None

    # Contadores del personaje, ítems y balas
    total_daño_recibido = 0
    puntaje_final = 0

    items_obtenidos = 0 # mejorar y/o poner directamente el inventario con un diccionario
    detalle_items = {}

    balas_disparadas = 0 # mucho quilombo añadir balas que colisionaron?
    balas_efectivas = 0

    # Contadores de enemigos
    enemigos_instanciados = 0
    detalle_instanciados = {"Mosca": 0} #completar

    enemigos_asesinados = 0
    detalle_asesinados = {"Mosca": 0} #acá van los nombres de los enemigos como clave y como valor arranca en 0

    #---------- Métodos de estado del jugador ----------
    @classmethod
    def cargar_estado_inicial(cls, jugador):
        cls.jugador_vivo = jugador.get_estado()
        cls.vida_inicial = jugador.get_vida()
        cls.daño_base = jugador.get_daño()
        cls.vm_inicial = jugador.get_velMovimiento()

    @classmethod
    def cargar_estado_final(cls, jugador):
        cls.jugador_vivo = jugador.get_estado()
        cls.vida_final = jugador.get_vida()
        cls.daño_final = jugador.get_daño()
        cls.vm_final = jugador.get_velMovimiento()

    #---------- Métodos para los contadores ----------
    @classmethod
    def sumar_daño_recibido(cls, valor):
        cls.total_daño_recibido += valor
    
    @classmethod
    def sumar_puntaje(cls,puntos):
        pass
    
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
    def resumen_stats(cls):
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
                "Puntaje final": cls.puntaje_final
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
    