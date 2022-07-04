import pygame
import pymunk as physics

class WaterParticle(object):
    def __init__(self, world, x, y, vx, vy):
        self.radius = 4
        
        self.max_force = 8
        
        self.force = self.max_force
        
        speed = 2000
        
        self.world = world
        
        self._mark_for_death = 0
        self.x, self.y = x, y
        self.vx = vx * speed
        self.vy = vy * speed
        self.shape = None
        self.body = None
        
        self.physics_object_created = False
        self._create_physics_object()
        
    def _create_physics_object(self):
        mass = self.force*100
        inertia = physics.moment_for_circle(mass, 0, self.radius, (0,0))
        self.body = physics.Body(mass, inertia)
        self.body.position = self.x, self.y
        self.shape = physics.Circle(self.body, self.radius, (0,0))
        self.shape.elasticity = 0
        self.shape.friction = 2
        self.shape.group = 1
        self.shape.collision_type = 2
        self.shape.wp = self
        self.world.space.add(self.body, self.shape)
        
    
    def mark_for_death(self):
        self._mark_for_death = .5
    
    def remove(self):
        self.world.space.remove(self.body, self.shape)
        
    def _read_from_physics(self):
        self.x = self.body.position.x
        self.y = self.body.position.y
        
    def update(self, dt):
        def force_for_velocity(vi, vf, dt, mass):
            fx = mass*((vf[0] - vi[0])/dt)
            fy = mass*((vf[1] - vi[1])/dt)
            return fx, fy
        if not self.physics_object_created:
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.body.apply_impulse((self.vx*150, self.vy*150))
            #self.body.apply_impulse(force_for_velocity(self.body.velocity, (self.vx*self.speed, self.vy*self.speed), 1, self.body.mass))
            self.physics_object_created = True
            
        #self.radius += dt * 6
        
        self.force -= dt * (4.5 + self._mark_for_death)
        self.body.mass = self.force
        self.shape.radius += dt * 6
        
        #self.x += self.vx * dt
        #self.y += self.vy * dt
        
        #self.body.update_velocity((self.vx, self.vy), 1, dt)
        self._read_from_physics()
    
    #def draw(self, target):
    #    pygame.draw.circle(target, (255,0,0, 255), (int(self.x), int(self.y)), int(self.radius + .5), 1)
        
    
    def draw(self, target):
        x, y = int(self.x-self.world.camera_x), int(self.y-self.world.camera_y)
        alpha = int((self.force / self.max_force) * 255)
        pygame.draw.circle(target, (100,100,200, alpha), (x, y), int(self.shape.radius + .5))
