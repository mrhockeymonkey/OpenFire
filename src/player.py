import pygame
from pygame.locals import *
from settings import *

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
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def _get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.vx = -PLAYER_SPEED
        if keys[K_RIGHT] or keys[K_d]:
            self.vx = PLAYER_SPEED
        if keys[K_UP] or keys[K_w]:
            self.vy = -PLAYER_SPEED
        if keys[K_DOWN] or keys[K_s]:
            self.vy = PLAYER_SPEED
        # to stop faster diagonal movement need to multipy by square root of 2
        if self.vx != 0 and self.y != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    def _collide_with_wall(self, direction):
        if direction == 'x':
            # detect is there is any pixel collision between sprite rects
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.vx > 0: # case when moving to the right
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: # case when moving to the left
                    self.x = hits[0].rect.right
                # cancel out velocity and update the player rect
                self.vx = 0
                self.rect.x = self.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.vy > 0: # case when moving down
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0: # case when moving up
                    self.y = hits[0].rect.bottom
                # cancel out velocity and update the player rect
                self.vy = 0
                self.rect.y = self.y

    
    def update(self):
        # first we check to see what keys are pressed to decide if movement, image or animation is needed
        self._get_keys()

        # update sprite pos (distance = velocity * time)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # collision detection
        self.rect.x = self.x
        self._collide_with_wall('x')
        self.rect.y = self.y
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
