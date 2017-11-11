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
BG_MUSIC = 'music/espionage.ogg'
GAME_SOUNDS = {
    'level_start': 'level_start.wav',
    'health_up': 'health_pack.wav',
    'gun_pickup': 'gun_pickup.wav'
}

DAMAGE_ALPHA = [i for i in range(0, 255, 25)]
LIGHT_MASK = 'light_350_med.png'
LIGHT_RADIUS = (500, 500)
NIGHT_COLOR = (20, 20, 20)

# Player
PLAYER_HEALTH = 20
PLAYER_IMAGE = 'rock1.png'
PLAYER_SPEED = 300 # the speed the player will move in pixels/sec
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)
PLAYER_HIT_SOUND = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav', 'pain/12.wav', 'pain/13.wav', 'pain/14.wav', ]

# Mob
MOB_HEALTH = 100
MOB_IMAGE = 'floating_eye.png'
MOB_SPEED = 100
MOB_HIT_RECT = pygame.Rect(0, 0, 24, 24)
MOB_DAMAGE = 2
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
MOB_DETECT_RADIUS = 300 # the distance a mob can detect player
MOB_HIT_SOUND = ['splat-15.wav']

# Weapons
BULLET_IMG = 'meteorGrey_tiny1.png'
WEAPONS = {}
WEAPONS['pistol'] = {
    'speed': 500, # the speed at which the bullet travels
    'lifetime': 2000, # the time in milliseconds the bullets persists
    'rate': 250, # the time in milliseconds between shots
    'kickback': 50, 
    'spread': 5, # the spread of bullets in degrees (5 = 2.5 degrees in either direction)
    'damage': 10, # the damage 
    'size': 'lg', # the size of the bullet
    'count': 1 # how many bullets spawned per shot
    #'sound': ['sfx_weapon_singleshot2.wav']
}
WEAPONS['shotgun'] = {
    'speed': 400, 
    'lifetime': 500, 
    'rate': 900, 
    'kickback': 300, 
    'spread': 20, 
    'damage': 10, 
    'size': 'sm',
    'count': 12
    #'sound': ['shotgun.wav']
}
WEAPON_SOUNDS = {
    'pistol': ['sfx_weapon_singleshot2.wav'],
    'shotgun': ['shotgun.wav']
}

# Effects
MUZZLE_FLASHES = ['laserRed08.png', 'laserRed09.png', 'laserRed10.png', 'laserRed11.png']

# Layers
WALL_LAYER = 1 # top most layer
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECT_LAYER = 4 # bottom layer

# Items
ITEM_IMAGES = {
    'health': 'genericItem_color_102.png',
    'shotgun': 'obj_shotgun.png'
    
}
ITEM_BOB_RANGE = 30
ITEM_BOB_SPEED = 0.3

