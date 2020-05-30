import pygame 
import constants
from actor import *
from art import *

class Ball(Actor):

    def __init__(self,img,x,y,speed_x,speed_y, multiplier):
        super().__init__(img,x,y)
        self.multiplier = multiplier
        self.set_speed(speed_x, speed_y)
        
    def update(self):
        self.rect.x += self.speed_x * self.multiplier
        self.rect.y += self.speed_y * self.multiplier

        #left edge
        if self.rect.x < 0:
            self.speed_x = self.speed_x * -1

        #right edge
        if self.rect.x > constants.SCREEN_WIDTH - self.rect.size[0]:
            self.speed_x = self.speed_x * -1

        #top edge
        if self.rect.y < 0:
            self.speed_y = self.speed_y * -1

        #bottom edge
        if self.rect.y > constants.SCREEN_HEIGHT - self.rect.size[1]:
            self.speed_y = self.speed_y * -1

    def get_multiplier(self):
            return self.multiplier

class NeutralBall(Ball):
    def __init__(self,x,y,speed_x,speed_y, multiplier=1):
        super().__init__( Art().get_image('ball'), x, y,speed_x,speed_y, multiplier)

class RedBall(Ball):
    def __init__(self,x,y,speed_x,speed_y, multiplier=1):
        super().__init__( Art().get_image('ball1'), x, y,speed_x,speed_y, multiplier)

class BlueBall(Ball):
    def __init__(self,x,y,speed_x,speed_y, multiplier=1):
        super().__init__( Art().get_image('ball2'), x, y,speed_x,speed_y, multiplier)
    
