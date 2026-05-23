#--------------librerias-----------------
import pygame
import os
#----------------------------------------
ANCHO=32
ALTO =32

class Jugador:
    def __init__(self,nombre,vida,vel_movimiento,daño,proyectil,rango,x,y):
        self.nombre         = nombre                            
        self.vida           = vida
        self.vel_movimiento = vel_movimiento
        self.daño           = daño
        self.proyectil      = proyectil
        self.rango          = rango
        
       
        ruta = os.path.join(os.path.dirname(__file__), "isaac_base_sprite.png")
        sprite_sheet = pygame.image.load(ruta).convert_alpha()


        self.sprite = sprite_sheet.subsurface((32, 0, 32, 32))

        self.sprite = sprite_sheet
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

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
        pantalla.blit(self.sprite, (self.x, self.y))
        




        