import unittest
import sys
from unittest.mock import patch

sys.path.append('..')

import constants
from actor import *

class test_Actor(unittest.TestCase):
    # can be created
    @patch('actor.pygame')
    def test_init(self,mock_pygame):
        actor = mock_pygame
        self.assertTrue(True)

    # can be created at a specific position
    def test_init_pos(self):
        actor = Actor(pygame.image.load('missing.png'),5,10)
        self.assertEqual(actor.rect.x, 5)
        self.assertEqual(actor.rect.y, 10)

    # if created out of bounds, resets back within bounds
    def test_init_bounds(self):
        actor = Actor(pygame.image.load('missing.png'),-5,-3)
        self.assertEqual(actor.get_x(), 0)
        self.assertEqual(actor.get_y(), 0)

    # can be updated automatically
    def test_update(self):
        actor = Actor(pygame.image.load('missing.png'))
        actor.update()
        self.assertTrue(True)

    # speed can be modified directly
    def test_set_speed(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)
        actor.set_speed_x(5)
        actor.set_speed_y(4)
        self.assertEqual(actor.speed_x, 5)
        self.assertEqual(actor.speed_y, 4)

    # speed can be modified via acceleration
    def test_acceleration(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)
        actor.accelerate(2,3)
        actor.accelerate(2,3)
        self.assertEqual(actor.speed_x, 4)
        self.assertEqual(actor.speed_y, 6)

    # can be stopped in x direction without affecting y speed
    def test_stop_x(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)
        actor.accelerate(5,3)
        self.assertEqual(actor.speed_x, 5)
        self.assertEqual(actor.speed_y, 3)
        actor.stop_x()
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 3)

    # can be stopped in y direction without affecting x speed
    def test_stop_y(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)
        actor.accelerate(5,3)
        self.assertEqual(actor.speed_x, 5)
        self.assertEqual(actor.speed_y, 3)
        actor.stop_y()
        self.assertEqual(actor.speed_x, 5)
        self.assertEqual(actor.speed_y, 0)

    # can be stopped abruptly
    def test_stop(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)
        actor.accelerate(5,5)
        self.assertEqual(actor.speed_x, 5)
        self.assertEqual(actor.speed_y, 5)
        actor.stop()
        self.assertEqual(actor.speed_x, 0)
        self.assertEqual(actor.speed_y, 0)

    # speed affects position after update
    def test_update_with_speed(self):
        actor = Actor(pygame.image.load('missing.png'))
        self.assertEqual(actor.rect.x, 0)
        self.assertEqual(actor.rect.y, 0)
        actor.set_speed_x(5)
        actor.set_speed_y(4)
        actor.update()
        actor.update()
        self.assertEqual(actor.rect.x, 10)
        self.assertEqual(actor.rect.y, 8)

    # cannot move out of bounds
    # left edge
    def test_out_of_bounds_left(self):
        actor = Actor(pygame.image.load('missing.png'),5,5)
        self.assertEqual(actor.get_pos()[0], 5)
        actor.set_speed_x(-10)
        actor.update()
        self.assertEqual(actor.get_pos()[0], 0)
        actor.update()
        self.assertEqual(actor.get_pos()[0], 0)
        
    # top edge
    def test_out_of_bounds_top(self):
        actor = Actor(pygame.image.load('missing.png'),5,5)
        self.assertEqual(actor.get_pos()[1], 5)
        actor.set_speed_y(-10)
        actor.update()
        self.assertEqual(actor.get_pos()[1], 0)
        actor.update()
        self.assertEqual(actor.get_pos()[1], 0)

    # right edge
    # the sprite used, 'missing.png', is 150x150 pixels
    def test_out_of_bounds_right(self):
        actor = Actor(pygame.image.load('missing.png'),
                      constants.SCREEN_WIDTH - 180,
                      constants.SCREEN_HEIGHT - 180)
        self.assertEqual(actor.get_pos()[0],
                         constants.SCREEN_WIDTH - 180)
        actor.set_speed_x(50)

        actor.update()
        self.assertEqual(actor.get_pos()[0],
                         constants.SCREEN_WIDTH - 150)
        actor.update()
        self.assertEqual(actor.get_pos()[0],
                         constants.SCREEN_WIDTH - 150)

    # bottom edge
    def test_out_of_bounds_bottom(self):
        actor = Actor(pygame.image.load('missing.png'),
                      constants.SCREEN_WIDTH - 180,
                      constants.SCREEN_HEIGHT - 180)
        self.assertEqual(actor.get_pos()[1],
                         constants.SCREEN_HEIGHT - 180)
        actor.set_speed_y(50)

        actor.update()
        self.assertEqual(actor.get_pos()[1],
                         constants.SCREEN_HEIGHT - 150)
        actor.update()
        self.assertEqual(actor.get_pos()[1],
                         constants.SCREEN_HEIGHT - 150)

    # position can be set directly
    def test_set_pos(self):
        img = pygame.image.load('missing.png')
        actor = Actor(img,0,0)
        actor.set_pos(3,4)
        self.assertEqual(3, actor.get_pos()[0])
        self.assertEqual(4, actor.get_pos()[1])

    # center position can be set directly
    def test_set_center(self):
        img = pygame.image.load('missing.png')
        actor = Actor(img,0,0)
        actor.set_center(3,4)
        self.assertEqual(3, actor.get_center()[0])
        self.assertEqual(4, actor.get_center()[1])
        self.assertFalse( actor.get_center()[0] == actor.get_pos()[0] )
        self.assertFalse( actor.get_center()[1] == actor.get_pos()[1] )

    # can be drawn on a screen
    def test_draw(self):
        screen = pygame.display.set_mode([constants.SCREEN_WIDTH,
                                  constants.SCREEN_HEIGHT])
        screen.fill(constants.WHITE)
        sprite_list = pygame.sprite.Group()
        actor = Actor(pygame.image.load('missing.png'))
        sprite_list.add(actor)
        sprite_list.update()
        sprite_list.draw(screen)
        pygame.display.flip()
        pygame.quit()
        

if __name__ == '__main__':
    unittest.main()
