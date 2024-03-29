import pygame
from tanks.grid import cell_to_screen, SCREEN_SIZE
from tanks.images import load_image

class GridSpriteBase(pygame.sprite.Sprite):
    """그리드에 위치한 스프라이트 기본 클래스는 상속에 사용됩니다."""
    sheet = None
    char = None
    destroyable = False
    tank_obstacle = True
    shell_obstacle = True
    die_obstacle = False
    speed_up = False
    b_speedup = False
    layer = 0

    def __init__(self, grid_x: int, grid_y: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = pygame.Rect(*cell_to_screen(grid_x, grid_y), *self.image.get_size())

class ConcreteWall(GridSpriteBase):
    sheet = load_image('concrete.png')
    char = '#'

class BrickWall(GridSpriteBase):
    sheet = load_image('brick.png')
    char = '%'
    destroyable = True

class Bush(GridSpriteBase):
    sheet = load_image('bush.png')
    char = '*'
    tank_obstacle = False
    shell_obstacle = False
    layer = 2

class Water(GridSpriteBase):
    sheet = load_image('water.png')
    char = '~'
    shell_obstacle = False

class Spike(GridSpriteBase):
    sheet = load_image('spike.png')
    char = 'x'
    shell_obstacle = False

class Mirror(GridSpriteBase):
    sheet = load_image('mirror.png')
    char = '+'
    
class Lava(GridSpriteBase):
    sheet = load_image('lava.png')
    char = '-'    
    shell_obstacle = False
    tank_obstacle = False
    die_obstacle = True

class Wood(GridSpriteBase):
    sheet = load_image('wood.png')
    char = '='    
    layer = 0
    tank_obstacle = False
    shell_obstacle = False

class Speedup(GridSpriteBase):
    sheet = load_image('speedup.png')
    char = 'h'    
    layer = 0
    tank_obstacle = False
    shell_obstacle = False
    speed_up = True

class shell_Speedup(GridSpriteBase):
    sheet = load_image('b_speedup.png')
    char = 'z'    
    layer = 0
    tank_obstacle = False
    shell_obstacle = False
    b_speedup = True
