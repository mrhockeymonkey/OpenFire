import pygame
from pygame.locals import *
from hbf import sprites
from settings import *
from itertools import chain
from random import choice

vec = pygame.math.Vector2

class Player(sprites.Sprite):
    """
    This class represents the main player. It derives from the "Sprite" class in Pygame.

    A player object has a rect for the player image and also a rect for the player hitbox
    The hitbox is used to determine collisions as solves some problems with using the image rect for collision detection. 
    """

    def __init__(self, game, pos):
        self.groups = game.all_sprites
        self.ssheets = {
            'attack': sprites.SpriteSheet(game.images['finn_and_jake_sword_combo']),
            'idle'  : sprites.SpriteSheet(game.images['finn_and_jake_idle']),
            'run'  : sprites.SpriteSheet(game.images['finn_and_jake_run'])
        }
        self.actions = {
            'attack': sprites.SpriteStripAnim(self.ssheets['attack'], (15, 0, 115, 90), 14, colorkey=-1,loop=False, frames=4),
            'idle': sprites.SpriteStripAnim(self.ssheets['idle'], (0, 0, 66, 65), 12, colorkey=-1, loop=True,  frames=7 ),
            'run': sprites.SpriteStripAnim(self.ssheets['run'], (0, 0, 54, 65), 12, colorkey=-1, loop=True,  frames=7 )
        }
        self.action = 'idle'
        init_image = self.actions[self.action].images[0]
        sprites.Sprite.__init__(self, game, self.groups, PLAYER_LAYER, pos, init_image) # inherit from Sprite
        self.hit_rect = PLAYER_HIT_RECT.copy() 
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.damaged = False
        self.facing = 'right'
        
        self.actions[self.action].iter()
        self.refresh_hitbox()
        self.rect = self.image.get_rect()

    def move(self, dir):
        # update action
        self.action = 'run'

        # update velocity and direction
        if dir == 'R':
            self.vel.x = PLAYER_SPEED
            self.facing = 'right'
        elif dir == 'L':
            self.vel.x = -PLAYER_SPEED
            self.facing = 'left'
        elif dir == 'U':
            self.vel.y = -PLAYER_SPEED
        elif dir == 'D':
            self.vel.y = PLAYER_SPEED
        else:
            raise ValueError("Value for 'dir' must be either 'U', 'D', 'L', or 'R'")

        # fix diagonal movement speed
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def stop(self):
        self.action = 'idle'
        self.vel = vec(0,0)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def attack(self):
        self.action = 'attack'
        self.actions[self.action].iter()

    def update(self):
        """ update is called once every loop before drawing to enact any outstanding changes to the player object"""
        # get keys to determine velocity
        #self._get_keys()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt

        #self.image = self.game.player_image.copy() #tis
        if self.damaged:
            try:
                val = next(self.damage_alpha)
                self.image.fill((255, 0, 0, val), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_hitbox()
        self.correct_collision(self, self.game.wall_sprites)
        self.correct_offmap(self)
        self.refresh_hitbox()


        #self.n += 1
        #if self.n >= len(self.strips):
        #    self.n = 0
        #self.strips[self.n].iter()
        #if self.vel != 0:

        #if self.vel.length() != 0:
        try:
            self.image = self.actions[self.action].next()
        except StopIteration as err:
            if self.action == 'attack':
                self.action = 'idle'
            else:
                raise err

        # flip image if facing left
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)