import pygame
import pytmx
import sys
import os
from pygame.locals import *
from pytmx import load_pygame
from settings import *
from player import Player, Wall

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
        self.game_map = pytmx.load_pygame(os.path.join(self.map_dir, MAP))

    def new(self):
        # start new game
        self.camera = {
            'x': 0,
            'y': 0
        }

        # Define sprites
        self.all_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.player = Player(self, HALF_WINDOWWIDTH, HALF_WINDOWHEIGHT)
        
        for i in range(0,4):
            Wall(self, 100 + i*64, HALF_WINDOWHEIGHT)

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

    def update(self):
        #Game loop - update
        #Adjust camera
        #Calculate the center pos for the player (the player object itself not the rect it is draw on)
        #I.e. the players position in the world, NOT the position on the screen!! (3 hours wasted on that bug!)
        player_center_x = self.player.x + int(self.player.width /2)
        player_center_y = self.player.y + int(self.player.height / 2)
        
        #if the player is more than cameraslack pixels away from the midpoint then
        #update value for camera to compensate and keep player at most cameraslack pixels from center
        if (self.camera['y'] + HALF_WINDOWHEIGHT) - player_center_y > CAMERASLACK: #Top edge
            self.camera['y'] = player_center_y + CAMERASLACK - HALF_WINDOWHEIGHT
        elif (self.camera['x'] + HALF_WINDOWWIDTH) - player_center_x > CAMERASLACK: #Left edge
            self.camera['x'] = player_center_x + CAMERASLACK - HALF_WINDOWWIDTH
        if player_center_y - (self.camera['y'] + HALF_WINDOWHEIGHT) > CAMERASLACK: #Bottom edge
            self.camera['y'] = player_center_y - CAMERASLACK - HALF_WINDOWHEIGHT
        elif player_center_x - (self.camera['x'] + HALF_WINDOWWIDTH) > CAMERASLACK: #Right edge
            self.camera['x'] = player_center_x - CAMERASLACK - HALF_WINDOWWIDTH

        self.all_sprites.update()

    def events(self):
        #Game loop - events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #elif event.type == KEYDOWN:
            #    # If D-Pad keys are pressed then signal movement (honoured below)
            #    if event.key == K_UP:
            #        self.player.move(dy = -PLAYERSPEED)
            #    elif event.key == K_DOWN:
            #        self.player.move(dy = PLAYERSPEED)
            #    elif event.key == K_RIGHT:
            #        self.player.move(dx = PLAYERSPEED)
            #    elif event.key == K_LEFT:
            #        self.player.move(dx = -PLAYERSPEED)
            

    def draw(self):
        #Game loop - draw
        #Draw map - Should this be a class?
        for layer in self.game_map.visible_layers:
            for x, y, gid, in layer:
                tile = self.game_map.get_tile_image_by_gid(gid)
                if tile != None:
                    self.screen.blit(tile, ((x * self.game_map.tilewidth - self.camera['x']), (y * self.game_map.tileheight - self.camera['y'])))

        #Draw sprites
        self.all_sprites.draw(self.screen)
        pygame.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

pygame.quit()