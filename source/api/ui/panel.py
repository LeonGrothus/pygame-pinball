from pygame import Surface
import pygame
from pygame.freetype import Font
from source.api.ui.button_style import ButtonStyle
from source.api.ui.ui_element_base import UIElementBase
from data.constants import ASSETS_PATH, DEFAULT_BUTTON_STYLE, DEFAULT_FONT

class TextObject:
    """
    This class should only be used as a parameter for the Panel class.

    Attributes:
        text (str): The text to display.
        color (Color): The color of the text.
        font_size (int): The size of the font.

    Methods:
        __init__(self, text: str, color: Color = (255, 255, 255), font_size: int = None)
    """
    def __init__(self, text, color=(255, 255, 255), font_size=None) -> None:
        """
        Creates a text object.

        Parameters:
            text (str): The text to display.
            color (Color): The color of the text.
            font_size (int): The size of the font.
        """
        self.text = text
        self.color = color
        self.font_size = font_size


class Panel(UIElementBase):
    """
    A class to represent a panel.

    This class is used to create panels. A panel is a UI element that can display text.

    Attributes:
        panel_style (ButtonStyle): The style of the panel.
        background (Surface): The background of the panel.
        margin (int): The margin between the text objects and the panel.
        text_objects (list[TextObject]): The text objects to display on the panel.
        font (Font): The font to use for the text objects.
        text_surfaces (list[Surface]): The precomputed text surfaces.

    Methods:
        __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs)
        add_text_object(self, text_object: TextObject)
        _scale_and_precompute_text(self, text_object: TextObject)
        draw(self)
        update_events(self, pygame_events)
    """

    def __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs):
        """
        Creates a panel.

        Parameters:
            screen (Surface): The screen to draw the panel on.
            rel_pos (tuple): The position of the UI element relative to the size of the screen.
            rel_pos_self (tuple): The position of the UI element relative to its own size.
            width (int): The width of the panel.
            height (int): The height of the panel.
            **kwargs: Additional arguments to pass to the UIElementBase class.

            Keyword Arguments:
                panel_style (ButtonStyle): The style of the panel.
                background (Surface): The background of the panel.
                margin (int): The margin between the text objects and the panel.
                text_objects (list[TextObject]): The text objects to display on the panel.
                font (Font): The font to use for the text objects.
        """
        super().__init__(screen, rel_pos, width, height, rel_pos_self)

        self.panel_style: ButtonStyle = kwargs.get("panel_style", ButtonStyle(DEFAULT_BUTTON_STYLE))
        self.background: Surface = kwargs.get("background", self.panel_style.create_button((width, height)))
        self.margin: int = kwargs.get("margin", 50)
        self.text_objects: list[TextObject] = kwargs.get("text_objects", [])
        self.font: Font = kwargs.get("font", Font(DEFAULT_FONT, 75))
        
        # Precompute text surfaces
        self.text_surfaces: list[Surface] = []
        for text_object in self.text_objects:
            self._scale_and_precompute_text(text_object)


    def add_text_object(self, text_object: TextObject) -> None:
        """
        Adds a TextObject to the panel.

        Parameters:
            text_object (TextObject): The TextObject to add.
        """
        self.text_objects.append(text_object)
        self._scale_and_precompute_text(text_object)
    
    def _scale_and_precompute_text(self, text_object: TextObject) -> None:
        """
        Scales the text to fit the panel and precomputes the text surface.

        Parameters:
            text_object (TextObject): The TextObject to scale and precompute.
        """

        min_font_size = 1
        max_font_size = (self._width - self.margin * 2 - (10*len(text_object.text))) if text_object.font_size is None else text_object.font_size
        optimal_font_size = min_font_size

        # Binary search for the optimal font size
        while min_font_size <= max_font_size:
            mid_font_size = (min_font_size + max_font_size) // 2
            text_rect = self.font.get_rect(text_object.text, size=mid_font_size)

            if text_rect.width <= self._width - 2 * self.margin:
                min_font_size = mid_font_size + 1
                optimal_font_size = mid_font_size
            else:
                max_font_size = mid_font_size - 1

        text_object.font_size = optimal_font_size
        text_surface = self.font.render(text_object.text, text_object.color, size=text_object.font_size)
        self.text_surfaces.append(text_surface[0])


    def draw(self) -> None:
        """
        Draws the panel.
        """
        self.screen.blit(self.background, (self._x, self._y))

        y_offset = self.margin
        for text_surface in self.text_surfaces:
            if y_offset + text_surface.get_height() + self.margin > self._height:
                break  # Don't draw this text surface or any following ones
            self.screen.blit(text_surface, (self._x + self.margin, self._y + y_offset))
            y_offset += text_surface.get_height() + self.margin

            
    def update_events(self, pygame_events) -> None:
        """
        Updates the panel.

        Parameters:
            pygame_events (list): The list of pygame events.
        """
        pass

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    text_object = TextObject("Hello, world!", font_size=None, color=(255, 255, 255))
    panel = Panel(screen, (0.5, 0.5), (0.5, 0.5), 400, 400, text_objects=[text_object])

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        panel.draw()

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()