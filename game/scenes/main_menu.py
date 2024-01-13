from pathlib import Path
import sys
from turtle import left
from pygame import Color, Surface, Vector2
import pygame
from api.management.scene import BaseDisplay
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button_better import Button
from api.ui.button_style import ButtonStyle
from api.utils import utils

from constants import PROJECT_PATH
from game.scenes.scoreboard_menu import Scoreboard
import copy


class MainMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.button_style = ButtonStyle(PROJECT_PATH / Path("assets/buttons/default_style"))

        self.font = Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 100)
        scoreboard_font = Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 50)

        self.title = "Pinball"

        raw_panel = pygame.image.load(PROJECT_PATH / Path("assets/panels/scoreboard.png")).convert_alpha()
        self.scoreboard = Scoreboard(Vector2(0, .3), Vector2(0, 0), scoreboard_font,
                                     1, utils.normalize_image_size(raw_panel), screen)

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        button_width = 250
        button_height = 125

        inactive_button = self.button_style.create_button((button_width, button_height), right_sided=True)
        hover_button = self.button_style.create_button((button_width, button_height), right_sided=True, gamma=.03)
        pressed_button = self.button_style.create_button((button_width, button_height), right_sided=True, gamma=.06)

        self.play_button = Button(self.screen, (1, .3), (1, 0), button_width, button_height,
                                  inactive_button=inactive_button, hover_button=hover_button, pressed_button=pressed_button, 
                                  text="Play", font_size=50, on_click=lambda: self.scene_manager.change_scene("main_pinball"))
        self.option_button = Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                            inactive_button=inactive_button, hover_button=hover_button, pressed_button=pressed_button, 
                            text="Options", font_size=50, on_click=lambda: self.scene_manager.change_scene("options_menu"))

        self.quit_button = Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                            inactive_button=inactive_button, hover_button=hover_button, pressed_button=pressed_button, 
                            text="Quit", font_size=50, on_click=lambda: self._quit())

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        self.play_button.draw()
        self.play_button.update_events(events)

        self.option_button.draw()
        self.option_button.update_events(events)

        self.quit_button.draw()
        self.quit_button.update_events(events)


        self.scoreboard.draw()

        text_rect = self.font.get_rect(self.title, size=self.font.size*2)  # type: ignore
        self.font.render_to(self.screen, ((self.screen.get_width()-text_rect.width) / 2, 50),
                            self.title, Color(255, 255, 255), size=self.font.size*2)  # type: ignore

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return super().update(delta_time, events)


    def _quit(self):
        pygame.quit()
        sys.exit()