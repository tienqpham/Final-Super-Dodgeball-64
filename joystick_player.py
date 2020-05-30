import pygame
import constants

from player import *

class JoystickPlayer(Player):
    def __init__(self, playerNumber, joystickNumber):
        super().__init__(playerNumber)

        self.control_index = joystickNumber
        
        self.joystick = pygame.joystick.Joystick(joystickNumber)
        self.joystick.init()
        
        self.top_speed = constants.JOYSTICK_PLAYER_SPEED
        self.deadzone = constants.DEADZONE

    def get_joystick(self):
        return self.joystick

    def handle_event(self, event):
        if event.type == pygame.JOYAXISMOTION:
            if self.joystick.get_axis(0) > self.deadzone or \
               self.joystick.get_axis(0) < self.deadzone * -1 :
                self.speed_x = int(self.top_speed * self.joystick.get_axis(0))
            else :
                self.speed_x = 0
            if self.joystick.get_axis(1) > self.deadzone or \
               self.joystick.get_axis(1) < self.deadzone * -1 :
                self.speed_y = int(self.top_speed * self.joystick.get_axis(1))
            else :
                self.speed_y = 0
