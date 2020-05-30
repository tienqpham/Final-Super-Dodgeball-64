import pygame
import constants
from level_manager import *
from title_screen import *
from file import *
from art import *
from sound import *
from music import *

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH,
                                  constants.SCREEN_HEIGHT])

clock = pygame.time.Clock()
 
level_manager = LevelManager()
level_manager.load_level(TitleScreen())

file = File()

art = Art()

sound = Sound()

music = Music()

done = False

# -------- Main Program Loop -----------
while not done:  
    # get current level from level manager
    current_level = level_manager.get_current_level()

    # exit game if current level == None
    if current_level == None:
        break

    # game logic
    current_level.update()
    current_level.draw(screen)

    # draw
 
    pygame.display.flip()
 
    clock.tick(60)

    # control logic loop
    for event in pygame.event.get():
        current_level.handle_keyboard_event(event)
        if event.type == pygame.QUIT:
            done = True
            break

pygame.quit()
