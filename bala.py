import pygame

class Bala:
    def __init__(self,x,y,dire_x,dire_Y):
        self.x      = x
        self.y      = y
        self.dire_x = dire_x
        self.dire_Y = dire_Y
        self.bala_vel=10

    def Trayectoria(self):
        self.x += self.dire_x * self.bala_vel
        self.y += self.dire_Y * self.bala_vel
        
    def Dibujar(self, pantalla):
      
        verde_base = (80, 200, 120)
        verde_oscuro = (40, 120, 70)

       
        pygame.draw.circle(pantalla, verde_base, (self.x, self.y), 10)
        
        
        pygame.draw.circle(pantalla, verde_oscuro, (self.x - 2, self.y - 2), 3)
        
        
        pygame.draw.circle(pantalla, (200, 255, 200), (self.x + 2, self.y + 2), 2)
