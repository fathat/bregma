import pygame
import math
import random

class filmgrain(object):
    """U-G-L-Y you aint got no alibi, you ugly, yeah yeah, you ugly!"""
    
    def __init__(self, screen_width, screen_height, num_scratches, min_length, max_length):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_length = min_length
        self.max_length = max_length
        self.num_scratches = num_scratches
        self.color = (0,0,0,127)
        self.framecount = 0
        self.start_point = None
        
    def update(self, dt):
        if self.framecount < 3:
            self.framecount += 1
        else:
            self.framecount = 0
            self.start_point = None
            
            if random.randint(0,10) == 1:
                rot = random.random()*6.28
                len = random.randint(self.min_length, self.max_length)
                
                x1 = random.randint(0, self.screen_width)
                y1 = random.randint(0, self.screen_width)
                x2 = math.cos(rot) * len
                y2 = math.sin(rot) * len
                
                self.start_point = (x1, y1)
                self.end_point = (x1-x2, y1-y2)        
        
    def draw(self, screen):
        if self.start_point != None:
            pygame.draw.line(screen, self.color, self.start_point, self.end_point, 2)
        
