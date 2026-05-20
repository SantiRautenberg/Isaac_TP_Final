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
        
    def Dibujar(self,pantalla):
         pygame.draw.circle(pantalla, (255,255,0), (self.x, self.y), 5)
