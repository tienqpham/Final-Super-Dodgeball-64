import pygame
import constants

from level_manager import *
from art import *

pygame.init()

class CreditsScreen():
    def __init__(self):
        self.joysticks = []

        for i in range(0,pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
            self.joysticks.append(pygame.joystick.Joystick(i))

        font = pygame.font.SysFont('Calibri', 40, True, False)
        font2 = pygame.font.SysFont('Calibri', 30, True, False)

        self.background_image = Art().get_image("basketBallCourt_dark")
        
        Credits = font.render("Credits:",True,constants.WHITE)
        programming = font2.render("Programming: Harrison Malloy, Tien Pham, Austin Tauer, Nicholas Riebel",True,constants.WHITE)
        art = font2.render("Art: Harrison Malloy",True,constants.WHITE)
        announcer = font2.render("Announcer: Harrison Malloy",True,constants.WHITE)
        music_sound = font2.render("Music and Sound Effects:",True,constants.WHITE)
        title_song = font2.render("Title song: 'Clicky' from Electronic (2018) by Manuel Senfft (www.tagirijus.de)",True,constants.WHITE)
        game_song = font2.render("Game song: 'Hard Fight' from Hard (2018) by Manuel Senfft (www.tagirijus.de)",True,constants.WHITE)
        colliding = font2.render("Balls colliding: https://opengameart.org/content/bombexplosion8bit",True,constants.WHITE)
        throwing = font2.render("Throwing ball: https://opengameart.org/content/sfxthrow - copyright Blender Foundation : apricot.blender.org",True,constants.WHITE)
        throwing2 = font2.render("Throwing sound effect from Yo Frankie! game",True,constants.WHITE)
        border = font2.render("Hitting Border: https://opengameart.org/content/short-alarm",True,constants.WHITE)
        hitting = font2.render("Getting hit by ball: https://opengameart.org/content/grunt author: n3b",True,constants.WHITE)

        self.text = []
        self.text.append(Credits)
        self.text.append(programming)
        self.text.append(art)
        self.text.append(announcer)
        self.text.append(music_sound)
        self.text.append(title_song)
        self.text.append(game_song)
        self.text.append(colliding)
        self.text.append(throwing)
        self.text.append(throwing2)
        self.text.append(hitting)
        
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

        for i in range(0,len(self.text)):
            rect = self.text[i].get_rect(center=(constants.SCREEN_WIDTH/2, (i+1)*50))
            screen.blit(self.text[i],rect)

        '''
        screen.blit(self.credits, [(constants.SCREEN_WIDTH/2 - self.credits.get_width()/2), 50])
        screen.blit(self.programming, [(constants.SCREEN_WIDTH/2 - self.programming.get_width()/2), 150])
        screen.blit(self.art, [(constants.SCREEN_WIDTH/2 - self.art.get_width()/2), 200])
        screen.blit(self.music_sound, [(constants.SCREEN_WIDTH/2 - self.music_sound.get_width()/2), 300])
        screen.blit(self.title_song, [(constants.SCREEN_WIDTH/2 - self.title_song.get_width()/2), 350])
        screen.blit(self.game_song, [(constants.SCREEN_WIDTH/2 - self.game_song.get_width()/2), 400])
        screen.blit(self.colliding, [(constants.SCREEN_WIDTH/2 - self.colliding.get_width()/2), 450])
        screen.blit(self.throwing, [(constants.SCREEN_WIDTH/2 - self.throwing.get_width()/2), 500])
        screen.blit(self.throwing2, [(constants.SCREEN_WIDTH/2 - self.throwing2.get_width()/2), 550])
        screen.blit(self.border, [(constants.SCREEN_WIDTH/2 - self.border.get_width()/2), 600])
        screen.blit(self.hitting, [(constants.SCREEN_WIDTH/2 - self.hitting.get_width()/2), 650])
        '''
        
