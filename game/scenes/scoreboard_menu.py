import json
from pathlib import Path
import pygame
from pygame.math import Vector2
from pygame.freetype import Font
from pygame.surface import Surface

from api.management.json_manager import JsonManager
from constants import PROJECT_PATH


class Scoreboard:
    def __init__(self, relative_pos: Vector2, relative_movement: Vector2, font: Font, scale: float, panel: Surface, surface: Surface) -> None:
        self.relative_pos = relative_pos
        self.font = font
        self.scale = scale
        self.panel = pygame.transform.scale(panel, (int(panel.get_width() * scale), int(panel.get_height() * scale)))
        self.surface = surface
        self.rect = pygame.Rect((relative_pos.x * surface.get_width()) - (self.panel.get_width() * relative_movement.x),
                                (relative_pos.y * surface.get_height()) - (self.panel.get_height() * relative_movement.y),
                                self.panel.get_width(), self.panel.get_height())
        self.entries = self.load_entries()

    def load_entries(self):
        json_manager = JsonManager(PROJECT_PATH / Path("data.json"))
        data = json_manager.load_json()
        if data is None:
            return []
        return data.get('scoreboard', {})

    def draw(self):
        self.surface.blit(self.panel, self.rect)

        title = "Scoreboard"
        title_font_size = 50 * self.scale
        title_rect = self.font.get_rect(title, size=title_font_size)

        title_x = self.rect.left + (self.rect.width - title_rect.width) / 2
        self.font.render_to(self.surface, (title_x, self.rect.top + title_rect.height),
                            title, (244, 194, 63), size=title_font_size)  # type: ignore
        end_of_title = self.rect.top + title_rect.height * 2.5
        
        text_height = end_of_title
        for i, entry in enumerate(self.entries, start=1):
            new_font_size = self.font.size * self.scale  # type: ignore

            text = f"{i:02}: {entry}: {self.entries[entry]}"
            text_rect = self.font.get_rect(text, size=new_font_size)

            while text_rect.width > self.rect.width - 50 * self.scale:
                new_font_size -= 5
                text_rect = self.font.get_rect(text, size=new_font_size)

            text_pos_x = self.rect.left + (self.rect.width - text_rect.width) / 2

            if(text_height + text_rect.height > self.rect.bottom):
                break

            self.font.render_to(self.surface, (text_pos_x, text_height), text, (255, 255, 255), size=new_font_size)  # type: ignore
            text_height += text_rect.height * 2
