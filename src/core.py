#! /usr/bin/env python

import pygame
from config import *
import player
import geometry
import random
from thrust import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mayhem by ahe103')
        self.font = pygame.font.Font(None, 36)
        #creats a screen
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
        self.background  = pygame.image.load("images/scrollspaceproper2.png")
        self.width, _ = self.background.get_size()        #sets a timer for FPS handling
        self.x = 0
        self.timer = pygame.time.Clock()


    def runtime(self):
        #start the game
        #set up the lists
        self.startup()
        while True:
            self.screen.blit(self.background, (0,0))
            #handle any events
            self.eventhandler()
            #mothod for scrolling the screen
            self.screenscroll()
            #check if the players want to restart
            self.restart_game()
            #move the object's sprites
            self.all_sprites.update()
            #draw the object's sprites
            self.all_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                pygame.draw.rect(self.screen, (255, 0, 0), sprite.rect, 1)
            #keep framerate
            self.timer.tick(FPS)
            #refresh the screen
            pygame.display.flip()


    def eventhandler(self):
    #handles any keyboard inputs or other somesuch
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                exit()
            if self.keys[pygame.K_ESCAPE]:
                exit()
            if self.keys[pygame.K_6]:
                self.startup()

        all_keys = pygame.key.get_pressed()

        p1keys = []
        p1keys.append(all_keys[pygame.K_w])
        p1keys.append(all_keys[pygame.K_a])
        p1keys.append(all_keys[pygame.K_d])
        p1keys.append(all_keys[pygame.K_LSHIFT])
        p1keys.append(all_keys[pygame.K_r])

        p2keys = []
        p2keys.append(all_keys[pygame.K_UP])
        p2keys.append(all_keys[pygame.K_LEFT])
        p2keys.append(all_keys[pygame.K_RIGHT])
        p2keys.append(all_keys[pygame.K_RSHIFT])
        p2keys.append(all_keys[pygame.K_BACKSPACE])

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
        #asteroidlist = img_list(self, "PLACEHOLDER", 0, 0, (0,0))
        #bullet = img_list(self, "placeholder", 0, 0, (0,0))


        #create players
        self.player1 = player.Player(self.screen, 200, SCREEN_Y-(SCREEN_Y//3), 0, thrustlist)
        self.player2 = player.Player(self.screen, 200, SCREEN_Y//3, 0,thrustlist)
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
        self.x -= 5
        self.screen.blit(self.background,(self.x+self.width,0))
        self.screen.blit(self.background,(self.x,0))
        if self.x < -self.width:
            self.x = 0
        


if __name__ == "__main__":
    test = Game()
    test.runtime()