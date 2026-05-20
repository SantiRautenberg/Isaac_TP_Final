#--------------librerias-----------------
import pygame
#----------------------------------------

class Jugador:  #la clase base de todo es jugardor
    def __init__(self,nombre,vida,vel_movimiento,daño,proyectil,rango,x,y):  #le di los siguientes atributos a mi criterio, puede ser modificado si surge otra idea
        self.nombre         = nombre                            
        self.vida           = vida
        self.vel_movimiento = vel_movimiento
        self.daño           = daño
        self.proyectil      = proyectil
        self.rango          = rango
        
        self.x = x  
        self.y = y
        
    def Moverse(self, keys): #el metodo Keys de pygame es para asignar el movimiento en pantalla (en este caso a travez de "vel_movimiento")
        if keys[pygame.K_a]:
            self.x -= self.vel_movimiento
        if keys[pygame.K_d]:
            self.x += self.vel_movimiento
        if keys[pygame.K_w]:
            self.y -= self.vel_movimiento
        if keys[pygame.K_s]:
            self.y += self.vel_movimiento
        
        
    def Dibujo(self, pantalla):
        pygame.draw.rect(pantalla,(255,0,0),(self.x,self.y,30,30)) #esto es otro atributo de pygames que dibuja en pantalla por posiciones (variable,color,tamaño del jugador)
        


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


        