import math
import random
from water_particle import WaterParticle

class ParticleMan(object):
    def __init__(self, app, world):
        self.particle_layer = app.screen.convert_alpha()
        self.particles = []
        
        self.world = world
        
    def add(self, mouse, pragma):
        mx, my = mouse
        
        mx += random.randint(-10, 10)
        my += random.randint(-10, 10)
        
        vx = (mx - pragma.x) 
        vy = (my - pragma.y)
        
        l = math.sqrt(vx ** 2 + vy ** 2)
            
        vx /= l
        vy /= l
        
        pragma.set_force(-vx * 10, -vy * 10)
            
        self.particles.append(
            WaterParticle(
                self.world,
                pragma.center_x,
                pragma.center_y,
                vx,
                vy)
            )
        
    def remove(self, particle):
        particle.remove()
        self.particles.remove(particle)
    
    def update(self, dt):
        particles = self.particles
        self.particles = []
        
        for wp in particles:
            wp.update(dt)
            
            if wp.force > 0:
                self.particles.append(wp)
            else:
                wp.remove()
                
    def draw(self, target):
        self.particle_layer.fill((0,0,0,0))
        
        for wp in self.particles:
            wp.draw(self.particle_layer)
            
        target.blit(self.particle_layer, (0,0))