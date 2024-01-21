import sys
from typing import Callable
from pygame import Surface
import pygame
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button import Button
from api.ui.button_style import ButtonStyle
from api.ui.text import Text

from api.ui.ui_element_base import UIElementBase
from constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from options import Options


class EndMenu:
    def __init__(self, screen: Surface, scene_manager, final_score: int) -> None:
        self.screen: Surface = screen
        self.scene_manager = scene_manager

        self.ui_elements: list[UIElementBase] = []

        self.font = Font(DEFAULT_FONT, 75)
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        asf = Options().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Game Over",
                                     width=Options().resolution[0]*7/8, font=self.font))
        self.ui_elements.append(Text(self.screen, (.5, .15), (.5, 0), text=f"Final Score: {final_score}",
                                     width=Options().resolution[0]*7/8, font=self.font))
        
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
        self.screen.blit(background, (0, 0))
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()

    def _options(self) -> None:
        self.scene_manager.change_scene("options_menu")

    def _main_menu(self) -> None:
        self.scene_manager.change_scene("main_menu")

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()
