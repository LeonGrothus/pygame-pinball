from pathlib import Path
from pygame import Color, Vector2
import pygame
from api.components.collider import PolygonCollider
from api.components.mesh import PolygonMesh
from api.components.renderer import Renderer
from api.objects.game_object import GameObject
from constants import ASSETS_PATH


class Spring(GameObject):
    """
    A class to represent a Spring. A Spring is a GameObject that is hit by the ball. When the Spring is hit, the score is increased.

    Attributes:
        add_to_score: int, the amount of score to add when the spring is hit
        spring_sound: pygame.mixer.Sound, the sound to play when the spring is hit

    Methods:
        __init__(self, scene, pos: Vector2, width: float = 20, height: float = 50, color: Color = Color(100, 100, 100), add_to_score: int = 25, rotation: float=0)
        on_trigger_enter(self, other: GameObject) -> None
    """

    def __init__(self, scene, pos: Vector2, width: float = 20, height: float = 50, color: Color = Color(100, 100, 100), add_to_score: int = 25, rotation: float=0):
        """
        Inits Spring with pos, width, height, color and add_to_score

        Arguments:
            scene: Scene, the scene of the Spring
            pos: Vector2, the position of the Spring
            width: float, the width of the Spring
            height: float, the height of the Spring
            color: Color, the color of the Spring
            add_to_score: int, the amount of score to add when the spring is hit
            rotation: float, the rotation of the Spring
        """    
    
        super().__init__(pos, 0, scene)
        self.add_to_score = add_to_score

        self.spring_sound: pygame.mixer.Sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/spring.wav"))

        rel_points = [
            Vector2(-width/2, -height/2),
            Vector2(width/2, -height/2),
            Vector2(width/2, height/2),
            Vector2(-width/2, height/2)
        ]
        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(is_trigger=True),
            Renderer()
        )

        self.transform.rotate(rotation)

    def on_trigger_enter(self, other: GameObject) -> None:
        """
        Increases the score and plays the spring_sound

        Arguments:
            other: GameObject, the other object

        Returns:
            None
        """

        self.scene.score += self.add_to_score
        self.sound_manager.play_sfx(self.spring_sound)
        return super().on_trigger_enter(other)