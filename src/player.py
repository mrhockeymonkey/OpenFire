import pygame
from pygame.locals import *
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    """
    This class represents the main player.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, game, x, y):
        # initialize sprite class, adding sprite to groups immediately
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # setup some properties
        self.game = game
        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        #self.x = x
        #self.y = y
        #self.vx, self.vy = 0, 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def _get_keys(self):
        self.vel = vec(0, 0)
        #self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[K_RIGHT] or keys[K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[K_UP] or keys[K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[K_DOWN] or keys[K_s]:
            self.vel.y = PLAYER_SPEED
        # to stop faster diagonal movement need to multipy by square root of 2
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071


    def _collide_with_wall(self, direction):
        if direction == 'x':
            # detect is there is any pixel collision between sprite rects
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.vel.x > 0: # case when moving to the right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0: # case when moving to the left
                    self.pos.x = hits[0].rect.right
                # cancel out velocity and update the player rect
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.vel.y > 0: # case when moving down
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0: # case when moving up
                    self.pos.y = hits[0].rect.bottom
                # cancel out velocity and update the player rect
                self.vel.y = 0
                self.rect.y = self.pos.y

    
    def update(self):
        # first we check to see what keys are pressed to decide if movement, image or animation is needed
        self._get_keys()

        # update sprite pos (distance = velocity * time)
        self.pos += self.vel * self.game.dt
        #self.x += self.vx * self.game.dt
        #self.y += self.vy * self.game.dt

        # collision detection
        self.rect.x = self.pos.x
        self._collide_with_wall('x')
        self.rect.y = self.pos.y
        self._collide_with_wall('y')

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wall_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


#class Wall(pygame.sprite.Sprite):
#    """
#    This class repesents walls/untraversable terrain
#    """
#
#    def __init__(self, game, x, y):
#        self.groups = game.all_sprites, game.wall_sprites
#        pygame.sprite.Sprite.__init__(self, self.groups)
#
#        self.image = game.player_image
#        self.x = x
#        self.y = y
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
#
#    def update(self, dt):
#        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
