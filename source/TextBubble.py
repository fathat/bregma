import pygame

class TextBubble(object):
    
    def __init__(self, text, font):
        self.surface = self.debugfont.render(text, False, (255,255,255))
        
    def draw(self):
        pass
