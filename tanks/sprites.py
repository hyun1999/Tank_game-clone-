import os.path
import pygame
from tanks.constants import PIXEL_RATIO
from tanks.grid import cell_to_screen, get_rect
from tanks.time import delta_time
from tanks.directions import *


def load_image(name):
    image = pygame.image.load(os.path.join('data', name))
    rect = image.get_rect()
    return pygame.transform.scale(image, (rect.w * PIXEL_RATIO, rect.h * PIXEL_RATIO))


class SpriteBase(pygame.sprite.Sprite):
    sheet = None

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class GridSprite(SpriteBase):
    char = None
    destroyable = False
    tank_obstacle = True
    shell_obstacle = True
    layer = 0

    def __init__(self, grid_x, grid_y, *groups):
        super().__init__(*cell_to_screen(grid_x, grid_y), *groups)


class ConcreteWall(GridSprite):
    sheet = load_image('concrete.png')
    char = '#'


class BrickWall(GridSprite):
    sheet = load_image('brick.png')
    char = '%'
    destroyable = True


class Bush(GridSprite):
    sheet = load_image('bush.png')
    char = '*'
    tank_obstacle = False
    shell_obstacle = False
    layer = 1


class Water(GridSprite):
    sheet = load_image('water.png')
    char = '~'
    shell_obstacle = False


class Shell(SpriteBase):
    sheet = load_image('shell.png')
    speed = 100

    def __init__(self, x, y, direction, *groups):
        rotate = 0
        self.vector_velocity = direction_to_vector(direction, self.speed)
        size = self.sheet.get_size()
        if direction == WEST:
            x -= size[0] * 1.5
            y -= size[1] / 2
            rotate = 90
        if direction == NORTH:
            x -= size[0] / 2
            y -= size[1]
        if direction == SOUTH:
            x -= size[0] / 2
            rotate = 180
        if direction == EAST:
            y -= size[1] / 2
            rotate = -90
        self.pos = pygame.Vector2(x, y)
        super().__init__(x, y, *groups)
        self.image = pygame.transform.rotate(self.image, rotate)

    def update(self):
        self.pos += self.vector_velocity * delta_time()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        field = get_rect()

        if self.pos.x > field.right or self.pos.x < field.left or self.pos.y > field.bottom or self.pos.y < field.top:
            self.kill()
            return

        for group in self.groups():
            for sprite in group:
                if sprite is not self:
                    if self.is_collided_with(sprite):
                        if isinstance(sprite, GridSprite):
                            if sprite.destroyable:
                                sprite.kill()
                                self.kill()
                            elif sprite.shell_obstacle:
                                self.kill()
                        elif isinstance(sprite, Shell):
                            self.kill()
                            sprite.kill()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
