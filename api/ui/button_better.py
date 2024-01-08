from pathlib import Path
from typing import Callable
from pygame import Color, Surface
import pygame
from api.ui.ui_element_base import UIElementBase
from constants import ASSETS_PATH
from pygame.freetype import Font


class Button(UIElementBase):
    def __init__(self, screen: Surface, rel_x: float, rel_y: float, **kwargs):
        """
        Creates a button.

        Parameters:
            screen (Surface): The screen to draw the button on.
            rel_x (float): The x-coordinate of the button relative to the size of the screen.
            rel_y (float): The y-coordinate of the button relative to the size of the screen.
            width (int): The width of the button.
            height (int): The height of the button.
            **kwargs: Additional arguments to pass to the UIElementBase class.
        """
        
        # Images
        # All button images must have the same size
        self.inactive_button: Surface = kwargs.get("inactive_button", pygame.image.load(ASSETS_PATH / Path("buttons/default_inactive.png")).convert_alpha())
        self.hover_button: Surface = kwargs.get("hover_button", pygame.image.load(ASSETS_PATH / Path("buttons/default_hover.png")).convert_alpha())
        self.pressed_button: Surface = kwargs.get("pressed_button", pygame.image.load(ASSETS_PATH / Path("buttons/default_pressed.png")).convert_alpha())
        self.image: Surface = self.inactive_button

        # Functions
        self.on_click: Callable = kwargs.get("on_click", lambda: None)

        # Text
        self.text_color: Color = kwargs.get("text_color", (255, 255, 255))
        self.font_size: int = kwargs.get("font_size", 50)
        self.text: str = kwargs.get("text", "")
        self.font: Font = kwargs.get("font", Font(ASSETS_PATH / Path("fonts/Tektur-Regular.ttf"), self.font_size))

        self.text_y_align: str = kwargs.get("text_y_align", "center")
        self.text_x_align: str = kwargs.get("text_x_align", "center")
        self.margin: int = kwargs.get("margin", 50)

        self.text_rect = self.font.get_rect(self.text, size=self.font_size)

        self.align_text()

        # Call the constructor of the base class
        super().__init__(screen, rel_x, rel_y, self.inactive_button.get_width(), self.inactive_button.get_height())

    def align_text(self):
        """
        Aligns the text of the button to the image.
        """

        self.text_rect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.text_x_align == 'left':
            self.text_rect.left = self._x + self.margin
        elif self.text_x_align == 'right':
            self.text_rect.right = self._x + self._width - self.margin

        if self.text_y_align == 'top':
            self.text_rect.top = self._y + self.margin
        elif self.text_y_align == 'bottom':
            self.text_rect.bottom = self._y + self._height - self.margin

    def update_events(self, pygame_events) -> None:
        """
        Updates the button.

        Parameters:
            pygame_events (list): A list of pygame events occurred in the last frame.
        """
        mouse_pos = pygame.mouse.get_pos()

        if self.contains(mouse_pos[0], mouse_pos[1]):
            if pygame.mouse.get_pressed()[0]:
                self.on_click()
                self.image = self.pressed_button
            else:
                self.image = self.hover_button
        else:
            self.image = self.inactive_button

    def draw(self) -> None:
        """
        Draws the button.
        """
        self.screen.blit(self.image, (self._x, self._y))
        self.font.render_to(self.screen, self.text_rect, self.text, self.text_color, size=self.font_size)

    def set_text(self, text: str) -> None:
        """
        Sets the text of the button.

        Parameters:
            text (str): The new text.
        """
        self.text = text
        self.text_rect = self.font.get_rect(self.text, size=self.font_size)
        self.align_text()

    def set_font_size(self, font_size: int) -> None:
        """
        Sets the font size of the button.

        Parameters:
            font_size (int): The new font size.
        """
        self.font_size = font_size
        self.text_rect = self.font.get_rect(self.text, size=self.font_size)
        self.align_text()
