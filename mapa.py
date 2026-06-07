#archivo del mapa
import pygame   


class obstaculo:
    def __init__(self,ancho,alto,x,y,color = (100,100,100)):
        self.dimensiones = pygame.Rect(x,y,ancho,alto)
        self.color = color
        pass
    
    
class salas:
    pass


class mapa:
    pass