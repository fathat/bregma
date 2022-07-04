import random
from actor import Actor

class enemy(Actor):
    def __init__(self, world, template, health, x, y, resources):
        Actor.__init__(self, 'enemy', world, template, x, y)
        self.resources = resources
        self.font = self.resources.get_font('../images/pixel.ttf', 8)
        self.frame_count = 1337
        self.target = None
        self.death_color = (100, 100, 255)
        self.health = health
        
    def update(self, dt):
        Actor.set_vector_and_normalize(self, self.target.x-self.x, self.target.y-self.y)
        Actor.update(self, dt)
        
    def draw(self, target):
        if self.frame_count < 200:
            self.frame_count += 1
            surface = self.font.render('Kitty!', False, (255,255,255))
            target.blit(surface, (self.x-self.world.camera_y,self.y-self.world.camera_y - 50))
            del surface
        else:
            if random.randint( 0, 1000) == 42:
                self.frame_count = 0
            
        Actor.draw(self, target)
        
    def good_target(self):
        if self.target == None or self.target.dead == True:
            return False
        
        return True
    
    def set_target(self, target):
        self.target = target