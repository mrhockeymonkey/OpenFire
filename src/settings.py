import os
import pygame

#Genral
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CAMERASLACK = 90

#Colours R    G    B
BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)
RED   = (255, 0  , 0  )

# -------- OPTIONS -------- #
#Map
MAP = 'map1.tmx'

#Player
PLAYER_IMAGE = 'rock1.png'
PLAYER_SPEED = 200
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)

#Mob
MOB_IMAGE = 'floating_eye.png'
MOB_HIT_RECT = pygame.Rect(0, 0, 32, 32)

#Shortcuts
HALF_WINDOWWIDTH = WINDOWWIDTH / 2
HALF_WINDOWHEIGHT = WINDOWHEIGHT / 2