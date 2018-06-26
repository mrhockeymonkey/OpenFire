import os
import pygame

# colours  R    G    B
BLACK  = (0  , 0  , 0  )
WHITE  = (255, 255, 255)
RED    = (255, 0  , 0  )
GREEN  = (0  , 255, 0  )
YELLOW = (255, 255, 0  )
CYAN   = (0  , 255, 255)

# game variables
FPS = 50
CAMERASLACK = 70
DEBUG = False
START_LEVEL = 0 # which the below LEVELS to start at when run (0-index based)
LEVELS = [ 
    {
        "map_file": "crypt_map_1.tmx", # tiled tmx file to render
        "enemy_total": 3, # total enemies
        "enemy_onscreen": 3, # maximum enemies on screen
        "night": False,
        "dungeon": False
    },
    {
        "map_file": "crypt_map_2.tmx",
        "enemy_total": 3,
        "enemy_onscreen": 3,
        "night": False,
        "dungeon": False
    },
    {
        "map_file": "crypt_map_3.tmx",
        "enemy_total": 30,
        "enemy_onscreen": 7,
        "night": True,
        "dungeon": True
    },
    {
        "map_file": "crypt_map_4.tmx",
        "enemy_total": 0,
        "enemy_onscreen": 0,
        "night": True,
        "dungeon": False
    }
]
FONT = 'AdventureTime.ttf' # the font file to use for all text
BG_MUSIC = 'music/before_the_dawn.ogg'
SOUNDS = {
    'health_up': 'health_pack.wav',
    'player_hit': 'player_hit.wav',
    'enemy_hit': 'enemy_hit.wav',
    'enemy_cut': 'enemy_cut.wav',
    'found_sword': 'found_sword.wav'
}

# player variables
PLAYER_HEALTH = 300
PLAYER_BASE_ATK = 50 # the amount of damage each attack will inflict
PLAYER_LUCK = 20 # the maximum bonus damage each attack will inflict
PLAYER_SPEED = 450 # the speed the player will move in pixels/sec
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 32)
PLAYER_HIT_KNOCKBACK = 100
PLAYER_FORCE = 200
PLAYER_UBER_MULTIPLIER = 3

# enemy variables
ENEMY_SPEED = 100
ENEMY_AVOID_RADIUS = 50
ENEMY_DETECT_RADIUS = 300 # the distance a mob can detect player
RUMO_HEALTH = 200
HOMUN_HEALTH = 300
HOMUNCULUS_HEALTH = 350

# images
IMAGES_TO_LOAD = {
    'fj_sword_combo': 'finn_and_jake_sword_combo.png',
    'fj_idle': 'finn_and_jake_idle.png',
    'fj_run': 'finn_and_jake_run.png',
    'fj_found1': 'finn_and_jake_found_sword_1.png',
    'fj_found2': 'finn_and_jake_found_sword_2.png',
    'fj_found3': 'finn_and_jake_found_sword_3.png',
    'fj_hit': 'finn_and_jake_hit.png', 
    'fp_idle': 'flame_princess_npc.png',
    'rumo': 'rumo.png',
    'homun': 'homun.png',
    'homunculus': 'homunculus.png',
    'health': 'health.png',
    'sword': 'sword.png'
}

# items variables
ITEM_BOB_RANGE = 30
ITEM_BOB_SPEED = 0.3
ITEM_HIT_RECT = pygame.Rect(0, 0, 5, 5)

# internals variables
MAP_CLIP_TOP = 365 # fudged ammount of whitespace to cut fromm the top of map to align objects correctly
LIGHT_MASK = 'light_350_med.png'
LIGHT_RADIUS = (500, 500)
NIGHT_COLOR = (20, 20, 20)
SWORD_STRIKE_RECT = pygame.Rect(0, 0, 70, 50)
FP_HIT_RECT = pygame.Rect(0, 0, 32, 32) # size of hit box for fp

# layers
WALL_LAYER = 1 # top most layer
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECT_LAYER = 4 # bottom layer