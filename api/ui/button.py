from pygame import Color, Surface, Vector2
import pygame
from pygame.font import Font


class Rect():
    def __init__(self, top_left_pos: Vector2, scale: Vector2):
        self.top_left_pos = top_left_pos
        self.scale = scale

    def point_inside(self, point: Vector2) -> bool:
        return (self.top_left_pos.x <= point.x <= self.top_left_pos.x + self.scale.x) and \
            (self.top_left_pos.y <= point.y <= self.top_left_pos.y + self.scale.y)


class Button():
    def __init__(self, pos: Vector2, text: str, text_color: Color, font: Font, scale: float, button: Surface):
        width = button.get_width()
        height = button.get_height()
        self.image = pygame.transform.scale(button, (int(width * scale), int(height * scale)))
        self.rect = Rect(pos, Vector2(self.image.get_width(), self.image.get_height()))
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, surface: Surface) -> bool:
        clicked = False

        pos = Vector2(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0] and self.rect.point_inside(pos):  # if mouse is over the button
            clicked = True

        # draw button on screen
        surface.blit(self.image, (self.rect.top_left_pos.x, self.rect.top_left_pos.y))
        surface.blit(self.font.render(self.text, True, self.text_color), (self.rect.top_left_pos.x + 10, self.rect.top_left_pos.y + 10))
        return clicked