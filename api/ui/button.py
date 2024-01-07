from pygame import Color, Surface, Vector2
import pygame
from pygame.freetype import Font


class Rect():
    def __init__(self, top_left_pos: Vector2, scale: Vector2):
        self.top_left_pos = top_left_pos
        self.scale = scale

    def point_inside(self, point: Vector2) -> bool:
        return (self.top_left_pos.x <= point.x <= self.top_left_pos.x + self.scale.x) and \
            (self.top_left_pos.y <= point.y <= self.top_left_pos.y + self.scale.y)

    def get_center(self) -> Vector2:
        return Vector2(int(self.top_left_pos.x + self.scale.x / 2), int(self.top_left_pos.y + self.scale.y / 2))


class Button():
    def __init__(self, relative_pos: Vector2, relative_movement: Vector2, text: str, text_color: Color, font: Font, scale: float, button: Surface, surface: Surface) -> None:
        width = button.get_width()
        height = button.get_height()
        self.image = pygame.transform.scale(button, (int(width * scale), int(height * scale)))
        self.rect = Rect(Vector2((relative_pos.x * surface.get_width()) - (self.image.get_width() * relative_movement.x),
                                 (relative_pos.y * surface.get_height()) - (self.image.get_height() * relative_movement.y)),
                         Vector2(self.image.get_width(), self.image.get_height()))
        self.text = text
        self.text_color = text_color
        self.font = font
        self.surface = surface
        self.scale = scale

    def align_button(self, pos: Vector2) -> None:
        self.rect.top_left_pos = pos

    def draw(self) -> bool:
        clicked = False

        pos = Vector2(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0] and self.rect.point_inside(pos):  # if mouse is over the button
            clicked = True

        self.surface.blit(self.image, (self.rect.top_left_pos.x, self.rect.top_left_pos.y))

        text_rect = self.font.get_rect(self.text, size=self.font.size*self.scale) # type: ignore
        text_rect.y = int((self.image.get_height()-text_rect.height)/2 + self.rect.top_left_pos.y)
        text_rect.x = int(self.rect.top_left_pos.x + 50 * self.scale)
        self.font.render_to(self.surface, text_rect, self.text, self.text_color, size=self.font.size*self.scale)  # type: ignore

        return clicked
