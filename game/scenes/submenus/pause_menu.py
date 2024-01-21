from typing import Callable
from pygame import Surface
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button import Button
from api.ui.button_style import ButtonStyle
from api.ui.text import Text

from api.ui.ui_element_base import UIElementBase
from constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from options import Options


class PauseMenu:
    def __init__(self, screen: Surface, options_action: Callable, resume_action: Callable, main_menu_action: Callable) -> None:
        self.screen: Surface = screen

        self.ui_elements: list[UIElementBase] = []

        self.font = Font(DEFAULT_FONT, 75)
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        asf = Options().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pause",
                                     width=Options().resolution[0]*7/8, font=self.font))

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
        self.screen.blit(background, (0, 0))
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()
