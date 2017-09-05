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

# Player
PLAYER_IMAGE = 'rock1.png'
PLAYER_SPEED = 300 # the speed the player will move in pixels/sec
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)

# Mob
MOB_IMAGE = 'floating_eye.png'
MOB_SPEED = 100
MOB_HIT_RECT = pygame.Rect(0, 0, 24, 24)

# Gun
BULLET_IMG = 'meteorGrey_tiny1.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 2000 # the time in milliseconds the bullets persists
BULLET_RATE = 100 # the time in milliseconds between shots
BULLET_KICKBACK = 50
BULLET_SPREAD = 5 # the spread of bullets in degrees 

#Shortcuts
HALF_WINDOWWIDTH = WINDOWWIDTH / 2
HALF_WINDOWHEIGHT = WINDOWHEIGHT / 2