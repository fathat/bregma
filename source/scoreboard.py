import pygame

class scoreboard:
    def __init__(self, x, y, resources):
        self.score = 0
        self.x = x
        self.y = y
        self.multiplier = 1
        self.resources = resources
        self.font = self.resources.get_font('../images/pixel.ttf', 16)
        
    def add_score(self, num):
        self.score += num * self.multiplier
        
    def draw(self, target):
        surface = self.font.render('Score:' + str(self.score), False, (255,255,255))
        target.blit(surface, (self.x,self.y))
        del surface
