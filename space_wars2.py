import sys
from time import sleep

import pygame

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from settings import Settings
from usership import Ship
from bullet import Bullet
from bishops import Bishop                                                                                                                                                  


class SpaceWars:
    #Parent class that manages game assets and behaviour

    def __init__(self):
        #Game initialised and game resources created
        pygame.init()


        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Space Wars")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.bishops = pygame.sprite.Group()
        #Create instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self._create_fleet()
        #Make play button
        self.play_button = Button(self, "Start game")
        self.background_image = pygame.image.load(u"C:/Users/darkg/source/repos/space_wars2/space_wars2/Space_Background1.png")

    def exe_game(self):
        #Game loop defined
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_bishops()
            self._update_screen()

    def _check_events(self):
        #Check and respond to all keyboard or controller events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position) 
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)     
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        #Keydown events
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        #Keyup events
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    

    def _fire_bullet(self):
        #Creates a bullet and add to bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update bullet position and delete used bullets
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_bishop_collisions()

    def _check_bullet_bishop_collisions(self):
        #Respond to bullet-bishop collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.bishops, True, True)

        if collisions:
            for bishops in collisions.values():
                self.stats.score += self.settings.bishop_points * len(bishops)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.check_high_score()

        if not self.bishops:
            #Destroy existing enemies and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase lvl
            self.stats.level += 1
            self.sb.prep_level()
        
    def _update_screen(self):
        #Update all images on screen
        self.screen.blit(self.background_image, (0,0))
        self.ship.blit1()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.bishops.draw(self.screen)
        self.sb.show_score()
        #Draw play button
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _create_fleet(self):
        #Creates fleet of enemies
        bishop = Bishop(self)
        bishop_width,bishop_height = bishop.rect.size
        bishop_width = bishop.rect.width
        available_space_x = self.settings.screen_width - (2* bishop_width)
        number_bishops_x = available_space_x // (2* bishop_width)

        #Determine number of rows that enemies fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*bishop_height)- ship_height)
        number_rows = available_space_y // (2* bishop_height)

        for row_number in range(number_rows):
            for bishop_number in range(number_bishops_x):
                self._create_bishop(bishop_number, row_number)


    def _create_bishop(self, bishop_number, row_number):
        bishop = Bishop(self)
        bishop_width, bishop_height = bishop.rect.size
        bishop.x = bishop_width + 2 * bishop_width * bishop_number
        bishop.rect.x = bishop.x
        bishop.rect.y = bishop_height + 2 * bishop.rect.height * row_number
        self.bishops.add(bishop)

    def _update_bishops(self):
        #Update enemies positions
        self.bishops.update()
        self._check_fleet_edges()

        self._check_bishops_bottom

        #Look for bishop-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.bishops):
            self._ship_hit()
            print("Enemy bishop hit!")

    def _check_fleet_edges(self):
        #Respond if enemy has reached the edge
        for bishop in self.bishops.sprites():
            if bishop.check_edges():
                self._change_fleet_direction()
                break
                

    def _change_fleet_direction(self):
        for bishop in self.bishops.sprites():
            bishop.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #Respond to ship being hit by bishop
        #Remove 1 life from user
        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Delete remaining enemies and bullets
            self.bishops.empty()
            self.bullets.empty()
            #Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_bishops_bottom(self):
        #Check if any bishops have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for bishop in self.bishops.sprites():
            if bishop.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self,mouse_position):
        #Start the game when the user clicks the button
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.stats.game_active:
        
            #Reset game settings
            self.settings.initialise_dynamic_settings()
            #Reset game stats
            self.stats.reset_stats()
       
            self.stats.game_active = True
        
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #Delete remaining enemies
            self.bishops.empty()
            self.bullets.empty()

            #Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
   

if __name__ == '__main__':
    #Game runs
    sw = SpaceWars()
    sw.exe_game()
