import unittest
import sys

sys.path.append('..')

import constants

from keyboard_player import *
from art import *

pygame.init()

pygame.display.init()

screen = pygame.display.set_mode([ constants.SCREEN_WIDTH,
                                   constants.SCREEN_HEIGHT ])

class test_KeyboardPlayer(unittest.TestCase):
    def test_init(self):
        player1 = KeyboardPlayer(1)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
