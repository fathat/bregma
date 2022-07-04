import pygame
import pymunk as physics
from collision import CollisionType

class Decoration(object):
    
    def __init__(self, world, image, broken_image, x, y):
        self.image = image
        self.world = world
        self.broken_image = broken_image
        self.x = x
        self.y = y
        self.type = 'decoration'
        self.kill_timeout = 1
        self.radius = self.image.get_width()//3
        self.broken = False
        self._create_physics_object(physics.inf)
        
    def _create_physics_object(self, mass):
        inertia = physics.moment_for_circle(mass, 0, self.radius, (0,0))
        self.body = physics.Body(mass, inertia)
        self.body.position = self.x, self.y
        self.shape = physics.Circle(self.body, self.radius, (0,0))
        self.shape.elasticity = 0.95
        self.shape.collision_type = CollisionType.decoration
        self.shape.actor = self
        self.world.space.add(self.body, self.shape)
        
    def _read_from_physics(self):
        self.x = self.body.position.x
        self.y = self.body.position.y
        
    def on_hit(self):
        self.broken = True
    
    def remove(self):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, target):
        x, y = self.x-self.world.camera_x, self.y - self.world.camera_y
        if not self.broken:
            target.blit(self.image, (x-self.image.get_width()//2, y-self.image.get_height()))
        else:
            target.blit(self.broken_image, (x-self.broken_image.get_width()//2, y-self.broken_image.get_height()))
            