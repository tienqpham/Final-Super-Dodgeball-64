import pygame
import constants

from level_manager import *
from credit_screen import *
from game_screen import *
from soccer_screen import *
from controller_screen import *
from howtoplay_screen import *
from art import *
from music import *
from vertical_menu import *
from sound import *

pygame.init()
pygame.joystick.init()

class TitleScreen():
    def __init__(self):

        self.title = Art().get_image('title')
        self.title_rect = self.title.get_rect(center=(constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/4))

        self.title_speed = 0

        self.joysticks = []

        for i in range(0,pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
            self.joysticks.append(pygame.joystick.Joystick(i))
        
        menu_off = []
        
        menu_off.append(Art().get_image('versus_split_off'))
        #menu_off.append(Art().get_image('soccer_split_off'))
        #menu_off.append(Art().get_image('practice_red_off'))
        menu_off.append(Art().get_image('howToPlay_red_off'))
        menu_off.append(Art().get_image('credits_red_off'))
        menu_off.append(Art().get_image('quit_red_off'))

        menu_on = []
        menu_on.append(Art().get_image('versus_split_on'))
        #menu_on.append(Art().get_image('soccer_split_on'))
        #menu_on.append(Art().get_image('practice_red_on'))
        menu_on.append(Art().get_image('howToPlay_red_on'))
        menu_on.append(Art().get_image('credits_red_on'))
        menu_on.append(Art().get_image('quit_red_on')),

        menu_rect = pygame.rect.Rect(0,
                                     constants.SCREEN_HEIGHT/2,
                                     constants.SCREEN_WIDTH,
                                     constants.SCREEN_HEIGHT/2)
        
        self.main_menu = VerticalMenu(menu_rect,menu_off,menu_on)
        
        Music().play_repeat("title_music")

        self.background_image = Art().get_image("basketBallCourt_dark")

        font = pygame.font.SysFont('Calibri', 50, True, False)
        font2 = pygame.font.SysFont('Calibri', 30, True, False)

        self.game_title = font.render("Super Dodgeball 64",True,constants.BLACK)
        self.game_screen = font.render("Press spacebar to start the game.",True,constants.BLACK)
        self.credit_screen = font.render("Press c to go to the credits.",True,constants.BLACK)
        self.howtoplay_screen = font.render("How to play? Press v",True,constants.BLACK)

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.load_game_mode()
            elif event.key == pygame.K_j:
                Sound().play_ready_round()

        elif event.type == pygame.JOYBUTTONDOWN:
            for joystick in self.joysticks:
                if joystick.get_button(0):
                    self.load_game_mode()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.load_game_mode()

        self.main_menu.handle_event(event)
                
                
    def load_game_mode(self):
        index = self.main_menu.get_selected()
        if index == 0:
            # load versus
            Sound().play_sound("vs")
            LevelManager().load_level(ControllerScreen(0))
        if index == 4:
            # load soccer
            #LevelManager.load_level(ControllerScreen(1))
            Sound().play_sound("soccer")
            if pygame.joystick.get_count() == 0:
                LevelManager().load_level(ControllerScreen())
            if pygame.joystick.get_count() >= 1:
                LevelManager().load_level(SoccerScreen())
        if index == 5:
            # load practice
            Sound().play_sound("practice")
            LevelManager().load_level(ControllerScreen(2))
            #pass
        if index == 1:
            # load howToPlay
            Sound().play_knowledge()
            LevelManager().load_level(HowtoplayScreen())
        if index == 2:
            # load credits
            Sound().play_knowledge()
            LevelManager().load_level(CreditsScreen())
        if index == 3:
            Sound().play_quit()
            pygame.time.wait(1200)
            LevelManager().leave_level()

    def update(self):
        #self.update_title_pos()
            
        self.main_menu.update()

    def update_title_pos(self):
        bound = constants.SCREEN_HEIGHT/4-80
        self.title_speed += 1
        self.title_rect.y += self.title_speed
        if self.title_rect.y > bound:
            self.title_rect.y = bound
            self.title_speed *= -1

    def draw(self, screen):
        screen.fill(constants.WHITE)

        screen.blit(self.background_image, [0, 0])

        screen.blit(self.title, self.title_rect)

        self.main_menu.draw(screen)

        #screen.blit(self.game_title, [(constants.SCREEN_WIDTH/2 - self.game_title.get_width()/2), (constants.SCREEN_HEIGHT/4)])
        #screen.blit(self.game_screen, [0, (constants.SCREEN_HEIGHT - 150)])
        #screen.blit(self.credit_screen, [0, (constants.SCREEN_HEIGHT - 100)])
        #screen.blit(self.howtoplay_screen, [0, (constants.SCREEN_HEIGHT - 50)])

        
