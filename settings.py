import pygame


class Settings:
    #Class to store settings for game

    def __init__(self):

        #Initialisation of game settings
        self.screen_width = 1200
        self.screen_height = 800
        #Ship settings
        self.ship_limit = 3
        #Projectile settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 255)
        self.bullets_allowed = 3
        #Enemy settings
        self.fleet_drop_speed = 20

        #How quickly the game speeds up
        self.speedup_scale = 1.25
        #How quickly the bishop point value increases
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        #Initialise settings that are not static and can change
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.bishop_speed = 1.0
        self.fleet_direction = 1
        #Scoring
        self.bishop_points = 50

    def increase_speed(self):
        #Increase speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bishop_speed *= self.speedup_scale

        self.bishop_points = int(self.bishop_points * self.score_scale)
        print(self.bishop_points)


        