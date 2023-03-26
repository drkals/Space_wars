class GameStats:
    #Class to track stats

    def __init__(self, sw_game):
        self.settings = sw_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        #Initialise stats that are modifiable
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1