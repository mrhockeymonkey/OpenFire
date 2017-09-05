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

        # loading files
        self.load_data()

    def load_data(self):
        self.dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.dir, '../img')
        self.map_dir = os.path.join(self.dir, '../map')

        self.player_image = pygame.image.load(os.path.join(self.img_dir, PLAYER_IMAGE))
        self.mob_image = pygame.image.load(os.path.join(self.img_dir, MOB_IMAGE))
        self.game_map = pytmx.load_pygame(os.path.join(self.map_dir, MAP))

    def new(self):

        self.map = Map(self)
        self.camera = Camera(self.map, WINDOWWIDTH, WINDOWHEIGHT)

        # Define sprites
        self.all_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.player = Player(self, HALF_WINDOWWIDTH, HALF_WINDOWHEIGHT)
        self.mob = Mob(self, 400, 600)

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
        #Game loop - update
        #Adjust camera
        #Calculate the center pos for the player (the player object itself not the rect it is draw on)
        #I.e. the players position in the world, NOT the position on the screen!! (3 hours wasted on that bug!)
        #player_center_x = self.player.x + int(self.player.width /2)
        #player_center_y = self.player.y + int(self.player.height / 2)
        
        #if the player is more than cameraslack pixels away from the midpoint then
        #update value for camera to compensate and keep player at most cameraslack pixels from center
        #if (self.camera['y'] + HALF_WINDOWHEIGHT) - player_center_y > CAMERASLACK: #Top edge
        #    self.camera['y'] = player_center_y + CAMERASLACK - HALF_WINDOWHEIGHT
        #elif (self.camera['x'] + HALF_WINDOWWIDTH) - player_center_x > CAMERASLACK: #Left edge
        #    self.camera['x'] = player_center_x + CAMERASLACK - HALF_WINDOWWIDTH
        #if player_center_y - (self.camera['y'] + HALF_WINDOWHEIGHT) > CAMERASLACK: #Bottom edge
        #    self.camera['y'] = player_center_y - CAMERASLACK - HALF_WINDOWHEIGHT
        #elif player_center_x - (self.camera['x'] + HALF_WINDOWWIDTH) > CAMERASLACK: #Right edge
        #    self.camera['x'] = player_center_x - CAMERASLACK - HALF_WINDOWWIDTH


        self.all_sprites.update()
        self.camera.update(self.player)
  

    def draw(self):

        # draw map
        self.map.draw(self.screen)

        # draw sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        
        # debug 
        pygame.display.set_caption("FPS: {:.2f}".format(self.clock.get_fps()))
        pygame.draw.rect(self.screen, WHITE, self.camera.apply(self.player.rect), 2) #screen, color, rect, thickness
        pygame.draw.rect(self.screen, RED, self.player.hit_rect, 2)
        
        # update the screen
        pygame.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

pygame.quit()