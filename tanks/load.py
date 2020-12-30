import random
import pygame.sprite
import os
from tanks.sprites import BrickWall, Bush, ConcreteWall, Water


def __load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise Exception(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    return image


def __load_sprites(level, group: pygame.sprite.Group):
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == str(BrickWall.Id):
                BrickWall(col, row, group)
                BrickWall.image = __load_image("brick.png")
            if level[row][col] == str(Bush.Id):
                Bush(col, row, group)
                Bush.image = __load_image("bush.png")
            if level[row][col] == str(ConcreteWall.Id):
                ConcreteWall(col, row, group)
                ConcreteWall.image = __load_image("concrete.png")
            if level[row][col] == str(Water.Id):
                Water(col, row, group)
                Water.image = __load_image("water.png")
    return 1


def load_level(filename, group: pygame.sprite.Group):
    level = [list(line.rstrip('\n')) for line in open(f"levels/{filename}")]
    __load_sprites(level, group)
    return 1

