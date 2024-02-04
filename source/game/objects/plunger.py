from pathlib import Path
import random
from pygame import Color, Vector2
import pygame
from source.api.components.collider import PolygonCollider
from source.api.components.mesh import PolygonMesh
from source.api.components.rigidbody import Rigidbody
from source.api.objects.game_object import GameObject
from data.constants import ASSETS_PATH


class Plunger(GameObject):
    """
    A class to represent a Plunger. A Plunger is a GameObject that is used to hit the ball.

    Attributes:
        impuls_range: tuple[int, int], the impuls range applied by the plunger
        plunger_sound: pygame.mixer.Sound, the sound to play when the plunger is hit

    Methods:
        __init__(self, scene, first_point: Vector2, second_point: Vector2, impuls_range: tuple[int, int] = (1000, 1000))
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
    """

    def __init__(self, scene, first_point: Vector2, second_point: Vector2, impuls_range: tuple[int, int] = (1000, 1000)) -> None:
        """
        Inits Plunger with first_point, second_point and impuls_range

        Arguments:
            scene: Scene, the scene of the Plunger
            first_point: Vector2, the first point of the Plunger
            second_point: Vector2, the second point of the Plunger
            impuls_range: tuple[int, int], the impuls range applied by the plunger
        """
        super().__init__(Vector2(), 0, scene)

        self.impuls_range = impuls_range
        self.plunger_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/plunger.wav"))

        points = [first_point, second_point]
        self.add_components(
            PolygonMesh(Color(0, 0, 0), points),
            PolygonCollider(),
        )

    def on_collision(self, other, point, normal) -> None:
        """
        Applies a random force to the other object

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
        """
        self.sound_manager.play_sfx(self.plunger_sound)
        other_rb = other.get_component_by_class(Rigidbody)
        other_rb.velocity.x = 0  # type: ignore
        impuls = random.randrange(self.impuls_range[0], self.impuls_range[1])
        other_rb.apply_impuls(normal * impuls)  # type: ignore
        return super().on_collision(other, point, normal)
