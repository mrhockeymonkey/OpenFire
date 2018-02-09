import pygame
from pygame.locals import *
from hbf import sprites
from settings import *
from random import choice

vec = pygame.math.Vector2

class Magatia(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        self.spritesheet = sprites.SpriteSheet(game.mob_ss_img) #copy?
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['magatia']) #copy?
        x = self.spritesheet.sheet.get_width() / 10
        sx = 9
        sy = 9
        x = 77.5
        y = self.spritesheet.sheet.get_height() / 4
        y = 80
        image = self.spritesheet.image_at((sx, sy, x, y), -1)
        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)
        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

        self.strips = {
            'attack': sprites.SpriteStripAnim(self.spritesheet, (sx, sy, x, y), 6, colorkey=-1, loop=True,frames=10),
            'normal': sprites.SpriteStripAnim(self.spritesheet, (sx, y, x, y), 6, colorkey=-1, loop=True,frames=10)

            #'down': SpriteStripAnim(self.spritesheet, (0, 0, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'left': SpriteStripAnim(self.spritesheet, (0, y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'right': SpriteStripAnim(self.spritesheet, (0, 2*y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'up': SpriteStripAnim(self.spritesheet, (0, 3*y, x, y), 4, colorkey=-1, loop=True,  frames=15 )
        }
        self.n = 'normal'
        self.strips[self.n].iter()

    def draw_health(self):
        width = int(self.rect.width  * self.health / MOB_HEALTH)
        health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(self.image, RED, health_bar)
        #pygame.draw.rect(self.game.screen, RED, health_bar)



    def update(self):
        super().update()

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_hitbox()
        self.correct_collision(self, self.game.wall_sprites)
        self.refresh_hitbox()

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            choice(self.game.mob_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat_image, self.pos)

        if self.vel.length() != 0:
            self.n = 'attack'
        else:
            self.n = 'normal'
        self.image = self.strips[self.n].next()

class HypnoWorm(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['hypnoworm']) #copy?
        image = self.spritesheet.image_at((0, 35*2, 60*2, 45*2), -1)
        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)

        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

        self.strips = {
            #attack': sprites.SpriteStripAnim(self.spritesheet, (0, sy, x, y), 6, colorkey=-1, loop=True,frames=10),
            'idle': sprites.SpriteStripAnim(self.spritesheet, (0, 35*2, 60*2, 45*2), 6, colorkey=-1, loop=True,frames=10)

            #'down': SpriteStripAnim(self.spritesheet, (0, 0, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'left': SpriteStripAnim(self.spritesheet, (0, y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'right': SpriteStripAnim(self.spritesheet, (0, 2*y, x, y), 4, colorkey=-1, loop=True,  frames=15 ),
            #'up': SpriteStripAnim(self.spritesheet, (0, 3*y, x, y), 4, colorkey=-1, loop=True,  frames=15 )
        }
        self.n = 'idle'
        self.strips[self.n].iter()

    def draw_health(self):
        width = int(self.rect.width  * self.health / MOB_HEALTH)
        health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(self.image, RED, health_bar)
        #pygame.draw.rect(self.game.screen, RED, health_bar)


    def update(self):
        super().update()

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_hitbox()
        self.correct_collision(self, self.game.wall_sprites)
        self.refresh_hitbox()

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            choice(self.game.mob_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat_image, self.pos)

        if self.vel.length() != 0:
            self.n = 'idle'
        else:
            self.n = 'idle'
        self.image = self.strips[self.n].next()


class Homun(sprites.Enemy):
    def __init__(self, game, pos):
        # pick enemy image
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['homun']) #copy?
        image = self.spritesheet.image_at((9, 9, 65, 60), -1)
        # inherit Enemy class
        sprites.Enemy.__init__(self, game, pos, image)
        
        self.hit_rect = MOB_HIT_RECT.copy()
        self.refresh_hitbox()
        #self.hit_rect.center = self.rect.center
        #self.hit_poly = polygon.Poly([self.hit_rect.topleft, self.hit_rect.topright, self.hit_rect.bottomright, self.hit_rect.bottomleft])
        self.health = MOB_HEALTH
        self.target = self.game.player

        self.strips = {
            'sleep': sprites.SpriteStripAnim(self.spritesheet, (9, 9, 64, 60), 4, colorkey=-1, loop=True,frames=20),
            'idle': sprites.SpriteStripAnim(self.spritesheet, (265, 4, 64, 70), 4, colorkey=-1, loop=True,frames=20),
            'move': sprites.SpriteStripAnim(self.spritesheet, (7, 80, 67, 90), 6, colorkey=-1, loop=True,frames=10), #+
                    #sprites.SpriteStripAnim(self.spritesheet, (201, 85, 70, 90), 3, colorkey=-1, loop=True,frames=10),
            'attack': sprites.SpriteStripAnim(self.spritesheet, (201, 85, 70, 90), 3, colorkey=-1, loop=True,frames=10),
            'hit': sprites.SpriteStripAnim(self.spritesheet, (7, 80, 67, 92), 3, colorkey=-1, loop=True,frames=10),
            'die': sprites.SpriteStripAnim(self.spritesheet, (0, 276, 90, 92), 3, colorkey=-1, loop=False,frames=8) + 
                sprites.SpriteStripAnim(self.spritesheet, (270, 276, 97, 92), 3, colorkey=-1, loop=False,frames=8)
        }
        self.n = 'idle'
        self.strips[self.n].iter()


    def update(self):
        super().update()

        # now that the sprite has been moved, test for collisions and correct
        self.refresh_hitbox()
        self.correct_collision(self, self.game.wall_sprites)
        self.refresh_hitbox()

        # keep the image and hit box together always
        self.rect.center = self.hit_rect.center


        if self.vel.length() != 0:
            self.n = 'move'
        else:
            self.n = 'idle'
        #if target_distance.length_squared() < MOB_ATTACK_RADIUS**2:
        #    self.n = 'attack'
        if self.health <= 0:
            choice(self.game.mob_hit_sounds).play()
            self.vel = vec(0,0)
            self.n = 'die'
            #self.kill()
            #self.game.map_img.blit(self.game.splat_image, self.pos)
        try:
            self.image = self.strips[self.n].next()
        except StopIteration as err:
            if self.n == 'die':
                self.kill()
                self.game.map_img.blit(self.game.splat_image, self.pos)
            else:
                raise err

        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        
