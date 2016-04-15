import pygame
from random import *
from config import *
import resource



class Asteroid(pygame.sprite.Sprite):
    '''
    the main obstacle of the game
    spawns resources at random when destroyed
    affected by gravity to some extent
    '''
    
    def __init__(self, asteroidlist):
        super().__init__()
        self.img_list = asteroidlist
        self.image = self.img_list[0]
        self.rect = self.image.get_rect()
        self.width = self.rect.right//2
        self.height = self.rect.bottom//2
        self.pos = Vector2D(SCREEN_X + SCREENBUFFER, randint(0 + self.rect.bottom, PLAYSCREEN_Y - self.rect.bottom))
        self.speed = Vector2D(0,randint(-2 , 2))
        self.counter = 0
        self.choicelist = []

    def update(self):
        '''
        animation giving the look of the asteroid spinning
        and moves the asteroid
        '''
        if self.counter < len(self.img_list):
            self.image = pygame.transform.scale(self.img_list[self.counter], (self.width, self.height))
            self.counter += 2
            self.counter %= len(self.img_list)-4

        foo = Vector2D(0,0)
        
        self.speed += GRAVITYFACTOR
        
        if self.speed.x < -ASTEROIDMAXSPD:
            foo += self.speed.normalized() * ASTEROIDMAXSPD
            self.speed.x = foo.x

        self.pos += self.speed

        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        if self.pos.x + SCREENBUFFER < 0:
            self.kill()
        if self.pos.y + SCREENBUFFER < 0 or self.pos.y - SCREENBUFFER > PLAYSCREEN_Y:
            self.kill

    def hit(self):
        '''
        spawn resource using random choice for ammo/fuel/shield
        '''
        returnval = 0
        if randint(0,1) < 1:
            new = resource.Resource()
            self.choicelist = [new.shield, new.fuel, new.shieldandammo, new.fuelandammo, new.ammo]
            l = self.choicelist[randint(0,4)]
            l(self.pos)
            returnval = new
            
        else:
            returnval = False

        self.kill()
        return returnval
