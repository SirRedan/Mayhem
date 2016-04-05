import pygame
import sys
import pygame.sprite as sprite

theClock = pygame.time.Clock()
background = pygame.image.load('images/scrollspace.png')
background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
w,h = background_size
x = 0
y = 0
running = True
while running:
    screen.blit(background,background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    x -= 5
    screen.blit(background,(x+w,y))
    screen.blit(background,(x,y))
    if x < -w:
        x = 0
    pygame.display.update()
    theClock.tick(25)
pygame.quit()