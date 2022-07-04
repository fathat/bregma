import pygame
import random
import pymunk as physics
import math
from pymunk import Vec2d
from actor import Actor, ActorAnimation
from hose import Hose
from particleman import ParticleMan
from enemy import enemy
from cat import cat
from collision import CollisionType
from scoreboard import scoreboard
from decoration import Decoration
from caption import Caption

class MonsterTemplate(object):
    def __init__(self, page, speed, mass, health):
        self.page = page
        self.speed = speed
        self.mass = mass
        self.health = health
    
    def create(self):
        """Makes a new monster"""
        fps = self.speed / 5 + random.random()
        return ActorAnimation(self.page, fps=fps)

class World(object):
    
    def __init__(self, resources, app):
        self.resources = resources
        self.shapes_to_remove = []
        self.actors_to_remove = []
        self.templates = []
        self.background = pygame.image.load('../images/level.bmp')
        #self.background.set_alpha(0)
        self._init_physics()
        self.alpha = 0
        self.pragma = Actor('pragma', self, MonsterTemplate(resources.get_image('../images/bregmommy_bw.png'), 80, 1.0, 5), 300, 300)
        self.pragma.shape.group = 1
        self.actors = [self.pragma]
        self.hose = Hose()
        self.particleman = ParticleMan(app, self)
        self.scoreboard = scoreboard(app.screen.get_width()-200, 0, resources)
        self.targets = []
        self.camera_x, self.camera_y = (0,0)
        self.quake_time = 0
        
        for cats in range(20):
            cats = cat(self,
                       MonsterTemplate(resources.get_image('../images/kid2_bw.png'), 20, 6.0, 10),
                       random.randint(0, 150),
                       random.randint(self.background.get_height()//2 - self.background.get_height()//8, self.background.get_height()//8 + self.background.get_height()//2), resources)
            self.actors.append(cats)
            self.targets.append(cats)
            
        self.bushes = []
        for bush in range(80):
            y1 = random.randint(30,self.background.get_height()//2-30)
            y2 = random.randint(self.background.get_height()//2+30, self.background.get_height()-30 )
            bush = Decoration(self,
                              resources.get_image('../images/azalea_bw.png'),
                              resources.get_image('../images/azalea.png'),
                              random.randint(188, 192),
                              random.choice([y1,y2]))
            bush.shape.collision_type = CollisionType.azalea
            self.actors.append(bush)
            self.bushes.append(bush)
            
        self.templates = [ MonsterTemplate(resources.get_image('../images/fatkins_bw.png'), 40, 1.0, 50),
                      MonsterTemplate(resources.get_image('../images/fatkins2_bw.png'), 20, 2.0, 40),
                      MonsterTemplate(resources.get_image('../images/baby.png'), 60, 0.15, 5)]
        
        self.cats_dead = False
        
    def _init_physics(self):
        physics.init_pymunk()
        self.space = physics.Space()
        self.space.resize_static_hash()
        self.space.resize_active_hash()
        
        static_body = physics.Body(physics.inf, physics.inf)
        static_lines = [physics.Segment(static_body, (0, 0), (0, self.background.get_height()), 0.0),
                        physics.Segment(static_body, (0, 0), (self.background.get_width(), 0), 0.0),
                        physics.Segment(static_body, (self.background.get_width(), 0), (self.background.get_width(), self.background.get_height()), 0.0),
                        physics.Segment(static_body, (0, self.background.get_height()), (self.background.get_width(), self.background.get_height()), 0.0)]  
        for line in static_lines:
            line.elasticity = 0.95
            line.collision_type = CollisionType.fence
        self.space.add_static(static_lines)
        
        #collision callback
        self.space.add_collisionpair_func(CollisionType.actor, CollisionType.particle, self.on_water_hit, self)
        self.space.add_collisionpair_func(CollisionType.dead_actor, CollisionType.fence, None, None)
        self.space.add_collisionpair_func(CollisionType.particle, CollisionType.fence, None, None)
        self.space.add_collisionpair_func(CollisionType.particle, CollisionType.azalea, self.on_water_azaleas, None)
        self.space.add_collisionpair_func(CollisionType.actor, CollisionType.cat, self.on_kid_hit_cat, None)
        
        #make sure actors pass through decorations
        self.space.add_collisionpair_func(CollisionType.actor, CollisionType.azalea, self.on_hit_azalea, None)

    def on_water_hit(self, shape_a, shape_b, contacts, normal_coefficient, data):
        a = shape_a.actor
        wp = shape_b.wp
        
        a.take_hit(wp.force)
        
        if a.health <= 0:
            self.actors_to_remove.append(shape_a)    
            self.scoreboard.add_score(1)
            
        self.shapes_to_remove.append(shape_b)
        
        return True
    
    def on_water_azaleas(self, shape_a, shape_b, contacts, normal_coefficeint, data):
        shape_b.actor.on_hit()
        if shape_a.wp.force > 7:
            shape_a.wp.force -= 1/60
            return False
        return True
    
    def on_hit_azalea(self, shape_a, shape_b, contacts, normal_coefficeint, data):
        if shape_a.actor == self.pragma: return False
        shape_a.actor.speed_multiplier = .25
        return False
    
    def are_azaleas_live(self):
        count = 0
        max_count = len(self.bushes)
        for x in self.bushes:
            if x.broken:
                count += 1
        return (count / float(max_count)) > .333
        
    
    def spawn_wave(self, size):
        resources = self.resources
        self.quake_time = 1.5
        self.scoreboard.multiplier *= 2
        health_scale = size % 50
       
        for i in xrange(size):
            template = random.choice(self.templates)
            
            health = template.health + health_scale
            
            actor = enemy(self,
                          template,
                          health,
                          random.randint(self.background.get_width()-10, self.background.get_width()),
                          random.randint(0+200, self.background.get_height()-200),
                          resources)
            #actor.set_speed(-template.speed+random.randint(1, 5))
            self.actors.append(actor)
    
    def kill_actors(self):
        for x in set(self.shapes_to_remove): self.particleman.remove(x.wp)
        self.shapes_to_remove = []
        
        #Make actors stop moving
        for x in set(self.actors_to_remove):
            x.actor.kill()
            
        self.actors_to_remove = []
        
    def on_kid_hit_cat(self, shape_a, shape_b, contacts, normal_coefficeint, data):
        if shape_a.actor.type == 'enemy':
            shape_b.actor.take_hit(5)
            shape_a.actor.health = 0
            self.actors_to_remove.append(shape_a)    
            if shape_b.actor.health < 1:
                self.actors_to_remove.append(shape_b)
                self.targets.remove(shape_b.actor)
            
            
        return True
        
    def check_for_collisions(self, point, radius, ignore=[]):
        for actor in self.actors:
            if actor in ignore: continue
            d = actor.distance_from(point)
            if actor.distance_from(point) < actor.radius + radius:
                return actor
        return None
    
    def update(self, dt):
        #self.alpha += dt/2.0
        #self.background.set_alpha( int(self.alpha * 255) )
        #self.alpha = min(1, self.alpha)
        actors = self.actors
        self.actors = []
        for actor in actors:
            if actor.type == 'enemy':
                if actor.good_target() != True:
                    if len(self.targets) != 0:
                        actor.set_target(self.targets[random.randint(0, len(self.targets)-1)])
                    else:
                        self.cats_dead = True
                    
            actor.update(dt)
                
            if actor.kill_timeout > 0:
                self.actors.append(actor)
            else:
                actor.remove()
        
        #update physics
      
        self.space.step(dt)
        self.kill_actors()
        
        self.hose.update(dt, self.pragma, pygame.mouse.get_pos())
        self.particleman.update(dt)
        self.quake_time -= dt
        self.quake_time = max(self.quake_time, 0)
        self.camera_y = math.sin(self.quake_time*60) * 4

    def draw(self, target):
        target.blit(self.background, (-self.camera_x, -self.camera_y ))
        self.hose.draw(target)
        self.actors.sort(cmp=lambda a,b:int(a.y-b.y) )
        for actor in self.actors:
            actor.draw(target)
            
        self.particleman.draw(target)
    
    def draw_scoreboard(self, target):
        self.scoreboard.draw(target)