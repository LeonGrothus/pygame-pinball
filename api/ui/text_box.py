import time
from pygame import Surface
import pygame
from api.ui.ui_element_base import UIElementBase


class TextBox(UIElementBase):
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
        """
        super().__init__(screen, rel_pos, width, height, rel_pos_self)

        self.selected = False
        self.show_cursor = False
        self.cursor_timer = 0
        self.cursor_pos = 0

        self.text = kwargs.get("text", "")

        self.inactive_image = kwargs.get("inactive_image", None)
        self.active_image = kwargs.get("active_image", None)

        self.on_submit = kwargs.get("on_submit", lambda *args: None)
        self.on_submit_args = kwargs.get("on_submit_args", [])

        self.placeholder = kwargs.get("placeholder", "")
        self.placeholder_color = kwargs.get("placeholder_color", (255, 255, 255))
        self.text_color = kwargs.get("text_color", (255, 255, 255))
        self.font_size = kwargs.get("font_size", 50)
        self.font = kwargs.get("font", None)

    def select(self) -> None:
        """
        Selects the text box.
        """

        self.selected = True
        self.show_cursor = True
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

        if pygame.mouse.get_pressed()[0]:
            if self.contains(mouse_pos[0], mouse_pos[1]):
                self.select()
            else:
                if self.selected:
                    self.on_submit(*self.on_submit_args)
                self.deselect()

        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                if self.selected:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_LEFT:
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_pos += 1
                    elif event.key == pygame.K_RETURN:
                        self.on_submit(*self.on_submit_args)
                        self.deselect()
                    else:
                        self.text += event.unicode
                        self.cursor_pos += 1

        return super().update_events(pygame_events)
    
    def draw(self) -> None:
        """
        Draws the text box.
        """

        if self.selected:
            self.screen.blit(self.active_image, (self._x, self._y))
        else:
            self.screen.blit(self.inactive_image, (self._x, self._y))

        if self.text == "":
            self.font.render_to(self.screen, (self._x + 10, self._y + self._height / 2 - self.font_size / 2), self.placeholder, self.placeholder_color, size=self.font_size)
        else:
            self.font.render_to(self.screen, (self._x + 10, self._y + self._height / 2 - self.font_size / 2), self.text, self.text_color, size=self.font_size)

        if self.selected:
            if time.time() - self.cursor_timer > 0.5:
                self.show_cursor = not self.show_cursor
                self.cursor_timer = time.time()

            if self.show_cursor:
                cursor_x = self.font.get_rect(self.text[:self.cursor_pos], size=self.font_size).width + 10
                pygame.draw.rect(self.screen, (255, 255, 255), (self._x + cursor_x, self._y + self._height / 2 - self.font_size / 2, 2, self.font_size))