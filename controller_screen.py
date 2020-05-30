import pygame
import constants

from level_manager import *
from art import *
from control_select import *
from game_screen import *
from soccer_screen import *
#from single_player import *

pygame.init()
pygame.joystick.init()

class ControllerScreen():
    # game_mode:
    #   0: standard versus
    #   1: soccer
    #   2: practice
    def __init__(self,game_mode=0):
        self.game_mode = game_mode
        if game_mode == 2:
            self.control_menu = ControlSelect(1)
        else:
            self.control_menu = ControlSelect()

        self.background_image = Art().get_image("basketBallCourt_dark")

        font = pygame.font.SysFont('Calibri', 25, True, False)

        self.ready_time = 0
        self.current_time = 0

        self.ready = False

        self.controller = font.render("Controller not detected!",True,constants.RED)

    def return_to_title(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
        LevelManager().leave_level()

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE or \
                event.key == pygame.K_TAB or \
                event.key == pygame.K_BACKSPACE) and \
                not self.control_menu.is_anyone_ready():
                
                self.return_to_title()

        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(0,pygame.joystick.get_count()):
                if pygame.joystick.Joystick(i).get_button(1) and\
                   not self.control_menu.is_anyone_ready():
                    self.return_to_title()
                    break

        self.control_menu.handle_event(event)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.control_menu.update()
        
        if self.control_menu.is_everyone_ready():
            if not self.ready:
                self.ready = True
                self.ready_time = self.current_time
            else:
                if self.current_time >= self.ready_time + constants.PROMPT_DELAY:
                    if self.game_mode == 0:
                        LevelManager().load_level(GameScreen(self.control_menu.get_player1_control(),
                                                             self.control_menu.get_player2_control()))
                    if self.game_mode == 1:
                        # load soccer
                        pass
                    if self.game_mode == 2:
                        LevelManager().load_level(SinglePlayer(self.control_menu.get_player1_control()))
                        pass
                    self.control_menu.reset()
                    self.ready = False
            

    def draw(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background_image, [0, 0])
        self.control_menu.draw(screen)

        #screen.blit(self.controller, [(constants.SCREEN_WIDTH/2 - self.controller.get_width()/2), (constants.SCREEN_HEIGHT/4)])
