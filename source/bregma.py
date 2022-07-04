import pygame
import pygame.font
import random
from caption import Caption, CaptionChain
from world import World
from resman import resman
from actor import Actor, ActorAnimation
from filmgrain import filmgrain
from states import GameState, IntroState, OutState
from sndman import sndman

fullscreen = False

class MainWindow(object):

    def __init__(self, *args, **kwargs):
        
        if fullscreen:
            self.width  = 0
            self.height = 0
            flags = pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE
        else:
            flags = 0
            self.width  = 1024
            self.height = 576
        
        self.screen = pygame.display.set_mode((self.width,self.height), flags )
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        
        self.key_down = {}
        for i in xrange(256): self.key_down[i] = False
        self.resources = resman()
        self.filmgrain = filmgrain(self.width, self.height, 10, 5, 20)
        self.sounds = sndman(self.resources, self.width, self.height)
        
        self.sounds.play_pos('../sounds/scifi002.wav', 0, 0)
        
        self.titlefont = self.resources.get_font('../images/pixel.ttf', 32)
        self.pixelfont = self.resources.get_font('../images/pixel.ttf', 16)
        self.debugfont = self.resources.get_font('../images/pixel.ttf', 8)
        self.states = {'intro': IntroState(self),
                       'game': GameState(self),
                       'out': OutState(self)}
        self.current_state = 'intro'
    
    def draw_text(self, text):
        surface = self.debugfont.render(text, False, (255,255,255))
        self.screen.blit(surface, (0,0))
        del surface
    
    @property
    def state(self):
        return self.states[self.current_state]
    
    def on_key_down(self, event):
        self.key_down[event.key] = True
    
    def on_key_up(self, event):
        self.key_down[event.key] = False
    
    def is_key_down(self, key):
        if self.key_down.has_key(key):
            return self.key_down[key]
        return False
    
    def on_update(self, dt):
        self.state.update(dt)
        if self.current_state == 'intro' and self.state.is_done():
            self.current_state = 'game'
            
        if self.current_state == 'game' and self.state.is_done():
            self.current_state = 'out'
            
        self.filmgrain.update(dt)
        
        mx, my = pygame.mouse.get_pos()

    def on_draw(self):
        self.screen.fill((0,0,0))
        self.state.draw(self.screen)
        #self.draw_text(str(int(self.clock.get_fps())))
        self.filmgrain.draw(self.screen)
        pygame.display.flip()
        
    def update(self):
        dt = self.clock.get_time()/1000.0
        if dt < 0 or dt > 1: dt = 0
        self.on_update(dt)
        self.on_draw()
        self.clock.tick(100)

app = None
def main():
    global app
    pygame.init()
    window = MainWindow()
    app = MainWindow()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.KEYDOWN:
                window.on_key_down(event)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return 0
                window.on_key_up(event)
                
        window.update()
        
        
if __name__ == '__main__': main()
