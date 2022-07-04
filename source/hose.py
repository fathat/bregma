import pygame
import math

class Hose(object):
    def __init__(self):
        self._node_distance = 10
        self.start_y = 300
        self.start_x = -1000
        self.points = [ (x, self.start_y) for x in range(self.start_x, 300, self._node_distance) ]
        
    def update(self, dt, pragma, mouse):
        mx, my = mouse
        
        mdx = mx - pragma.x
        mdy = my - pragma.y
        mdistance = math.sqrt( mdx**2 + mdy**2)
        mnx = (mdx/mdistance)*self._node_distance
        mny = (mdy/mdistance)*self._node_distance
        
        self.points[0] = (self.start_x, self.start_y)
        self.points[-1] = (pragma.x+mnx, pragma.center_y+mny)
        self.points[-2] = (pragma.x, pragma.center_y)
        #self.points[-3] = (pragma.x-mnx, pragma.center_y-mny)
        
        for i in xrange(1, len(self.points)-1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i+1]
            dx = x2 - x1
            dy = y2 - y1
            distance = math.sqrt(dx**2 + dy**2)
            if distance == 0: distance = .01
            nx, ny = dx/distance, dy/distance
            
            correction = -(self._node_distance - distance)
            new_distance = distance + correction
            self.points[i] = x1+nx*correction, y1+ny*correction
            
        
        
    def draw(self, screen):
        prev = self.points[0]
        
        for point in self.points[1:]:
            pygame.draw.aaline(screen, (240, 240, 240), prev, point, 1)
            #pygame.draw.circle(screen, (255, 0, 0), point, 1)
        
            prev = point
        
        
