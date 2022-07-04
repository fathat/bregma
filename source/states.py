import pygame
import pygame.mixer
import random
import math
from caption import Caption, CaptionChain
from world import World
from resman import resman
from actor import Actor, ActorAnimation

class State(object):
    def __init__(self):
        self.first_update = True

    
    def update(self, dt):
        if self.first_update:
            self.first_update = False
            self.on_start()
        self.on_update(dt)

class IntroState(State):
    def __init__(self, app):
        State.__init__(self)
        self.app = app
        self.done = False
        caption_args = (app.pixelfont, app.width // 2, app.height //2, 'center', 'center', 1.0, 1.5, 1.0)
        self.intro = CaptionChain([Caption('TEAM SPARKLE MOTION PRESENTS'.lower(), *caption_args),
                                   Caption('A Tragedy in Two Acts', *caption_args),
                                   Caption('"BREGMA"', app.titlefont, app.width//2, app.height//2, 'center', 'center', 2, 4.0, 2)])
        #app.resources.get_music('intro.mp3')
        
    
    def on_start(self):
        pass
        self.app.sounds.play_pos('../sounds/song.ogg', self.app.width//2, self.app.height//2)
        #pygame.mixer.music.load('song.ogg')
        #pygame.mixer.music.play(0)
    
    def on_update(self, dt):
        self.intro.on_update(dt)
        if self.intro.is_done(): self.done = True
        if self.app.is_key_down(pygame.K_SPACE): self.done=True
    
    def is_done(self):
        return self.done
    
    def draw(self, target):
        self.intro.on_draw(target)

class OutState(State):
    def __init__(self, app):
        State.__init__(self)
        self.app = app
        self.done = False
        self.intro = None
        
        
    def on_start(self):
        self.app.sounds.play_pos('../sounds/vocoded.wav', self.app.screen.get_width()//2, 300)
        #pygame.mixer.music.rewind()
        caption_args = (self.app.pixelfont, self.app.width // 2, self.app.height //2, 'center', 'center', 1.0, 2.5, 1.0)
        self.intro = CaptionChain([Caption('...as the children stomp your kittens to death...', *caption_args),
                                   Caption('...you call in vain to bregma...', *caption_args),
                                   Caption('...bregma...', *caption_args),
                                   Caption('NEW HIGH SCORE: ' + str(self.app.states['game'].world.scoreboard.score), *caption_args),
                                   Caption('(Thanks for playing!)', *caption_args),
                                   Caption('Coding: Ian Overgard, Brett Sawyer, Eoin Coffey', *caption_args),
                                   Caption('Artwork: Ian Overgard, Tanya Olszewski', *caption_args),
                                   Caption('Creepy Lady Voice: Eoin Coffey', *caption_args),
                                   Caption('Awesome porch: Brett Sawyer', *caption_args),
                                   Caption('(press esc to quit)', *caption_args)])
    
    def on_update(self, dt):
        if self.intro:
            self.intro.on_update(dt)
        if self.intro.is_done(): self.done = True
    
    def is_done(self):
        return self.done
    
    def draw(self, target):
        if self.intro:
            self.intro.on_draw(target)
        

class GameState(State):
    def __init__(self, app):
        State.__init__(self)
        self.spawn_delay = 50
        self.time_till_spawn = 5
        self.wave_size = 50
        self.live = False
        self.app = app
        self.world = World(app.resources, app)
        caption_args = (self.app.pixelfont, app.width // 2, app.height // 3, 'center', 'center', 0.5, 6.0, 0.5)
        self.caption = CaptionChain([Caption('Your precious cat Bregma has been taken...'.lower(), *caption_args),
                                     Caption('...the children are always after your cats...'.lower(), *caption_args),
                                     Caption('...but now you have a hose to keep the children away...'.lower(), *caption_args),
                                     Caption('...everything seems quiet right now..'.lower(), *caption_args),
                                     Caption('...too quiet...'.lower(), *caption_args),
                                     Caption('Perhaps you should water your azalea bushes...?', *caption_args)])
        self.play_caption = Caption('DEFEND YOUR CATS!!!!', *caption_args)
        self.level_caption =  Caption('LEVEL UP', *caption_args)
        self.done = False
        
    def on_start(self):
        #self.app.resources.get_music('song.mp3')
        #pygame.mixer.music.play(0, 0)
        #self.world.spawn_wave()
        pass

    def start_game(self):
        self.caption.finish()
        self.play_caption.start()
        self.live = True
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load('song2.mp3')
        #pygame.mixer.music.play(0, 0)
        
        #then bregma runs in
        
        # then the children come, and the screen quakes
    
    def is_done(self):
        return self.done
    
    def on_update(self, dt):
        mouse_down = pygame.mouse.get_pressed()[0]
        mx, my = pygame.mouse.get_pos()
        
        vx, vy = 0, 0
        if self.app.is_key_down(pygame.K_w):
            vy = -40
        if self.app.is_key_down(pygame.K_s):
            vy = 40
        if self.app.is_key_down(pygame.K_a):
            vx = -40
        if self.app.is_key_down(pygame.K_d):
            vx = 40
            
        self.world.pragma.set_vector_and_normalize(vx, vy)
        self.world.pragma.set_look(mx, my)
        
        if mouse_down:
            self.world.particleman.add((mx, my), self.world.pragma)
        self.caption.on_update(dt)
        self.world.update(dt)
        
        if self.world.are_azaleas_live():
            if not self.live:
                self.start_game()
            self.play_caption.on_update(dt)
            self.time_till_spawn -= dt
            if self.time_till_spawn <= 0:
                if self.play_caption.is_done():
                    self.play_caption = self.level_caption
                    self.play_caption.start()
                    
                self.spawn_delay *= 0.8
                self.spawn_delay = max(10, self.spawn_delay)
                self.time_till_spawn = self.spawn_delay
                self.world.spawn_wave(self.wave_size)
                self.wave_size *= 1.1
                for t in self.world.templates:
                    t.speed *= 1.1
        
        if self.world.cats_dead:
            self.done = True
    
    def draw(self, target):
        self.world.draw(target)
        if self.caption.is_done():
            self.play_caption.on_draw(target)
            self.world.draw_scoreboard(target)
        else:
            self.caption.on_draw(target)
        
        
        