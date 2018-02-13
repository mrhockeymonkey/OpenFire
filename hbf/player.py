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
        
        self.spritesheet = sprites.SpriteSheet(game.player_ss_img)
        x = self.spritesheet.sheet.get_width() / 4
        y = self.spritesheet.sheet.get_height() / 4
        image = self.spritesheet.image_at((0, 50, 130, 130), -1)
        sprites.Sprite.__init__(self, game, self.groups, PLAYER_LAYER, pos, image) # inherit from Sprite
        
        self.hit_rect = PLAYER_HIT_RECT.copy() 
        self.refresh_hitbox()
        
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH

        self.weapon = 'pistol'
        self.damaged = False

        self.weaponn = sprites.Weapon(self.game, self.pos)

        #self.ss = SpriteSheet(os.path.join('C:/Users/Scott/OneDrive/Code/HappyBattleFactor/img', 'steampunk_f12.png'))
        #self.sprite_sheet = SpriteSheet(self.game.player_image)
        x = self.spritesheet.sheet.get_width() / 4
        y = self.spritesheet.sheet.get_height() / 4
        self.strips = {
            'idle': sprites.SpriteStripAnim(self.spritesheet, (0, 25*2, 66*2, 65*2), 12, colorkey=-1, loop=True,  frames=7 ),
            'run': sprites.SpriteStripAnim(self.spritesheet, (0, 860*2, 54*2, 65*2), 12, colorkey=-1, loop=True,  frames=7 )
            #'down': sprites.SpriteStripAnim(self.spritesheet, (0, 0, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'left': sprites.SpriteStripAnim(self.spritesheet, (0, y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'right': sprites.SpriteStripAnim(self.spritesheet, (0, 2*y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'up': sprites.SpriteStripAnim(self.spritesheet, (0, 3*y, x, y), 4, colorkey=-1, loop=True,  frames=15 )
        }
        
        self.n = 'idle'
        self.strips[self.n].iter()
        
        #self.image = game.player_ss_img
        #self.image = self.strips[self.n].next()
        self.rect = self.image.get_rect()
        #self.image = self.strips[self.n].next()
        #self.image = pygame.transform.scale(self.image, (50,50))

    def _get_keys(self):
        self.vel = vec(0, 0)

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.vel.x = -PLAYER_SPEED
            self.n = 'run'
        if keys[K_RIGHT] or keys[K_d]:
            self.vel.x = PLAYER_SPEED
            self.n = 'run'
        if keys[K_UP] or keys[K_w]:
            self.vel.y = -PLAYER_SPEED
            self.n = 'run'
        if keys[K_DOWN] or keys[K_s]:
            self.vel.y = PLAYER_SPEED
            self.n = 'run'
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
                sprites.Bullet(self.game, self.pos, dir, WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            #kick back
            #self.vel = vec(-BULLET_KICKBACK).rotate(-self.rot)
            #muzzle flash
            sprites.MuzzleFlash(self.game, self.pos)

    # update is called once every loop before drawing to enact any outstanding changes to the player object
    def update(self):
        # get keys to determine velocity
        self._get_keys()

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
        self.refresh_hitbox()


        #self.n += 1
        #if self.n >= len(self.strips):
        #    self.n = 0
        #self.strips[self.n].iter()
        #if self.vel != 0:

        #if self.vel.length() != 0:
        self.image = self.strips[self.n].next()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.image = pygame.transform.flip(self.image, True, False)