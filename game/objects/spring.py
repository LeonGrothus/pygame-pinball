from pathlib import Path
from pygame import Color, Vector2
import pygame
from api.components.collider import PolygonCollider
from api.components.mesh import PolygonMesh
from api.components.renderer import Renderer
from api.objects.game_object import GameObject
from constants import ASSETS_PATH


class Spring(GameObject):
    def __init__(self, scene, pos: Vector2, width: float = 20, height: float = 50, color: Color = Color(100, 100, 100), add_to_score: int = 25, rotation: float=0):
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
        self.scene.score += self.add_to_score
        self.sound_manager.play_sfx(self.spring_sound)
        return super().on_trigger_enter(other)