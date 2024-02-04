import time
from typing import Callable
from pygame import Color, Surface
import pygame
from source.api.ui.button_style import ButtonStyle
from source.api.ui.ui_element_base import UIElementBase
from pygame.freetype import Font
from data.constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT


class TextBox(UIElementBase):
    """
    A class to represent a text box.

    This class is used to create text boxes. A text box can be selected and has a text.

    Attributes:
        selected (bool): Whether the text box is selected.
        show_cursor (bool): Whether the cursor should be shown.
        cursor_timer (float): The timer for the cursor.
        cursor_pos (int): The position of the cursor.
        text (str): The text of the text box.
        inactive_image (Surface): The image of the text box when it is inactive.
        active_image (Surface): The image of the text box when it is active.
        on_submit (Callable): The function to call when the text box is submitted.
        placeholder (str): The placeholder text of the text box.
        placeholder_color (Color): The color of the placeholder text.
        text_color (Color): The color of the text.
        font_size (int): The size of the font.
        font (Font): The font of the text.
        margin (int): The margin between the text and the edge of the text box.
        
    Methods:
        __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs)
        select(self)
        deselect(self)
        update_events(self, pygame_events)
        draw(self)
    """

    def __init__(self, screen: Surface, rel_pos: tuple[float, float], rel_pos_self: tuple[float, float], width: int, height: int, **kwargs):
        """
        Creates a text box.

        Parameters:
            screen (Surface): The screen to draw the text box on.
            rel_x (float): The x-coordinate of the text box relative to the size of the screen.
            rel_y (float): The y-coordinate of the text box relative to the size of the screen.
            width (int): The width of the text box.
            height (int): The height of the text box.
            **kwargs: Additional arguments to pass to the UIElementBase class.

            Keyword Arguments:
                inactive_image (Surface): The image of the text box when it is inactive.
                active_image (Surface): The image of the text box when it is active.
                on_submit (Callable): The function to call when the text box is submitted.
                on_submit_args (list): The arguments to pass to the on_submit function.
                placeholder (str): The placeholder text of the text box.
                placeholder_color (Color): The color of the placeholder text.
                text_color (Color): The color of the text.
                font_size (int): The size of the font.
                font (Font): The font of the text.
                margin (int): The margin between the text and the edge of the text box.
        """
        super().__init__(screen, rel_pos, width, height, rel_pos_self)

        self.selected = False
        self.show_cursor = False
        self.cursor_timer = 0
        self.cursor_pos = 0

        self.text = kwargs.get("text", "")

        button = None # type: ignore
        if not "inactive_image" in kwargs and not "active_image" in kwargs:
            button_style: ButtonStyle = kwargs.get("button_style", ButtonStyle(DEFAULT_BUTTON_STYLE))
            button: Surface = button_style.create_button((width, height))
        self.inactive_image: Surface = kwargs.get("inactive_image", button)
        self.active_image: Surface = kwargs.get("active_image", button)

        self.on_submit: Callable = kwargs.get("on_submit", lambda text: None)

        self.placeholder: str = kwargs.get("placeholder", "")
        self.placeholder_color: Color = kwargs.get("placeholder_color", (255, 255, 255))
        self.text_color: Color = kwargs.get("text_color", (255, 255, 255))
        self.font_size: int = kwargs.get("font_size", 50)
        self.font: Font = kwargs.get("font", Font(DEFAULT_FONT, 75))

        self.margin: float = kwargs.get("margin", 10)

    def select(self) -> None:
        """
        Selects the text box.
        """

        self.selected = True
        self.show_cursor = True
        self.cursor_pos = len(self.text)
        self.cursor_timer = time.time()

    def deselect(self) -> None:
        """
        Deselects the text box.
        """

        self.selected = False
        self.show_cursor = False
        self.cursor_timer = time.time()

    def update_events(self, pygame_events) -> None:
        """
        Updates the text box.

        Parameters:
            pygame_events (list): The list of pygame events.
        """

        mouse_pos = pygame.mouse.get_pos()

        if self.selected:
            if time.time() - self.cursor_timer > 0.5:
                self.show_cursor = not self.show_cursor
                self.cursor_timer = time.time()

        for event in pygame_events: 
            if event.type == pygame.MOUSEBUTTONDOWN: # If the mouse is clicked
                if self.contains(mouse_pos[0], mouse_pos[1]): # If the mouse is inside the text box
                    self.select() # Select the text box
                else:
                    if self.selected: # If the text box is selected
                        self.on_submit(self.text) # Submit the text
                    self.deselect() # Deselect the text box

            if event.type == pygame.KEYDOWN: # If a key is pressed
                if self.selected:
                    if event.key == pygame.K_BACKSPACE: # If the backspace key is pressed
                        self.text = self.text[:-1] # Remove the last character
                        self.cursor_pos -= 1 # Move the cursor back 
                    elif event.key == pygame.K_LEFT: # If the left arrow key is pressed 
                        self.cursor_pos = max(0, self.cursor_pos - 1) # Move the cursor back
                    elif event.key == pygame.K_RIGHT: # If the right arrow key is pressed 
                        self.cursor_pos = min(len(self.text), self.cursor_pos + 1) # Move the cursor forward
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: # If the enter or escape key is pressed
                        self.on_submit(self.text) # Submit the text
                        self.deselect() # Deselect the text box 
                    else:
                        new_text = self.text + event.unicode # Add the pressed key to the text
                        text_width = self.font.get_rect(new_text).width # Get the width of the text 
                        if text_width < self._width - self.margin: # If the text fits inside the text box
                            self.text = new_text # Add the pressed key to the text
                            self.cursor_pos += 1 # Move the cursor forward
    
    def draw(self) -> None:
        """
        Draws the text box.
        """

        if self.selected:
            # Draw the active image
            self.screen.blit(self.active_image, (self._x, self._y))
        else:
            # Draw the inactive image
            self.screen.blit(self.inactive_image, (self._x, self._y))

        if self.text == "":
            # Draw the placeholder text
            self.font.render_to(self.screen, (self._x + 10, self._y + self._height / 2 - self.font_size / 2), self.placeholder, self.placeholder_color, size=self.font_size)
        else:
            # Draw the text
            self.font.render_to(self.screen, (self._x + 10, self._y + self._height / 2 - self.font_size / 2), self.text, self.text_color, size=self.font_size)

            if self.show_cursor: # If the cursor should be shown
                # Draw the cursor
                cursor_x = self.font.get_rect(self.text[:self.cursor_pos], size=self.font_size).width + 10
                pygame.draw.rect(self.screen, (255, 255, 255), (self._x + cursor_x, self._y + self._height / 2 - self.font_size / 2, 2, self.font_size))