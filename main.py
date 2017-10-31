import pygame
import sys
import hbf.game as game

if __name__ == '__main__':
    g = game.Game()
    while not g.exit:
        g.new()
        g.run()

print('exiting game...')
pygame.quit()
sys.exit()