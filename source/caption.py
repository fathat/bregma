import pygame

class Caption(object):
    def __init__(self, text, font, x, y, anchor_x, anchor_y, fade_in_delay, life, fade_out_delay):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.alpha = 0
        self.state = 'ready'
        self.fade_in_rate = 1.0 / fade_in_delay
        self.fade_out_rate = 1.0 / fade_out_delay
        self.life = life
        self.surface = font.render(text, False, (255, 255, 255))
        self.surface.set_alpha(0)
    
    def is_done(self):
        return self.state == 'done'
    
    def start(self):
        self.state = 'fade_in'
    
    def set_alpha(self, alpha):
        self.surface.set_alpha(max(1, min(255, int(self.alpha*255))))
        #r, g, b, a = self.label.color
        #self.label.color = r, g, b, int(self.alpha*255)
    
    def on_update(self, dt):
        if self.state == 'fade_in':
            self.alpha += dt*self.fade_in_rate
            self.alpha = min(1, self.alpha)
            if self.alpha == 1:
                self.state = 'live'
        elif self.state == 'live':
            self.life -= dt
            if self.life <= 0:
                self.state = 'fade_out'
        elif self.state == 'fade_out':
            self.alpha -= dt*self.fade_out_rate
            self.alpha = max(0, self.alpha)
            if self.alpha == 0:
                self.state = 'done'
        self.set_alpha(self.alpha)
        
    def on_draw(self, target):
        target.blit(self.surface, (self.x-self.surface.get_width()//2, self.y-self.surface.get_height()//2))
        
class CaptionChain(object):
    def __init__(self, captions):
        self.captions = captions
        self.current_index = -1
    
    def finish(self):
        self.current_index = len(self.captions)
    
    def is_done(self):
        return self.current_index >= len(self.captions)
    
    def on_update(self, dt):
        if self.is_done(): return 
        if self.current_index == -1 or self.captions[self.current_index].is_done():
            self.current_index += 1
            if self.current_index >= len(self.captions):
                return
            self.captions[self.current_index].start()
        else:
            self.captions[self.current_index].on_update(dt)
    
    def on_draw(self, target):
        if self.is_done(): return
        self.captions[self.current_index].on_draw(target)
    
    