import pygame
from pygame.locals import *
from hbf import sprites
from settings import *

class Magatia(sprites.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.mob_sprites
        self.spritesheet = sprites.SpriteSheet(game.mob_ss_img) #copy?
        x = self.spritesheet.sheet.get_width() / 10
        sx = 9
        sy = 9
        x = 77.5
        y = self.spritesheet.sheet.get_height() / 4
        y = 80
        image = self.spritesheet.image_at((sx, sy, x, y), -1)
        
        sprites.Sprite.__init__(self, game, self.groups, MOB_LAYER, pos, image)  # inherit from Sprite
        
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

class HypnoWorm(sprites.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.mob_sprites
        self.spritesheet = sprites.SpriteSheet(game.spritesheets['hypnoworm']) #copy?
        x = self.spritesheet.sheet.get_width() / 10

        image = self.spritesheet.image_at((0, 35*2, 60*2, 45*2), -1)
        
        sprites.Sprite.__init__(self, game, self.groups, MOB_LAYER, pos, image)  # inherit from Sprite
        
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