import pygame
import pytmx
from settings import *

class TileMap(object):
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def _render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self._render(temp_surface)
        return temp_surface

class Hud(object):
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y
        self.hbar_length = 100
        self.hbar_height = 20
        self.hbar_outline =  pygame.Rect(x, y, self.hbar_length, self.hbar_height)
        self.hbar_outline_col = WHITE
        self.hbar_fill = pygame.Rect(x, y, self.hbar_length, self.hbar_height)
        self.hbar_fill_col = GREEN

    def update(self):
        # calculate percent health player has
        pct = self.player.health / self.player.max_health
        if pct < 0:
            pct = 0

        # based on pct choose color
        if pct > 0.6:
            self.hbar_fill_col = GREEN
        elif pct > 0.3:
            self.hbar_fill_col = YELLOW
        else:
            self.hbar_fill_col = RED

        # update the hud rect that will be drawn
        fill = pct * self.hbar_length
        self.hbar_fill = pygame.Rect(self.x, self.y, fill, self.hbar_height)


class Camera(object):
    """The camera is simply a Rect that moves with the player
    As the camera moves other objects are shifted the same amount in the opposite direction
    to create the feeling that the camera is scrolling through the map"""
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
