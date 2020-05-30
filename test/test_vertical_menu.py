import unittest
import pygame
import sys

sys.path.append('..')

import constants

from vertical_menu import *
from art import *

art = Art()

pygame.init()

pygame.display.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

screen = pygame.display.set_mode([ SCREEN_WIDTH,
                                   SCREEN_HEIGHT ])

class test_VerticalMenu(unittest.TestCase):
    
    def test_init(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        for i in range(0,3):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)

        
        self.assertTrue(True)

    def test_update(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        for i in range(0,3):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)

        
        myMenu.update()
        self.assertTrue(True)

    def test_get_selected(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        for i in range(0,3):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)

        
        myMenu.update()
        self.assertEqual(-1,myMenu.get_selected())

    def test_get_length(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        length = 3
        for i in range(0,length):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)
        self.assertEqual(length,myMenu.get_length())

        items_off.clear()
        items_on.clear()
        
        length = 6
        for i in range(0,length):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))

        otherMenu = VerticalMenu(rect,items_off,items_on)
        self.assertEqual(length,otherMenu.get_length())
        
    def test_cursor_down(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        for i in range(0,3):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)

        
        #myMenu.update()
        self.assertEqual(-1,myMenu.get_selected())
        myMenu.cursor_down()
        myMenu.update()
        self.assertEqual(0,myMenu.get_selected())
        for i in range(0,3):
            myMenu.cursor_down()
        self.assertEqual(myMenu.get_length()-1,
                         myMenu.get_selected())

    def test_cursor_up(self):
        rect = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        items_off = []
        items_on = []
        for i in range(0,3):
            items_off.append(Art().get_image("ball"))
            items_on.append(Art().get_image("ball1"))
            
        myMenu = VerticalMenu(rect,items_off,items_on)
        self.assertEqual(-1,myMenu.get_selected())
        myMenu.cursor_up()
        myMenu.update()
        self.assertEqual(0,myMenu.get_selected())

        for i in range(0,3):
            myMenu.cursor_down()
        self.assertEqual(myMenu.get_length()-1,
                         myMenu.get_selected())

        for i in range(0,3):
            myMenu.cursor_up()
        self.assertEqual(0,
                         myMenu.get_selected())


if __name__ == '__main__':
    unittest.main()
