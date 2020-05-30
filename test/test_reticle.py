import unittest
import pygame
import sys

sys.path.append('..')

import constants

from reticle import *
from art import *

pygame.init()
pygame.display.init()

art = Art()

class test_reticle(unittest.TestCase):
    
    # can be created
    def test_init(self):
        ret = Reticle(0,0,1)
        self.assertTrue(True)

    # can be updated automatically
    def test_update(self):
        ret = Reticle(0,0,1)
        ret.update()
        self.assertTrue(True)

    # can be created at coordinates on screen
    def test_init_pos(self):
        
        ret = Reticle(10,20,1)
        self.assertEqual(ret.get_pos()[0], 10)
        self.assertEqual(ret.get_pos()[1], 20)

    # reticle can be partly off screen
    def test_init_off_screen(self):
        
        ret = Reticle(-5,-5,1)

        # coordinates of upper-left corner should be off screen
        self.assertEqual(-5, ret.get_pos()[0])
        self.assertEqual(-5, ret.get_pos()[1])

    # reticle center cannot be off screen
    def test_out_of_bounds(self):
        
        ret = Reticle(0,0,1)

        ret.set_center(-5, -5)
        ret.update()
        self.assertEqual(0, ret.get_center()[0])
        self.assertEqual(0, ret.get_center()[1])

        ret.set_center(constants.SCREEN_WIDTH+50, constants.SCREEN_HEIGHT+50)
        ret.update()
        self.assertEqual(constants.SCREEN_WIDTH, ret.get_center()[0])
        self.assertEqual(constants.SCREEN_HEIGHT, ret.get_center()[1])

    # can be drawn on a screen
    def test_draw(self):
        screen = pygame.display.set_mode([constants.SCREEN_WIDTH,
                                          constants.SCREEN_HEIGHT])
        screen.fill(constants.WHITE)
        sprite_list = pygame.sprite.Group()
        
        
        ret = Reticle(0,0,1)
        
        sprite_list.add(ret)
        sprite_list.update()
        sprite_list.draw(screen)
        pygame.display.flip()

    

if __name__ == '__main__':
    unittest.main()
