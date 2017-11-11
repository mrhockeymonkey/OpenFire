import pygame
from pygame.locals import *
from random import uniform, randint, choice
import pytweening as tween
from settings import *
from itertools import chain
from hbf import animation

vec = pygame.math.Vector2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, game, groups, layer, image, pos):
        pygame.sprite.Sprite.__init__(self, self.groups) # inherite from pygame sprite class and add to groups
        self.game = game
        self.layer = layer # used to decide order in which things are drawn, i.e. bullets below walls becuase you cannot shoot through a wall
        self.image = image # the image for the sprite
        self.rect = self.image.get_rect() # the rect of the image
        self.width = self.image.get_width() # the width of the sprite
        self.height = self.image.get_height() # the height of the sprite
        self.pos = pos # the sprite position as a vector
        self.vel = vec(0, 0) # the sprite velocity as a vector
        self.rot = 0 # the sprites rotation
        self.rect.center = self.pos # update sprite to be at given pos

    @staticmethod
    def collide_hitrect(sprite1, sprite2):
        """Returns bool. Determines if a sprite's hitrect has collided with another rect.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        return sprite1.hit_rect.colliderect(sprite2.rect)

    def correct_collision(self, sprite, group, direction):
        if direction == 'x':
            # detect is there is any pixel collision between sprite rects
            hits = pygame.sprite.spritecollide(sprite, group, False, Sprite.collide_hitrect) #sprite, group, dokill, collided (callback function to override method of checking collisions)
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx: #i.e. if player center > wall center then player is on RHS
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width
                if hits[0].rect.centerx < sprite.hit_rect.centerx: # player is LHS
                    sprite.pos.x = hits[0].rect.right
                # cancel out velocity and update the player rect
                sprite.vel.x = 0
                sprite.hit_rect.x = sprite.pos.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, False, Sprite.collide_hitrect)
            if hits:
                if hits[0].rect.centery > sprite.hit_rect.centery: # player below
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height
                if hits[0].rect.centery < sprite.hit_rect.centery: # player above
                    sprite.pos.y = hits[0].rect.bottom
                # cancel out velocity and update the player rect
                sprite.vel.y = 0
                sprite.hit_rect.y = sprite.pos.y


class Obstacle(Sprite):
    def __init__(self, game, pos, w, h):
        self.groups = game.wall_sprites
        Sprite.__init__(self, game, self.groups, WALL_LAYER, game.player_image, pos) # inherit from Sprite
        self.rect = pygame.Rect(pos.x, pos.y, w, h)


#class Player(pygame.sprite.Sprite):
class Player(Sprite):
    """
    This class represents the main player. It derives from the "Sprite" class in Pygame.

    A player object has a rect for the player image and also a rect for the player hitbox
    The hitbox is used to determine collisions as solves some problems with using the image rect for collision detection. 
    """

    def __init__(self, game, pos):
        self.groups = game.all_sprites
        Sprite.__init__(self, game, self.groups, PLAYER_LAYER, game.player_image, pos) # inherit from Sprite
        
        self.hit_rect = PLAYER_HIT_RECT.copy() 
        self.hit_rect.center = self.rect.center
        
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH

        self.weapon = 'pistol'
        self.damaged = False

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
            self.shoot()

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1,0).rotate(-self.rot)
            
            for i in range(WEAPONS[self.weapon]['count']):
                Bullet(self.game, self.pos, dir, WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            #kick back
            #self.vel = vec(-BULLET_KICKBACK).rotate(-self.rot)
            #muzzle flash
            MuzzleFlash(self.game, self.pos)

    # update is called once every loop before drawing to enact any outstanding changes to the player object
    def update(self):
        # get keys to determine velocity
        self._get_keys()

        # update sprite pos (distance = velocity * time), this gives smooth movement independant of frame rate
        self.pos += self.vel * self.game.dt
        self.image = self.game.player_image.copy() #tis
        if self.damaged:
            try:
                val = next(self.damage_alpha)
                print(val)
                self.image.fill((255, 0, 0, val), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        # collision detection, we update the hit_rect and test for collisions
        self.hit_rect.x = self.pos.x
        self.correct_collision(self, self.game.wall_sprites, 'x')
        self.hit_rect.y = self.pos.y
        self.correct_collision(self, self.game.wall_sprites, 'y')

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

class Mob(Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.mob_sprites
        Sprite.__init__(self, game, self.groups, MOB_LAYER, game.mob_image.copy(), pos)  # inherit from Sprite
        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.health = MOB_HEALTH
        self.target = self.game.player

    def draw_health(self):
        width = int(self.rect.width  * self.health / MOB_HEALTH)
        health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(self.image, RED, health_bar)
        #pygame.draw.rect(self.game.screen, RED, health_bar)

    def avoid_mobs(self):
        for mob in self.game.mob_sprites:
            if mob != self:
                # if the vector from other mob to self is within the avoid radius, update acc
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS: 
                    self.acc += dist.normalize() #normalize = size of 1 so we just update direction

    def update(self):
        target_distance = self.game.player.pos - self.pos
        if target_distance.length_squared() < MOB_DETECT_RADIUS**2: #why?
            # update target (player.pos - mob.pos is the vector FROM mob->player)
            #self.target = self.game.player.pos - self.pos # the vector from mob to player
            
            # update image depending on location of target, i.e. always face the player. 
            #if self.target.x < 0:
            #    self.image = self.image_left
            #elif self.target.x > 0:
            #    self.image = self.image_right

            # calcukate the rotation from x axis to player object
            # angle_to get the angle between that vectore and the x axis
            self.rot = target_distance.angle_to(vec(1,0))

            # the acceleration is always in the direction of the player
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(MOB_SPEED)
            self.acc += self.vel * -1 # friction
            
            # Laws of motion: a = v/t or v = a*t
            self.vel += self.acc * self.game.dt
            
            # ??? d = v*t
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            #sself.rect.center = self.pos

        # collision detection
        self.hit_rect.x = self.pos.x
        self.correct_collision(self, self.game.wall_sprites, 'x')
        self.hit_rect.y = self.pos.y
        self.correct_collision(self, self.game.wall_sprites, 'y')

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            choice(self.game.mob_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat_image, self.pos)


class Bullet(Sprite):
    def __init__(self, game, pos, dir, dmg):
        self.groups = game.all_sprites, game.bullet_sprites
        Sprite.__init__(self, game, self.groups, BULLET_LAYER, game.bullet_image, pos) # inherit from Sprite

        # bullet positional
        self.pos = vec(pos) # this create a copy of the pos passed in
        #self.rect.center = self.pos
        spread = uniform(-WEAPONS[self.game.player.weapon]['spread'], WEAPONS[self.game.player.weapon]['spread']) # randomize the path the bullet will take between BULLET_SPREAD
        self.vel = dir.rotate(spread) * WEAPONS[self.game.player.weapon]['speed'] * uniform(0.9, 1.1)
        # bullet specific
        self.dmg = dmg
        self.spawn_time = pygame.time.get_ticks() # record at what time the bullet was spawned

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if pygame.sprite.spritecollideany(self, self.game.wall_sprites):
            self.kill()

        # check to see if bullet lifetime has passed
        if pygame.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['lifetime']:
            self.kill()


class MuzzleFlash(Sprite):
    def __init__(self, game, pos):
        self.groups =game.all_sprites
        size = randint(20, 50)
        image = pygame.transform.scale(choice(game.gun_flashes), (size,size))
        Sprite.__init__(self, game, self.groups, EFFECT_LAYER, image, pos) # inherit from Sprite

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 40:
            self.kill()

class Item(Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.item_sprites
        Sprite.__init__(self, game, self.groups, ITEMS_LAYER, game.item_images[type], pos) # inherit from Sprite

        self.type = type
        self.animation = 'rise'
        self.step = 0

    def update(self):
        # bobbing motion - this is split into two phases: rise & bounce
        animation.Animate.rise_and_bounce(self, ITEM_BOB_RANGE, ITEM_BOB_SPEED)
