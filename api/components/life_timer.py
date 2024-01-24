
from pathlib import Path
from pygame import Color, Vector2
import pygame
from api.components.component import Component
from api.components.mesh import Mesh
from api.objects.game_object import GameObject
from constants import ASSETS_PATH


class LifeTimer(Component):
    def __init__(self, colors: list[Color], lives: int = 10, hit_sound = None):
        super().__init__()

        self.colors = colors
        self.lives = lives

        self.hit_sound: pygame.mixer.Sound = hit_sound # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bumper01.wav"))

    def on_init(self) -> None:
        self.mesh: Mesh = self.parent.get_component_by_class(Mesh) # type: ignore
        if not self.mesh:
            raise Exception("No mesh component found")
        return super().on_init()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        self.lives -= 1
        if self.lives < 0:
            self.parent.on_destroy()
        self.mesh.color = self.colors[self.lives]

        self.parent.sound_manager.play_sfx(self.hit_sound)
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        return {
            "colors": self.colors,
            "lives": self.lives
        }
    
    def deserialize(self, data: dict) -> 'LifeTimer':
        self.colors = data["colors"]
        self.lives = data["lives"]
        return self