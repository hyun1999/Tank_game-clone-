import sys
import os.path
from math import ceil
import pygame
import tanks.grid as grid
from tanks.constants import SCREEN_SIZE, MAP_SIZE
from tanks.sprites import ConcreteWall, BrickWall, Bush, Water, Spike, Tank
from tanks.ui import TextButton, Label, GameLogo, ScreenMessage, font_medium, font_small
from tanks.input import mouse_keys_just_pressed
from random import randint

_current = None


def current_scene():
    return _current


def load_scene(scene):
    global _current
    if _current:
        _current.teardown()
    _current = scene


class Scene:
    def __init__(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()

    def update(self):
        self.all_sprites.update()

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def teardown(self):
        self.all_sprites.empty()


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        GameLogo(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4, self.all_sprites)
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2

        play_btn = TextButton(x, y, 'Играть', font_medium, self.all_sprites)
        help_btn = TextButton(x, y + 70, 'Помощь', font_medium, self.all_sprites)
        exit_btn = TextButton(x, y + 140, 'Выход', font_medium, self.all_sprites)

        play_btn.on_click = lambda b: load_scene(LevelSelectMenu())
        help_btn.on_click = lambda b: load_scene(HelpMenu())
        exit_btn.on_click = lambda b: sys.exit()


class HelpMenu(Scene):
    help_text = [
        'Для победы уничтожьте танк',
        'противника 3 раза',
        '',
        'Игрок 1',
        'Передвижение: WASD',
        'Огонь: Пробел',
        '',
        'Игрок 2',
        'Передвижение: Стрелки',
        'Огонь: Enter'
    ]

    def __init__(self):
        super().__init__()
        x, y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]

        Label(x, 50, 'Помощь', font_medium, self.all_sprites)
        for i in range(len(self.help_text)):
            Label(x, 150 + 40 * i, self.help_text[i], font_small, self.all_sprites)

        back_btn = TextButton(x, y - 40, 'Назад', font_small, self.all_sprites)
        back_btn.on_click = lambda b: load_scene(MainMenu())


class LevelSelectMenu(Scene):
    def __init__(self):
        super().__init__()
        self.levels = Level.get_available()
        self.current_page = 0
        self.level_buttons = []

        x = SCREEN_SIZE[0] // 4
        self.title = Label(x * 2, 50, 'Выбор уровня', font_medium, self.all_sprites)
        for i in range(12):
            btn = TextButton(x * 2, 100 + 45 * (i + 1), '', font_small, self.all_sprites)
            self.level_buttons.append(btn)
        y = SCREEN_SIZE[1] - 80
        self.btn_prev = TextButton(x, y, 'ПРЕД', font_small, self.all_sprites)
        self.page_label = Label(x * 2, y, '', font_medium, self.all_sprites)
        self.btn_next = TextButton(x * 3, y, 'СЛЕД', font_small, self.all_sprites)
        self.btn_back = TextButton(x * 2, y + 40, 'Назад', font_small, self.all_sprites)

        self.btn_prev.on_click = self.on_prev_btn
        self.btn_next.on_click = self.on_next_btn
        self.btn_back.on_click = lambda b: load_scene(MainMenu())
        for btn in self.level_buttons:
            btn.on_click = lambda b: load_scene(Level.load(b.raw_text + '.txt'))

        self.render_page()

    def render_page(self):
        i = self.current_page
        n = len(self.level_buttons)
        levels = self.levels[n * i:n * (i + 1)]
        self.page_label.text = f'{i + 1}/{ceil(len(self.levels) / n)}'
        for j in range(n):
            if j < len(levels):
                self.level_buttons[j].raw_text = levels[j]
                self.level_buttons[j].enabled = True
            else:
                self.level_buttons[j].enabled = False

    def on_prev_btn(self, btn):
        self.current_page = max(self.current_page - 1, 0)
        self.render_page()

    def on_next_btn(self, btn):
        self.current_page = min(self.current_page + 1, len(self.levels) // len(self.level_buttons))
        self.render_page()


class Level(Scene):
    score_to_win = 3

    def __init__(self, filename, score=None):
        super().__init__()
        self.filename = filename
        self.score = score if score else [0, 0]
        self.game_finished = False

        grid_x = MAP_SIZE[0] // 2 - 1
        self.tank1 = Tank(*grid.cell_to_screen(grid_x, MAP_SIZE[1] - 2), True, self.all_sprites)
        self.tank2 = Tank(*grid.cell_to_screen(grid_x, 0), False, self.all_sprites)

        self.start_message = ScreenMessage("Приготовится!", font_medium, 2, self.all_sprites)
        self.end_message = None

    def update(self):
        if self.start_message.alive():
            self.start_message.update()
            return
        if self.end_message:
            self.end_message.update()
            if not self.end_message.alive():
                if not self.game_finished:
                    load_scene(Level.load(self.filename, self.score))
                else:
                    load_scene(LevelSelectMenu())
            return
        super().update()

        finish_round = False
        if not self.tank1.alive():
            self.score[1] += 1
            finish_round = True
        if not self.tank2.alive():
            self.score[0] += 1
            finish_round = True

        if finish_round:
            if self.score == [self.score_to_win, self.score_to_win]:
                end_message_text = 'Ничья!'
                self.game_finished = True
            elif self.score[0] == self.score_to_win:
                end_message_text = 'Игрок 1 победил!'
                self.game_finished = True
            elif self.score[1] == self.score_to_win:
                end_message_text = 'Игрок 2 победил!'
                self.game_finished = True
            else:
                end_message_text = f'{self.score[0]} : {self.score[1]}'
            self.end_message = ScreenMessage(end_message_text, font_medium, 3, self.all_sprites)
            return

    def draw(self, surface):
        surface.fill((116, 116, 116))  # gray
        pygame.draw.rect(surface, 'black', grid.get_rect())
        super().draw(surface)

    @classmethod
    def load(cls, filename, score=None):
        level = cls(filename, score)
        level_map = [list(line.rstrip('\n')) for line in open(os.path.join('levels', filename))]
        for row in range(len(level_map)):
            for col in range(len(level_map[row])):
                if level_map[row][col] == BrickWall.char:
                    BrickWall(col, row, level.all_sprites)
                if level_map[row][col] == Bush.char:
                    Bush(col, row, level.all_sprites)
                if level_map[row][col] == ConcreteWall.char:
                    ConcreteWall(col, row, level.all_sprites)
                if level_map[row][col] == Water.char:
                    Water(col, row, level.all_sprites)
                if level_map[row][col] == Spike.char:
                    Spike(col, row, level.all_sprites)
        return level

    @staticmethod
    def get_available():
        def check(f):
            return os.path.isfile(os.path.join('levels', f)) and f.endswith('.txt')
        return list(map(lambda x: x[:-4], filter(check, os.listdir('levels'))))
