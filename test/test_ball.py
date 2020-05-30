import unittest
import sys

sys.path.append('..')

import constants
from actor import *
from ball import *

class test_Ball(unittest.TestCase):
    # can be created
    def test_init(self):
        ball = Ball(pygame.image.load('missing.png'),0,0,1,1,1)
        self.assertTrue(True)


    # can be updated automatically
    def test_update(self):
        ball = Ball(pygame.image.load('missing.png'),0,0,1,1,1)
        ball.update()
        self.assertTrue(True)

    # left edge
    def test_out_of_bounds_left(self):
        ball = Ball(pygame.image.load('missing.png'),0,0,-10,5,1)
        ball.set_speed_x(-10)
        ball.update()
        #self.assertEqual(ball.set_speed_x(10))
       
        

if __name__ == '__main__':
    unittest.main()
