import math
from pygame import Surface
import pygame
from source.api.ui.ui_element_base import UIElementBase
from pygame.freetype import Font
from source.api.utils.event_value import EventValue

from data.constants import DEFAULT_FONT


class Text(UIElementBase):
    """
    A class to represent a text UI element.

    This class extends the UIElementBase class and adds functionality for displaying text.

    Attributes:
        text (str): The text to display.
        font (Font): The font to use for the text.
        font_size (int): The size of the font.
        color (Tuple[int, int, int]): The color of the text.

    Methods:
        __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], **kwargs)
        update_text(self, text)
        calculate_font_size(self)
        draw(self)
        update_events(self, pygame_events)
    """

    def __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], **kwargs):
        """
        Initializes a Text object with the given position, surface, and keyword arguments.

        Arguments:
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
        self.text: EventValue[str] = EventValue(kwargs.get("text", "text"))
        self.text.subscribe(self.update_text)

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

        rect = self.font.get_rect(self.text.value, size=self.font_size)
        super().__init__(screen, rel_pos, rect.width, rect.height, rel_pos_self)

        self.text_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA) # Create a surface for the text
        self.font.render_to(self.text_surface, (0, 0), self.text.value, fgcolor=self.color, size=self.font_size) # Render the text onto the surface

    def update_text(self, text) -> None:
        """
        Updates the text surface. Should be called whenever the text changes.

        Arguments:
            text (str): The new text to display.

        Returns:
            None
        """
        rect = self.font.get_rect(text, size=self.font_size)  # Get the size of the text
        self._width = rect.width
        self._height = rect.height
        # Create a new surface with the new size
        self.text_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.font.render_to(self.text_surface, (0, 0), text, fgcolor=self.color,
                            size=self.font_size)  # Render the text onto the surface

    def calculate_font_size(self) -> int:
        """
        Calculates the font size based on the desired width and height.

        Returns:
            int: The font size.
        """

        font_size = 1  # Start with a font size of 1
        text_rect = self.font.get_rect(self.text.value, size=font_size)  # Get the size of the text
        text_width, text_height = text_rect.size  # Get the width and height of the text

        # If the desired width is not given, set it to infinity
        desired_width = math.inf if self.desired_width is None else self.desired_width
        # If the desired height is not given, set it to infinity
        desired_height = math.inf if self.desired_height is None else self.desired_height

        while text_width < desired_width and text_height < desired_height:  # While the text is smaller than the desired size
            font_size += 1  # Increase the font size by 1
            text_rect = self.font.get_rect(self.text.value, size=font_size)  # Get the size of the text
            text_width, text_height = text_rect.size  # Get the width and height of the text
        return font_size - 1  # Return the font size minus 1

    def draw(self) -> None:
        """
        Draws the text on the surface.

        This method uses the font, text, and color attributes to render the text and then blits it onto the surface.

        Returns:
            None
        """
        self.screen.blit(self.text_surface, (self._x, self._y))

    def update_events(self, pygame_events) -> None:
        return super().update_events(pygame_events)

### Test Code ###


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
