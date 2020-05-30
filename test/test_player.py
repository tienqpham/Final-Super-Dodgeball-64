import unittest
import pygame
import sys

sys.path.append('..')

import constants

from player import *
from art import *

art = Art()

pygame.init()

pygame.display.init()

screen = pygame.display.set_mode([ constants.SCREEN_WIDTH,
                                   constants.SCREEN_HEIGHT ])

class test_player(unittest.TestCase):
    def test_init(self):
        player1 = Player(1)
        player2 = Player(2)
        self.assertTrue(True)

    def test_player_default_hit_points(self):
        player1 = Player(1)
        self.assertEqual(player1.get_hit_points(), 5)

    def test_player_input_hit_points(self):
        player1 = Player(1, 10)
        self.assertEqual(player1.get_hit_points(), 10)

    def can_not_be_damage_by_negative_amount(self):
        player1 = Player(1)
        player1.damage(-1)
        self.assertEqual(player1.get_hit_points(), 5)
        
    def test_player_can_take_default_damage(self):
        player1 = Player(1)
        player1.damage()
        self.assertEqual(player1.get_hit_points(), 4)

    def test_player_can_take_input_damage(self):
        player1 = Player(1)
        player1.damage(3)
        self.assertEqual(player1.get_hit_points(), 2)

    # BEGIN PLAYER 1 SPECIFIC TESTS
    
    # cannot move out of bounds
    # left edge
    def test_P1_out_of_bounds_left(self):
        player1 = Player(1)
        self.assertEqual(player1.get_pos()[0],
                         constants.SCREEN_WIDTH/4)
        player1.set_speed_x(-1000)
        self.assertEqual(player1.get_speed()[0], -1000)
        player1.update()
        self.assertEqual(player1.get_pos()[0], 0)
        
    # top edge
    def test_P1_out_of_bounds_top(self):
        player1 = Player(1)
        self.assertEqual(player1.get_pos()[1],
                         constants.SCREEN_HEIGHT/2)
        player1.set_speed_y(-1000)
        self.assertEqual(player1.get_speed()[1], -1000)
        player1.update()
        self.assertEqual(player1.get_pos()[1], 0)

    # right edge
    def test_P1_out_of_bounds_right(self):
        player1 = Player(1)
        self.assertEqual(player1.get_pos()[0],
                         constants.SCREEN_WIDTH/4)
        player1.set_speed_x(1000)

        player1.update()
        self.assertEqual(player1.get_pos()[0],
                         constants.SCREEN_WIDTH/2 - player1.rect.size[0])

    # bottom edge
    def test_P1_out_of_bounds_bottom(self):
        player1 = Player(1)
        self.assertEqual(player1.get_pos()[1],
                         constants.SCREEN_HEIGHT/2)
        player1.set_speed_y(1000)

        player1.update()
        self.assertEqual(player1.get_pos()[1],
                         constants.SCREEN_HEIGHT - player1.rect.size[1])


    # END PLAYER 1 SPECIFIC TESTS

    # BEGIN PLAYER 2 SPECIFIC TESTS
    
    # cannot move out of bounds
    # left edge
    def test_P2_out_of_bounds_left(self):
        player2 = Player(2)
        self.assertEqual(player2.get_pos()[0],
                         constants.SCREEN_WIDTH/4*3)
        player2.set_speed_x(-1000)
        self.assertEqual(player2.get_speed()[0], -1000)
        player2.update()
        self.assertEqual(player2.get_pos()[0], constants.SCREEN_WIDTH/2)
        
    # top edge
    def test_P2_out_of_bounds_top(self):
        player2 = Player(2)
        self.assertEqual(player2.get_pos()[1],
                         constants.SCREEN_HEIGHT/2)
        player2.set_speed_y(-1000)
        self.assertEqual(player2.get_speed()[1], -1000)
        player2.update()
        self.assertEqual(player2.get_pos()[1], 0)

    # right edge
    def test_P2_out_of_bounds_right(self):
        player2 = Player(2)
        self.assertEqual(player2.get_pos()[0],
                         constants.SCREEN_WIDTH/4*3)
        player2.set_speed_x(1000)

        player2.update()
        self.assertEqual(player2.get_pos()[0],
                         constants.SCREEN_WIDTH - player2.rect.size[0])

    # bottom edge
    def test_P2_out_of_bounds_bottom(self):
        player2 = Player(2)
        self.assertEqual(player2.get_pos()[1],
                         constants.SCREEN_HEIGHT/2)
        player2.set_speed_y(1000)

        player2.update()
        self.assertEqual(player2.get_pos()[1],
                         constants.SCREEN_HEIGHT - player2.rect.size[1])


    # END PLAYER 2 SPECIFIC TESTS


if __name__ == '__main__':
    unittest.main()
