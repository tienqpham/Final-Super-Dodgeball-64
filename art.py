import pygame

import constants

from file import *

class Art():
    class __Art:
        def __init__(self):
            # needs images
            self.imgList = {'missing': File().load("missing"),
                            'targetBlue': File().load("targetBlue"),
                            
                            'ball': File().load("ball"),
                            
                            'player1': File().load("player1"),
                            'player2': File().load("player2"),
                            
                            'reticle1': File().load("reticle1"),
                            'reticle2': File().load("reticle2"),

                            'shield1': File().load("shield_red"),
                            'shield2': File().load("shield_blue"),
                            
                            'ball1': File().load("ball1"),
                            'ball2': File().load("ball2"),
                            
                            'gamepad_select': File().load("gamepad_select"),
                            'keyboard_select': File().load("keyboard_select"),

                            'howtoplay':File().load("howtoplay"),
                            
                            'ready1_off': File().load("ready1_off"),
                            'ready1_on': File().load("ready1_on"),
                            'ready2_off': File().load("ready2_off"),
                            'ready2_on': File().load("ready2_on"),

                            'title': File().load("title"),

                            'quit_off': File().load("quit_green_off"),
                            'quit_on': File().load("quit_green_on"),
                            'resume_off': File().load("resume_green_off"),
                            'resume_on': File().load("resume_green_on"),

                            'quit_red_off': File().load("quit_red_off"),
                            'quit_red_on': File().load("quit_red_on"),
                            'practice_red_off': File().load("practice_red_off"),
                            'practice_red_on': File().load("practice_red_on"),
                            'versus_split_off': File().load("versus_split_off"),
                            'versus_split_on': File().load("versus_split_on"),
                            'howToPlay_red_off': File().load("howToPlay_red_off"),
                            'howToPlay_red_on': File().load("howToPlay_red_on"),
                            'soccer_split_off': File().load("soccer_split_off"),
                            'soccer_split_on': File().load("soccer_split_on"),
                            'credits_red_off': File().load("credits_red_off"),
                            'credits_red_on': File().load("credits_red_on"),

                            'timerFrame': File().load("timerFrame"),

                            'round1': File().load("round1"),
                            'round2': File().load("round2"),
                            'finalRound': File().load("finalRound"),
                            'ready': File().load("ready"),
                            'go': File().load("go"),

                            'player1_wins': File().load("player1_wins"),
                            'player2_wins': File().load("player2_wins"),
                            'draw_game': File().load("draw_game"),

                            'time': File().load("time"),
                            'knockout': File().load("knockout"),
                            
                            'paused': File().load("paused"),
                            'basketBallCourt': File().load("basketBallCourt"),
                            'basketBallCourt_dark': File().load("basketBallCourt_dark"),

                            'paused': File().load("paused"),
                            'soccerBall': File().load("soccerBall"),
                            'soccerField': File().load("soccerField"),
                            'tempGoal': File().load("tempGoal")}
            

            self.P1healthBarsList = {'5': File().load("health_red_5of5"),
                                     '4': File().load("health_red_4of5"),
                                     '3': File().load("health_red_3of5"),
                                     '2': File().load("health_red_2of5"),
                                     '1': File().load("health_red_1of5"),
                                     '0': File().load("health_red_0of5")}

            self.P2healthBarsList = {'5': File().load("health_blue_5of5"),
                                     '4': File().load("health_blue_4of5"),
                                     '3': File().load("health_blue_3of5"),
                                     '2': File().load("health_blue_2of5"),
                                     '1': File().load("health_blue_1of5"),
                                     '0': File().load("health_blue_0of5")}
            

            self.digit_list = {'0': File().load("digital0"),
                               '1': File().load("digital1"),
                               '2': File().load("digital2"),
                               '3': File().load("digital3"),
                               '4': File().load("digital4"),
                               '5': File().load("digital5"),
                               '6': File().load("digital6"),
                               '7': File().load("digital7"),
                               '8': File().load("digital8"),
                               '9': File().load("digital9")}

            self.round_list = {'1': File().load("round1"),
                               '2': File().load("round2"),
                               '0': File().load("finalRound")}

        # class methods
        def get_image(self, id):
            img = self.imgList.get(id)
            image = pygame.image.load(str(img)).convert()
            image.set_colorkey(constants.TRANSPARENT_COLOR)
            return image

        def get_round(self, id):
            img = self.round_list.get(id)
            image = pygame.image.load(str(img)).convert()
            image.set_colorkey(constants.TRANSPARENT_COLOR)
            return image

        def get_digit(self,id):
            img = self.digit_list.get(id)
            image = pygame.image.load(str(img)).convert()
            image.set_colorkey(constants.BLACK)
            return image

        def get_health_bar_image(self,player_number,id):
            if player_number == 1:
                img = self.P1healthBarsList.get(id)
            elif player_number == 2:
                img = self.P2healthBarsList.get(id)
            image = pygame.image.load(str(img)).convert()
            image.set_colorkey(constants.TRANSPARENT_COLOR)
            return image


    instance = None
    def __init__(self):
        if not Art.instance:
            Art.instance = Art.__Art()

    def __getattr__(self, name):
        return getattr(self.instance, name)
