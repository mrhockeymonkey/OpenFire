import pygame
from pygame.locals import *
from hbf import sprites
from settings import *
from random import choice

vec = pygame.math.Vector2

class Rumo(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        #self.spritesheet = sprites.SpriteSheet(game.mob_ss_img) #copy?
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['rumo']) #copy?
        image = self.spritesheet.image_at((0, 0, 51, 79), -1)
        self.actions = {
            'idle': sprites.SpriteStripAnim(self.spritesheet, (10, 0, 47, 75), 6, colorkey=-1, loop=True,frames=10),
            'move': sprites.SpriteStripAnim(self.spritesheet, (10, 75, 47, 75), 6, colorkey=-1, loop=True,frames=10),
            'hit': sprites.SpriteStripAnim(self.spritesheet, (10, 150, 47, 75), 1, colorkey=-1, loop=False,frames=10),
            'die': sprites.SpriteStripAnim(self.spritesheet, (10, 225, 64, 85), 3, colorkey=-1, loop=False,frames=10) + 
                sprites.SpriteStripAnim(self.spritesheet, (203, 225, 50, 85), 3, colorkey=-1, loop=False,frames=10)
        }

        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)
        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

    def update(self):
        super().update()


class Homunculus(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['homunculus']) #copy?
        # pick an initial image
        image = self.spritesheet.image_at((0, 35*2, 60*2, 45*2), -1)
        self.actions = {
            #attack': sprites.SpriteStripAnim(self.spritesheet, (0, sy, x, y), 6, colorkey=-1, loop=True,frames=10),
            'idle': sprites.SpriteStripAnim(self.spritesheet, (0, 35*2, 60*2, 45*2), 6, colorkey=-1, loop=True,frames=10),
            'die': sprites.SpriteStripAnim(self.spritesheet, (0, 35*2, 60*2, 45*2), 6, colorkey=-1, loop=True,frames=10)

            #'down': SpriteStripAnim(self.spritesheet, (0, 0, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'left': SpriteStripAnim(self.spritesheet, (0, y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'right': SpriteStripAnim(self.spritesheet, (0, 2*y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'up': SpriteStripAnim(self.spritesheet, (0, 3*y, x, y), 4, colorkey=-1, loop=True,  frames=15 )
        }
        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)

        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

    def update(self):
        super().update()


class Homun(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['homun']) #copy?
        image = self.spritesheet.image_at((9, 9, 65, 60), -1)
        self.actions = {
            'sleep': sprites.SpriteStripAnim(self.spritesheet, (9, 9, 64, 60), 4, colorkey=-1, loop=True,frames=20),
            'idle': sprites.SpriteStripAnim(self.spritesheet, (265, 4, 64, 70), 4, colorkey=-1, loop=True,frames=20),
            'move': sprites.SpriteStripAnim(self.spritesheet, (7, 80, 67, 90), 6, colorkey=-1, loop=True,frames=10), #+
                    #sprites.SpriteStripAnim(self.spritesheet, (201, 85, 70, 90), 3, colorkey=-1, loop=True,frames=10),
            'attack': sprites.SpriteStripAnim(self.spritesheet, (201, 85, 70, 90), 3, colorkey=-1, loop=True,frames=10),
            'hit': sprites.SpriteStripAnim(self.spritesheet, (0, 276, 90, 92), 1, colorkey=-1, loop=False,frames=10),
            'die': sprites.SpriteStripAnim(self.spritesheet, (0, 276, 90, 92), 3, colorkey=-1, loop=False,frames=8) + 
                sprites.SpriteStripAnim(self.spritesheet, (270, 276, 97, 92), 3, colorkey=-1, loop=False,frames=8)
        }
        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)
        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

    def update(self):
        super().update()
        
