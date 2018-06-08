import pygame
from pygame.locals import *
from hbf import sprites
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
        self.groups = game.all_sprites
        self.layer = PLAYER_LAYER
        self.ssheet_w = 200
        self.ssheet_h = 150
        self.ssheets = {
            'attack': sprites.SpriteSheet(game.images['finn_and_jake_sword_combo']),
            'idle'  : sprites.SpriteSheet(game.images['finn_and_jake_idle']),
            'run'   : sprites.SpriteSheet(game.images['finn_and_jake_run']),
            'sword1': sprites.SpriteSheet(game.images['finn_and_jake_found_sword_1']),
            'sword2': sprites.SpriteSheet(game.images['finn_and_jake_found_sword_2']),
            'sword3': sprites.SpriteSheet(game.images['finn_and_jake_found_sword_3'])
        }
        self.actions = {
            'attack': sprites.SpriteStripAnim(self.ssheets['attack'], (0, 0, self.ssheet_w, self.ssheet_h), 14, colorkey=-1,loop=False, frames=5),
            'idle'  : sprites.SpriteStripAnim(self.ssheets['idle'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=True,  frames=7 ),
            'run'   : sprites.SpriteStripAnim(self.ssheets['run'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=True,  frames=7 ),
            'sword' : sprites.SpriteStripAnim(self.ssheets['sword1'], (0, 0, self.ssheet_w, self.ssheet_h), 12, colorkey=-1, loop=False,  frames=7 ) +
                sprites.SpriteStripAnim(self.ssheets['sword2'], (0, 0, self.ssheet_w, self.ssheet_h), 8, colorkey=-1, loop=False,  frames=7 ) +
                sprites.SpriteStripAnim(self.ssheets['sword3'], (0, 0, self.ssheet_w, self.ssheet_h), 6, colorkey=-1, loop=False,  frames=7 )
        }
        self.action = 'idle'
        init_image = self.actions[self.action].images[0]
        sprites.Sprite.__init__(self, game, pos, init_image) # inherit from Sprite
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect_offset = vec(0, 50)
        self.atk_rect = None
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.damaged = False
        self.facing = 'right'
        
        self.actions[self.action].iter()
        self.refresh_hitbox(offset=self.hit_rect_offset)
        #self.rect = pygame.Rect(0, 0, 115, 65)#self.image.get_rect()

        

    def move(self, dir):
        # 
        if self.action == 'sword':
            return
        
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
        self.vel = vec(0,0)
        if self.action == 'sword':
            return
        self.action = 'idle'

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def attack(self):
        self.action = 'attack'
        self.actions[self.action].iter()
        self.damage = PLAYER_BASE_ATK + randint(0, PLAYER_LUCK)
        if self.facing == 'right':
            self.strike_pos = (self.pos.x + 40, self.pos.y + 40)
        else:
            self.strike_pos = (self.pos.x - 40, self.pos.y + 40)
        self.game.FT_SWORDSTRIKE_1 = 14
        self.game.FT_SWORDSTRIKE_2 = 37


    def pick_up_sword(self):
        print("found sword")
        self.action = 'sword'
        self.actions[self.action].iter()
        

    #def get_colorkey_hitmask(self, image, rect, key=None):
    #    """returns a hitmask using an image's colorkey.
    #    image->pygame Surface,
    #    rect->pygame Rect that fits image,
    #    key->an over-ride color, if not None will be used instead of the image's colorkey"""
    #    if key==None:colorkey=image.get_colorkey()
    #    else:colorkey=key
    #    mask=[]
    #    for x in range(rect.width):
    #        mask.append([])
    #        for y in range(rect.height):
    #            mask[x].append(not image.get_at((x,y)) == colorkey)
    #    return mask

    def update(self):
        """ update is called once every loop before drawing to enact any outstanding changes to the player object"""

        # flash if player has been hit
        if self.damaged:
            try:
                val = next(self.damage_alpha)
                self.image.fill((255, 0, 0, val), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        
        # update the player image to next in animation
        try:
            self.image = self.actions[self.action].next()
        except StopIteration as err:
            if self.action in ['attack','sword']:
                self.action = 'idle'
            else:
                raise err

        # flip image if facing left
        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        #self.rect = self.image.get_rect()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_hitbox(offset=self.hit_rect_offset)
        self.correct_collision(self, self.game.wall_sprites)
        self.correct_offmap(self)
        self.refresh_hitbox(offset=self.hit_rect_offset)

        #self.mask = pygame.mask.from_surface(self.image)