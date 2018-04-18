import pygame
from pygame.locals import *
from hbf import sprites
from settings import *
from random import choice

vec = pygame.math.Vector2

class FlamePrincess(sprites.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        self.ssheets = {
            'idle'  : sprites.SpriteSheet(game.images['flame_princess_npc'])
        }
        self.actions = {
            'idle': sprites.SpriteStripAnim(self.ssheets['idle'], (30, 0, 32, 72), 6, colorkey=-1, loop=True,  frames=10 )
        }
        self.action = 'idle'
        init_image = self.actions[self.action].images[0]
        sprites.Sprite.__init__(self, game, self.groups, PLAYER_LAYER, pos, init_image) # inherit from Sprite

        self.actions[self.action].iter()
        
        #self.hit_rect = MOB_HIT_RECT.copy()
        #self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        #self.health = MOB_HEALTH
        #self.target = self.game.player

    def update(self):
        self.image = self.actions[self.action].next()
        #super().update()

