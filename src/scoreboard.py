from config import *
import pygame

class Scoreboard():
    '''
    creates the scoreboard that is displayed at the bottom of the screen
    displaying the players remaining shield, ammo, fuel and score
    '''
    def __init__(self, gamescreen, font):
        self.screen = gamescreen
        self.font = font
        self.offset = None

    def update(self, p1, p2):
        '''
        updates the scoreboard below the playarea
        '''
        self.hud = pygame.Surface((SCREEN_X,PLAYSCREEN_Y))
        self.hud.fill((200,200,200))
        self.blittext(p1, p2)
        self.screen.blit(self.hud, (0, PLAYSCREEN_Y))

    def blittext(self, p1, p2):
        '''
        blits the scoretext upon the scoreboard
        '''
        # Player 1
        score = ["Shields: {}/10".format(p1.shield),
                 "Ammo: {}/50".format(p1.ammo),
                 "Fuel: {}/1000".format(p1.fuel),
                 "Score: {}".format(p1.score)]
        score = [self.font.render(line, True, (0, 0, 0)) for line in score]
        width = max((line.get_width() for line in score))
        height = self.font.get_height()
        for linenum, line in enumerate(score):
            self.hud.blit(line, (0, height*linenum))
        
        # Player 2
        score = ["Shields: {}/10".format(p2.shield),
                 "Ammo: {}/50".format(p2.ammo),
                 "Fuel: {}/1000".format(p2.fuel),
                 "Score: {}".format(p2.score)]
        score = [self.font.render(line, True, (0, 0, 0)) for line in score]
        width = max((line.get_width() for line in score))
        if not self.offset:
            self.offset = width
        height = self.font.get_height()
        for linenum, line in enumerate(score):
            self.hud.blit(line, (SCREEN_X-self.offset, height*linenum))

