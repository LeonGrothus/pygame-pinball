from pygame import Vector2, Color
import pygame
from api.management.scene import Scene
from game.objects.ball import Ball
from game.objects.boundry import Boundry
from game.objects.flipper import Flipper

class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)
        
    def awake(self) -> None:
        self.add_gameobject(Ball(Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)))
        self.add_gameobject(Boundry())
        self.add_gameobject(Flipper(Vector2(self.screen.get_width() / 2 - 100, self.screen.get_height() - 50)))
        self.add_gameobject(Flipper(Vector2(self.screen.get_width() / 2 + 100, self.screen.get_height() - 50)))
        return super().awake()