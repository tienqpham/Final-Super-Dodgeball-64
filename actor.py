import pygame
import constants

class Actor(pygame.sprite.Sprite):

    def __init__(self, img, x=0, y=0, rebound=0):
        super().__init__()
        self.rebound = rebound

        self.image = img
        
        self.image.set_colorkey(constants.TRANSPARENT_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_x = 0
        self.speed_y = 0

        self.left_bound = 0
        self.right_bound = constants.SCREEN_WIDTH
        self.top_bound = 0
        self.low_bound = constants.SCREEN_HEIGHT

        self.check_out_of_bounds()

    # increments directional speeds by given amounts
    # positive values accelerate down and right,
    # negative values accelerate up and left
    def accelerate(self, x, y):
        self.speed_x += x
        self.speed_y += y

    def set_speed_x(self, x):
        self.speed_x = x

    def set_speed_y(self, y):
        self.speed_y = y

    def set_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y

    def get_speed(self):
        return [self.speed_x, self.speed_y]

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def set_center(self, x, y):
        self.rect.x = x - (self.rect.size[0]/2)
        self.rect.y = y - (self.rect.size[1]/2)

    # returns an array containing coordinates of the center
    def get_center(self):
        return [ self.rect.x + (self.rect.size[0]/2),
                 self.rect.y + (self.rect.size[1]/2) ]

    # returns an array containing coordinates of upper-left corner
    def get_pos(self):
        return [self.rect.x, self.rect.y]

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def stop_y(self):
        self.speed_y = 0

    def stop_x(self):
        self.speed_x = 0

    def stop(self):
        self.stop_y()
        self.stop_x()

    def set_rebound(self, rebound):
        self.rebound = rebound

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.check_out_of_bounds()
        
    def check_out_of_bounds(self):
        # x
        # left edge
        if self.rect.x < self.left_bound:
            
            self.rect.x = self.left_bound

        # right edge
        if self.rect.x > self.right_bound - self.rect.size[0]:
            
            self.rect.x = self.right_bound - self.rect.size[0] - self.rebound

        # y
        # top edge
        if self.rect.y < self.top_bound:
            
            self.rect.y = self.top_bound

        # bottom edge
        if self.rect.y > self.low_bound - self.rect.size[1]:
            
            self.rect.y = self.low_bound - self.rect.size[1] - self.rebound
