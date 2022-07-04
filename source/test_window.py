import pygame
from resman import *
import hose

class Window(object):

    def __init__(self, *args, **kwargs):
        self.width  = 800
        self.height = 600
        self.clock = pygame.time.Clock()        
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.resources = resman()
        self.debugfont = self.resources.get_font('pixel.ttf', 8)

        self.hose = hose.Hose()
    
    def draw_text(self, text, x, y):
        surface = self.debugfont.render(text, False, (255,255,255))
        self.screen.blit(surface, (x,y))
        del surface
    
    def on_update(self, dt):
        
        #Update physics here -- dt is update rate in seconds
        
        x, y = pygame.mouse.get_pos()
        self.hose.update(dt, x, y)
        
        pass
    

    def on_draw(self):
        self.screen.fill((0,0,0))
        
        self.hose.draw(self.screen)
        pygame.draw.line(self.screen, (255, 0, 0), (200, 10), (300, 15))
        
        self.draw_text(str(int(self.clock.get_fps())), 0, 0)
        pygame.display.flip()
        
    def update(self):
        dt = self.clock.get_time()/1000.0
        if dt < 0 or dt > 1: dt = 0
        self.on_update(dt)
        self.on_draw()
        self.clock.tick(100)

def main():
    pygame.init()
    window = Window()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        window.update()
        
if __name__ == '__main__': main()