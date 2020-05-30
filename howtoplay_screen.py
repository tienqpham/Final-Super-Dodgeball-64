import pygame
import constants

from level_manager import *
from music import *
from art import *

pygame.init()

class HowtoplayScreen():
    def __init__(self):
        self.joysticks = []

        for i in range(0,pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
            self.joysticks.append(pygame.joystick.Joystick(i))

        font = pygame.font.SysFont('Calibri', 50, True, False)
        font2 = pygame.font.SysFont('Calibri', 30, True, False)

        self.background_image = Art().get_image("basketBallCourt_dark")

        self.how = font.render("How to play?",True,constants.BLACK)
        self.player1 = font2.render("Player 1 Controls",True,constants.BLACK)
        self.player2 = font2.render("Player 2 Controls",True,constants.BLACK)
        self.player1_shooting = font2.render("Left or Right mouse to shoot.",True,constants.BLACK)
        self.player1_moving = font2.render("WASD to move.",True,constants.BLACK)
        self.player1_aiming = font2.render("Use mouse to aim.",True,constants.BLACK)
        self.player1_pause = font2.render("Press spacebar to pause",True,constants.BLACK)
        self.player2_shooting = font2.render("LB/RB to shoot.",True,constants.BLACK)
        self.player2_moving = font2.render("Left Joystick to move.",True,constants.BLACK)
        self.player2_aiming = font2.render("Right Joystick to aim.",True,constants.BLACK)
        self.player2_pause = font2.render("Press start to pause.",True,constants.BLACK)
        self.gameplay1 = font2.render("When balls of different colors collide, their velocities are added along with their speed multipliers.",True,constants.BLACK)
        self.gameplay2 = font2.render("The player that survives longer wins.",True,constants.BLACK)
        self.esc = font2.render("Press ESC on any screen to leave (Pressing ESC on title screen quit the game).",True,constants.BLACK)

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or \
               event.key == pygame.K_TAB or \
               event.key == pygame.K_BACKSPACE:
                LevelManager().leave_level()
        elif event.type == pygame.JOYBUTTONDOWN:
            for joystick in self.joysticks:
                if joystick.get_button(1):
                    LevelManager().leave_level()
              
    def update(self):
        pass

    def draw(self, screen):
        screen.fill(constants.WHITE)

        screen.blit(self.background_image, [0, 0])
        screen.blit(Art().get_image('howtoplay'), [0,0])

        '''
        screen.blit(self.how, [(constants.SCREEN_WIDTH/2 - self.how.get_width()/2), 50])
        screen.blit(self.esc, [(constants.SCREEN_WIDTH/2 - self.esc.get_width()/2), 500])
        screen.blit(self.player1, [(constants.SCREEN_WIDTH/4 - self.player1.get_width()/2), 150])
        screen.blit(self.player1_shooting, [(constants.SCREEN_WIDTH/4 - self.player1_shooting.get_width()/2), 200])
        screen.blit(self.player1_moving, [(constants.SCREEN_WIDTH/4 - self.player1_moving.get_width()/2), 250])
        screen.blit(self.player1_aiming, [(constants.SCREEN_WIDTH/4 - self.player1_aiming.get_width()/2), 300])
        screen.blit(self.player1_pause, [(constants.SCREEN_WIDTH/4 - self.player1_pause.get_width()/2), 350])
        screen.blit(self.player2, [(((constants.SCREEN_WIDTH/4) * 3) - self.player2.get_width()/2), 150])
        screen.blit(self.player2_shooting, [(((constants.SCREEN_WIDTH/4) * 3) - self.player2_shooting.get_width()/2), 200])
        screen.blit(self.player2_moving, [(((constants.SCREEN_WIDTH/4) * 3) - self.player2_moving.get_width()/2), 250])
        screen.blit(self.player2_aiming, [(((constants.SCREEN_WIDTH/4) * 3) - self.player2_aiming.get_width()/2), 300])
        screen.blit(self.player2_pause, [(((constants.SCREEN_WIDTH/4) * 3) - self.player2_pause.get_width()/2), 350])
        screen.blit(self.gameplay1, [(((constants.SCREEN_WIDTH/4)) - self.player2_pause.get_width()/2), 400])
        screen.blit(self.gameplay2, [(((constants.SCREEN_WIDTH/4)) - self.player2_pause.get_width()/2), 450])
        '''
