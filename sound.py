import pygame
import random
from file import *


class Sound():
    class __Sound:
        def __init__(self):
            self.announcer_volume = 1
            # needs sfx
            self.soundlist = {"balls_colliding": File().load("colliding"),
                              "hitting_border": File().load("border"),
                              "player_shooting": File().load("shooting"),
                              "hit_by_ball": File().load("hitting"),
                              "finalround": File().load("normal_finalround"),
                              "heycomeon": File().load("normal_heycomeon"),
                              "heystepitup": File().load("normal_heystepitup"),
                              "itsnotover": File().load("normal_itsnotover"),
                              "neverseenabattle": File().load("normal_neverseenabattle"),
                              "player1wins": File().load("normal_player1wins"),
                              "player2wins": File().load("normal_player2wins"),
                              "round1": File().load("normal_round1"),
                              "round2": File().load("normal_round2"),
                              "round3": File().load("normal_round3"),
                              "round4": File().load("normal_round4"),
                              "straight": File().load("normal_straight"),
                              "vs": File().load("normal_vs"),
                              "soccer": File().load("normal_soccer"),
                              "practice": File().load("normal_practice"),
                              "draw_game": File().load("normal_drawgame"),
                              "time": File().load("normal_time"),
                              "timeup":File().load("normal_timeup")} # load sfx from file
            
            self.roundreadylist = {"1": File().load("normal_fightfortheages"),
                                   "2": File().load("normal_areyouready"),
                                   "3": File().load("normal_areyouready2"),
                                   "4": File().load("normal_faceitstraight"),
                                   "5": File().load("normal_getready"),
                                   "6": File().load("normal_goforbroke")}

            self.round2readylist = {"1": File().load("normal_heycomeon"),
                                    "2": File().load("normal_heystepitup"),
                                    "3": File().load("normal_warmingup"),
                                    "4": File().load("normal_youcantgiveitup"),
                                    "5": File().load("normal_itsnotover")}

            self.finalroundreadylist = {"1": File().load("normal_dodgeorbedodge"),
                                        "2": File().load("normal_doordodge"),
                                        "3": File().load("normal_battleofthecentury"),
                                        "4": File().load("normal_noholdbard"),
                                        "5": File().load("normal_nosecondchance"),
                                        "6": File().load("normal_letloose")}

            self.golist= {"1": File().load("normal_goforit"),
                          "2": File().load("normal_goforitman"),
                          "3": File().load("normal_letsparty")}

            self.winlist= {"1": File().load("normal_Icantbelievemyeyes"),
                          "2": File().load("normal_knockout"),
                          "3": File().load("normal_leaveamark"),
                          "4": File().load("normal_leaveamark2")}

            self.knowledgelist = {"1": File().load("normal_knowledgeispower"),
                                  "2": File().load("normal_readup"),
                                  "3": File().load("normal_checkitout")}

            self.quitlist= {"1": File().load("normal_solong"),
                            "2": File().load("normal_seeyoulater"),
                            "3": File().load("normal_comebacksoon")}

        def play_round(self,num):
            if num == 0:
                sound = pygame.mixer.Sound(self.soundlist.get('finalround'))
                sound.set_volume(self.announcer_volume)
                sound.play()
            elif num == 1:
                sound = pygame.mixer.Sound(self.soundlist.get('round1'))
                sound.set_volume(self.announcer_volume)
                sound.play()
            elif num == 2:
                sound = pygame.mixer.Sound(self.soundlist.get('round2'))
                sound.set_volume(self.announcer_volume)
                sound.play()

        def play_time(self):
            num = random.randint(1,2)
            if num == 1:
                sound = pygame.mixer.Sound(self.soundlist.get('time'))
                sound.play()
            if num == 2:
                sound = pygame.mixer.Sound(self.soundlist.get('timeup'))
                sound.play()

        def play_sound(self, id):
            sound = pygame.mixer.Sound(self.soundlist.get(id))
            sound.play()

        def play_ready_round(self):
            string = str(random.randint(1,len(self.roundreadylist)))
            print(string)
            sound = pygame.mixer.Sound(self.roundreadylist.get(string))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_ready_round2(self):
            sound = pygame.mixer.Sound(self.round2readylist.get(str(random.randint(1,len(self.round2readylist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_ready_finalround(self):
            sound = pygame.mixer.Sound(self.finalroundreadylist.get(str(random.randint(1,len(self.finalroundreadylist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_go(self):
            sound = pygame.mixer.Sound(self.golist.get(str(random.randint(1,len(self.golist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_win(self):
            sound = pygame.mixer.Sound(self.winlist.get(str(random.randint(1,len(self.winlist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_knowledge(self):
            sound = pygame.mixer.Sound(self.knowledgelist.get(str(random.randint(1,len(self.knowledgelist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

        def play_quit(self):
            sound = pygame.mixer.Sound(self.quitlist.get(str(random.randint(1,len(self.quitlist)))))
            sound.set_volume(self.announcer_volume)
            sound.play()

    instance = None
    def __init__(self):
        if not Sound.instance:
            Sound.instance = Sound.__Sound()

    def __getattr__(self, name):
        return getattr(self.instance, name)
