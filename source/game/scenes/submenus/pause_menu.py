from typing import Callable
from pygame import Surface
from pygame.event import Event
from pygame.freetype import Font
from source.api.ui.button import Button
from source.api.ui.button_style import ButtonStyle
from source.api.ui.text import Text

from source.api.ui.ui_element_base import UIElementBase
from data.constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from source.api.management.options_manager import OptionsManager


class PauseMenu:
    """
    A class to represent the pause menu.

    This class is used to create the pause menu. The pause menu is shown when the player pauses the game.

    Attributes:
        screen (Surface): The screen to draw the menu on.
        ui_elements (list): A list of UI elements.
        font (Font): The font of the text.
        button_style (ButtonStyle): The style of the buttons.

    Methods:
        __init__(self, screen: Surface, options_action: Callable, resume_action: Callable, main_menu_action: Callable)
        update(self, events: list[Event], background: Surface)
    """

    def __init__(self, screen: Surface, options_action: Callable, resume_action: Callable, main_menu_action: Callable) -> None:
        """
        Creates the pause menu.

        Arguments:
            screen (Surface): The screen to draw the menu on.
            options_action (Callable): The function to call when the options button is clicked.
            resume_action (Callable): The function to call when the resume button is clicked.
            main_menu_action (Callable): The function to call when the main menu button is clicked.
        """
        self.screen: Surface = screen

        self.ui_elements: list[UIElementBase] = []

        self.font = Font(DEFAULT_FONT, 75)
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        asf = OptionsManager().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pause",
                                     width=OptionsManager().resolution[0]*7/8, font=self.font))

        button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .3), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Resume", font_size=button_font_size, on_click=resume_action))

        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Options", font_size=button_font_size, on_click=options_action))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Menu", font_size=button_font_size, on_click=main_menu_action))

    def update(self, events: list[Event], background: Surface) -> None:
        """
        Updates the pause menu.

        Arguments:
            events (list): A list of pygame events.
            background (Surface): The background to draw on the screen.
        """
        self.screen.blit(background, (0, 0))
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()
