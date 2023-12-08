# modified from mangogame code

import pygame

class Block(pygame.sprite.Sprite):
    WALL = 0
    FREEZER = 1
    CHURRO = 2
    SAMPLE = 3

    def __init__(self, x=50, y=50, wall_type=0):
        super().__init__()

        filepath = "assets/images/"

        # Load the image
        if wall_type == self.WALL:
            self.image = pygame.image.load(filepath+"wall.png")
        elif wall_type == self.FREEZER:
            self.image = pygame.image.load(filepath+"freezer.png")
        elif wall_type == self.CHURRO:
            self.image = pygame.image.load(filepath+"churro.png")
        elif wall_type == self.SAMPLE:
            self.image = pygame.image.load(filepath+"sample.png")

        self.type = wall_type
        
        # Set the position to be the center of the image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        