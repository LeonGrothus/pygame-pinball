from pathlib import Path
import sys
from pygame import Color, Surface, Vector2
import pygame
from api.management.scene import BaseDisplay
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button import Button
from api.utils import utils

from constants import PROJECT_PATH
from game.scenes.scoreboard_menu import Scoreboard
import copy


class MainMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.font = Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 100)
        scoreboard_font = Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 50)

        raw_button = pygame.image.load(PROJECT_PATH / Path("assets/buttons/default_left.png")).convert_alpha()
        self.button = utils.normalize_image_size(raw_button)

        self.title = "Pinball"

        raw_panel = pygame.image.load(PROJECT_PATH / Path("assets/panels/scoreboard.png")).convert_alpha()
        self.scoreboard = Scoreboard(Vector2(0, .3), Vector2(0, 0), scoreboard_font, 1, utils.normalize_image_size(raw_panel) , screen)

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        self.play_button = Button(Vector2(1, .3), Vector2(1, 0), "Play", Color(255, 255, 255), self.font, .5, self.button, self.screen)
        self.options_button = Button(Vector2(1, .45), Vector2(1, 0), "Options", Color(255, 255, 255), self.font, .5, self.button, self.screen)
        self.quit_button = Button(Vector2(1, .60), Vector2(1, 0), "Quit", Color(255, 255, 255), self.font, .5, self.button, self.screen)
        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        if self.play_button.draw():
            self.scene_manager.change_scene("main_pinball")

        if self.options_button.draw():
            self.scene_manager.change_scene("options_menu")

        if self.quit_button.draw():
            pygame.quit()
            sys.exit()

        self.scoreboard.draw()

        text_rect = self.font.get_rect(self.title, size=self.font.size*2) # type: ignore
        self.font.render_to(self.screen, ((self.screen.get_width()-text_rect.width) / 2, 50), self.title, Color(255, 255, 255), size=self.font.size*2)  # type: ignore

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return super().update(delta_time, events)
