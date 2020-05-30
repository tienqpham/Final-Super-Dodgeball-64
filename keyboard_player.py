import pygame
import constants

from player import *

class KeyboardPlayer(Player):

    def __init__(self, playerNumber):
            
        super().__init__(playerNumber)
        self.top_speed = constants.KEYBOARD_PLAYER_SPEED
        self.control_index = -1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: # up
                self.accelerate(0, self.top_speed * -1)
            
            elif event.key == pygame.K_a: # left
                self.accelerate(self.top_speed * -1, 0)
                
            elif event.key == pygame.K_s: # down
                self.accelerate(0, self.top_speed)
                
            elif event.key == pygame.K_d: # right
                self.accelerate(self.top_speed, 0)


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w: # up
                self.accelerate(0,self.top_speed)
                
            elif event.key == pygame.K_a: # left
                self.accelerate(self.top_speed,0)
                
            elif event.key == pygame.K_s: # down
                self.accelerate(0,self.top_speed * -1)
                
            elif event.key == pygame.K_d: # right
                self.accelerate(self.top_speed * -1,0)
                
