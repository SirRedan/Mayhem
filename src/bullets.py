import pygame
import random
from config import *



class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/bullet.png"), BULLETASPECT)
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.pos = owner.pos
        self.speed = owner.direction * BULLETSPEED
        owner.groups()[0].add(self)

    def update(self):
        
        self.pos += self.speed
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

