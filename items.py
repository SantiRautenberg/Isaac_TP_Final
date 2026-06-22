from abc import ABC, abstractmethod
from estadistica import Estadisticas
    
class ItemPasivo(ABC):

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        Estadisticas.sumar_items_obtenidos(nombre)

    @abstractmethod
    def aplicar(self, jugador):
        pass

# Encanto del vampiro
class EncantoDelVampiro(ItemPasivo):

    def __init__(self):

        self.id = 1
        
        super().__init__(
            nombre="Encanto del vampiro",
            descripcion="+3 Ataque"
        )

        self.enemigos_eliminados = 0

    def aplicar(self, jugador):

        jugador.aumentar_daño(3)

    def enemigo_derrotado(self, jugador):

        self.enemigos_eliminados += 1

        if self.enemigos_eliminados == 3:
            jugador.curar(0.5)
            self.enemigos_eliminados = 0   
            
# Hormonas de crecimiento
class HormonasDeCrecimiento(ItemPasivo):

    def __init__(self):

        self.id = 2
        
        super().__init__(
            nombre="Hormonas de crecimiento",
            descripcion="+1 de daño, +2 de velocidad"
        )

    def aplicar(self, jugador):
        jugador.aumentar_daño(1)
        jugador.aumentar_velocidad(1)
        
# Cabeza de Cricket
class CabezaDeCricket(ItemPasivo):

    def __init__(self):

        self.id = 3
        
        super().__init__(
            nombre="Cabeza de Cricket",
            descripcion="+1 de daño, x1.5 de daño"
        )

    def aplicar(self, jugador):
        cantidad = (jugador.get_daño() + 1) * 1.25
        jugador.set_daño(cantidad)
        

# Honguito
class Honguito(ItemPasivo):

    def __init__(self):

        self.id = 4
        
        super().__init__(
            nombre="Honguito",
            descripcion="+2 de Velocidad"
        )

    def aplicar(self, jugador):
        jugador.aumentar_velocidad(1)
        
# Alfajor hongueado
class AlfajorHongueado(ItemPasivo):

    def __init__(self):
        
        self.id = 5
        
        super().__init__(
            nombre="Alfajor hongueado",
            descripcion="-2 de vida, -1 velocidad, +3 daño"
        )

    def aplicar(self, jugador):

        jugador.recibir_daño(2)
        jugador.reducir_velocidad(1)
        jugador.aumentar_daño(2)
        
# Sangre de Martir
class SangreDeMartir(ItemPasivo):

    def __init__(self):

        self.id = 6
        
        super().__init__(
            nombre="Sangre de Martir",
            descripcion="Da +1 de ataque"
        )

    def aplicar(self, jugador):

        jugador.aumentar_daño(1)
        
# <3
class Corazon(ItemPasivo):

    def __init__(self):

        self.id = 7
        
        super().__init__(
            nombre="<3",
            descripcion="+1 Vida max + Full curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(1)
        jugador.curacion_completa()
        
# Desayuno
class Desayuno(ItemPasivo):

    def __init__(self):

        self.id = 8

        super().__init__(
            nombre="Desayuno",
            descripcion="+1 Vida max +1 Curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(1)
        jugador.curar(1)
        
# Almuerzo
class Almuerzo(ItemPasivo):

    def __init__(self):

        self.id = 9

        super().__init__(
            nombre="Almuerzo",
            descripcion="+1 Vida max +1 Curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(1)
        jugador.curar(1)
        
# Cena
class Cena(ItemPasivo):

    def __init__(self):

        self.id = 11

        super().__init__(
            nombre="Cena",
            descripcion="+1 Vida max +1 Curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(1)
        jugador.curar(1)
        
# Carne podrida
class CarnePodrida(ItemPasivo):

    def __init__(self):

        self.id = 12

        super().__init__(
            nombre="Carne podrida",
            descripcion="+1 Vida max +1 Curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(1)
        jugador.curar(1)
        
# Higado crudo
class HigadoCrudo(ItemPasivo):

    def __init__(self):

        self.id = 13

        super().__init__(
            nombre="Higado crudo",
            descripcion="+2 Vida max + Full curación"
        )

    def aplicar(self, jugador):

        jugador.añadir_contenedor(2)
        jugador.curacion_completa()
        
# Ozempic
class Ozempic(ItemPasivo):

    def __init__(self):

        self.id = 14

        super().__init__(
            nombre="Ozempic",
            descripcion="-2 vida maxima, +4 velocidad"
        )

    def aplicar(self, jugador):

        jugador.reducir_vida_maxima(1)
        jugador.aumentar_velocidad(1)
        
# Cañon de vidrio
class CañonDeVidrio(ItemPasivo):

    def __init__(self):

        self.id = 15

        super().__init__(
            nombre="Cañon de vidrio",
            descripcion="-1 Vida maxima, +5 daño"
        )

    def aplicar(self, jugador):

        jugador.reducir_vida_maxima(1)
        jugador.aumentar_daño(5)
        
