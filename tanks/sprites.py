import pygame
from tanks.constants import CELL_SIZE
from tanks.grid import cell_to_screen


class GridSprite(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(*cell_to_screen(grid_x, grid_y), CELL_SIZE, CELL_SIZE)


class ConcreteWall(GridSprite):
    pass


class BrickWall(GridSprite):
    pass


class Bush(GridSprite):
    pass


class Water(GridSprite):
    pass
