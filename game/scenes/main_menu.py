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
from api.ui.text_box import TextBox
from api.ui.ui_element_base import UIElementBase

from constants import DEFAULT_BUTTON_STYLE, PROJECT_PATH
from options import Options


class MainMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)
        self.ui_elements: list[UIElementBase] = []

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        self.json_manager = JsonManager(PROJECT_PATH / Path("data.json"))

        asf = Options().asf
        button_width = int(285 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pinball",
                                     width=Options().resolution[0]*7/8))

        button_set = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .30), (1, 0), button_width, button_height,
                                inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                text="New Game", font_size=button_font_size, on_click=self.new_game))

        save_game = self.json_manager.load_json().get("save_game", None)
        resume_text = "Resume" if save_game else "No Safe"
        resume_action = lambda: self.load_save_game(save_game) if save_game else lambda: None
        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text=resume_text, font_size=button_font_size, on_click=resume_action))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text="Options", font_size=button_font_size, on_click=lambda: self.scene_manager.change_scene("options_menu")))

        self.ui_elements.append(Button(self.screen, (1, .75), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text="Quit", font_size=button_font_size, on_click=lambda: self._quit()))

        scoreboard_width = Options().resolution[0]/2
        scoreboard_height = Options().resolution[1]*.3+button_height
        scoreboard_style = self.button_style.create_button((scoreboard_width, scoreboard_height), left_sided=True)

        scoreboard_entries = [TextObject("Scoreboard", color=(244, 194, 63))] + self.load_scoreboard_entries()
        self.ui_elements.append(Panel(self.screen, (0, .3), (0, 0), scoreboard_width, scoreboard_height,
                                background=scoreboard_style, text_objects=scoreboard_entries, margin=25*asf))

        self.ui_elements.append(Text(self.screen, (.5, .995), (.5, 1), text="Credits: Leon Grothus, Hendik Süberkrüb, Leon Echsler",
                                     width=Options().resolution[0]*15/16))

        text_button_set = self.button_style.create_button_set(
            (scoreboard_width, button_height), 0.03, 2, left_sided=True)

        username = Options().load_user_name()
        text = "" if username == "Player" else username
        self.ui_elements.append(TextBox(self.screen, (0, .75), (0, 0), scoreboard_width, button_height, placeholder="Username", 
                                        margin=20*asf, placeholder_color=(150, 150, 150), text=text,
                                        inactive_image=text_button_set[0], active_image=text_button_set[1],
                                        font_size=button_font_size, on_submit=lambda text: self.save_user_name(text)))

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        for element in self.ui_elements:
            element.draw()
            element.update_events(events)

        return super().update(delta_time, events)

    def unload(self) -> None:
        self.ui_elements.clear()
        return super().unload()
    
    def new_game(self) -> None:
        data = self.json_manager.load_json()
        if "save_game" in data:
            del data["save_game"]
            self.json_manager.save_json(data)
        self.scene_manager.change_scene("main_pinball")
    
    def load_save_game(self, save_game: dict) -> None:
        self.scene_manager.change_scene("main_pinball").deserialize(save_game)
    
    def save_user_name(self, username: str) -> None:
        if username == "":
            username = "Player"
        Options().store_user_name(username)

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
