import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #Class to manage fired projectiles
    def __init__(self, sw_game):
        #Create object at ship current position
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.color = self.settings.bullet_color

        #Create bullet at (0,0) and set to ship position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = sw_game.ship.rect.midtop

        #Store bullets position
        self.y = float(self.rect.y)

    def update(self):
        #Update bullet position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        #Draw bullet
        pygame.draw.rect(self.screen, self.color, self.rect)