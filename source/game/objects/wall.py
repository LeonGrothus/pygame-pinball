from pathlib import Path
from pygame import Vector2, Color
import pygame
from source.api.components.scale_renderer import ScaleRenderer
from source.api.components.texture_renderer import TextureRenderer
from source.api.objects.game_object import GameObject
from source.api.components.mesh import CircleMesh, PolygonMesh
from source.api.components.collider import CircleCollider, PolygonCollider
from source.api.components.renderer import Renderer
from source.api.components.mesh import CircleMesh, PolygonMesh
from source.api.components.collider import CircleCollider, PolygonCollider
from source.api.components.renderer import Renderer
from source.api.components.bumper import Bumper
from source.api.components.change_score import ChangeScore
from source.api.components.life_timer import LifeTimer
from source.api.components.simple_movement import SimpleMovement
from data.constants import ASSETS_PATH, COLLISION_FRICTION as CF


class PolygonWall(GameObject):
    """
    A class to represent a PolygonWall. A PolygonWall is a GameObject that is used to bounce the ball off of.

    Attributes:
        hit_sound: pygame.mixer.Sound, the sound to play when the PolygonWall is hit
        sound_manager: SoundManager, the sound manager of the game
        scene: Scene, the scene of the PolygonWall
        rel_points: list[Vector2], the relative points of the PolygonWall
        friction: float, the friction of the PolygonWall
        pos: Vector2, the position of the PolygonWall
        color: Color, the color of the PolygonWall
        visible: bool, whether the PolygonWall is visible

    Methods:
        __init__(self, scene, rel_points: list[Vector2], friction: float = CF, pos: Vector2 = Vector2(0, 0), color: Color = Color(100, 100, 100), visible: bool = True, hit_sound=None)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None
    """
    def __init__(self, scene, rel_points: list[Vector2], friction: float = CF, pos: Vector2 = Vector2(0, 0), color: Color = Color(100, 100, 100), visible: bool = True, hit_sound=None):
        """
        Inits PolygonWall with pos, color and radius

        Arguments:
            scene: Scene, the scene of the PolygonWall
            rel_points: list[Vector2], the relative points of the PolygonWall
            friction: float, the friction of the PolygonWall
            pos: Vector2, the position of the PolygonWall
            color: Color, the color of the PolygonWall
            visible: bool, whether the PolygonWall is visible
        """
        
        super().__init__(pos, 0, scene)

        self.hit_sound: pygame.mixer.Sound = hit_sound  # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/hit_sound.wav"))

        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        """
        Plays the hit_sound

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision

        Returns:
            None
        """
        self.sound_manager.play_sfx(self.hit_sound)
        return super().on_collision(other, point, normal)


class CircleWall(GameObject):
    """
    A class to represent a CircleWall. A CircleWall is a GameObject that is used to bounce the ball off of.

    Attributes:
        hit_sound: pygame.mixer.Sound, the sound to play when the PolygonWall is hit
        sound_manager: SoundManager, the sound manager of the game
        scene: Scene, the scene of the PolygonWall
        rel_points: list[Vector2], the relative points of the PolygonWall
        friction: float, the friction of the PolygonWall
        pos: Vector2, the position of the PolygonWall
        color: Color, the color of the PolygonWall
        visible: bool, whether the PolygonWall is visible

    Methods:
        __init__(self, scene, pos: Vector2, radius: float, friction: float = CF, color: Color = Color(100, 100, 100), visible: bool = True, hit_sound=None)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'CircleWall'
    """
    
    def __init__(self, scene, pos: Vector2, radius: float, friction: float = CF, color: Color = Color(100, 100, 100), visible: bool = True, hit_sound=None):
        """
        Inits CircleWall with pos, color and radius

        Arguments:
            scene: Scene, the scene of the CircleWall
            pos: Vector2, the position of the CircleWall
            radius: float, the radius of the CircleWall
            friction: float, the friction of the CircleWall
            color: Color, the color of the CircleWall
            visible: bool, whether the CircleWall is visible
        """
        
        super().__init__(pos, 0, scene)

        self.hit_sound: pygame.mixer.Sound = hit_sound  # type: ignore
        if not self.hit_sound:
            self.hit_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/hit_sound.wav"))

        self.add_components(
            CircleMesh(color, radius=radius),
            CircleCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        """
        Plays the hit_sound

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision

        Returns:
            None
        """

        self.sound_manager.play_sfx(self.hit_sound)
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        """
        Serializes the CircleWall

        Returns:
            dict: the serialized CircleWall
        """
        return {
            self.__class__.__name__: {
                "components": {c.__class__.__name__: c.serialize() for c in self.components},
                "transform": self.transform.serialize()
            }
        }

    def deserialize(self, data: dict) -> 'CircleWall':
        """
        Deserializes the CircleWall

        Arguments:
            data: dict, the serialized CircleWall

        Returns:
            CircleWall: the deserialized CircleWall
        """

        self.components.clear()
        self.transform.deserialize(data["transform"])
        components = []
        component_data = data["components"]
        for component_class in data["components"]:
            component = globals()[component_class]().deserialize(component_data[component_class])
            components.append(component)
        self.add_components(*components)
        return self
