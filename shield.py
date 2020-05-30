import pygame
import constants
import sys

sys.path.append('..')

from art import *
from actor import *

class Shield(Actor):
    def __init__(self,x,y,playerNumber):
        img = Art().get_image('shield1')

        if playerNumber == 2:
            img = Art().get_image('shield2')

        if playerNumber != 1 and playerNumber != 2:
            raise ValueError("Invalid player number for shield")

        super().__init__(img,x,y)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.check_out_of_bounds()

    # shield can pass halfway off screen in either direction
    # shield center cannot pass off screen
    def check_out_of_bounds(self):

        # x
        # left edge
        if self.get_center()[0] < 0:
            self.stop_x()
            self.rect.x = 0 - (self.rect.size[0]/2)

        # right edge
        if self.get_center()[0] > constants.SCREEN_WIDTH:
            self.stop_x()
            self.rect.x = constants.SCREEN_WIDTH - (self.rect.size[0]/2)

        # y
        # top edge
        if self.get_center()[1] < 0:
            self.stop_y()
            self.rect.y = 0 - (self.rect.size[1]/2)
            
        # bottom edge
        if self.get_center()[1] > constants.SCREEN_HEIGHT:
            self.stop_y()
            self.rect.y = constants.SCREEN_HEIGHT - (self.rect.size[1]/2)
