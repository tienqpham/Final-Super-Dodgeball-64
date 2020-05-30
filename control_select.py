import pygame

import constants

from level_manager import *
from art import *

class ControlSelect():

    def __init__(self, player_count=2):

        self.keyboard_img = Art().get_image("keyboard_select")
        self.gamepad_img = Art().get_image("gamepad_select")

        self.ready1_on = Art().get_image("ready1_on")
        self.ready1_off = Art().get_image("ready1_off")
        self.ready2_on = Art().get_image("ready2_on")
        self.ready2_off = Art().get_image("ready2_off")

        self.keyboard_height = self.keyboard_img.get_rect().size[1]
        self.gamepad_height = self.gamepad_img.get_rect().size[1]

        self.gap_y = 30
        
        self.player_count = player_count
        
        self.player1_fill = False
        self.player2_fill = False
        self.player1_ready = False
        self.player2_ready = False
        self.player1_control = -2
        self.player2_control = -2

        self.joystick_count = pygame.joystick.get_count()
        self.total_count = self.joystick_count + 1

        self.joysticks = []

        self.is_joystick_in_use = []

        for i in range(0, self.joystick_count):
            self.is_joystick_in_use.append(False)
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[i].init()

        self.is_keyboard_in_use = False

    # returns True if all player(s) are ready
    # returns False if any player is not ready
    def is_everyone_ready(self):
        if self.player_count == 1:
            return self.player1_ready
        elif self.player_count == 2:
            return self.player1_ready and self.player2_ready

    def is_anyone_ready(self):
        return self.player1_ready or self.player2_ready

    # returns the ID of player1's assigned joystick
    # returns -1 if player1 is assigned keyboard
    def get_player1_control(self):
        return self.player1_control

    # returns the ID of player2's assigned joystick
    # returns -1 if player2 is assigned keyboard
    def get_player2_control(self):
        return self.player2_control

    # resets menu to initial state
    def reset(self):
        self.player1_fill = False
        self.player2_fill = False
        self.player1_ready = False
        self.player2_ready = False
        self.player1_control = -2
        self.player2_control = -2
        self.is_keyboard_in_use = False
        for i in range(0, self.joystick_count):
            self.is_joystick_in_use[i] = False

    def update(self):
        pass

    def draw(self, screen):
        self.draw_controllers(screen)
        self.draw_players(screen)

    def draw_controllers(self, screen):
        if not self.is_keyboard_in_use:
            # blit keyboard sprite centered at screen_width/2, gap_y + imgHeight/2
            
            rect = self.keyboard_img.get_rect(center=[constants.SCREEN_WIDTH/2, self.keyboard_height/2 + self.gap_y])
            screen.blit(self.keyboard_img, rect)

        for i in range(0, self.joystick_count):
            if not self.is_joystick_in_use[i]:
                # blit gamepad sprite centered at
                # screen_width/2, gap_y*(i+2) + joystick_sprite_height*i + keyboard_sprite_height
                rect = self.gamepad_img.get_rect(center=[constants.SCREEN_WIDTH/2,0])
                rect.y = self.gap_y*(i+2) + self.gamepad_height*i + self.keyboard_height
                screen.blit(self.gamepad_img, rect)

    def draw_players(self, screen):
        if not self.player1_ready:
            # blit ready_red_off centered at constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2 + gamepad_height
            rect = self.ready1_off.get_rect(center=[constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2 + self.gamepad_height])
            screen.blit(self.ready1_off, rect)

        if self.player_count ==2 and \
        not self.player2_ready:
            # blit ready_bleu_off centered at constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2 + gamepad_height
            rect = self.ready2_off.get_rect(center=[constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2 + self.gamepad_height])
            screen.blit(self.ready2_off, rect)
                
        if self.player1_fill:
            if self.player1_control == -1:
                # blit keyboard sprite centered at
                # screen_width/4, screen_height/2
                rect = self.keyboard_img.get_rect(center=[constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2])
                screen.blit(self.keyboard_img, rect)
                
            elif self.player1_control >= 0:
                # blit gamepad sprite centered at
                # screen_width/4, screen_height/2
                rect = self.gamepad_img.get_rect(center=[constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2])
                screen.blit(self.gamepad_img, rect)

            if self.player1_ready:
                #blit ready_red_on centered at constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2 + gamepad_height
                rect = self.ready1_on.get_rect(center=[constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2 + self.gamepad_height])
                screen.blit(self.ready1_on, rect)

        if self.player2_fill:
            if self.player2_control == -1:
                # blit keyboard sprite centered
                # at screen_width*3/4, screen_height/2
                rect = self.keyboard_img.get_rect(center=[constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2])
                screen.blit(self.keyboard_img, rect)
            
            elif self.player2_control >= 0:
                # blit gamepad sprite centered at
                # screen_width*3/4, screen_height/2
                rect = self.gamepad_img.get_rect(center=[constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2])
                screen.blit(self.gamepad_img, rect)

            if self.player2_ready:
                #blit ready_blue_on centered at constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2 + gamepad_height
                rect = self.ready2_on.get_rect(center=[constants.SCREEN_WIDTH*3/4, constants.SCREEN_HEIGHT/2 + self.gamepad_height])
                screen.blit(self.ready2_on, rect)

    def handle_event(self, event):
        # keypress
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        # joybutton press            
        if event.type == pygame.JOYBUTTONDOWN:
            self.handle_joybuttondown(event)

        # joyhat press
        if event.type == pygame.JOYHATMOTION:
            self.handle_joyhatmotion(event)

    def handle_joyhatmotion(self,event):
        for i in range(0,self.joystick_count):
            # left hat press
            if self.joysticks[i].get_hat(0)[0] == -1:
                # player 1 assigns controller
                if not self.is_joystick_in_use[i] and not self.player1_fill and self.player1_control == -2:
                    self.is_joystick_in_use[i] = True
                    self.player1_fill = True
                    self.player1_control = self.joysticks[i].get_id()
                    print("player 1 selected joystick " + str(self.joysticks[i].get_id()))
                    print('')

                # player 2 unassigns controller
                elif self.is_joystick_in_use[i] and self.player2_fill and self.player2_control == self.joysticks[i].get_id() and not self.player2_ready:
                    self.is_joystick_in_use[i] = False
                    self.player2_fill = False
                    self.player2_control = -2
                    print("player 2 unselected joystick " + str(self.joysticks[i].get_id()))
                    print('')

            # right hat press
            elif self.joysticks[i].get_hat(0)[0] == 1:
                # player 2 assigns controller
                if self.player_count ==2 and not self.is_joystick_in_use[i] and \
                   not self.player2_fill and self.player2_control == -2:
                    self.is_joystick_in_use[i] = True
                    self.player2_fill = True
                    self.player2_control = self.joysticks[i].get_id()
                    print("player 2 selected joystick " + str(self.joysticks[i].get_id()))
                    print('')

                # player 1 unassigns controller
                elif self.is_joystick_in_use[i] and self.player1_fill and self.player1_control == self.joysticks[i].get_id() and not self.player1_ready:
                    self.is_joystick_in_use[i] = False
                    self.player1_fill = False
                    self.player1_control = -2
                    print("player 1 unselected joystick " + str(self.joysticks[i].get_id()))
                    print('')
                        
    def handle_joybuttondown(self,event):
        
        for i in range(0,self.joystick_count):
            # X/A button press
            if self.joysticks[i].get_button(0):
                if self.player1_control == i:
                    if self.player1_fill:
                        self.player1_ready = True
                elif self.player2_control == i:
                    if self.player2_fill:
                        self.player2_ready = True
            # Circle/B button press
            elif self.joysticks[i].get_button(1):
                if self.player1_control == i:
                    if self.player1_ready:
                        self.player1_ready = False
                elif self.player2_control == i:
                    if self.player2_ready:
                        self.player2_ready = False
                        
    def handle_keydown(self,event):
        # left keypress
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            # player 1 assigns keyboard
            if not self.player1_fill and self.player1_control == -2 and not self.is_keyboard_in_use:
                self.player1_fill = True
                self.player1_control = -1
                self.is_keyboard_in_use = True
                print("player 1 selected keyboard")
                print('')

            # player 2 unassigns keyboard
            elif self.player2_fill and self.player2_control == -1 and self.is_keyboard_in_use and not self.player2_ready:
                self.player2_fill = False
                self.player2_control = -2
                self.is_keyboard_in_use = False
                print("player 2 unselected keyboard")
                print('')
                
        # right keypress
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            # player 2 assigns keyboard
            if self.player_count ==2 and not self.player2_fill and \
               self.player2_control == -2 and not self.is_keyboard_in_use:
                self.player2_fill = True
                self.player2_control = -1
                self.is_keyboard_in_use = True
                print("player 2 selected keyboard")
                print('')

            # player 1 unassigns keyboard
            elif self.player1_fill and self.player1_control == -1 and self.is_keyboard_in_use and not self.player1_ready:
                self.player1_fill = False
                self.player1_control = -2
                self.is_keyboard_in_use = False
                print("player 1 unselected keyboard")
                print('')

        # spacebar press
        elif event.key == pygame.K_SPACE:
            if self.player1_control == -1:
                if self.player1_fill:
                    self.player1_ready = True
            elif self.player2_control == -1:
                if self.player2_fill:
                    self.player2_ready = True

        # escape/tab/backspace press
        elif event.key == pygame.K_ESCAPE or \
             event.key == pygame.K_TAB or \
             event.key == pygame.K_BACKSPACE:
            if self.player1_control == -1:
                if self.player1_ready:
                    self.player1_ready = False
            elif self.player2_control == -1:
                if self.player2_ready:
                    self.player2_ready = False
