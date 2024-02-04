from pathlib import Path
import sys
from turtle import left
from webbrowser import BackgroundBrowser
from pygame import Surface
import pygame
from source.api.management.background_manager import BackgroundManager
from source.api.management.image_manager import ImageManager
from source.api.scene.scene import BaseDisplay
from pygame.event import Event
from source.api.ui.button import Button
from source.api.ui.button_style import ButtonStyle
from source.api.ui.panel import Panel, TextObject
from source.api.ui.text import Text
from source.api.ui.text_box import TextBox
from source.api.ui.ui_element_base import UIElementBase

from data.constants import DEFAULT_BUTTON_STYLE, PROJECT_PATH
from source.api.management.options_manager import OptionsManager


class MainMenu(BaseDisplay):
    """
    A class to represent the main menu. This class is used to create the main menu.

    Attributes:
        screen (Surface): The screen to draw the menu on.
        scene_manager (SceneManager): The scene manager.
        ui_elements (list): A list of UI elements.
        button_style (ButtonStyle): The style of the buttons.
        image_manager (ImageManager): The image manager.

    Methods:
        __init__(self, screen: Surface, scene_manager)
        awake(self)
        update(self, delta_time: float, events: list[Event])
        unload(self)
        new_game(self)
        load_save_game(self)
        save_user_name(self, user_name: str)
        load_scoreboard_entries(self)
        _quit(self)
    """
    def __init__(self, screen: Surface, scene_manager, background_manager: BackgroundManager) -> None:
        """
        Creates the main menu.

        Arguments:
            screen (Surface): The screen to draw the menu on.
            scene_manager (SceneManager): The scene manager.
        """
        
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)
        self.ui_elements: list[UIElementBase] = []

        super().__init__(screen, scene_manager, background_manager)

    def awake(self) -> None:
        """
        Creates the main menu.

        Returns:
            None
        """

        self.image_manager = ImageManager(PROJECT_PATH / Path("data/data.png"))

        asf = OptionsManager().asf
        user_name = OptionsManager().user_name

        button_width = int(285 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pinball",
                                     width=OptionsManager().resolution[0]*7/8))

        button_set = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .30), (1, 0), button_width, button_height,
                                inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                text="New Game", font_size=button_font_size, on_click=self.new_game))

        save_game = self.image_manager.load_json().get("save_game", None)
        resume_text = "Resume" if save_game else "No Safe"
        resume_action = lambda: self.load_save_game() if save_game else lambda: None
        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text=resume_text, font_size=button_font_size, on_click=resume_action))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text="Options", font_size=button_font_size, on_click=lambda: self.scene_manager.change_scene("options_menu")))

        self.ui_elements.append(Button(self.screen, (1, .75), (1, 0), button_width, button_height,
                                       inactive_button=button_set[0], hover_button=button_set[1], pressed_button=button_set[2],
                                       text="Quit", font_size=button_font_size, on_click=lambda: self._quit()))

        scoreboard_width = OptionsManager().resolution[0]/2
        scoreboard_height = OptionsManager().resolution[1]*.3+button_height
        scoreboard_style = self.button_style.create_button((scoreboard_width, scoreboard_height), left_sided=True)

        scoreboard_entries = [TextObject("Scoreboard", color=(244, 194, 63))] + self.load_scoreboard_entries()
        self.ui_elements.append(Panel(self.screen, (0, .3), (0, 0), scoreboard_width, scoreboard_height,
                                background=scoreboard_style, text_objects=scoreboard_entries, margin=25*asf))

        self.ui_elements.append(Text(self.screen, (.5, .995), (.5, 1), text="Credits: Leon Grothus, Hendik Süberkrüb, Leon Echsler",
                                     width=OptionsManager().resolution[0]*15/16))

        text_button_set = self.button_style.create_button_set(
            (scoreboard_width, button_height), 0.03, 2, left_sided=True)

        text = "" if user_name == "Player" else user_name
        self.ui_elements.append(TextBox(self.screen, (0, .75), (0, 0), scoreboard_width, button_height, placeholder="Username", 
                                        margin=20*asf, placeholder_color=(150, 150, 150), text=text,
                                        inactive_image=text_button_set[0], active_image=text_button_set[1],
                                        font_size=button_font_size, on_submit=lambda text: self.save_user_name(text)))

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Updates the main menu.

        Arguments:
            delta_time (float): The time since the last frame.
            events (list[Event]): The events that happened since the last frame.

        Returns:
            None
        """
        super().update(delta_time, events)
        
        for element in self.ui_elements:
            element.draw()
            element.update_events(events)

    def unload(self) -> None:
        """
        Unloads the main menu.

        Returns:
            None
        """

        self.ui_elements.clear()
        return super().unload()
    
    def new_game(self) -> None:
        """
        Starts a new game.

        Returns:
            None
        """

        data = self.image_manager.load_json()
        data["save_game"] = {}
        self.image_manager.save_json(data)
        self.scene_manager.change_scene("main_pinball")
    
    def load_save_game(self) -> None:
        """
        Loads the save game.

        Returns:
            None
        """

        self.scene_manager.change_scene("main_pinball").deserialize()
    
    def save_user_name(self, user_name: str) -> None:
        if user_name != "":
            OptionsManager().user_name = user_name
            OptionsManager().save()

    def load_scoreboard_entries(self) -> list[TextObject]:
        """
        Loads the scoreboard entries.

        Returns:
            list: A list of scoreboard entries.
        """
        data = self.image_manager.load_json()
        if data is None: # if there is no data, return an empty list
            return []
 
        entries = data.get('scoreboard', {}) # get the scoreboard entries
        entries = dict(sorted(entries.items(), key=lambda x:x[1], reverse=True)) # sort the entries by score
        text_objects = [] # create a list of text objects
        for i, entry in enumerate(entries, start=1): # iterate over the entries
            text = f"{i:02}: {entry}: {entries[entry]}" # create the text
            text_object = TextObject(text, font_size=None, color=(255, 255, 255)) # create the text object
            text_objects.append(text_object) # append the text object to the list

        return text_objects

    def _quit(self) -> None:
        """
        Quits the game.

        Returns:
            None
        """
        pygame.quit()
        sys.exit()
