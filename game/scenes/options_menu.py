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


class OptionsMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.button_style = ButtonStyle(PROJECT_PATH / Path("assets/buttons/default_style"))

        self.font = Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 100)
        self.title = "Options"

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        button_width = 250
        button_height = 125

        back_inactive_button = self.button_style.create_button((button_width, button_height), left_sided=True, bottom_sided=True)
        back_hover_button = self.button_style.create_button((button_width, button_height), left_sided=True, bottom_sided=True, gamma=.03)
        back_pressed_button = self.button_style.create_button((button_width, button_height), left_sided=True, bottom_sided=True, gamma=.06)

        apply_inactive_button = self.button_style.create_button((button_width, button_height), right_sided=True, bottom_sided=True)
        apply_hover_button = self.button_style.create_button((button_width, button_height), right_sided=True, bottom_sided=True, gamma=.03)
        apply_pressed_button = self.button_style.create_button((button_width, button_height), right_sided=True, bottom_sided=True, gamma=.06)

        self.back_button = Button(self.screen, (0, 1), (0, 1), button_width, button_height,
                                  inactive_button=back_inactive_button, hover_button=back_hover_button, pressed_button=back_pressed_button, 
                                  text="Back", font_size=50, on_click=lambda: self.scene_manager.change_scene("main_menu"))
        self.apply_button = Button(self.screen, (1, 1), (1, 1), button_width, button_height,
                            inactive_button=apply_inactive_button, hover_button=apply_hover_button, pressed_button=apply_pressed_button, 
                            text="Apply", font_size=50, on_click=lambda: self._apply_changes())

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        self.back_button.draw()
        self.back_button.update_events(events)

        self.apply_button.draw()
        self.apply_button.update_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return super().update(delta_time, events)


    def _apply_changes(self):
        pass