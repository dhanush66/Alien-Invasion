import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bulleets fired from the ship"""

    def __init__(self, ai_game):
        """ Craate a bullet object at the ship's current postions."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet up the screen"""
        #Update the excat postion of the bullet
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


    def draw_bullet(self):
        """Draw the buller to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)