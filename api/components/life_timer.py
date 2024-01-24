
from pathlib import Path
from pygame import Color, Vector2
import pygame
from api.components.component import Component
from api.components.mesh import Mesh
from api.objects.game_object import GameObject
from constants import ASSETS_PATH


class LifeTimer(Component):
    def __init__(self, colors: list[Color] = [], lives: int = 10, hit_sound = None):
        super().__init__()

        self.colors: list[Color] = colors
        self.lives = lives

        self.hit_sound: pygame.mixer.Sound = hit_sound # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bumper01.wav"))

    def on_init(self) -> None:
        self.mesh: Mesh = self.parent.get_component_by_class(Mesh) # type: ignore
        if not self.mesh:
            raise Exception("No mesh component found")
        if len(self.colors) < self.lives + 1:
            raise Exception("Not enough colors for the amount of lives")
        # default color is the self.lifes+1 color in the list
        self.mesh.color = self.colors[self.lives + 1]
        return super().on_init()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        if self.lives <= 0:
            self.parent.on_destroy()
        self.mesh.color = self.colors[self.lives]

        self.parent.sound_manager.play_sfx(self.hit_sound)
        self.lives -= 1
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        colors_tuples = [(color.r, color.g, color.b) for color in self.colors]
        return {
            "colors": colors_tuples,
            "lives": self.lives
        }
    
    def deserialize(self, data: dict) -> 'LifeTimer':
        self.colors = [Color(color[0], color[1], color[2]) for color in data["colors"]]
        self.lives = data["lives"]
        print(self.lives)
        return self