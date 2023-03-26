import pygame.font
from pygame.sprite import Group
from usership import Ship

class Scoreboard:
    #Class to represent scoring information

    def __init__(self,sw_game):
        #Initialise scorekeeping attributes
        self.sw_game = sw_game
        self.screen = sw_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sw_game.settings
        self.stats = sw_game.stats

        #Font settings
        self.text_colour = (255,0,0)
        self.font = pygame.font.SysFont(None,48)
        #Prep score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #Turn score into image
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour,True)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        #Draw score on screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        #Turn the high score into an image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, True)

        #Center the high score at top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def check_high_score(self):
        #Check for new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        #Turn level into image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_colour,True)

        #Position level below score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        #Show how many ships left
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.sw_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
