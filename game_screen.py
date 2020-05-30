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
from shield import *
from ball import *
from vertical_menu import *
from timer import *

class GameScreen():
    def __init__(self, player1_control=-1, player2_control=0, round_num=0, rounds_won1=0, rounds_won2=0):

        self.final_round = 3
        self.round_num = round_num
        self.rounds_won1 = rounds_won1
        self.rounds_won2 = rounds_won2
        timer_rect = pygame.rect.Rect(constants.SCREEN_WIDTH/2-56,10,
                                      100,100)
        
        self.timer = Timer(timer_rect,60)
        self.timer.start()

        self.center_screen = [constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/2]

        self.gap = 100
        pygame.mouse.set_visible(False)
        self.chaos_mode_on = False

        pause_on = []
        pause_off = []
        pause_on.append(Art().get_image('resume_on'))
        pause_on.append(Art().get_image('quit_on'))
        pause_off.append(Art().get_image('resume_off'))
        pause_off.append(Art().get_image('quit_off'))

        pause_rect = pygame.rect.Rect(constants.SCREEN_WIDTH/2 - pause_on[0].get_rect().size[0],
                                      constants.SCREEN_HEIGHT/2 - pause_on[1].get_rect().size[0],
                                      pause_on[0].get_rect().size[0]*2,
                                      pause_on[0].get_rect().size[1]*4)

        if player1_control == player2_control or \
           (player1_control < 0 and player2_control < 0):
            raise ValueError("two players cannot share the same input device")
        
        self.pause_menu = VerticalMenu(pause_rect,pause_off,pause_on)

        if player1_control < 0:
            self.player1 = KeyboardPlayer(1)
            self.player2 = JoystickPlayer(2,player2_control)
        else:
            self.player1 = JoystickPlayer(1,player1_control)
            if player2_control < 0:
                self.player2 = KeyboardPlayer(2)
            else:
                self.player2 = JoystickPlayer(2, player2_control)
        
        Music().stop()
        Music().play_repeat("game_music")

        self.background_image = Art().get_image("basketBallCourt")
        
        self.player1_health_bar = Art().get_health_bar_image(1,"5")
        self.player2_health_bar = Art().get_health_bar_image(2,"5")
        
        self.timer_box = Art().get_image("timerFrame")
    
        font = pygame.font.SysFont('Calibri', 20, True, False)
        font2 = pygame.font.SysFont('Calibri', 40, True, False)

        self.gameover = font2.render("Gameover",True,constants.BLACK)
        self.p1_win_text = font2.render("Player 1 Wins!!!!",True,constants.RED)
        self.p2_win_text = font2.render("Player 2 Wins!!!!",True,constants.BLUE)
        self.draw_text = font2.render("DRAW GAME",True,constants.BLACK)
        self.temp = font.render("Work in progress",True,constants.BLACK)

        # every onscreen sprite must be added to this group
        self.all_sprites = pygame.sprite.Group()
                
        # sprites with distinct functionality
        # (red balls, neutral balls, etc)
        # should each have their own group
        self.blue_balls = pygame.sprite.Group()
        self.red_balls = pygame.sprite.Group()
        self.yellow_balls = pygame.sprite.Group()

        self.players = pygame.sprite.Group()

        self.reticles = pygame.sprite.Group()

        self.shields = pygame.sprite.Group()

        self.players.add(self.player1)
        self.players.add(self.player2)

        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        self.reticle1 = Reticle(0, 0, 1) # x, y, player number

        self.reticle2 = Reticle(0 ,0, 2) # x, y, player number

        self.last_shot = [pygame.time.get_ticks(), pygame.time.get_ticks()]
        
        self.reticles.add(self.reticle1)
        self.reticles.add(self.reticle2)

        self.all_sprites.add(self.reticle1)
        self.all_sprites.add(self.reticle2)

        self.shield1 = Shield(0,0,1)
        self.shield2 = Shield(0,0,2)

        self.shields.add(self.shield1)
        self.shields.add(self.shield2)

        self.all_sprites.add(self.shield1)
        self.all_sprites.add(self.shield2)

        self.paused = False
        self.started = False
        self.check = False
        self.time = pygame.time.get_ticks()
        
        self.game_over = False
        self.knockout = False
        self.player1_wins = False
        self.player2_wins = False
        self.draw_game = False
        self.announcements_over = False

        #self.generate_test_balls()


    def quit(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
        Music().stop()
        Music().play_repeat("title_music")
        LevelManager().leave_level()


    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    self.toggle_pause()
                else:
                    self.quit()
            if event.key == pygame.K_SPACE and not self.game_over:
                if self.paused:
                    if self.pause_menu.get_selected()==0:
                        self.unpause()
                    elif self.pause_menu.get_selected()==1:
                        self.quit()
                        

        elif event.type == pygame.JOYBUTTONDOWN:
            if not self.game_over:
                for player in self.players:
                    if player.get_control() >= 0:
                        if player.get_joystick().get_button(7):
                            self.toggle_pause()
                        elif player.get_joystick().get_button(0):
                            if self.paused:
                                if self.pause_menu.get_selected()==0:
                                    self.unpause()
                                elif self.pause_menu.get_selected()==1:
                                    self.quit()
                        elif player.get_joystick().get_button(5) or \
                             player.get_joystick().get_button(4):
                            if not self.game_over and not self.paused:
                                self.shoot(player.get_player_number())
                                print("player" + str(player.get_player_number()) + "shoots")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_over and not self.paused:
                for player in self.players:
                    if player.get_control() == -1:
                        self.shoot(player.get_player_number())
                        print("player" + str(player.get_player_number()) + "shoots")

        self.player1.handle_event(event)
        self.player2.handle_event(event)
        if self.paused:
            self.pause_menu.handle_event(event)

    def who_is_winning(self):
        if self.player1.get_hit_points() > self.player2.get_hit_points():
            return 1
        elif self.player1.get_hit_points() < self.player2.get_hit_points():
            return 2
        else:
            return 0

    def announce_round_end(self, screen):
        if pygame.time.get_ticks() > self.time + constants.PROMPT_DELAY*2:
            self.announcements_over = True
        if pygame.time.get_ticks() > self.time + constants.PROMPT_DELAY:
            # player # wins OR draw
            # player 1 wins
            if self.player1_wins:
                if not self.check:
                    Sound().play_sound('player1wins')
                    self.check = True
                img = Art().get_image('player1_wins')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
            # player 2 wins
            elif self.player2_wins:
                if not self.check:
                    Sound().play_sound('player2wins')
                    self.check = True
                img = Art().get_image('player2_wins')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
            # draw
            elif self.draw:
                if not self.check:
                    Sound().play_sound('draw_game')
                    self.check = True
                img = Art().get_image('draw_game')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)

        else:
            # knockout or time
            # time
            if self.timer.is_time_up():
                img = Art().get_image('time')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
                if self.check:
                    Sound().play_time()
                    self.check = False
                    self.time = pygame.time.get_ticks()
            # knockout
            elif self.knockout:
                img = Art().get_image('knockout')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
                if self.check:
                    Sound().play_win()
                    self.check = False
                    self.time = pygame.time.get_ticks()
                

    def announce_round_start(self, screen):
        if pygame.time.get_ticks() > self.time + constants.PROMPT_DELAY*3:
            # round starts
            self.time = pygame.time.get_ticks()
            self.started = True
        elif pygame.time.get_ticks() >= self.time + constants.PROMPT_DELAY*2:
            # go
            if not self.check:
                Sound().play_go()
                self.check = True
            img = Art().get_image('go')
            rect = img.get_rect(center = self.center_screen)
            screen.blit(img, rect)
        elif pygame.time.get_ticks() >= self.time + constants.PROMPT_DELAY:
            # round #
            if self.check:
                Sound().play_round(self.round_num)
                self.check = False
            img = Art().get_round(str(self.round_num))
            rect = img.get_rect(center = self.center_screen)
            screen.blit(img, rect)
            
        else:
            # ready?
            if not self.check:
                Sound().play_ready_round()
                self.check = True
                self.time = pygame.time.get_ticks()
            img = Art().get_image('ready')
            rect = img.get_rect(center = self.center_screen)
            screen.blit(img, rect)
            

    def update(self):
        print(str(self.check))
        if self.started and not self.game_over and not self.paused:
            self.timer.update()
            self.update_reticles()
            self.update_shields()
            self.all_sprites.update()
            self.check_collisions()
            self.check_health()
            if self.timer.is_time_up() and not self.game_over:
                self.end_round()

        if self.paused:
            self.pause_menu.update()
        if self.announcements_over and self.game_over:
            #self.load_next_round()
            pass


    def end_round(self):
        self.game_over = True
        self.time = pygame.time.get_ticks()
        self.reticles.remove(self.reticle1)
        self.reticles.remove(self.reticle2)
        # player 1 wins
        if self.who_is_winning() == 1:
            self.player1_wins = True
            self.all_sprites.remove(self.player2)
            self.players.remove(self.player2)
        # player 2 wins
        elif self.who_is_winning() == 2:
            self.player2_wins = True
            self.all_sprites.remove(self.player1)
            self.players.remove(self.player1)
        # draw game            
        else:
            self.draw_game = True
        if self.player1.get_hit_points() == 0 or \
           self.player2.get_hit_points() == 0:
            self.knockout = True

    def load_next_round(self):
        if self.round_num == 0:
            # make the rematch/quit menu
            pass
        elif self.round_num >= 1:
            round_to_load = self.round_num + 1
            if round_to_load == self.final_round:
                round_to_load = 0
            LevelManager().leave_level()
            if self.player1_wins:
                self.rounds_won1 += 1

            elif self.player2_wins:
                self.rounds_won2 += 1

            elif self.draw:
                self.rounds_won1 += 1
                self.rounds_won2 += 1
                
            LevelManager().load(GameScreen(self.player1.get_control(),
                                               self.player2.get_control(),
                                               round_to_load,
                                               self.rounds_won1,
                                               self.rounds_won2))

    def draw_background(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background_image, [0, 0])
        screen.blit(self.timer_box,
                    [(constants.SCREEN_WIDTH/2) - (self.timer_box.get_rect().size[0]/2),
                     0])
        
        screen.blit(self.temp, [0,0])        

    def draw_health_bars(self, screen):
        screen.blit(self.player1_health_bar, [(constants.SCREEN_WIDTH/2 - self.player1_health_bar.get_width()) - self.gap, 5])
        screen.blit(self.player2_health_bar, [((constants.SCREEN_WIDTH/2) + self.gap), 5])

    def draw(self, screen):
        
        self.draw_background(screen)
        self.draw_health_bars(screen)
        self.timer.draw(screen)
        self.players.draw(screen)
        if not self.started:
            self.announce_round_start(screen)
        else:
            self.red_balls.draw(screen)
            self.blue_balls.draw(screen)
            self.yellow_balls.draw(screen)
            self.shields.draw(screen)
            self.reticles.draw(screen)
            #self.draw_gameover(screen)  
        if self.paused and not self.game_over:
            self.pause_menu.draw(screen)
        if self.game_over:
            self.announce_round_end(screen)


    def draw_gameover(self, screen):
        if self.game_over == True:
            #screen.blit(self.gameover, [(constants.SCREEN_WIDTH/2 - self.gameover.get_width()/2), constants.SCREEN_HEIGHT/4])
            if self.player1_wins == True:
                img = Art().get_image('player1_wins')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
                #screen.blit(self.p1_win_text, [(constants.SCREEN_WIDTH/4 - self.p1_win_text.get_width()/2), constants.SCREEN_HEIGHT/4])

            elif self.player2_wins == True:
                img = Art().get_image('player2_wins')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
                #screen.blit(self.p2_win_text, [(((constants.SCREEN_WIDTH/4) * 3) - self.p2_win_text.get_width()/2), constants.SCREEN_HEIGHT/4])

            elif self.draw_game:
                img = Art().get_image('draw_game')
                rect = img.get_rect(center = self.center_screen)
                screen.blit(img, rect)
                #draw_rect = self.draw_text.get_rect(center=(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2))
                #screen.blit(self.draw_text, draw_rect)


    def print_pause_screen(self, screen):
        img = Art().get_image('paused')
        img.set_colorkey(constants.TRANSPARENT_COLOR)
        pos = [constants.SCREEN_WIDTH/2 - (img.get_rect().size[0]/2), constants.SCREEN_HEIGHT/2 - (img.get_rect().size[1]/2)]
        screen.blit(img, pos)

        
    def update_reticles(self):
        # player1 keyboard, player2 joystick
        if self.player1.get_control() == -1:
            self.reticle1.set_center(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            self.reticle2.set_center((self.player2.get_joystick().get_axis(4) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player2.get_center()[0],
                                     (self.player2.get_joystick().get_axis(3) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player2.get_center()[1] )
            
        # player1 joystick, player2 keyboard
        elif self.player2.get_control() == -1:
            self.reticle1.set_center((self.player1.get_joystick().get_axis(4) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player1.get_center()[0],
                                     (self.player1.get_joystick().get_axis(3) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player1.get_center()[1] )
            self.reticle2.set_center(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            
            
        # player1 joystick, player2 joystick
        elif self.player1.get_control >= 0 and \
             self.player2.get_control >= 0:
            self.reticle1.set_center((self.player1.get_joystick().get_axis(4) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player1.get_center()[0],
                                     (self.player1.get_joystick().get_axis(3) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player1.get_center()[1] )
            self.reticle2.set_center((self.player2.get_joystick().get_axis(4) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player2.get_center()[0],
                                     (self.player2.get_joystick().get_axis(3) * constants.JOYSTICK_RETICLE_DISTANCE) + self.player2.get_center()[1] )


    def update_shields(self):
        if True:
            d = [0,0]
            d[0] = self.reticle1.get_center()[0] - self.player1.get_center()[0]
            d[1] = self.reticle1.get_center()[1] - self.player1.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            if hypo == 0:
                hypo = 0.1
            relative_pos = [ d[0]/hypo * constants.SHIELD_DISTANCE,
                             d[1]/hypo * constants.SHIELD_DISTANCE]

            self.shield1.set_center(self.player1.get_center()[0] + relative_pos[0],
                                    self.player1.get_center()[1] + relative_pos[1])
        if True:
            d = [0,0]
            d[0] = self.reticle2.get_center()[0] - self.player2.get_center()[0]
            d[1] = self.reticle2.get_center()[1] - self.player2.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            if hypo == 0:
                hypo = 0.1
            relative_pos = [ d[0]/hypo * constants.SHIELD_DISTANCE,
                             d[1]/hypo * constants.SHIELD_DISTANCE]

            self.shield2.set_center(self.player2.get_center()[0] + relative_pos[0],
                                    self.player2.get_center()[1] + relative_pos[1])

    def check_collisions(self):
        #self.check_blue_on_blue()
        #self.check_red_on_red()
        self.check_blue_on_red()
        if self.chaos_mode_on :
            self.check_yellow_on_yellow()
            self.check_yellow_on_red()
            self.check_yellow_on_blue()

        self.check_shields()
        
        self.check_players()
        

    def check_shields(self):
        blue_hits = pygame.sprite.spritecollide(self.shield1, self.blue_balls, False)

        for ball in blue_hits:
            ball.set_speed(ball.get_speed()[0]*-1,ball.get_speed()[1]*-1)

        red_hits = pygame.sprite.spritecollide(self.shield2, self.red_balls, False)

        for ball in red_hits:
            ball.set_speed(ball.get_speed()[0]*-1,ball.get_speed()[1]*-1)        
            

    def check_players(self):
        if not self.game_over:
            blue_hits = pygame.sprite.spritecollide(self.player1, self.blue_balls, True)
            yellow_hits = pygame.sprite.spritecollide(self.player1, self.yellow_balls, True)

            if len(blue_hits) > 0 or len(yellow_hits) > 0:
                self.player1.damage()

            red_hits = pygame.sprite.spritecollide(self.player2, self.red_balls, True)
            yellow_hits = pygame.sprite.spritecollide(self.player2, self.yellow_balls, True)

            if len(red_hits) > 0 or len(yellow_hits) > 0:
                self.player2.damage()

    def check_health(self):
        self.player1_health_bar = Art().get_health_bar_image(1,str(self.player1.get_hit_points()))
        if self.player1.get_hit_points() <= 0:
            if not self.game_over:
                self.end_round()

        self.player2_health_bar = Art().get_health_bar_image(2,str(self.player2.get_hit_points()))
        if self.player2.get_hit_points() <= 0:
            if not self.game_over:
                self.end_round()

    def can_shoot(self, player_number):
        if player_number == 1:
            return pygame.time.get_ticks() - self.last_shot[0] > constants.SHOT_DELAY
        elif player_number == 2:
            return pygame.time.get_ticks() - self.last_shot[1] > constants.SHOT_DELAY

    def shoot(self, player_number):
        if player_number == 1 and self.can_shoot(player_number):
            self.last_shot[0] = pygame.time.get_ticks()
            d = [0,0]
            d[0] = self.reticle1.get_center()[0] - self.player1.get_center()[0]
            d[1] = self.reticle1.get_center()[1] - self.player1.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            if hypo == 0:
                hypo = 0.1
            speed = [ d[0]/hypo * constants.SHOT_SPEED,
                      d[1]/hypo * constants.SHOT_SPEED]
            #print(speed)
            newBall = RedBall(self.player1.get_pos()[0],
                              self.player1.get_pos()[1],
                              speed[0], speed[1])
            newBall.set_center(self.player1.get_center()[0],
                               self.player1.get_center()[1])
            self.red_balls.add(newBall)
            self.all_sprites.add(newBall)
            Sound().play_sound("player_shooting")
            
        elif player_number == 2 and self.can_shoot(player_number):
            self.last_shot[1] = pygame.time.get_ticks()
            d = [0,0]
            d[0] = self.reticle2.get_center()[0] - self.player2.get_center()[0]
            d[1] = self.reticle2.get_center()[1] - self.player2.get_center()[1]
            hypo = math.sqrt( math.pow(d[0],2) + math.pow(d[1],2) )
            if hypo == 0:
                hypo = 0.1
            speed = [ d[0]/hypo * constants.SHOT_SPEED,
                      d[1]/hypo * constants.SHOT_SPEED]
            #print(speed)
            newBall = BlueBall(self.player2.get_pos()[0],
                              self.player2.get_pos()[1],
                              speed[0], speed[1])
            newBall.set_center(self.player2.get_center()[0],
                               self.player2.get_center()[1])
            self.blue_balls.add(newBall)
            self.all_sprites.add(newBall)
            Sound().play_sound("player_shooting")

    def combine_blue_ball(self, ball1, ball2):
        pos = [0,0]
        speed = [0,0]
        multi = 0
        
        pos[0] += ball1.get_pos()[0]/2
        pos[0] += ball2.get_pos()[0]/2
        pos[1] += ball1.get_pos()[1]/2
        pos[1] += ball2.get_pos()[1]/2

        speed[0] += ball1.get_speed()[0]
        speed[0] += ball2.get_speed()[0]
        speed[1] += ball1.get_speed()[1]
        speed[1] += ball2.get_speed()[1]

        multi += ball1.get_multiplier()
        multi += ball2.get_multiplier()

        return BlueBall(pos[0], pos[1], speed[0], speed[1])

    def combine_red_ball(self, ball1, ball2):
        pos = [0,0]
        speed = [0,0]
        multi = 0
        
        pos[0] += ball1.get_pos()[0]/2
        pos[0] += ball2.get_pos()[0]/2
        pos[1] += ball1.get_pos()[1]/2
        pos[1] += ball2.get_pos()[1]/2

        speed[0] += ball1.get_speed()[0]
        speed[0] += ball2.get_speed()[0]
        speed[1] += ball1.get_speed()[1]
        speed[1] += ball2.get_speed()[1]

        multi += ball1.get_multiplier()
        multi += ball2.get_multiplier()

        return RedBall(pos[0], pos[1], speed[0], speed[1])

    def combine_yellow_ball(self, ball1, ball2):
        pos = [0,0]
        speed = [0,0]
        multi = 0
        
        pos[0] += ball1.get_pos()[0]/2
        pos[0] += ball2.get_pos()[0]/2
        pos[1] += ball1.get_pos()[1]/2
        pos[1] += ball2.get_pos()[1]/2

        speed[0] += ball1.get_speed()[0]
        speed[0] += ball2.get_speed()[0]
        speed[1] += ball1.get_speed()[1]
        speed[1] += ball2.get_speed()[1]

        multi += ball1.get_multiplier()
        multi += ball2.get_multiplier()

        return NeutralBall(pos[0], pos[1], speed[0], speed[1])
       
    def check_blue_on_blue(self):
        for ball in self.blue_balls:
            self.blue_balls.remove(ball)
            self.all_sprites.remove(ball)
            collide = pygame.sprite.spritecollide(ball, self.blue_balls, True)
            
            if len(collide) == 0:
                self.blue_balls.add(ball)
                self.all_sprites.add(ball)

            elif len(collide) == 1:
                # call class method
                # pass collide[0] and ball
                newBall = self.combine_blue_ball(collide[0], ball)

            
                self.blue_balls.add(newBall)
                self.all_sprites.add(newBall)

    def check_red_on_red(self):
        for ball in self.red_balls:
            self.red_balls.remove(ball)
            self.all_sprites.remove(ball)
            collide = pygame.sprite.spritecollide(ball, self.red_balls, True)
            
            if len(collide) == 0:
                self.red_balls.add(ball)
                self.all_sprites.add(ball)

            elif len(collide) == 1:
                newBall = self.combine_red_ball(collide[0], ball)

            
                self.red_balls.add(newBall)
                self.all_sprites.add(newBall)

    def check_yellow_on_yellow(self):
        for ball in self.yellow_balls:
            self.yellow_balls.remove(ball)
            self.all_sprites.remove(ball)
            collide = pygame.sprite.spritecollide(ball, self.yellow_balls, True)
            
            if len(collide) == 0:
                self.yellow_balls.add(ball)
                self.all_sprites.add(ball)

            elif len(collide) == 1 and self.chaos_mode_on:
                newBall = self.combine_yellow_ball(collide[0], ball)

                self.yellow_balls.add(newBall)
                self.all_sprites.add(newBall)

    def check_blue_on_red(self):
        blue_collide = pygame.sprite.groupcollide(self.blue_balls, self.red_balls, False, False)
        red_collide = pygame.sprite.groupcollide(self.red_balls, self.blue_balls, True, True)
        
        if len(blue_collide) == 1 and len(red_collide) == 1 and self.chaos_mode_on:
            # call class method
            # pass in blue_collide[0] and red_collide[0]
            #newBall = self.combine_yellow_ball(blue_collide[0], red_collide[0])

            speed = [0,0]
            pos = [0,0]
            multi = 0

            
            for ball in blue_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            for ball in red_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            newBall = NeutralBall(pos[0], pos[1], speed[0], speed[1])
            self.yellow_balls.add(newBall)
            self.all_sprites.add(newBall)
            Sound().play_sound("balls_colliding")

    def check_yellow_on_red(self):
        yellow_collide = pygame.sprite.groupcollide(self.yellow_balls, self.red_balls, False, False)
        red_collide = pygame.sprite.groupcollide(self.red_balls, self.yellow_balls, True, True)
        
        if len(yellow_collide) > 0 and len(red_collide) > 0:
            speed = [0,0]
            pos = [0,0]
            multi = 0

            for ball in yellow_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            for ball in red_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            newBall = NeutralBall(pos[0], pos[1], speed[0], speed[1])
            self.yellow_balls.add(newBall)
            self.all_sprites.add(newBall)
            Sound().play_sound("balls_colliding")

    def check_yellow_on_blue(self):
        yellow_collide = pygame.sprite.groupcollide(self.yellow_balls, self.blue_balls, False, False)
        blue_collide = pygame.sprite.groupcollide(self.blue_balls, self.yellow_balls, True, True)
        
        if len(yellow_collide) > 0 and len(blue_collide) > 0:
            speed = [0,0]
            pos = [0,0]
            multi = 0

            for ball in yellow_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            for ball in blue_collide:
                pos[0] += ball.get_pos()[0]/2
                pos[1] += ball.get_pos()[1]/2
            
                speed[0] += ball.get_speed()[0]
                speed[1] += ball.get_speed()[1]
            
                multi += ball.get_multiplier()

            newBall = NeutralBall(pos[0], pos[1], speed[0], speed[1])
            self.yellow_balls.add(newBall)
            self.all_sprites.add(newBall)
            Sound().play_sound("balls_colliding")

    def generate_test_balls(self):
        for i in range(3):
            x = random.randrange(0, constants.SCREEN_WIDTH)
            y = random.randrange(0, constants.SCREEN_HEIGHT)
            speed_x = random.randrange(-2, 3)
            speed_y = random.randrange(-2, 3)
            blueBall = BlueBall(x, y, speed_x, speed_y, 1)
            self.blue_balls.add(blueBall)
            self.all_sprites.add(blueBall)
            
        for i in range(3):
            x = random.randrange(0, constants.SCREEN_WIDTH)
            y = random.randrange(0, constants.SCREEN_HEIGHT)
            speed_x = random.randrange(-2, 3)
            speed_y = random.randrange(-2, 3)
            redBall = RedBall(x, y, speed_x, speed_y, 1)
            self.red_balls.add(redBall)
            self.all_sprites.add(redBall)

    #Pause methods
    def pause(self):
        self.paused = True
        self.pause_menu.reset(0)
        pygame.mouse.set_visible(True)
    
    def unpause(self):
        self.paused = False
        self.pause_menu.reset()
        pygame.mouse.set_visible(False)

    def is_paused(self):
        return self.paused

    def toggle_pause(self):
        if self.paused:
            self.unpause()
        else:
            self.pause()
