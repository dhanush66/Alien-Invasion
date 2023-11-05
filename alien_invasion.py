import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Overall class to manage game assets and behavior"""

    def __init__(self):
        """ Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Wathc for keyboard and mouse events.
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    # Helper method
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
    
    def _check_keydown_events(self, event):
        """Respond to keypress"""
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        """Respond to keyup"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet =Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self):
        """Update postion of bullers and get rif of old bullets"""

        #Update the bullet positions.
        self.bullets.update()

        #Get rid of bullets that have disapperaed.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #Check for any bullets the have hit aliens.
        # if so, get rid of the bullet and tha alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        #create another fleet if all existing aliens destroyed
        if not self.aliens:
            #Destroy existion bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Crate the fleet of aliens."""
        #Create an alien and keep addign aliens until other's no room left
        #spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height)
        number_alien_y = available_space_y // (2* alien_height)

        for row_number in range(number_alien_y):
            for alien_number in range(number_aliens_x):
                #Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        new_alien =Alien(self)
        alien_width, alien_height = new_alien.rect.size
        new_alien.x = alien_width + 2 * alien_width * alien_number
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = alien_height + 2 * alien_height *row_number
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien ship collisions.

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for alines htting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's directions"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond  the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left
            self.stats.ships_left -=1

            #Get rid of any remaining buyllets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(1)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom fo the screen"""

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

if __name__=='__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()