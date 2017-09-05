import pygame
import pytmx
import sys
import os

from pygame.locals import *
from pytmx import load_pygame

from settings import *
from player import Player, Wall, Mob
from tilemap import Map, Camera

class Game:
    def __init__(self):
        # initiate game
        pygame.init()
        pygame.key.set_repeat(1, 1) # (delay, repeat)
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.draw_debug = False

        # loading files
        self.load_data()

    def load_data(self):
        self.dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir, '../img')
        self.map_dir = os.path.join(self.dir, '../map')

        self.player_image = pygame.image.load(os.path.join(self.img_dir, PLAYER_IMAGE))
        self.bullet_image = pygame.image.load(os.path.join(self.img_dir, BULLET_IMG))
        self.mob_image = pygame.image.load(os.path.join(self.img_dir, MOB_IMAGE))
        self.game_map = pytmx.load_pygame(os.path.join(self.map_dir, MAP))

    def new(self):

        self.map = Map(self)
        self.camera = Camera(self.map, WINDOWWIDTH, WINDOWHEIGHT)

        # Define sprites
        self.all_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.player = Player(self, HALF_WINDOWWIDTH, HALF_WINDOWHEIGHT)
        for i in range(0,10):
            Mob(self, 100*i, 70*i)

        for i in range(0,4):
            Wall(self, 100 + i*64, HALF_WINDOWHEIGHT - 150)

        self.run()

    def run(self):
        # Game loop
        while True:
            # clock.tick delays loop enough to stay at the correct FPS
            # dt is how long the previous frame took in seconds, this is used to produce smooth movement independant of frame rate
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        #Game loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        # call the update method on all sprites
        self.all_sprites.update()

        # ???
        self.camera.update(self.player)

        # bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mob_sprites, self.bullet_sprites, False, True)
        for hit in hits:
            hit.kill()
  

    def draw(self):

        # draw map
        self.map.draw(self.screen)

        # draw sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        
        # debug 
        if self.draw_debug == True:
            pygame.display.set_caption("FPS: {:.2f}".format(self.clock.get_fps()))
            pygame.draw.rect(self.screen, WHITE, self.camera.apply(self.player.rect), 2) #screen, color, rect, thickness
            pygame.draw.rect(self.screen, RED, self.player.hit_rect, 2)
            for sprite in self.mob_sprites:
                pygame.draw.rect(self.screen, WHITE, self.camera.apply(sprite.rect), 2)
                pygame.draw.rect(self.screen, RED, sprite.hit_rect, 2)
                pygame.draw.line(self.screen, RED, (sprite.pos), (sprite.pos + sprite.target )) # target line
        
        # update the screen
        pygame.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

pygame.quit()