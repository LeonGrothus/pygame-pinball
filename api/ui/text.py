import math
from pathlib import Path
from time import sleep
from pygame import Surface
import pygame
from api.ui.ui_element_base import UIElementBase
from pygame.freetype import Font 

from constants import ASSETS_PATH, DEFAULT_FONT


class Text(UIElementBase):
    """
    A class to represent a text UI element.

    This class extends the UIElementBase class and adds functionality for displaying text.

    Attributes:
        text (str): The text to display.
        font (Font): The font to use for the text.
        font_size (int): The size of the font.
        color (Tuple[int, int, int]): The color of the text.
    """
    def __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], **kwargs):
        """
        Initializes a Text object with the given position, surface, and keyword arguments.

        Parameters:
            screen (Surface): The screen to draw the Text on.
            rel_pos (tuple): The position of the UI element relative to the size of the screen.
            rel_pos_self (tuple): The position of the UI element relative to its own size.
            **kwargs: Additional arguments to pass to the UIElementBase class.

            Keyword Arguments:
                text (str): The text to display.
                font (Font): The font to use for the text.
                font_size (int): The size of the font.
                color (Tuple[int, int, int]): The color of the text.
                width (int): The width of the text.
                height (int): The height of the text.
        """
        self.text = kwargs.get("text", "text")
        self.font: Font = kwargs.get("font", Font(DEFAULT_FONT, 75))
        self.color = kwargs.get("color", (255, 255, 255))

        # Font size
        if not "font_size" in kwargs and not "width" in kwargs and not "height" in kwargs:
            raise ValueError("Either font_size or width or height must be given.")

        self.font_size = kwargs.get("font_size", None)
        self.desired_width = kwargs.get("width", None)
        self.desired_height = kwargs.get("height", None)

        if self.font_size is None:
            self.font_size = self.calculate_font_size()

        rect = self.font.get_rect(self.text, size=self.font_size)
        super().__init__(screen, rel_pos, rect.width, rect.height, rel_pos_self)

        self.text_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.font.render_to(self.text_surface, (0, 0), self.text, fgcolor=self.color, size=self.font_size)
    
    def calculate_font_size(self):
        font_size = 1
        text_rect = self.font.get_rect(self.text, size=font_size)
        text_width, text_height = text_rect.size

        desired_width =  math.inf if self.desired_width is None else self.desired_width
        desired_height = math.inf if self.desired_height is None else self.desired_height

        while text_width < desired_width and text_height < desired_height:
            font_size += 1
            text_rect = self.font.get_rect(self.text, size=font_size)
            text_width, text_height = text_rect.size
        return font_size - 1

    def draw(self):
        """
        Draws the text on the surface.

        This method uses the font, text, and color attributes to render the text and then blits it onto the surface.
        """
        self.screen.blit(self.text_surface, (self._x, self._y))    
    
    def update_events(self, pygame_events) -> None:
        return super().update_events(pygame_events)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    text = Text(screen, (0.5, 0.5), (.5, .5), text="Test Text", width=400)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        text.draw()

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()