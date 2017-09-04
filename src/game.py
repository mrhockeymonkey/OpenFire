import pygame
import pytmx
import sys
import os
from pygame.locals import *
from pytmx import load_pygame
from settings import *
from player import Player

def main():

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    CLOCK = pygame.time.Clock()

    camera = {
        'x': 0,
        'y': 0
    }
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False

    #Loading files
    game_map = pytmx.load_pygame(MAP)
    player_image = pygame.image.load(PLAYERIMG)

    #Define sprites
    all_sprites_list = pygame.sprite.Group()
    player = Player(player_image, HALF_WINDOWWIDTH, HALF_WINDOWHEIGHT, camera)
    all_sprites_list.add(player)

    # -------- Main Program Loop -------- #
    while True:

        #Adjust camera
        #Calculate the center pos for the player (the player object itself not the rect it is draw on)
        #I.e. the players position in the world, NOT the position on the screen!! (3 hours wasted on that bug!)
        player_center_x = player.x + int(player.width /2)
        player_center_y = player.y + int(player.height / 2)
        
        #if the player is more than cameraslack pixels away from the midpoint then
        #update value for camera to compensate and keep player at most cameraslack pixels from center
        if (camera['y'] + HALF_WINDOWHEIGHT) - player_center_y > CAMERASLACK: #Top edge
            camera['y'] = player_center_y + CAMERASLACK - HALF_WINDOWHEIGHT
        elif (camera['x'] + HALF_WINDOWWIDTH) - player_center_x > CAMERASLACK: #Left edge
            camera['x'] = player_center_x + CAMERASLACK - HALF_WINDOWWIDTH
        if player_center_y - (camera['y'] + HALF_WINDOWHEIGHT) > CAMERASLACK: #Bottom edge
            camera['y'] = player_center_y - CAMERASLACK - HALF_WINDOWHEIGHT
        elif player_center_x - (camera['x'] + HALF_WINDOWWIDTH) > CAMERASLACK: #Right edge
            camera['x'] = player_center_x - CAMERASLACK - HALF_WINDOWWIDTH

        #Draw map - Should this be a class?
        for layer in game_map.visible_layers:
            for x, y, gid, in layer:
                tile = game_map.get_tile_image_by_gid(gid)
                if tile != None:
                    SCREEN.blit(tile, ((x * game_map.tilewidth - camera['x']), (y * game_map.tileheight - camera['y'])))

        #Draw sprites
        all_sprites_list.draw(SCREEN)

        #Check events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                # If D-Pad keys are pressed then signal movement (honoured below)
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                elif event.key == K_DOWN:
                    moveUp = False
                    moveDown = True
                elif event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                elif event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
            
            #elif event.type == KEYDOWN:
            #    # If D-Pad keys are pressed then signal movement (honoured below)
            #    if event.key == K_UP:
            #        moveDown = False
            #        moveUp = True
            #    elif event.key == K_DOWN:
            #        moveUp = False
            #        moveDown = True
            #    elif event.key == K_RIGHT:
            #        moveLeft = False
            #        moveRight = True
            #    elif event.key == K_LEFT:
            #        moveRight = False
            #        moveLeft = True
#
            #elif event.type == KEYUP:
            #    # If D-Pad keys are released then stop movement
            #    if event.key == K_UP:
            #        moveUp = False
            #    elif event.key == K_DOWN:
            #        moveDown = False
            #    elif event.key == K_RIGHT:
            #        moveRight = False
            #    elif event.key == K_LEFT:
            #        moveLeft = False
#
        # Honour movement
        if moveUp:
            player.move('U', MOVERATE, camera)
        elif moveDown:
            player.move('D', MOVERATE, camera)
        elif moveRight:
            player.move('R', MOVERATE, camera)
        elif moveLeft:
            player.move('L', MOVERATE, camera)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()