import pygame
from timer import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

clock = pygame.time.Clock()

done = False

rect = pygame.Rect(0,0, 200, 200)

my_timer = Timer(rect,60)


while not done:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                break
            elif event.key == pygame.K_SPACE:
                my_timer.toggle_pause()

    my_timer.update()
    screen.blit(Art().get_image('timerFrame'),[0,0])
    my_timer.draw(screen)
    
    pygame.display.flip()

pygame.quit()
