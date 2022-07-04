import pygame

class sndman(object):
    """U-G-L-Y you aint got no alibi, you ugly, yeah yeah, you ugly!"""
    
    def __init__(self, resource_manager, width, height):
        self.resources = resource_manager
        self.width = width;
        self.height = height
        pygame.mixer.init()
        
    def play(self, sound_name, sound_volume):
        channel = pygame.mixer.find_channel()
        
        if channel != None:
            asound = self.resources.get_audio(sound_name)
            channel.set_volume(sound_volume)
            asound.play()
        
    def play_pos(self, sound_name, x, y):
        channel = pygame.mixer.find_channel()
        
        if channel != None:
            left_vol = 1.0
            right_vol = 1.0
            screen_mid = self.width / 2
            
            if x > screen_mid:
                tmpX = self.width  - x
                ratio = tmpX / screen_mid
                
                left_vol *= ratio
            else:
                ratio = x / screen_mid
                
                right_vol *= ratio
            
            asound = self.resources.get_audio(sound_name)
            channel.set_volume(left_vol, right_vol)
            asound.play()
