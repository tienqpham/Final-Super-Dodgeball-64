import pygame
import random
import math

import constants

from level_manager import *
from art import *
from music import *
from sound import *
from keyboard_player import *
from joystick_player import *
from reticle import *
from ball import *
from game_screen import*
from math import *


class SoccerScreen(GameScreen):
    def __init__(self, player1_control=-1, player2_control=0):
        super().__init__(player1_control=-1, player2_control=0)
        self.soccerBall = NeutralBall(800, 800, 0, 0, 1)
        self.speed = 10
        self.hitScale = 1.5
        self.soccerBalls = pygame.sprite.Group()
        self.soccerBalls.add(soccerBall)
        self.goals1 = pygame.sprite.Group()
        goals1.add(SoccerGoal().__init__(1))
        self.goals2 = pygame.sprite.Group()
        goals2.add(SoccerGoal().__init__(2))
        

    #should be updated along with game_screen
    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.joystick.quit()
                pygame.joystick.init()
                for i in range(pygame.joystick.get_count()):
                    pygame.joystick.Joystick(i).init()
                Music().stop()
                Music().play_repeat("title_music")
                LevelManager().leave_level()
            elif event.key == pygame.K_SPACE and not self.game_over:
                self.toggle_pause()
        
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.player2.get_joystick().get_button(7) and not self.game_over:
                self.toggle_pause()
            #elif self.player2.get_joystick().get_button(5) or self.player2.get_joystick().get_button(4):
                #if not self.game_over and not self.paused:
                    #self.shoot(2)
                    #print("player 2 shoots")

        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #if not self.game_over and not self.paused:
                #self.shoot(1)
                #print("player 1 shoots")

        #if not self.paused: 
        self.player1.handle_control_event(event)

    def update(self) :
        self.check_collisions()

    def check_collisions(self):
        self.check_player1()
        self.check_player2()
        self.check_goal1()
        self.check_goal2()
    
    def check_player1(self):
        if not self.game_over:
            ball_hits = pygame.sprite.spritecollide(self.player1, self.soccerBalls, True)

            if len(ball_hits) > 0:
                shoot(1)

    def check_player2(self):
        if not self.game_over:
            ball_hits = pygame.sprite.spritecollide(self.player1, self.soccerBalls, True)

            if len(ball_hits) > 0:
                shoot(2)
                

    def check_goal1(self):
        if not self.game_over:
            goalHits = pygame.sprite.spritecollide(self.goals1, self.soccer_balls, True)
            self.game_over = True
            self.player2_wins = True
            self.all_sprites.remove(self.player1)
            self.players.remove(self.player1)
            self.reticles.remove(self.reticle1)
            self.reticles.remove(self.reticle2)

    def check_goal2(self):
        if not self.game_over:
            goalHits = pygame.sprite.spritecollide(self.goals2, self.soccer_balls, True)
            self.game_over = True
            self.player1_wins = True
            self.all_sprites.remove(self.player2)
            self.players.remove(self.player2)
            self.reticles.remove(self.reticle1)
            self.reticles.remove(self.reticle2)
                
    def shoot(self, player_number):
        if player_number == 1:
            d = [0,0]
            d[0] = self.reticle1.get_center()[0] - self.player1.get_center()[0]
            d[1] = self.reticle1.get_center()[1] - self.player1.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            speed = [ d[0]/hypo * constants.SHOT_SPEED,
                      d[1]/hypo * constants.SHOT_SPEED]
            soccerBall.speed_x += speed[0] * hitScale
            soccerBall.x += soccerBall.speed_x
            soccerBall.y += soccerBall.speed_y
            Sound().play_sound("player_shooting")
            
        elif player_number == 2:
            d = [0,0]
            d[0] = self.reticle2.get_center()[0] - self.player2.get_center()[0]
            d[1] = self.reticle2.get_center()[1] - self.player2.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            speed = [ d[0]/hypo * constants.SHOT_SPEED,
                      d[1]/hypo * constants.SHOT_SPEED]
            soccerBall.speed_x += speed[0] * hitScale
            soccerBall.x += soccerBall.speed_x
            soccerBall.y += soccerBall.speed_y
            Sound().play_sound("player_shooting")














