import pygame
from config import *
from Vector2D import *
from random import *



class Resource(pygame.sprite.Sprite):
    '''
    the object that makes a player/ship regain one or more stats
    '''
    
    def __init__(self):
        super().__init__()
        self.image = 0
        self.rect = pygame.rect.Rect(0,0,0,0)
        self.pos = Vector2D(SCREEN_X//2,PLAYSCREEN_Y//2)
        self.x = 2
        self.yspeed = randint(-5,5)
        self.speed = Vector2D(self.x,self.yspeed)
        self.pickuptype = 0

    def shield(self, pos):
        '''
        sets the resource to spawn as the "Shield" resource
        '''
        self.image = pygame.transform.scale(pygame.image.load("images/wrench.png"), DROPASPECT)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.pickuptype = "shield"

    def fuel(self, pos):
        '''
        sets the resource to spawn as the "Fuel" resource
        '''
        self.image = pygame.transform.scale(pygame.image.load("images/fuel.png"), DROPASPECT)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.pickuptype = "fuel"

    def ammo(self, pos):
        '''
        sets the resource to spawn as the "Ammo" resource
        '''
        self.image = pygame.transform.scale(pygame.image.load("images/casing.png"), DROPASPECT)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.pickuptype = "ammo"

    def shieldandammo(self, pos):
        '''
        sets the resource to spawn as the "Shield and ammo" resource
        '''
        self.image = pygame.transform.scale(pygame.image.load("images/sammo.png"), DROPASPECT)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.pickuptype = "shieldandammo"

    def fuelandammo(self, pos):
        '''
        sets the resource to spawn as the "Fuel and ammo" resource
        '''
        self.image = pygame.transform.scale(pygame.image.load("images/fammo.png"), DROPASPECT)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.pickuptype = "fuelandammo"

    def update(self):
        self.speed = Vector2D(max(-2, self.x-1), self.yspeed)
        self.pos += self.speed

    def hit(self):
        '''
        removes the resource and returns the type when hit
        '''
        self.kill()
        return self.pickuptype