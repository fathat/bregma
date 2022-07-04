import pygame
#Brett's face is ugly!
#but not as ugly as Ian's!

class resman(object):
    """U-G-L-Y you aint got no alibi, you ugly, yeah yeah, you ugly!"""
    
    def __init__(self):
        self.resources = {}
        
    def get_image(self, resource_name):
        if not self.resources.has_key(resource_name):
            self.resources[resource_name] = pygame.image.load(resource_name)
                
        return self.resources[resource_name]
        
    def get_music(self, resource_name):
        if not self.resources.has_key(resource_name):
            self.resources[resource_name] = pygame.mixer.music.load(resource_name)
            
    def get_audio(self, resource_name):
        if not self.resources.has_key(resource_name):
            self.resources[resource_name] = pygame.mixer.Sound(resource_name)
            
        return self.resources[resource_name]
            
    def get_font(self, resource_name, size ):
        key = (resource_name, size )
        if not self.resources.has_key(key):
            self.resources[key] = pygame.font.Font(resource_name, size)
            
        return self.resources[key]
        
    def unload(self, resource_name):
        del self.resources[resource_name]


#utility functions
def convert_to_grayscale(surface):
    n = surface.convert()
    print n.get_bitsize()
    n.lock()
    
    for y in xrange(surface.get_height()):
        for x in xrange(surface.get_width()):
            r,g,b,a = surface.get_at((x,y))
            average = (r+g+b)/3
            n.set_at((x,y), (average, average, average, a))
    n.unlock()
    return n
