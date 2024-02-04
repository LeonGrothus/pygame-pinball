
from pathlib import Path
from pygame import Color, Vector2
import pygame
from source.api.components.component import Component
from source.api.components.mesh import Mesh
from source.api.objects.game_object import GameObject
from data.constants import ASSETS_PATH


class LifeTimer(Component):
    """
    A class to represent a LifeTimer. A LifeTimer is a visual representation of the amount of lives left.
    When the LifeTimer is hit, the color changes. When the LifeTimer has no lives left, the parent is destroyed.

    Attributes:
        colors: list[Color], the colors of the timer
        lives: int, the amount of lives
        hit_sound: pygame.mixer.Sound, the sound to play when the timer is hit

    Methods:
        __init__(self, colors: list[Color] = [], lives: int = 10, hit_sound = None)
        on_init(self)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'LifeTimer'
    """

    def __init__(self, colors: list[Color] = [], lives: int = 10, hit_sound = None):
        """
        Inits LifeTimer with colors and lives

        Arguments:
            colors: list[Color], the colors of the timer
            lives: int, the amount of lives
        """

        super().__init__()

        self.colors: list[Color] = colors
        self.lives = lives

        self.hit_sound: pygame.mixer.Sound = hit_sound # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bumper01.wav"))

    def on_init(self) -> None:
        """
        Gets the mesh of the parent

        Returns:
            None
        """

        self.mesh: Mesh = self.parent.get_component_by_class(Mesh) # type: ignore
        if not self.mesh:
            raise Exception("No mesh component found")
        if len(self.colors) < self.lives + 1:
            raise Exception("Not enough colors for the amount of lives")
        # default color is the self.lifes+1 color in the list
        self.mesh.color = self.colors[self.lives + 1]
        return super().on_init()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        """
        Changes the color of the timer and plays the hit sound

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
        """

        if self.lives <= 0:
            self.parent.on_destroy()
        self.mesh.color = self.colors[self.lives]

        self.parent.sound_manager.play_sfx(self.hit_sound)
        self.lives -= 1
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        """
        Serializes the LifeTimer

        Returns:
            dict: a dictionary containing the LifeTimer's data
        """

        colors_tuples = [(color.r, color.g, color.b) for color in self.colors]
        return {
            "colors": colors_tuples,
            "lives": self.lives
        }
    
    def deserialize(self, data: dict) -> 'LifeTimer':
        """
        Deserializes the LifeTimer

        Arguments:
            data: dict, a dictionary containing the LifeTimer's data

        Returns:
            LifeTimer: the modified LifeTimer instance
        """

        self.colors = [Color(color[0], color[1], color[2]) for color in data["colors"]]
        self.lives = data["lives"]
        return self