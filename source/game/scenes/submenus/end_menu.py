import sys
from pygame import Surface
import pygame
from pygame.event import Event
from pygame.freetype import Font
from source.api.ui.button import Button
from source.api.ui.button_style import ButtonStyle
from source.api.ui.text import Text

from source.api.ui.ui_element_base import UIElementBase
from data.constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from source.api.management.options_manager import OptionsManager


class EndMenu:
    """
    A class to represent the end menu.

    This class is used to create the end menu. The end menu is shown when the player loses the game.

    Attributes:
        screen (Surface): The screen to draw the menu on.
        scene_manager (SceneManager): The scene manager.
        ui_elements (list): A list of UI elements.
        font (Font): The font of the text.
        button_style (ButtonStyle): The style of the buttons.

    Methods:
        __init__(self, screen: Surface, scene_manager, final_score: int)
        update(self, events: list[Event], background: Surface)
        _options(self)
        _main_menu(self)
        _quit(self)
    """
    def __init__(self, screen: Surface, scene_manager, final_score: int) -> None:
        """
        Creates the end menu.

        Arguments:
            screen (Surface): The screen to draw the menu on.
            scene_manager (SceneManager): The scene manager.
            final_score (int): The final score of the player.
        """
        self.screen: Surface = screen
        self.scene_manager = scene_manager

        self.ui_elements: list[UIElementBase] = []

        self.font = Font(DEFAULT_FONT, 75)
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        asf = OptionsManager().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Game Over",
                                     width=OptionsManager().resolution[0]*7/8, font=self.font))
        self.ui_elements.append(Text(self.screen, (.5, .15), (.5, 0), text=f"Final Score: {final_score}",
                                     width=OptionsManager().resolution[0]*7/8, font=self.font))
        
        button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .3), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Menu", font_size=button_font_size, on_click=self._main_menu))

        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Options", font_size=button_font_size, on_click=self._options))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Quit", font_size=button_font_size, on_click=self._quit))

    def update(self, events: list[Event], background: Surface) -> None:
        """
        Updates the end menu.

        Arguments:
            events (list): A list of pygame events occurred in the last frame.
            background (Surface): The background of the menu.
        """
        self.screen.blit(background, (0, 0))
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()

    def _options(self) -> None:
        """
        Changes the scene to the options menu.

        Returns:
            None
        """
        self.scene_manager.change_scene("options_menu")

    def _main_menu(self) -> None:
        """
        Changes the scene to the main menu.

        Returns:
            None
        """
        self.scene_manager.change_scene("main_menu")

    def _quit(self) -> None:
        """
        Quits the game.

        Returns:
            None
        """
        pygame.quit()
        sys.exit()
