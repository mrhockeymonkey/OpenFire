import os
import pygame

# genral
FPS = 60
CAMERASLACK = 70
DEBUG = False

# colours  R    G    B
BLACK  = (0  , 0  , 0  )
WHITE  = (255, 255, 255)
RED    = (255, 0  , 0  )
GREEN  = (0  , 255, 0  )
YELLOW = (255, 255, 0  )
CYAN   = (0  , 255, 255)

# general
MAPS = [
    "crypt_map_1.tmx",
    "crypt_map_2.tmx",
    "crypt_map_3.tmx"
]
MAP_CLIP_TOP = 365 # fudged ammount of whitespace to cut fromm the top of map to align objects correctly
FONT = 'AdventureTime.ttf' # the font file to use for all text
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

# Finn
PLAYER_HEALTH = 300
PLAYER_BASE_ATK = 50 # the amount of damage each attack will inflict
PLAYER_LUCK = 20 # the maximum bonus damage each attack will inflict


PLAYER_SPRITESHEET = 'finn_and_jake.png'
PLAYER_SPEED = 450 # the speed the player will move in pixels/sec
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)
PLAYER_HIT_SOUND = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav', 'pain/12.wav', 'pain/13.wav', 'pain/14.wav', ]

NPC_HIT_RECT = pygame.Rect(0, 0, 32, 32) # size of hit box for npcs

# Mob
MOB_HEALTH = 1000
MOB_IMAGE = 'mithril_mutae.png'
MOB_SPEED = 100
MOB_HIT_RECT = pygame.Rect(0, 0, 24, 24)
MOB_DAMAGE = 2
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
MOB_DETECT_RADIUS = 300 # the distance a mob can detect player
MOB_ATTACK_RADIUS = 150 # the distance a mob can attack a player from
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
WEAPONS['chainsaw'] = {
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
    'shotgun': 'fg_42_by_ashmo.png',
    'pistol': 'german_pistol_by_ashmo.png',
    'chainsaw': 'chainsaw_by_ashmo.png',
    'sword': 'sword.png'
}
ITEM_BOB_RANGE = 30
ITEM_BOB_SPEED = 0.3
ITEM_HIT_RECT = pygame.Rect(0, 0, 5, 5)

