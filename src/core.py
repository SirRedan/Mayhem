#! /usr/bin/env python

import pstats as pstats
import cProfile as profile
import pygame
from config import *
import player
from random import *
from img_list import *
from asteroid import *
from Vector2D import *
from scoreboard import *



class Game:
    '''
    the core of the game, handles everything that the objects themselves dont
    '''
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mayhem by ahe103')
        self.font = pygame.font.Font(None, 36)
        #creats a screen
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
        self.background  = pygame.image.load("images/scrollspaceproper2.png")
        self.width, _ = self.background.get_size()
        self.x = 0
        self.timer = pygame.time.Clock()
        self.asteroids = []
        self.ast_list_list = []
        self.resolist = []
        self.sboard = Scoreboard(self.screen, self.font)



    def runtime(self):
        '''
        the brains of the game, runs in an infinite while loop. 
        interrupted by Escape or clicking the close button
        '''
        #start the game
        #set up the lists
        self.startup()
        while True:

            self.screen.blit(self.background, (0,0))
            #handle any events
            self.eventhandler()
            #mothod for scrolling the screen
            self.screenscroll()
            #handle collisions
            self.collision_handling()
            #check if the players want to restart
            self.restart_game()
            #spawn asteroids at random
            if randint(0,100) < 10:
                self.asteroids.append(Asteroid(choice(self.ast_list_list)))
                self.all_sprites.add(self.asteroids[-1])
            
            #move the object's sprites
            self.all_sprites.update()
            #draw the object's sprites
            self.all_sprites.draw(self.screen)
            #keeps the scoreboard up to date
            self.sboard.update(self.player1, self.player2)
            #keep framerate
            self.timer.tick(FPS)
            #refresh the screen
            pygame.display.flip()


    def eventhandler(self):
        '''
        handles any keyboard inputs or other somesuch
        '''
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                exit()
            if self.keys[pygame.K_ESCAPE]:
                exit()
            if self.keys[pygame.K_6]:
                self.startup()

        all_keys = pygame.key.get_pressed()
        #list of player 1 control keys
        p1keys = []
        p1keys.append(all_keys[pygame.K_UP])
        p1keys.append(all_keys[pygame.K_LEFT])
        p1keys.append(all_keys[pygame.K_RIGHT])
        p1keys.append(all_keys[pygame.K_RSHIFT])
        p1keys.append(all_keys[pygame.K_BACKSPACE])
        #list of player 2 control keys
        p2keys = []
        p2keys.append(all_keys[pygame.K_w])
        p2keys.append(all_keys[pygame.K_a])
        p2keys.append(all_keys[pygame.K_d])
        p2keys.append(all_keys[pygame.K_LSHIFT])
        p2keys.append(all_keys[pygame.K_r])
        #pass them to the object
        self.player1.handle(p1keys)
        self.player2.handle(p2keys)




    def startup(self):
        '''
        makes objects for the given amount
        as stated in the PARAMETERS file
        '''
        
        #making the necessary gorups for the sprites
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.thrustgroup = pygame.sprite.Group()
        self.asteroidsgroup = pygame.sprite.Group()

        #creating animation lists
        thrustlist = img_list(self,"images/thrustscale25.png", 8, 8, (8,8))
        asteroidlist = img_list(self, "images/asteroid+50.png", 21, 7, (21,7))

        #making two separate asteroid sprites
        asteroidlist2 = img_list(self, "images/asteroid2+50.png", 21, 7, (21,7))
        #adding them to a list for use later
        self.ast_list_list.append(asteroidlist)
        self.ast_list_list.append(asteroidlist2)

        #create players
        self.player1 = player.Player(self.screen, 200, PLAYSCREEN_Y-(PLAYSCREEN_Y//3), 0, thrustlist, SHIPP1)
        self.player2 = player.Player(self.screen, 200, PLAYSCREEN_Y//3, 0,thrustlist, SHIPP2)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)


        

    def restart_game(self):
        '''
        resets the game when both
        players agree to do so
        '''
        if self.player1.restart and self.player2.restart:
            self.startup()


    def screenscroll(self):
        '''
        moves an image in the background to make it scroll
        adding to the sense of movement
        '''
        self.x -= 5
        self.screen.blit(self.background,(self.x+self.width,0))
        self.screen.blit(self.background,(self.x,0))
        if self.x < -self.width:
            self.x = 0

    def collision_handling(self):
        '''
        does the checks for collisions between 
        the different objects in the game cycle
        players, asteroids, bullets and so on
        '''
        for roid in self.asteroids:
            if roid.rect.colliderect(self.player1.rect):                        #rough collision
                if pygame.sprite.collide_mask(roid, self.player1):              #fine collision
                    collide = (self.player1.pos - roid.pos).normalized() * (-5) #shoving the player
                    self.player1.hit(collide)                                   #out of the way
                
            if roid.rect.colliderect(self.player2.rect):                        #as above but for 
                if pygame.sprite.collide_mask(roid, self.player2):              #the other player
                    collide = (self.player2.pos - roid.pos).normalized() * (-5)
                    self.player2.hit(collide)

        for shot in self.player1.bullet_list:
            for roid in self.asteroids:
                if shot.rect.colliderect(roid.rect):                            #collision between bullets and asteroids
                    if pygame.sprite.collide_mask(shot, roid):
                        self.asteroids.remove(roid)                             #asteroid is destroyed
                        shot.hit()                                              #the bullet does it's checks
                        self.player1.pointgain(ASTEROIDSHOT)
                        reso = roid.hit()                                       #does the asteroid drop a resource?
                        if reso:
                            self.resolist.append(reso)                          #add the resource to current resources
                            self.all_sprites.add(reso)                          #add it to the spritepool
                        
                #if shot.rect.colliderect(self.player2.rect):
                    #if pygame.sprite.collide_mask(shot, self.player2):         #bullet-player collision is faulty resulting in crash
                        #collide = (self.player2.pos-shot.pos).normalized()*(-1)
                        #shot.hit()
                        #self.player1.hit(collide)

        for shot in self.player2.bullet_list:                                   #same as above only for player 2
            for roid in self.asteroids:
                if shot.rect.colliderect(roid.rect):
                    if pygame.sprite.collide_mask(shot, roid):
                        self.asteroids.remove(roid)
                        shot.hit()
                        self.player2.pointgain(ASTEROIDSHOT)
                        reso = roid.hit()
                        if reso:
                            self.resolist.append(reso)
                            self.all_sprites.add(reso)

                #if shot.rect.colliderect(self.player2.rect):
                    #if pygame.sprite.collide_mask(roid, self.player1):
                        #collide = (self.player2.pos-shot.pos).normalized()*(-1)
                        #shot.hit() 
                        #self.player2.hit(collide)


        if self.player1.rect.colliderect(self.player2.rect):                    #player-player collision
            if pygame.sprite.collide_mask(self.player1, self.player2):

                collidep1=(self.player1.pos-self.player2.pos).normalized()*(-3) #player 1 gets reflected with some force opposite of the way he was traveling
                collidep2=(self.player2.pos-self.player1.pos).normalized()*(-3) #same fut affecting player 2
                self.player1.hit(collidep1)
                self.player2.hit(collidep2)

        for resource in self.resolist:
            if self.player1.rect.colliderect(resource.rect):                    #if player 1 collides with the resource he gets it
                if pygame.sprite.collide_mask(self.player1, resource):
                        resotype = resource.hit()
                        self.player1.pickup(resotype)
                        self.player1.pointgain(ITEMPICKUP)
                        self.resolist.remove(resource)
            if self.player2.rect.colliderect(resource.rect):
                if pygame.sprite.collide_mask(self.player2, resource):          #same but affecting player 2
                        resotype = resource.hit()
                        self.player2.pickup(resotype)
                        self.player2.pointgain(ITEMPICKUP)
                        self.resolist.remove(resource)


if __name__ == "__main__":
    test = Game()
    profile.run("test.runtime()", "cProfile.txt")
    p = pstats.Stats('cProfile.txt')
    p.sort_stats('tottime').print_stats(20)