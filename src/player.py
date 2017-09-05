import pygame
from pygame.locals import *
from settings import *

vec = pygame.math.Vector2

# used to determine when a hit_rect has collided with another sprite
# this is used as a callback function in pygame.sprite.pritecollide()
def collide_hit_rect(sprite1, sprite2):
    return sprite1.hit_rect.colliderect(sprite2.rect)

class Player(pygame.sprite.Sprite):
    """
    This class represents the main player.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, game, x, y):
        # initialize sprite class, adding sprite to groups immediately
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # player image
        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # player position and velocity
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        # player hitbox
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

    def _get_keys(self):
        self.vel = vec(0, 0)

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
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False, collide_hit_rect) #sprite, group, dokill, collided (callback function to override method of checking collisions)
            if hits:
                if self.vel.x > 0: # case when moving to the right
                    self.pos.x = hits[0].rect.left - self.hit_rect.width
                if self.vel.x < 0: # case when moving to the left
                    self.pos.x = hits[0].rect.right
                # cancel out velocity and update the player rect
                self.vel.x = 0
                self.hit_rect.x = self.pos.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0: # case when moving down
                    self.pos.y = hits[0].rect.top - self.hit_rect.height
                if self.vel.y < 0: # case when moving up
                    self.pos.y = hits[0].rect.bottom
                # cancel out velocity and update the player rect
                self.vel.y = 0
                self.hit_rect.y = self.pos.y

    # update is called once every loop before drawing to enact any outstanding changes to the player object
    def update(self):
        # first we check to see what keys are pressed to decide if movement, image or animation is needed
        self._get_keys()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt

        # collision detection
        self.hit_rect.x = self.pos.x
        self._collide_with_wall('x')
        self.hit_rect.y = self.pos.y
        self._collide_with_wall('y')

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # mob image
        self.image = self.game.mob_image
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # mob position and velocity
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # mob hitbox
        self.hit_rect = MOB_HIT_RECT
        self.hit_rect.center = self.rect.center

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


