import pygame
import constants

from level_manager import *
from art import *

pygame.init()

class GameoverScreen():
    def __init__(self):

        font = pygame.font.SysFont('Calibri', 60, True, False)

        self.gameover = font.render("Gameover",True,constants.RED)

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Music().stop()
                Music().play_repeat("title_music")
                LevelManager().load_level(TitleScreen())

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(constants.WHITE)

        screen.blit(self.gameover, [(constants.SCREEN_WIDTH/2 - self.gameover.get_width()/2), constants.SCREEN_HEIGHT/2])

        
