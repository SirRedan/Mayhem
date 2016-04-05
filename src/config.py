from Vector2D import Vector2D
#main parameters of the Game

# declare the screen size
SCREEN_X = 1366
SCREEN_Y = 768

# declare some colours
BLACK      = (   0,   0,   0)
WHITE      = ( 255, 255, 255)
RED        = ( 255,   0,   0)
ORANGE     = ( 255, 128,   0)
YELLOW     = ( 255, 255,   0)
LIGHTGREEN = ( 128, 255,   0)
LIGHTBLUE  = (   0, 128, 255)
PINK       = ( 255,   0, 255)
PURPLE     = ( 128,   0, 255)
GREEN      = (   0, 255,   0)
BLUE       = (   0,   0, 255)
BROWN      = ( 138, 115,  76)
DARKGREEN  = (   0, 204,   0)
TEAL       = (   0, 255, 255)
DARKBLUE   = (   0,   0, 255)
WARMPINK   = ( 255,   0, 128)
GREY       = ( 160, 160, 160)
COLORS = [RED, ORANGE, YELLOW, LIGHTGREEN, LIGHTBLUE, PINK, PURPLE, GREEN, BLUE, BROWN, DARKGREEN, TEAL, DARKBLUE, WARMPINK]
SHIPS = ["images/ships/ship1.png", "images/ships/ship2.png","images/ships/ship3.png","images/ships/ship4.png","images/ships/ship5.png","images/ships/ship6.png"]
SMALLASPECTSHIP = (50,50)
BULLETASPECT = (25,25)
SHIPANDTHRUST = (196, 178)
GRAVITYFACTOR = Vector2D(-1, 0)
ACCELERATION = 3
BULLETSPEED = 30
SPEEDLIMIT = 10

FPS = 30


#rule importance

