import pygame
import random
import math
from config import *
from Vector2D import *
import bullets


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, startposx, startposy, startorient, thrustlist):
        super().__init__()
        #the original image and the image to draw from
        self.original = pygame.transform.scale(pygame.image.load(random.choice(SHIPS)),SMALLASPECTSHIP)
        self.image = self.original.copy()
        #the list for the thrusting animation
        self.thrustlist = thrustlist
        self.direction = Vector2D(1, 0)

        #positional and rotational attributes
        self.rect = self.image.get_rect(center=(startposx, startposy))
        self.pos = Vector2D(startposx, startposy)
        self.speed = Vector2D(0, 0)
        self.counter = 0
        self.screen = screen
        self.cooldown = 0

        #various flags
        self.thrust_flag = False
        self.restart = False

    def handle(self, list_o_keys):
        if list_o_keys[0]:
            self.thrust_flag = True
        else:
            self.thrust_flag = False

        if list_o_keys[1]:
            self.direction = self.direction.rotate(-5)
        if list_o_keys[2]:
            self.direction = self.direction.rotate(5)
        if list_o_keys[3]:
            self.shoot()
        if list_o_keys[4]:
            self.restart = True

    def update(self):
        #operations a player can perform by
        # raising flags with the keyboard
        if self.thrust_flag:
            self.speed += self.direction * ACCELERATION
            if self.speed.magnitude() > SPEEDLIMIT:
                self.speed = self.speed.normalized() * SPEEDLIMIT
        else:
            self.speed *= 0.95

        self.speed += GRAVITYFACTOR
        self.pos += self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.rotate()
        self.cooldown = max(0, self.cooldown - 1)

    def rotate(self):
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        #static function for rotating
        self.image = pygame.transform.rotate(self.original, angle)
        self.rect = self.image.get_rect(center=self.rect.center) 
        if self.thrust_flag:
            #excerts thrust upon the ship

            #animates the thruster
            #keeps the center of the ship, 
            #makes a new surface and mask
            ship_thrust = pygame.Surface((150, 150))
            ship_pos = ship_thrust.get_rect().centerx - self.original.get_width()/2, ship_thrust.get_rect().centery - self.original.get_height()/2
            thrust_pos = 0, ship_thrust.get_rect().centery - self.thrustlist[self.counter].get_height()/2
            #keeps track of what stage of the 
            #animation it's at
            ship_thrust.blit(self.thrustlist[self.counter], thrust_pos)
            self.counter += 1
            self.counter %= 63

            ship_thrust.blit(self.original, ship_pos)
            ship_thrust.set_colorkey((0,0,0))

            self.image = pygame.transform.rotate(ship_thrust, angle)
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        #propels a bullet object forward
        if not self.cooldown:
            bullets.Bullet(self)
            self.cooldown = 5
