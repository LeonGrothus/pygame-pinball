from pygame import Surface
import pygame
from source.api.ui.button_style import ButtonStyle
from source.api.ui.ui_element_base import UIElementBase
from source.api.utils.event_value import EventValue
from data.constants import ASSETS_PATH, DEFAULT_BUTTON_STYLE
import source.api.utils.utils as utils

class Slider(UIElementBase):
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

        self.min = kwargs.get("min", 0)
        self.max = kwargs.get("max", 100)
        self.step = kwargs.get("step", 1)
        self.value =  EventValue(utils.clamp(kwargs.get("initial_value", 0), self.min, self.max))

        self.selected = False

        button_style: ButtonStyle = kwargs.get("button_style", ButtonStyle(DEFAULT_BUTTON_STYLE))
        self.blob_image = kwargs.get("handle_image", button_style.create_button((int(height*1.5), int(height*1.5))))
        self.handle_image = kwargs.get("handle_image", button_style.create_button((width, height)))


    def update_events(self, pygame_events) -> None:
        """
        Updates the slider.

        Parameters:
            pygame_events (list): The list of pygame events.
        """

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame_events:
            if self.contains(mouse_pos[0], mouse_pos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selected = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False

        if self.selected:
            unclamped = self.round((mouse_pos[0] - self._x) / self._width * (self.max - self.min) + self.min)
            self.value.set_value(max(min(unclamped, self.max), self.min))

        return super().update_events(pygame_events)

    def round(self, value):
        return self.step * round(value / self.step)

    def draw(self) -> None:
        """
        Draws the slider.
        """

        # Draw the handle
        self.screen.blit(self.handle_image, (self._x, self._y))
        # Draw the blob
        blob_width = self.blob_image.get_width()
        pos_x = self._x - blob_width/2 + (self._width) * utils.map_range(self.value.get_value(), self.min, self.max, 0, 1)
        pos_y = self._y + (self._height - self.blob_image.get_height()) / 2
        self.screen.blit(self.blob_image, (pos_x, pos_y))
        return super().draw()
    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    slider = Slider(screen, (0.5, 0.5), (0.5, 0.5), 400, 50, min=0, max=100, step=1, initial_value=50)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        slider.update_events(events)
        slider.draw()

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()