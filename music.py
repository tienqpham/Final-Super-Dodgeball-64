import pygame
from file import *

class Music():
    class __Music():
    
    
        def __init__(self):
            # needs songs
            self.songlist = {"title_music": File().load("titlemusic"),
                             "new_title_music": File().load("newtitlemusic"),
                             "game_music": File().load("gamemusic")} 
            self.isPaused = False
            
        def play_once(self, id):
            pygame.mixer.music.load(self.songlist.get(id))
            pygame.mixer.music.play()
            self.isPaused = False

        def play_repeat(self, id):
            file_location = self.songlist.get(id)
            print(file_location)
            pygame.mixer.music.load(self.songlist.get(id))
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)
            self.isPaused = False

        def stop(self):
            pygame.mixer.music.stop()

        def toggle_pause(self):
            if self.isPaused == False:
                pygame.mixer.music.pause()
                self.isPaused = True
            else:
                pygame.mixer.music.unpause()
                self.isPaused = False
            

    instance = None
    def __init__(self):
        if not Music.instance:
            Music.instance = Music.__Music()

    def __getattr__(self, name):
        return getattr(self.instance, name)
