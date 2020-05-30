import pygame
import constants
from art import *
from control_select import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 900
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT])

art = Art()

clock = pygame.time.Clock()

done = False

my_selector = ControlSelect(1)

while not done:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        my_selector.handle_event(event)
        if event.type == pygame.QUIT:
            done = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                break
            elif event.key == pygame.K_SPACE:
                if my_selector.get_player1_control() < -1:
                    print("no player 1 peripheral selected")
                if my_selector.get_player1_control() == -1:
                    print("player 1 uses keyboard")
                if my_selector.get_player1_control() == 0:
                    print("player 1 uses joystick 0")
                if my_selector.get_player1_control() == 1:
                    print("player 1 uses joystick 1")
                if my_selector.get_player2_control() < -1:
                    print("no player 2 peripheral selected")
                if my_selector.get_player2_control() == -1:
                    print("player 2 uses keyboard")
                if my_selector.get_player2_control() == 0:
                    print("player 2 uses joystick 0")
                if my_selector.get_player2_control() == 1:
                    print("player 2 uses joystick 1")
                if my_selector.is_everyone_ready():
                    print("READY!")
                else:
                    print("NOT READY!")
        elif event.type == pygame.JOYBUTTONDOWN:
            for i in range(0, pygame.joystick.get_count()):
                if pygame.joystick.Joystick(i).get_button(0):
                    if my_selector.get_player1_control() < -1:
                        print("no player 1 peripheral selected")
                    if my_selector.get_player1_control() == -1:
                        print("player 1 uses keyboard")
                    if my_selector.get_player1_control() == 0:
                        print("player 1 uses joystick 0")
                    if my_selector.get_player1_control() == 1:
                        print("player 1 uses joystick 1")
                    if my_selector.get_player2_control() < -1:
                        print("no player 2 peripheral selected")
                    if my_selector.get_player2_control() == -1:
                        print("player 2 uses keyboard")
                    if my_selector.get_player2_control() == 0:
                        print("player 2 uses joystick 0")
                    if my_selector.get_player2_control() == 1:
                        print("player 2 uses joystick 1")
                    if my_selector.is_everyone_ready():
                        print("READY!")
                    else:
                        print("NOT READY!")

            print('')
            print('')
    my_selector.draw(screen)

    pygame.display.flip()

pygame.quit()
