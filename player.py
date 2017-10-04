import pygame
from pygame.locals import *
from random import uniform

from settings import *

vec = pygame.math.Vector2

# used to determine when a hit_rect has collided with another sprite
# this is used as a callback function in pygame.sprite.pritecollide()
def collide_hit_rect(sprite1, sprite2):
    return sprite1.hit_rect.colliderect(sprite2.rect)

def collide_wall(sprite, group, direction):
    if direction == 'x':
        # detect is there is any pixel collision between sprite rects
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect) #sprite, group, dokill, collided (callback function to override method of checking collisions)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx: #i.e. if player center > wall center then player is on RHS
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width
            if hits[0].rect.centerx < sprite.hit_rect.centerx: # player is LHS
                sprite.pos.x = hits[0].rect.right
            # cancel out velocity and update the player rect
            sprite.vel.x = 0
            sprite.hit_rect.x = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery: # player below
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height
            if hits[0].rect.centery < sprite.hit_rect.centery: # player above
                sprite.pos.y = hits[0].rect.bottom
            # cancel out velocity and update the player rect
            sprite.vel.y = 0
            sprite.hit_rect.y = sprite.pos.y

class Player(pygame.sprite.Sprite):
    """
    This class represents the main player. It derives from the "Sprite" class in Pygame.

    A player object has a rect for the player image and also a rect for the player hitbox
    The hitbox is used to determine collisions as solves some problems with using the image rect for collision detection. 
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
        self.rot = 0
        # player hitbox
        self.hit_rect = PLAYER_HIT_RECT.copy() 
        self.hit_rect.center = self.rect.center
        
        self.last_shot = 0
        self.health = PLAYER_HEALTH

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

        if keys[K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1,0).rotate(-self.rot)
                Bullet(self.game, self.pos, dir)
                
                #kick back
                #self.vel = vec(-BULLET_KICKBACK).rotate(-self.rot)

    # update is called once every loop before drawing to enact any outstanding changes to the player object
    def update(self):
        # get keys to determine velocity
        self._get_keys()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt

        # collision detection, we update the hit_rect and test for collisions
        self.hit_rect.x = self.pos.x
        collide_wall(self, self.game.wall_sprites, 'x')
        self.hit_rect.y = self.pos.y
        collide_wall(self, self.game.wall_sprites, 'y')

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # mob image
        self.image_left = self.game.mob_image
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # mob position and velocity
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # mob hitbox
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.health = MOB_HEALTH

    def draw_health(self):
        width = int(self.rect.width  * self.health / 100)
        health_bar = pygame.Rect(0, 0, width, 20)
        pygame.draw.rect(self.game.screen, RED, health_bar)


    def update(self):
        # update target (player.pos - mob.pos is the vector FROM mob->player)
        self.target = self.game.player.pos - self.pos # the vector from mob to player
        
        # update image depending on location of target, i.e. always face the player. 
        if self.target.x < 0:
            self.image = self.image_left
        elif self.target.x > 0:
            self.image = self.image_right

        # calcukate the rotation from x axis to player object
        # angle_to get the angle between that vectore and the x axis
        self.rot = self.target.angle_to(vec(1,0))

        # the acceleration is always in the direction of the player
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1 # friction
        
        # Laws of motion: a = v/t or v = a*t
        self.vel += self.acc * self.game.dt
        
        # ??? d = v*t
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #sself.rect.center = self.pos

        # collision detection
        self.hit_rect.x = self.pos.x
        collide_wall(self, self.game.wall_sprites, 'x')
        self.hit_rect.y = self.pos.y
        collide_wall(self, self.game.wall_sprites, 'y')

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullet_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # bullet image
        self.image = self.game.bullet_image
        self.rect = self.image.get_rect()
        # bullet positional
        self.pos = vec(pos) # this create a copy of the pos passed in
        self.rect.center = self.pos
        spread = uniform(-BULLET_SPREAD / 2, BULLET_SPREAD / 2) # randomize the path the bullet will take between BULLET_SPREAD
        self.vel = dir.rotate(spread) * BULLET_SPEED
        # bullet specific
        self.spawn_time = pygame.time.get_ticks() # record at what time the bullet was spawned

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if pygame.sprite.spritecollideany(self, self.game.wall_sprites):
            self.kill()

        # check to see if bullet lifetime has passed
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

#class Wall(pygame.sprite.Sprite):
#    def __init__(self, game, x, y):
#        self.groups = game.all_sprites, game.wall_sprites
#        pygame.sprite.Sprite.__init__(self, self.groups)
#        self.game = game
#        self.image = self.game.player_image
#        self.rect = self.image.get_rect()
#        self.x = x
#        self.y = y
#        self.rect.x = self.x
#        self.rect.y = self.y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.wall_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.player_image
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        #self.rect.x = self.x
        #self.rect.y = self.y


