from pathlib import Path
from pygame import Vector2, Color
import pygame
from api.components.bumper import Bumper
from api.components.change_score import ChangeScore
from api.components.life_timer import LifeTimer
from api.components.scale_renderer import ScaleRenderer
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh, PolygonMesh
from api.components.collider import CircleCollider, PolygonCollider
from api.components.renderer import Renderer
from constants import ASSETS_PATH, COLLISION_FRICTION as CF
from options import Options


class PolygonWall(GameObject):
    def __init__(self, scene, rel_points: list[Vector2], friction: float = CF, pos: Vector2 = Vector2(0, 0), color: Color = Color(100, 100, 100), visible: bool = True, hit_sound = None):
        super().__init__(pos, 0, scene)

        self.hit_sound: pygame.mixer.Sound = hit_sound # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/hit_sound.wav"))

        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        self.sound_manager.play_sfx(self.hit_sound)
        return super().on_collision(other, point, normal)


class CircleWall(GameObject):
    def __init__(self, scene, pos: Vector2, radius: float, friction: float = CF, color: Color = Color(100, 100, 100), visible: bool = True, hit_sound = None):
        super().__init__(pos, 0, scene)

        self.hit_sound: pygame.mixer.Sound = hit_sound # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/hit_sound.wav"))

        self.add_components(
            CircleMesh(color, radius=radius),
            CircleCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        self.sound_manager.play_sfx(self.hit_sound)
        return super().on_collision(other, point, normal)
    
    def serialize(self) -> dict:
        return {
            self.__class__.__name__: {
                "components": {c.__class__.__name__: c.serialize() for c in self.components},
                "transform": self.transform.serialize()
            }
        }
    
    def deserialize(self, data: dict) -> 'CircleWall':
        self.components.clear()
        self.transform.deserialize(data["transform"])
        components = []
        component_data = data["components"]
        for component_class in data["components"]:
            component = globals()[component_class]().deserialize(component_data[component_class])
            components.append(component)
        self.add_components(*components)
        return self
