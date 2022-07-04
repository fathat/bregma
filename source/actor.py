import math
import pygame
import pymunk as physics
from resman import resman
from collision import CollisionType

class ActorAnimation(object):
    
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    
    def __init__(self, page, width=None, height=None, fps=7):
        self.page = page
        self.grid_width = width if width else self.page.get_width()//3
        self.grid_height = height if height else self.page.get_height()//4
        self.row = 0
        self.frame = 0
        self.sequence = [0, 1, 2, 1]
        self.fps = fps
        self.frame_life = 1.0/self.fps
        
    def set_anim(self, number):
        self.row = number
    
    def update(self, dt):
        self.frame_life = max(self.frame_life-dt, 0)
        if self.frame_life == 0:
            self.frame_life = 1.0/self.fps
            self.frame = (self.frame + 1) % len(self.sequence) 
    
    def draw(self, target, x, y):
        target.blit(self.page,
                    (x-12, y-32),
                    (self.sequence[self.frame]*self.grid_width,
                     self.row*self.grid_height,
                     self.grid_width,
                     self.grid_height))

def force_for_velocity(vi, vf, dt, mass):
    fx = mass*((vf[0] - vi[0])/dt)
    fy = mass*((vf[1] - vi[1])/dt)
    return fx, fy
        
class Actor(object):
    
    def __init__(self, type, world, template, x, y):
        self.type = type
        self.world = world
        self.animation = template.create()
        self.x, self.y = x, y
        self.radius = self.animation.grid_width/3.0
        self.vx = 0
        self.vy = 0
        self.fx = 0
        self.fy = 0
        self.speed = template.speed
        self.dead = False
        self.lx = None
        self.ly = None
        self.color = (0, 255, 0)
        self.kill_timeout = 1
        self.health = template.health
        self.speed_multiplier = 1
        
        self._create_physics_object(template.mass)
        
    def _create_physics_object(self, mass):
        inertia = physics.moment_for_circle(mass, 0, self.radius, (0,0))
        self.body = physics.Body(mass, inertia)
        self.body.position = self.x, self.y
        self.shape = physics.Circle(self.body, self.radius, (0,0))
        self.shape.elasticity = 0.95
        self.shape.collision_type = 1
        self.shape.actor = self
        self.world.space.add(self.body, self.shape)
        
    def _read_from_physics(self):
        self.x = self.body.position.x
        self.y = self.body.position.y
    
    def take_hit(self, force):
        self.health -= force
        
    def kill(self):
        self.dead = True
        self.shape.collision_type = CollisionType.dead_actor
        self.kill_timeout = 3
        
    def remove(self):
        self.world.space.remove(self.body, self.shape)
    
    def set_force(self, vx, vy):
        self.fx = vx
        self.fy = vy
        
    def add_force(self, vx, vy):
        self.fx += vx
        self.fy += vy
        
    def distance_from(self, point):
        return math.sqrt(self.distance_squared(point))

    def distance_squared(self, point):
        return (self.x - point[0])**2 + (self.y - point[1])**2
    
    @property
    def center_x(self):
        return self.x
    
    @property
    def center_y(self):
        return self.y - 10
    
    def set_vector(self, vx, vy):
        self.vx = vx
        self.vy = vy
        
    def set_vector_and_normalize(self, x, y):
        len = math.sqrt( x**2 + y**2)
        
        if( len != 0 ):
            self.vx = x/len
            self.vy = y/len
        else:
            self.vx = 0
            self.vy = 0
        
    def set_look(self, lx, ly):
        self.lx = lx
        self.ly = ly
        
    
    def _find_proper_animation(self, vx, vy):
        if self.vx == 0 and self.vy == 0:
            return ActorAnimation.DOWN
        if self.vx > 0:
            return ActorAnimation.RIGHT
        elif self.vx < 0:
            return ActorAnimation.LEFT
        elif self.vy < 0:
            return ActorAnimation.UP
        elif self.vy > 0:
            return ActorAnimation.DOWN
        
        
    
    def _find_from_look(self, lx, ly):
        dx = lx - self.x
        dy = ly - self.y
        
        l = math.sqrt(dx ** 2 + dy ** 2)
        nx = dx / l
        ny = dy / l
        
        theta = (math.atan2(ny, nx) * 180) / math.pi
        index = int(((theta + 45) / 90) % 4)
        
        if index == 0:
            return ActorAnimation.RIGHT
        elif index == 1:
            return ActorAnimation.DOWN
        elif index == 2:
            return ActorAnimation.LEFT
        elif index == 3:
            return ActorAnimation.UP
    
    def check_for_collisions(self, dt, world):
        if world.check_for_collisions((self.x, self.y), self.radius, ignore=[self]):
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)
    
    def update(self, dt):
        if self.lx and self.ly:
            self.animation.set_anim(self._find_from_look(self.lx, self.ly))
        else:
            self.animation.set_anim(self._find_proper_animation(self.vx, self.vy))
        
        if abs(self.vx) > 0 or abs(self.vy) > 0:
            self.animation.update(dt)
        #self.x += self.vx * dt
        #self.y += self.vy * dt
        #self.x += self.fx * dt
        #self.y += self.fy * dt
        if not self.dead:
            #self.body.update_velocity((self.vx*self.speed*15*self.speed_multiplier, self.vy*self.speed*15*self.speed_multiplier), 0.75, dt)
            self.body.apply_impulse(force_for_velocity(self.body.velocity, (self.vx*self.speed*self.speed_multiplier, self.vy*self.speed*self.speed_multiplier), 1, self.body.mass))
            self.body.apply_impulse((self.fx, self.fy))
        self.fx = 0
        self.fy = 0
        
        if self.dead:
            self.kill_timeout -= dt
        
        self._read_from_physics()
    
    
    def draw_death(self, target):
        pygame.draw.circle(target, self.death_color, (int(self.center_x + .5), int(self.center_y + .5)), int(self.radius + .5), 0)
    
    def draw(self, target):
        #self.draw_debug(target)
        if self.dead:
            self.draw_death(target)
        self.animation.draw(target, self.x-self.world.camera_x, self.y-self.world.camera_y)
    