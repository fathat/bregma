import random
from actor import Actor
from caption import Caption
from collision import CollisionType

class cat(Actor):
    def __init__(self, world, template, x, y, resources):
        Actor.__init__(self, 'cat', world, template, x, y)
        self.shape.collision_type = CollisionType.cat
        self.caption = None
        self.resources = resources
        self.font = self.resources.get_font('../images/pixel.ttf', 8)
        self.frame_count = 1337;
        self.death_color = (255, 0, 0)
        
    def update(self, dt):
        if random.randint(0,20) == 1:
            dir = random.randint(0,20)
            
            if dir == 1:
                Actor.set_vector_and_normalize(self, 40, 0)
            elif dir == 2:
                Actor.set_vector_and_normalize(self, -40, 0)
            elif dir == 3:
                Actor.set_vector_and_normalize(self, 0, 40)
            elif dir == 4:
                Actor.set_vector_and_normalize(self, 0, -40)
            else:
                Actor.set_vector_and_normalize(self, 0, 0)
            
        Actor.update(self, dt)
        
    def draw(self, target):
        if self.frame_count < 120:
            self.frame_count += 1
            surface = self.font.render('Meow!', False, (255,255,255))
            target.blit(surface, (self.x,self.y - 35))
            del surface
        else:
            if random.randint( 0, 1000) == 42:
                self.frame_count = 0
            
        Actor.draw(self, target)