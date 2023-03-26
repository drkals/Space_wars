import pygame
from pygame.sprite import Sprite

class Bishop(Sprite):
    #Class for a  single bishop in holy fleet

    def __init__(self, sw_game,scale_factor = 0.13):
        #Initialise bishop and set starting position
        super().__init__()
        self.screen = sw_game.screen
        self.scale_factor = scale_factor
        self.settings = sw_game.settings

        #Load bishop image
        self.image = pygame.image.load(u"C:/Users/darkg/source/repos/space_wars2/space_wars2/Bishop.bmp")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()* self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect()

        #Each bishop to start in top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store horizontal position
        self.x = float(self.rect.x)


    def check_edges(self):
        #Return true if the enemy is at the edge of the screen (boundary)
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        #Move enemy to the right or left
        self.x += (self.settings.bishop_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    
