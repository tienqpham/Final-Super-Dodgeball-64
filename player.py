import pygame

import constants

from art import *
from actor import *

class Player(Actor):
    def __init__(self, playerNumber, hit_points = 5):
        self.hitpoint = hit_points
        self.control_index = -2
        left_bound = 0
        right_bound = constants.SCREEN_WIDTH/2
        spawn_place = [0,0]
        
        if playerNumber == 1:
            self.imgg = Art().get_image('player1')
            left_bound = 0
            right_bound = constants.SCREEN_WIDTH/2
            spawn_place = [ constants.SCREEN_WIDTH/4,
                            constants.SCREEN_HEIGHT/2 ]
            
        elif playerNumber == 2:
            self.imgg = Art().get_image('player2')
            left_bound = constants.SCREEN_WIDTH/2
            right_bound =  constants.SCREEN_WIDTH
            spawn_place = [ ( constants.SCREEN_WIDTH/4 ) * 3,
                            constants.SCREEN_HEIGHT/2 ]

        else:
            raise ValueError('invalid player number')

        self.playerNumber = playerNumber

        super().__init__(self.imgg, spawn_place[0], spawn_place[1])
        self.left_bound = left_bound
        self.right_bound = right_bound

    def get_player_number(self):
        return self.playerNumber

    def get_control(self):
        return self.control_index

    def damage(self, amount = 1):
        if amount <= 0:
            pygame.error("can not take negative damage")
        self.hitpoint -= amount
        
    def get_hit_points(self):
        return self.hitpoint

    # does nothing unless overridden
    def handle_event(self, event):
        pass
