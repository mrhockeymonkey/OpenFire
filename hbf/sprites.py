import pygame
from pygame.locals import *
from random import uniform, randint, choice
import pytweening as tween
from settings import *
from hbf import animation, polygon

vec = pygame.math.Vector2


class Sprite(pygame.sprite.Sprite):
    """ Generic sprite object that other classes can inherit from """
    def __init__(self, game, pos, image=None):
        pygame.sprite.Sprite.__init__(self, self.groups) # inherite from pygame sprite class and add to groups
        self.game = game
        self.image = image
        if self.image:
            self.rect = self.image.get_rect() # the rect of the image
        else:
            # if there is no image then we create a placeholder rect. 
            # the inheriting class is expected to deal with its own rect
            self.rect = pygame.Rect(0, 0, 100, 100)
        self.pos = pos # the sprite position as a vector
        self.vel = vec(0, 0) # the sprite velocity as a vector
        self.rot = 0 # the sprites rotation
        self.refresh_rect()

    @staticmethod
    def collide_rect(sprite1, sprite2):
        """Returns bool. Determines if a sprite's hit_rect has collided with another rect.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        return sprite1.hit_rect.colliderect(sprite2.rect)

    @staticmethod
    def collide_hitrect(sprite1, sprite2):
        """Returns bool. Determines if a sprite's hit_rect has collided with another hit_rect.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        return sprite1.hit_rect.colliderect(sprite2.hit_rect)

    @staticmethod
    def collide_hitpoly(sprite1, sprite2):
        """ Returnsbool. Determines if a spites hit_poly has collided with another hit_poly object.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        collision, mpv = sprite1.hit_poly.collidepoly(sprite2.hit_poly)
        return collision

    def update(self):
        pass

    def draw_debug(self):
        pygame.draw.rect(self.game.screen, WHITE, self.game.camera.apply(self.rect), 1)
        try:
            pygame.draw.rect(self.game.screen, RED, self.game.camera.apply(self.hit_rect), 1)
        except AttributeError as ae:
            pass

    def refresh_rect(self, offset=None):
        """updates the rect and hit_rect to the sprite current pos"""
        self.rect.center = self.pos
        try:
            if offset:
                self.hit_rect.center = self.pos + offset
            else:
                self.hit_rect.center = self.pos
        except AttributeError as ae:
            pass

    def refresh_poly(self):
        """updates the hit_poly to the sprite current pos"""
        self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])

    def correct_wall_collision(self):
        """ Walls consist of an outer rect and an inner polygon. We only test polygon collision when the sprite rect has
        collided with a wall rect becuase polygon collision is expensive """
        self.game.nearby_wall_sprites.empty()
        
        # detect nearby wall using the collide_rect method
        nearby_walls = pygame.sprite.spritecollide(self, self.game.wall_sprites, False, Sprite.collide_rect)
        if nearby_walls:
            # detect collisions using the collide_polygon method
            self.game.nearby_wall_sprites.add(nearby_walls)
            hits = pygame.sprite.spritecollide(self, self.game.nearby_wall_sprites, False, Sprite.collide_hitpoly)
            self.game.polytests += 1
            if hits:
                # if there are any hits we want the minimum push vector to move the sprite away accordingly
                collision, mpv = self.hit_poly.collidepoly(hits[0].hit_poly)
                self.pos.x = self.pos.x + mpv[0]
                self.pos.y = self.pos.y + mpv[1]
                self.vel.x = 0

    def correct_offmap(self, sprite):
        """
        limit the sprite position to be within the bounds of the map
        """
        sprite.pos.x = max(0 + sprite.rect.width/2, sprite.pos.x) # left
        sprite.pos.y = max(0 + sprite.rect.height/2, sprite.pos.y) # top
        sprite.pos.x = min(self.game.map.width - sprite.rect.width/2, sprite.pos.x) # right
        sprite.pos.y = min(self.game.map.height - sprite.rect.height/2, sprite.pos.y) # bottom


class Damage(Sprite):
    def __init__(self, game, pos, val,col):
        self.groups = game.all_sprites, game.damage_sprites
        self.layer = BULLET_LAYER
        size = 30
        image = pygame.font.Font(None, size).render(str(val), True, col)
        Sprite.__init__(self, game, pos, image)
        self.vel = vec(10, -30)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.refresh_rect()
        if pygame.time.get_ticks() - self.spawn_time > 500:
            self.kill()


class LevelExit(Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.exit_sprites
        self.layer = BULLET_LAYER
        Sprite.__init__(self, game, pos)
        self.hit_rect = self.rect


class ObstacleRect(Sprite):
    def __init__(self, game, pos, w, h):
        self.groups = game.all_sprites, game.wall_sprites
        self.layer = WALL_LAYER
        Sprite.__init__(self, game, pos) # inherit from Sprite
        self.rect = pygame.Rect(pos.x, pos.y, w, h)


class ObstaclePoly(Sprite):
    def __init__(self, game, pos, points):
        self.groups = game.all_sprites, game.wall_sprites
        self.layer = WALL_LAYER
        Sprite.__init__(self, game, pos) # inherit from Sprite?????
        self.polygon = polygon.Poly(points)
        self.hit_poly = self.polygon
        self.rect = self.get_rect()

    def get_rect(self):
        """return a rect that contains this polygon"""
        x = list(map(lambda x: x[0], self.polygon.points))
        y = list(map(lambda y: y[1], self.polygon.points))

        return pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

    def draw_debug(self):
        super().draw_debug()
        pygame.draw.polygon(self.game.screen, CYAN, (self.game.camera.apply_poly(self.hit_poly)).points, 1)


class SwordStrike(Sprite):
    """ Serves as a means of transmitting player attack into enemy sprites with a frame based timer"""
    def __init__(self, game, pos, damage, force):
        self.groups = game.all_sprites, game.sword_sprites
        self.layer = BULLET_LAYER
        Sprite.__init__(self, game, pos)
        self.damage = damage
        self.force = force
        self.hit_rect = SWORD_STRIKE_RECT.copy()
        self.spawn_time = pygame.time.get_ticks() # record at what time the bullet was spawned

    def update(self):
        self.refresh_rect()
        if pygame.time.get_ticks() - self.spawn_time > 40:
            self.kill()


class Item(Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.item_sprites
        self.layer = ITEMS_LAYER
        Sprite.__init__(self, game, pos, game.images[type]) # inherit from Sprite
        self.type = type
        self.hit_rect = ITEM_HIT_RECT.copy()
        self.animation = 'rise'
        self.step = 0

    def update(self):
        # bobbing motion - this is split into two phases: rise & bounce
        animation.rise_and_bounce(self, ITEM_BOB_RANGE, ITEM_BOB_SPEED)
        self.refresh_rect()

class FlamePrincess(Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.npc_sprites
        self.layer = PLAYER_LAYER
        self.ssheets = {
            'idle'  : animation.SpriteSheet(game.images['fp_idle'])
        }
        self.actions = {
            'idle': animation.SpriteStripAnim(self.ssheets['idle'], (30, 0, 32, 72), 6, colorkey=-1, loop=True,  frames=10 )
        }
        self.action = 'idle'
        init_image = self.actions[self.action].images[0]
        Sprite.__init__(self, game, pos, init_image) # inherit from Sprite
        self.actions[self.action].iter()
        self.hit_rect = FP_HIT_RECT.copy()
        self.refresh_rect()

    def update(self):
        self.image = self.actions[self.action].next()

