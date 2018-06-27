import pygame
from pygame.locals import *
from hbf import sprites, animation
from settings import *
from itertools import chain
from random import choice, randint

vec = pygame.math.Vector2

class Player(sprites.Sprite):
    """
    This class represents the main player. It derives from the "Sprite" class in Pygame.

    A player object has a rect for the player image and also a rect for the player hitbox
    The hitbox is used to determine collisions as solves some problems with using the image rect for collision detection. 
    """

    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.lit_sprites
        self.layer = PLAYER_LAYER
        self.ssheet_w = 200
        self.ssheet_h = 150
        self.ssheets = {
            'attack': animation.SpriteSheet(game.images['fj_sword_combo']),
            'idle'  : animation.SpriteSheet(game.images['fj_idle']),
            'run'   : animation.SpriteSheet(game.images['fj_run']),
            'sword1': animation.SpriteSheet(game.images['fj_found1']),
            'sword2': animation.SpriteSheet(game.images['fj_found2']),
            'sword3': animation.SpriteSheet(game.images['fj_found3']),
            'hit'   : animation.SpriteSheet(game.images['fj_hit'])
        }
        self.actions = {
            'attack': animation.SpriteStripAnim(self.ssheets['attack'], (0, 0, self.ssheet_w, self.ssheet_h), 14, colorkey=-1,loop=False, frames=5),
            'idle'  : animation.SpriteStripAnim(self.ssheets['idle'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=True,  frames=7 ),
            'run'   : animation.SpriteStripAnim(self.ssheets['run'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=True,  frames=7 ),
            'hit'   : animation.SpriteStripAnim(self.ssheets['hit'], (0, 0, self.ssheet_w, self.ssheet_h), 4, colorkey=-1, loop=False,  frames=7 ),
            'sword' : animation.SpriteStripAnim(self.ssheets['sword1'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=False,  frames=7 ) +
                animation.SpriteStripAnim(self.ssheets['sword2'], (0, 0, self.ssheet_w, self.ssheet_h), 8, colorkey=-1, loop=False,  frames=7 ) +
                animation.SpriteStripAnim(self.ssheets['sword3'], (0, 0, self.ssheet_w, self.ssheet_h), 6, colorkey=-1, loop=False,  frames=7 )
        }
        self.action = 'idle'
        init_image = self.actions[self.action].images[0]
        sprites.Sprite.__init__(self, game, pos, init_image) # inherit from Sprite
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect_offset = vec(0, 50)
        self.atk_rect = None
        self.health = PLAYER_HEALTH
        self.invun = False
        self.uber = False
        self.max_health = PLAYER_HEALTH
        self.facing = 'right'
        self.light_mask = self.game.light_mask.copy()
        self.light_rect = self.light_mask.get_rect()
        self.actions[self.action].iter()
        self.refresh_rect(offset=self.hit_rect_offset)
        self.refresh_poly()

    def move(self, dir):
        if self.action in ['sword', 'hit']:
            return # cancel movement
        
        self.invun = False
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
        self.vel = vec(0,0)
        if self.action == 'sword':
            return
        self.action = 'idle'


    def hit(self, dmg, dir):
        if not self.invun:
            print("Player HP -{0}".format(dmg))
            self.health = self.health - dmg
            self.vel = vec(PLAYER_HIT_KNOCKBACK, 0).rotate(-dir)
            self.action = 'hit'
            self.actions[self.action].iter()
            self.game.sounds['player_hit'].play()
            sprites.Damage(self.game, (self.pos.x, self.pos.y - 50), dmg, RED)
            self.invun = True

    def attack(self):
        self.action = 'attack'
        self.actions[self.action].iter()
        if self.uber:
            self.damage = PLAYER_BASE_ATK * PLAYER_UBER_MULTIPLIER 
            self.force = PLAYER_FORCE * int(PLAYER_UBER_MULTIPLIER/2)
        else:
            self.damage = PLAYER_BASE_ATK + randint(0, PLAYER_LUCK)
            self.force = PLAYER_FORCE
        if self.facing == 'right':
            self.strike_pos = (self.pos.x + 40, self.pos.y + 40)
        else:
            self.strike_pos = (self.pos.x - 40, self.pos.y + 40)
        self.game.FT_SWORDSTRIKE_1 = 14
        self.game.FT_SWORDSTRIKE_2 = 37
        self.invun = True


    def pick_up_sword(self):
        print("found sword")
        self.uber = True
        self.invun = True
        self.action = 'sword'
        self.actions[self.action].iter()
        self.game.sounds['found_sword'].play()

    def update(self):
        """ update is called once every loop before drawing to enact any outstanding changes to the player object"""
        
        # update the player image to next in animation
        try:
            self.image = self.actions[self.action].next()
        except StopIteration as err:
            if self.action in ['attack','sword', 'hit']:
                if self.action == 'hit':
                    self.vel = vec(0, 0)
                self.action = 'idle'
                self.invun = False
            else:
                raise err

        # flip image if facing left
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        #self.rect = self.image.get_rect()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_rect(offset=self.hit_rect_offset)
        self.refresh_poly()
        self.correct_wall_collision()
        self.correct_offmap(self)
        self.refresh_rect(offset=self.hit_rect_offset)
        self.refresh_poly()
        self.light_rect.center = self.rect.center

        #self.mask = pygame.mask.from_surface(self.image)