import pygame
from pygame.locals import *
from settings import *


class Map:
    def __init__(self, game):
        self.game = game
        self.map = self.game.game_map
        self.tilewidth = self.map.tilewidth
        self.tileheight = self.map.tileheight
        self.width = self.map.width * self.tilewidth
        self.height = self.map.height * self.tileheight

    def draw(self, screen):
        for layer in self.map.visible_layers:
            for x, y, gid, in layer:
                tile = self.map.get_tile_image_by_gid(gid)
                if tile != None:
                    tile_x = x * self.tilewidth
                    tile_y = y * self.tileheight
                    tile_rect = pygame.Rect(tile_x, tile_y , tile_x + self.tilewidth, tile_y + self.tileheight)
                    screen.blit(tile, self.game.camera.apply(tile_rect))


"""
The camera is simply a Rect that moves with the player

As the camera moves other objects are shifted the same amount in the opposite direction
to create the feeling that the camera is scrolling through the map
"""
class Camera:
    def __init__(self, map, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, self.width, self.height)
        self.map = map

    # given a rect simply shift it the amount the camera has "moved"
    def apply(self, rect):
        return rect.move(self.camera.topleft)

    # updates the pos of the camera based on the target being tracked
    def update(self, target):
        # update the pos of the camera rect
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.map.width - self.width), x) # right
        y = max(-(self.map.height - self.height), y) # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)