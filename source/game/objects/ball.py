from pathlib import Path
from pygame import Vector2, Color
import pygame
from source.api.components.tray import Tray
from source.api.objects.game_object import GameObject
from source.api.components.mesh import CircleMesh
from source.api.components.collider import CircleCollider
from source.api.components.rigidbody import Rigidbody
from source.api.components.renderer import Renderer
from data.constants import ASSETS_PATH


class Ball(GameObject):
    """
    A class to represent a Ball. A Ball is a GameObject that is used to destroy bricks and bounce off the paddle.

    Attributes:
        radius: int, the radius of the ball
        hide: bool, whether the ball is hidden

    Methods:
        __init__(self, scene, pos: Vector2, color: Color = Color(255, 255, 255), radius=25)
        on_destroy(self)
        on_update(self, delta_time: float)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Ball'
        hide_ball(self)
    """

    def __init__(self, scene, pos: Vector2, color: Color = Color(255, 255, 255), radius=25, forced_spawn = False) -> None:
        """
        Inits Ball with pos, color and radius

        Arguments:
            scene: Scene, the scene of the Ball
            pos: Vector2, the position of the Ball
            color: Color, the color of the Ball
            radius: int, the radius of the Ball
            forced_spawn: bool, whether the ball is forced to spawn
        """

        self.radius = radius
        self.hide = False
        self.forced_spawn = forced_spawn
        super().__init__(pos, 5, scene)

        self.add_components(
            CircleMesh(color, self.radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )
        self.scene.active_balls += 1

        self.ball_destroyed_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/ball_destroyed.wav"))

    def on_destroy(self) -> None:
        """
        Plays the ball_destroyed_sound and decreases the amount of active balls

        Returns:
            None
        """

        self.sound_manager.play_sfx(self.ball_destroyed_sound)
        self.scene.active_balls -= 1
        return super().on_destroy()

    def on_update(self, delta_time: float) -> None:
        """
        Overrides the on_update method of GameObject. If the ball is hidden, it does not update.

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """

        if self.hide:
            return
        if self.transform.pos.y > self.scene.screen.get_height() + self.radius/2:
            self.on_destroy()
        return super().on_update(delta_time)

    def serialize(self) -> dict:
        """
        Serializes the Ball

        Returns:
            dict: the serialized Ball
        """

        return {
            self.__class__.__name__: {
                "components": {c.__class__.__name__: c.serialize() for c in self.components},
                "transform": self.transform.serialize(),
                "forced_spawn": self.forced_spawn
            }
        }

    def deserialize(self, data) -> 'Ball':
        """
        Deserializes the Ball

        Arguments:
            data: dict, the serialized Ball

        Returns:
            Ball: the deserialized Ball
        """

        self.components.clear()
        self.transform.deserialize(data["transform"])
        self.forced_spawn = data["forced_spawn"]
        components = []
        component_data = data["components"]
        for component_class in data["components"]:
            component = globals()[component_class]().deserialize(component_data[component_class])
            components.append(component)
        self.add_components(*components)
        return self

    def hide_ball(self):
        """
        Hides the ball

        Returns:
            None
        """
        self.transform.pos = Vector2(-100, -100)
        self.hide = True
