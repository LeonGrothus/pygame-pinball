from pathlib import Path
from pygame import Color, Surface, Vector2
import pygame
from api.management.scene import BaseDisplay
from pygame.event import Event
from api.ui.button import Button

from constants import PROJECT_PATH


class MainMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.font = pygame.font.Font(PROJECT_PATH / Path("assets/fonts/Tektur-Regular.ttf"), 32)  # type: ignore # Load the custom font
        self.button = pygame.image.load(PROJECT_PATH / Path("assets/buttons/default.png")).convert_alpha()
        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        self.play_button = Button(Vector2(50,50), "Play", Color(255,255,255), self.font, 0.05, self.button)
        return super().awake()
    
    def update(self, delta_time: float, events: list[Event]) -> None:
        if self.play_button.draw(self.screen):
            self.scene_manager.change_scene("main_pinball")
        return super().update(delta_time, events)
    