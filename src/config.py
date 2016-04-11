from Vector2D import Vector2D
import pygame
#main parameters of the Game

# declare the screen size
SCREEN_X        = 1366  #left to right og the display
SCREEN_Y        = 1366  #top to bottom of the display
PLAYSCREEN_X    = 1366  #width of the screen
PLAYSCREEN_Y    = 768   #distance from the top of the display to the range of 16:9 aspect ratio
SCORESCREEN_Y   = 598   #distance from playscreen to the bottom of the display

PLAYSCREEN    = pygame.Rect(0, 0, 1366, 768) #the entire play area
SCREENBUFFER    = 100 #a fixed buffer for the screen

SHIPP1          = ["images/ships/ship1.png","images/ships/ship2.png","images/ships/ship3.png"]  #ships for player 1
SHIPP2          = ["images/ships/ship4.png","images/ships/ship5.png","images/ships/ship6.png"]  #ships for player 2

#aspectratios/sizes for certain sprites
SMALLASPECTSHIP = (50,50)
BULLETASPECT    = (25,25)
SHIPANDTHRUST   = (196, 178)
DROPASPECT    = (30,30)

#the all important Gravity "pulling" to the Left
GRAVITYFACTOR   = Vector2D(-1, 0)

#speed modifiers
ACCELERATION    = 3
BULLETSPEED     = 30
SPEEDLIMIT      = 10

#asteroid modifiers
ASTEROIDNUM     = 10
ASTEROIDMAXSPD  = 5

#point modifiers
ASTEROIDSHOT    = 10
ITEMPICKUP      = 50

#Max limits for ship stats
MAX_AMMO        = 50
MAX_FUEL        = 1000
MAX_SHIELD      = 10

#wishes for framerate 
FPS             = 60