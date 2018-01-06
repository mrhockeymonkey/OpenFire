#from __future__ import absolute_import, division, print_function

import pygame
import sys
import hbf

if __name__ == '__main__':
    g = hbf.core.Game()
    while not g.exit:
        g.new()
        g.run()

pygame.quit()
sys.exit()