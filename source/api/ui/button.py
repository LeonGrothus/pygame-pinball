from typing import Callable
from pygame import Color, Surface
import pygame
from source.api.ui.button_style import ButtonStyle
from source.api.ui.ui_element_base import UIElementBase
from data.constants import ASSETS_PATH, DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from pygame.freetype import Font


class Button(UIElementBase):
    """
    A class to represent a button.

    This class is used to create buttons. The button can be clicked and has a text.

    Attributes:
        inactive_button (Surface): The image of the button when it is inactive.
        hover_button (Surface): The image of the button when the mouse is hovering over it.
        pressed_button (Surface): The image of the button when it is pressed.
        on_click (Callable): The function to call when the button is clicked.
        text_color (Color): The color of the text.
        font_size (int): The size of the font.
        text (str): The text of the button.
        font (Font): The font of the text.
        text_y_align (str): The vertical alignment of the text.
        text_x_align (str): The horizontal alignment of the text.
        margin (int): The margin between the text and the edge of the button.
        
    Methods:
        __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs)
        update_events(self, pygame_events)
        draw(self)
        set_text(self, text: str)
        set_font_size(self, font_size: int)
    """

    def __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs):
        """
        Creates a button.

        Parameters:
            screen (Surface): The screen to draw the button on.
            rel_pos (tuple): The position of the UI element relative to the size of the screen.
            rel_pos_self (tuple): The position of the UI element relative to its own size.
            width (int): The width of the button.
            height (int): The height of the button.
            **kwargs: Additional arguments to pass to the UIElementBase class.

            Keyword Arguments:
                inactive_button (Surface): The image of the button when it is inactive.
                hover_button (Surface): The image of the button when the mouse is hovering over it.
                pressed_button (Surface): The image of the button when it is pressed.
                on_click (Callable): The function to call when the button is clicked.
                text_color (Color): The color of the text.
                font_size (int): The size of the font.
                text (str): The text of the button.
                font (Font): The font of the text.
                text_y_align (str): The vertical alignment of the text.
                text_x_align (str): The horizontal alignment of the text.
                margin (int): The margin between the text and the edge of the button.
        """
        super().__init__(screen, rel_pos, width, height, rel_pos_self)

        # Images
        # Either inactive_button, hover_button and pressed_button are given or button_style must be given
        button_style: ButtonStyle = kwargs.get("button_style", ButtonStyle(DEFAULT_BUTTON_STYLE))
        self.inactive_button: Surface = kwargs.get("inactive_button", button_style.create_button((width, height))) # type: ignore
        self.hover_button: Surface = kwargs.get("hover_button", button_style.create_button((width, height))) # type: ignore
        self.pressed_button: Surface = kwargs.get("pressed_button", button_style.create_button((width, height))) # type: ignore
        self.image: Surface = self.inactive_button

        # Functions
        self.on_click: Callable = kwargs.get("on_click", lambda: None)

        # Text
        self.text_color: Color = kwargs.get("text_color", (255, 255, 255))
        self.font_size: int = kwargs.get("font_size", 50)
        self.text: str = kwargs.get("text", "")
        self.font: Font = kwargs.get("font", Font(DEFAULT_FONT, 75))

        self.text_y_align: str = kwargs.get("text_y_align", "center")
        self.text_x_align: str = kwargs.get("text_x_align", "center")
        self.margin: int = kwargs.get("margin", 50)

        self.text_rect = self.font.get_rect(self.text, size=self.font_size)

        self.align_text()

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
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.image = self.pressed_button
                    self.on_click()
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
