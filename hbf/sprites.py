import pygame
from pygame.locals import *
from random import uniform, randint, choice
import pytweening as tween
#import pylygon
from settings import *
from itertools import chain
from hbf import animation
from hbf import polygon

vec = pygame.math.Vector2

class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, sprite_sheet, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        
        if not isinstance(sprite_sheet, SpriteSheet):
            raise TypeError("argument 'sprite_sheet' must be of type SpriteSheet")
        self.images = sprite_sheet.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

class Sprite(pygame.sprite.Sprite):
    def __init__(self, game, groups, layer, pos, image):
        pygame.sprite.Sprite.__init__(self, self.groups) # inherite from pygame sprite class and add to groups
        self.game = game
        self.layer = layer # used to decide order in which things are drawn, i.e. bullets below walls becuase you cannot shoot through a wall
        #self.spritesheet = SpriteSheet(spritesheet_img)
        #if sprite_rect is None: #if sprite_rect not specified will assume the whole image to be displayed
        #    sprite_rect = spritesheet_img.get_rect()
        #self.image = self.spritesheet.image_at(spritesheet_img.get_rect(), colorkey=-1) # the initial image for the sprite
        self.image = image
        self.rect = self.image.get_rect() # the rect of the image
        #self.width = self.image.get_width() # the width of the sprite
        #self.height = self.image.get_height() # the height of the sprite
        self.pos = pos # the sprite position as a vector
        self.vel = vec(0, 0) # the sprite velocity as a vector
        self.rot = 0 # the sprites rotation

        self.rect.center = self.pos # update sprite to be at given pos, here we use pos as the center insteasd of topleft


    @staticmethod
    def collide_hitrect(sprite1, sprite2):
        """Returns bool. Determines if a sprite's hitrect has collided with another rect.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        return sprite1.hit_rect.colliderect(sprite2.rect)


    @staticmethod
    def collide_polygon(sprite1, sprite2):
        """ Returnsbool. Determines if a spites hit_poly has collided with another Poly object.
        This is used as an override for the standard collision detection of pygame.sprite.spritecollide()"""
        collision, mpv = sprite1.hit_poly.collidepoly(sprite2.hit_poly)
        return collision

    def update(self):
        pass # this method always exists for a sprite but each subclass of sprite should decide what to update depending on its purpose

    def refresh_hitbox(self):
        """updates the hit_rect and hit_poly to the sprite current pos"""
        self.hit_rect.center = self.pos
        self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])

    def correct_collision(self, sprite, group):
        """Adjust the position of the sprite so that it does not collide with the group. i.e. to stop sprite
        walking through walls and other obstacles"""
        # hits is the list of sprites that the calling sprite has collided with. eg the wall a player has run into
        hits = pygame.sprite.spritecollide(sprite, group, False, Sprite.collide_polygon) #sprite, group, dokill, collided (callback function to override method of checking collisions)
        if hits:
            # if there are any hits we want the minimum push vector to move the sprite away
            collision, mpv = sprite.hit_poly.collidepoly(hits[0].hit_poly)
            
            # update the sprite accordingly
            sprite.pos.x = sprite.pos.x + mpv[0]
            sprite.pos.y = sprite.pos.y + mpv[1]
            sprite.vel.x = 0
            



class Obstacle(Sprite):
    def __init__(self, game, pos, w, h):
        self.groups = game.wall_sprites
        Sprite.__init__(self, game, self.groups, WALL_LAYER, pos, game.player_ss_img) # inherit from Sprite
        self.rect = pygame.Rect(pos.x, pos.y, w, h)


class ObstaclePoly(Sprite):
    def __init__(self, game, pos, points):
        self.groups = game.wall_sprites
        Sprite.__init__(self, game, self.groups, WALL_LAYER, pos, game.player_ss_img) # inherit from Sprite?????
        self.polygon = polygon.Poly(points)
        self.hit_poly = self.polygon








class Weapon(Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        Sprite.__init__(self, game, self.groups, PLAYER_LAYER, pos, game.item_images['pistol']) # inherit from Sprite

    def update(self):
        self.image = self.game.item_images[self.game.player.weapon]
        self.pos = self.game.player.pos
        self.rect.center = self.pos



class Bullet(Sprite):
    def __init__(self, game, pos, dir, dmg):
        self.groups = game.all_sprites, game.bullet_sprites
        Sprite.__init__(self, game, self.groups, BULLET_LAYER, pos, game.bullet_image) # inherit from Sprite

        # bullet positional
        self.pos = vec(pos) # this create a copy of the pos passed in

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
        Sprite.__init__(self, game, self.groups, EFFECT_LAYER, pos, image) # inherit from Sprite

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 40:
            self.kill()

class Item(Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.item_sprites
        Sprite.__init__(self, game, self.groups, ITEMS_LAYER, pos, game.item_images[type]) # inherit from Sprite

        self.type = type
        self.animation = 'rise'
        self.step = 0

    def update(self):
        # bobbing motion - this is split into two phases: rise & bounce
        animation.rise_and_bounce(self, ITEM_BOB_RANGE, ITEM_BOB_SPEED)


class SpriteSheet(object):
    def __init__(self, sheet):
        self.sheet = sheet
        #try:
        #    self.sheet = pygame.image.load(filename).convert()
        #except pygame.error as message:
        #    print('Unable to load spritesheet image:' + filename)
        #    raise SystemExit(message)
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert() #create new surface
        image.fill(self.sheet.get_at((0,0))) # fill original image background
        image.blit(self.sheet, (0, 0), rect) # blit portion of sprite sheet
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

