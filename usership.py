import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    #Ship management class

    def __init__(self,sw_game,scale_factor = 0.2):
        super().__init__()
        #Initialise ship and set start position
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.screen_rect = sw_game.screen.get_rect()
        self.scale_factor = scale_factor

        #Load ship image
        self.image = pygame.image.load(u"C:/Users/darkg/source/repos/space_wars2/space_wars2/RepublisSpaceship.bmp")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()* self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 50)

        self.x = float(self.rect.x)

        #Continuous movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Updates ships movement depending on key press
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blit1(self):
        #Draw ship
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #Center ship on the screen
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 50)
        self.x = float(self.rect.x)
