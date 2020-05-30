import pygame

import constants

from art import *
from actor import *

class SoccerGoal(Actor):
    def __init__(self, goalNumber):
        self.imgg = Art().get_image('tempGoal')
        
        
        if goalNumber == 1:
            spawn_place = [0, constants.SCREEN_HEIGHT/2]
        elif goalNumber == 2:
            spawn_place = [constants.SCREEN_HEIGHT * 3 / 4, constants.SCREEN_HEIGHT/2]

        else:
            raise ValueError('invaid player number')

        self.goalNumber = goalNumber
        
        super().__init__(self.imgg, spawn_place[0], spawn_place[1])

    def get_goal_number(self):
        return self.goalNumber
    
