from pathlib import Path
import sys
from turtle import left
from pygame import Color, Surface, Vector2
import pygame
from api.management.json_manager import JsonManager
from api.management.scene import BaseDisplay
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button import Button
from api.ui.button_style import ButtonStyle
from api.ui.panel import Panel, TextObject
from api.ui.text import Text
from api.ui.ui_element_base import UIElementBase

from constants import ASSETS_PATH, PROJECT_PATH
from options import Options


class MainMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.button_style = ButtonStyle(PROJECT_PATH / Path("assets/buttons/default_style"))

        self.font = Font(ASSETS_PATH / Path("fonts/Tektur-Regular.ttf"), 75)
        self.ui_elements: list[UIElementBase] = []

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        asf = Options().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pinball",
                                     width=Options().resolution[0]*7/8, font=self.font))

        button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .3), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Play", font_size=button_font_size, on_click=lambda: self.scene_manager.change_scene("main_pinball")))
        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Options", font_size=button_font_size, on_click=lambda: self.scene_manager.change_scene("options_menu")))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Quit", font_size=button_font_size, on_click=lambda: self._quit()))

        scoreboard_width = Options().resolution[0]/2
        scoreboard_height = Options().resolution[1]*.3+button_height
        scoreboard_style = self.button_style.create_button((scoreboard_width, scoreboard_height), left_sided=True)

        scoreboard_entries = [TextObject("Scoreboard", color=(244, 194, 63))] + self.load_scoreboard_entries()
        self.ui_elements.append(Panel(self.screen, (0, .3), (0, 0), scoreboard_width, scoreboard_height,
                                background=scoreboard_style, text_objects=scoreboard_entries, margin=25*asf))

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        for element in self.ui_elements:
            element.draw()
            element.update_events(events)

        return super().update(delta_time, events)

    def unload(self) -> None:
        self.ui_elements.clear()
        return super().unload()

    def load_scoreboard_entries(self):
        json_manager = JsonManager(PROJECT_PATH / Path("data.json"))
        data = json_manager.load_json()
        if data is None:
            return []

        entries = data.get('scoreboard', {})
        text_objects = []
        for i, entry in enumerate(entries, start=1):
            text = f"{i:02}: {entry}: {entries[entry]}"
            text_object = TextObject(text, font_size=None, color=(255, 255, 255))
            text_objects.append(text_object)

        return text_objects

    def _quit(self):
        pygame.quit()
        sys.exit()
