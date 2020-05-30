import pygame

import constants

from art import *

class Timer():

    # PARAMETERS:
    # start_time:
    #   the time, in seconds, at which the clock starts
    # max_time:
    #   the upper limit of the clock time;
    #   not used when counting down from start_time to 0
    # count_by_update_cycle:
    #   TRUE: time is measured by the number of update cycles
    #   FALSE: time is measured using real time
    # count_down:
    #   TRUE: the timer will count down from start_time to 0
    #   FALSE: the timer will count up from start_time
    # start_immediately:
    #   TRUE: calls to update() will immediately affect
    #         the clock time
    #   FALSE: start() must be called before calls to
    #          update() will affect the clock time
    def __init__(self, rect, start_time, max_time = 999,
                 count_by_update_cycle=False,
                 count_down=True, start_immediately=False):

        self.count_by_update = count_by_update_cycle

        self.rect = rect
        self.left = self.rect.x
        self.right = self.left + self.rect.size[0]
        self.top = self.rect.y
        self.bottom = self.top + self.rect.size[1]

        if count_down:
            self.digits = len(str(start_time))
        else:
            self.digits = len(str(max_time))

        self.start_time = start_time
        self.max_time = max_time

        if count_by_update_cycle:
            self.current_time = 0
            self.last_check = 0
        else:
            self.current_time = pygame.time.get_ticks()
        
        self.clock_time = start_time
        
        self.count_down = count_down

        self.is_paused = not start_immediately

    # returns the time, in seconds, on the clock
    # PARAMETERS:
    # as_list:
    #   TRUE: returns time as a list of single-digit integers
    #   FALSE: returns time as a single integer
    def get_time(self, as_list = False):
        if not as_list:
            return self.clock_time
        else:
            timeString = str(self.clock_time)

            timeArr = []
        
            for digit in timeString:
                timeArr.append(int(digit))

            return timeArr

    # returns TRUE if the timer can no longer advance
    # returns FALSE if the timer can still advance
    def is_time_up(self):
        if self.count_down:
            return self.clock_time == 0
        else:
            return self.clock_time == self.max_time

    # resets current time on the clock to the start time
    def reset(self):
        self.clock_time = self.start_time

    # sets current time on the clock to the specified time
    def set_time(self, time):
        self.clock_time = time

    # sets the timer to start counting if either paused
    # or set not to start immediately;
    # functionally identical to unpause()
    def start(self):
        self.unpause()

    def pause(self):
        self.is_paused = True

    def unpause(self):
        self.is_paused = False

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def update(self):
        if not self.is_paused:
            if self.has_one_second_passed():
                if not self.count_down and self.clock_time < self.max_time:
                    self.clock_time += 1
                elif self.count_down and self.clock_time > 0:
                    self.clock_time -= 1

    def draw(self, screen):
        arr = self.get_time(True)

        imgs = []
        for num in arr:
            imgs.append(Art().get_digit(str(num)))

        width = imgs[0].get_rect().size[0]
        gap = 4

        for i in range(0, self.digits-len(imgs)):
            imgs.insert(0,Art().get_digit('0'))

        for i in range(0, len(imgs)):
            screen.blit(imgs[i], (self.left + (width+gap)*i,
                                  self.top))
        

    def has_one_second_passed(self):
        if self.count_by_update:
            self.current_time += 1
            if self.current_time >= self.last_check + 60:
                self.last_check = self.current_time
                return True
            else:
                return False
        else:
            if pygame.time.get_ticks() >= self.current_time + 1000:
                self.current_time = pygame.time.get_ticks()
                return True
            else:
                return False
