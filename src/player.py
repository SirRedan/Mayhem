import pygame
import random
import math
from config import *
from Vector2D import *
import bullets


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, startposx, startposy, startorient, thrustlist, shiplist):
        super().__init__()
        #the original image and the image to draw from
        self.original = pygame.transform.scale(pygame.image.load(random.choice(shiplist)),SMALLASPECTSHIP)
        self.image = self.original.copy()
        #the list for the thrusting animation
        self.thrustlist = thrustlist
        self.direction = Vector2D(1, 0)

        #positional and rotational attributes
        self.rect = self.image.get_rect(center=(startposx, startposy))
        self.pos = Vector2D(startposx, startposy)
        self.speed = Vector2D(0, 0)
        
        #used for the thruster animation
        self.counter = 0
        self.screen = screen

        #cooldowwn for firing bullets
        self.cooldown = 0
        #amount of shield
        self.shield = 10
        #amount of ammo
        self.ammo = 50
        #amount of fuel
        self.fuel = 1000
        #score counter
        self.score = 0
        #invulnerability frame counter
        self.invuln = 0

        #various flags
        self.thrust_flag = False
        self.restart = False

        self.bullet_list = []


    def handle(self, list_o_keys):
        '''
        takes in the list of keys from the event handler in a set 
        order so that multiple sets of conrols could be added theoretically
        '''
        if list_o_keys[0]:
            if self.fuel > 0:
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
        '''
        performs the actions the player has set with the controls
        '''
        if self.shield:
            if self.thrust_flag:
                self.speed += self.direction * ACCELERATION
                if self.speed.magnitude() > SPEEDLIMIT:
                    self.speed = self.speed.normalized() * SPEEDLIMIT
                    self.fuel -= 2
            else:
                self.speed *= 0.95

            self.speed += GRAVITYFACTOR
            self.pos += self.speed
            self.pos.y = min(max(0, self.pos.y), PLAYSCREEN_Y)
            self.pos.x = min(self.pos.x, SCREEN_X)
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.invuln = max(0, self.invuln - 1)
            self.rotate()
            self.cooldown = max(0, self.cooldown - 1)

            if self.pos.x + self.rect.right < 0:
                self.shield = max(0, self.shield - 1)
                if not self.shield:
                    self.hit(0)
    def rotate(self):
        '''
        rotates and moves the ship, also handles the invuln frames image difference
        '''
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        #static function for rotating
        self.image = pygame.transform.rotate(self.original, angle)
        self.shipimage = self.image
        self.mask = pygame.transform.rotate(self.original, angle)
        self.rect = self.image.get_rect(center=self.rect.center) 
        if self.thrust_flag:
            '''
            excerts thrust upon the ship
            '''

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
            self.counter %= len(self.thrustlist)

            ship_thrust.blit(self.original, ship_pos)
            ship_thrust.set_colorkey((0,0,0))

            self.image = pygame.transform.rotate(ship_thrust, angle).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=self.rect.center)
        if self.invuln:
            self.image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        

    def shoot(self):
        #propels a bullet object forward, sets a cooldown and drains ammo
        if not self.cooldown and self.ammo > 0:
            projectile = bullets.Bullet(self)
            self.bullet_list.append(projectile)
            self.groups()[0].add(projectile)
            self.cooldown = 5
            self.ammo -= 1

    def hit(self, collision):
        '''
        if a collision happens there should be a reaction from the ship
        as such if hit with something of sufficient weight like a ship or
        asteroid the ship will bounce back if not powering the thrustrs

        the ship also loses charges on it's shield if hit, and then has
        a grace period before being able to get hit again
        '''
        if collision:
            self.speed -= self.speed.magnitude() * collision
            if self.speed.magnitude() > SPEEDLIMIT:
                self.speed = self.speed.normalized() * SPEEDLIMIT
                if not self.invuln:
                    self.shield -= 1
                    self.invuln += 20
            if self.shield == 0:
                self.kill()

    def pickup(self, pickuptype):
        '''
        various pickup actions from the given resource picked ups
        '''
        if pickuptype is "ammo":
            self.ammo = min(self.ammo + 5, MAX_AMMO)
        if pickuptype is "fuel":
            self.fuel = min(self.fuel + 100, MAX_FUEL)
        if pickuptype is "shield":
            self.shield = min(self.shield + 3, MAX_SHIELD)
        if pickuptype is "fuelandammo":
            self.fuel = min(self.fuel + 100, MAX_FUEL)
            self.ammo = min(self.ammo + 5, MAX_AMMO)
        if pickuptype is "shieldandammo":
            self.shield = min(self.shield + 3, MAX_SHIELD)
            self.ammo = min(self.ammo + 5, MAX_AMMO)

    def pointgain(self, value):
        self.score += value