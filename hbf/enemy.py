import pygame
from pygame.locals import *
from hbf import sprites, animation
from settings import *
from random import choice

vec = pygame.math.Vector2

class Enemy(sprites.Sprite):
    def __init__(self, game, pos, image):
        self.groups = game.all_sprites, game.mob_sprites
        self.layer = MOB_LAYER
        sprites.Sprite.__init__(self, game, pos, image)
        self.action = 'idle'
        self.facing = 'left'
        self.invun = False
        self.hit_rect = self.image.get_rect()
        self.actions[self.action].iter()

    def avoid_mobs(self):
        for mob in self.game.mob_sprites:
            if mob != self:
                # if the vector from other mob to self is within the avoid radius, update acc
                dist = self.pos - mob.pos
                if 0 < dist.length() < ENEMY_AVOID_RADIUS: 
                    self.acc += dist.normalize() #normalize = size of 1 so we just update direction

    def hit(self, damage, knockback):
        if not self.invun:
            print("Enemy HP -{0}".format(damage))
            self.health = self.health - damage
            if self.game.player.facing == 'left':
                self.vel = vec(-knockback, 0)
            else:
                self.vel = vec(knockback, 0)
                
            self.action = 'hit'
            self.actions[self.action].iter()
            if self.game.player.uber:
                self.game.sounds['enemy_cut'].play()
            else:
                self.game.sounds['enemy_hit'].play()

            sprites.Damage(self.game, (self.pos.x, self.pos.y - 50), damage, WHITE)
            self.invun = True

    def update_pos(self):
        # move when player in range or if player is powered up
        self.target_distance = self.game.player.hit_rect.center - self.pos
        if self.target_distance.length_squared() < ENEMY_DETECT_RADIUS**2 or self.game.player.uber: # See notes on Pythagorean theorem
            # calculate the rotation from x axis to player object
            self.rot = self.target_distance.angle_to(vec(1,0))
            self.acc = vec(1, 0).rotate(-self.rot) # accelerate in the direction of the player
            self.avoid_mobs() # avoid other sprites
            self.acc.scale_to_length(ENEMY_SPEED) 
            self.acc += self.vel * -1 # simulate friction
            self.vel += self.acc * self.game.dt # Laws of motion: a = v/t or v = a*t
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 # ??? d = v*t
            self.refresh_rect()
            self.refresh_poly()
            #self.correct_collision(self, self.game.wall_sprites) # now that the sprite has been moved, test for collisions and correct
            self.correct_wall_collision() # now that the sprite has been moved, test for collisions and correct
            self.refresh_rect()
            self.refresh_poly()
        else:
            self.vel = vec(0,0)

    def update_img(self):
        if self.health <= 0:
            #choice(self.game.ENEMY_HIT_SOUND).play()
            self.vel = vec(0,0)
            self.action = 'die'

        if self.action != 'hit' and self.action != 'die':
            if self.vel.length() != 0:
                self.action = 'move'
            else:
                self.action = 'idle'

        try:
            self.image = self.actions[self.action].next()
        except StopIteration as err:
            if self.action == 'die':
                self.kill()
                self.game.mob.remove(self)
            elif self.action == 'hit':
                self.invun = False
                self.action = 'move'
            else:
                raise err

        if 90 < self.rot < 180 or -180 < self.rot < -90: #player is to the left
            if self.facing == 'left':
                pass
            else:
                self.image = pygame.transform.flip(self.image, True, False)
        if 0 < self.rot < 90 or -90 < self.rot < 0: # player is to the right
            if self.facing == 'right':
                pass
            else:
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.update_pos()
        self.update_img()




class Rumo(Enemy):
    def __init__(self, game, pos):
        self.spritesheet = animation.SpriteSheet(game.images['rumo'].copy())
        image = self.spritesheet.image_at((0, 0, 51, 79), -1)
        self.actions = {
            'idle': animation.SpriteStripAnim(self.spritesheet, (10, 0, 47, 75), 6, colorkey=-1, loop=True,frames=10),
            'move': animation.SpriteStripAnim(self.spritesheet, (10, 75, 47, 75), 6, colorkey=-1, loop=True,frames=10),
            'hit': animation.SpriteStripAnim(self.spritesheet, (10, 150, 47, 75), 1, colorkey=-1, loop=False,frames=10),
            'die': animation.SpriteStripAnim(self.spritesheet, (10, 225, 64, 85), 3, colorkey=-1, loop=False,frames=10) + 
                animation.SpriteStripAnim(self.spritesheet, (203, 225, 50, 85), 3, colorkey=-1, loop=False,frames=10)
        }
        Enemy.__init__(self, game, pos, image)
        self.health = RUMO_HEALTH
        self.max_health = RUMO_HEALTH
        self.atk = 3
        self.target = self.game.player

    def update(self):
        super().update()


class Homunculus(Enemy):
    def __init__(self, game, pos):
        self.spritesheet = animation.SpriteSheet(game.images['homunculus'].copy())
        image = self.spritesheet.image_at((0, 35*2, 60*2, 45*2), -1)
        self.actions = {
            'idle': animation.SpriteStripAnim(self.spritesheet, (2, 0, 88, 122), 6, colorkey=-1, loop=True,frames=10),
            'move': animation.SpriteStripAnim(self.spritesheet, (2, 121, 90, 124), 6, colorkey=-1, loop=True,frames=10),
            'die': animation.SpriteStripAnim(self.spritesheet, (10, 370, 110, 138), 4, colorkey=-1, loop=False,frames=10),
            'hit': animation.SpriteStripAnim(self.spritesheet, (10, 370, 110, 138), 1, colorkey=-1, loop=False,frames=12)
        }
        Enemy.__init__(self, game, pos, image)
        self.health = HOMUNCULUS_HEALTH
        self.max_health = HOMUNCULUS_HEALTH
        self.atk = 7
        self.target = self.game.player

    def update(self):
        super().update()


class Homun(Enemy):
    def __init__(self, game, pos):
        self.spritesheet = animation.SpriteSheet(game.images['homun'].copy())
        image = self.spritesheet.image_at((9, 9, 65, 60), -1)
        self.actions = {
            'sleep': animation.SpriteStripAnim(self.spritesheet, (9, 9, 64, 60), 4, colorkey=-1, loop=True,frames=20),
            'idle': animation.SpriteStripAnim(self.spritesheet, (265, 4, 64, 70), 4, colorkey=-1, loop=True,frames=20),
            'move': animation.SpriteStripAnim(self.spritesheet, (7, 80, 67, 90), 6, colorkey=-1, loop=True,frames=10),
            'attack': animation.SpriteStripAnim(self.spritesheet, (201, 85, 70, 90), 3, colorkey=-1, loop=True,frames=10),
            'hit': animation.SpriteStripAnim(self.spritesheet, (0, 276, 90, 92), 1, colorkey=-1, loop=False,frames=10),
            'die': animation.SpriteStripAnim(self.spritesheet, (0, 276, 90, 92), 3, colorkey=-1, loop=False,frames=8) + 
                animation.SpriteStripAnim(self.spritesheet, (270, 276, 97, 92), 3, colorkey=-1, loop=False,frames=8)
        }
        Enemy.__init__(self, game, pos, image)
        self.health = HOMUN_HEALTH
        self.max_health = HOMUN_HEALTH
        self.atk = 11
        self.target = self.game.player

    def update(self):
        super().update()
        
