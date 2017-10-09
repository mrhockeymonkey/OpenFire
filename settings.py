import os
import pygame

#Genral
FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CAMERASLACK = 90
DEBUG = True

#Colours  R    G    B
BLACK  = (0  , 0  , 0  )
WHITE  = (255, 255, 255)
RED    = (255, 0  , 0  )
GREEN  = (0  , 255, 0  )
YELLOW = (255, 255, 0  )
CYAN   = (0  , 255, 255)

# -------- OPTIONS -------- #
#Map
MAP = 'grasslands_1.tmx'

# Player
PLAYER_HEALTH = 100
PLAYER_IMAGE = 'rock1.png'
PLAYER_SPEED = 300 # the speed the player will move in pixels/sec
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)

# Mob
MOB_HEALTH = 100
MOB_IMAGE = 'floating_eye.png'
MOB_SPEED = 100
MOB_HIT_RECT = pygame.Rect(0, 0, 24, 24)
MOB_DAMAGE = 2
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50

# Gun
BULLET_IMG = 'meteorGrey_tiny1.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 2000 # the time in milliseconds the bullets persists
BULLET_RATE = 100 # the time in milliseconds between shots
BULLET_KICKBACK = 50
BULLET_SPREAD = 5 # the spread of bullets in degrees 
BULLET_DAMAGE = 10

# Effects
MUZZLE_FLASHES = ['laserRed08.png', 'laserRed09.png', 'laserRed10.png', 'laserRed11.png']

# Layers
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECT_LAYER = 4

# Items
ITEM_IMAGES = {'health': 'genericItem_color_102.png'}