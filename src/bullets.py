import pygame
import random
from config import *



class Bullet(pygame.sprite.Sprite):
    '''
    a projectile spawned by the player by shooting
    it interacts with every object on the screen
    '''
    image = pygame.transform.scale(pygame.image.load("images/bullet.png"), BULLETASPECT)
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.pos = owner.pos
        self.speed = owner.direction * BULLETSPEED
        self.rect = self.image.get_rect()
        owner.groups()[0].add(self) #all_sprites


    def update(self):
        '''
        moves in a straight line and gets removed when not within the screen
        '''
        self.pos += self.speed
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        if not PLAYSCREEN.contains(self):
            self.hit()

    def hit(self):
        '''
        how to act when hitting anything
        '''
        self.kill()
        self.owner.bullet_list.remove(self)


