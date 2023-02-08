import random
import pygame
from player import *
from player_ai import *


#start the pygame engine
pygame.init()

#start the pygame font engine
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 23) #load a font for use

#start the sound engine
pygame.mixer.init();

#game variables
simOver = False
ai_players = []
map1 = Map()
camera_offset = (0,0)
camera_pos = (500,500)

#game independent variables (needed for every pygame)
FPS = 60 #60 Frames Per Second for the game update cycle
fpsClock = pygame.time.Clock() #used to lock the game to 60 FPS
screen = pygame.display.set_mode((1280,720)) #initialize the game window
world = pygame.Surface((3000,3000))

def create_ai_players():
    for i in range(50):
        ai_players.append(PlayerAI())

def create_map_1():
    map1.add(Platform(0,690,2400,30,(0,255,0)))
    map1.add(Platform(100,600,400,30,(0,255,0)))
    map1.add(Platform(200,500,400,30,(0,255,0)))
    map1.add(Platform(100,350,200,30,(0,255,0)))
    map1.add(Platform(270,250,200,30,(0,255,0)))
    map1.add(Platform(600,200,30,400,(0,255,0)))
    map1.add(Platform(715,120,300,30,(0,255,0)))
    map1.add(Platform(740,700,300,30,(0,255,0)))
    map1.add_coin(Coin(600,650))
    map1.add_coin(Coin(220,450))
    map1.add_coin(Coin(730,80))
    map1.set_gravity(-4)

def draw_mouse_coords():
    textSurface = myfont.render(str(pygame.mouse.get_pos()), True, (255,255,255))
    world.blit(textSurface, (50, 30))
    #textSurface = myfont.render(str(p1.get_score()), True, (255,255,255))
    #world.blit(textSurface, (50, 70))

def clear_screen():
    pygame.draw.rect(world, (0,0,0), (0, 0, world.get_rect().width, world.get_rect().height))

def update_camera():
    global camera_pos
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        camera_pos = (camera_pos[0]+10, camera_pos[1])
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        camera_pos = (camera_pos[0]-10, camera_pos[1])
    if pygame.key.get_pressed()[pygame.K_UP]:
        camera_pos = (camera_pos[0], camera_pos[1]-10)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        camera_pos = (camera_pos[0], camera_pos[1]+10)

# initialize all data before gameplay
create_map_1()
create_ai_players()
for p in ai_players:
    p.setMap(map1)

#main while loop
while not simOver:
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            simOver = True

    # draw code
    clear_screen()
    map1.draw(world)
    for p in ai_players:
        p.draw(world)
    draw_mouse_coords()

    # player update code
    update_camera()
    for p in ai_players:
        p.act()
    x_offset = 0
    y_offset = 0
    x_offset = 640 - camera_pos[0]
    y_offset = 350 - camera_pos[1]
    camera_offset = (x_offset, y_offset)
    #camera_pos = ((player_pos[0], player_pos[1] - 900))

    #put all the graphics on the screen
    #should be the LAST LINE of game code
    screen.blit(world,camera_offset)
    pygame.display.flip()
    fpsClock.tick(FPS) #slow the loop down to 60 loops per second