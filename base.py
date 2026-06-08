from abc import ABC,abstractmethod

class Base(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def dibujar(self, pantalla):
        # Cada entidad tiene el método dibujo
        pass

    @abstractmethod
    def actualizar(self, pantalla, *args):
        # Actualiza para cada entidad del juego
        pass
