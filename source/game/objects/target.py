from pathlib import Path
from pygame import Color, Vector2
import pygame
import pygame
from pygame import Color
from pygame.time import get_ticks
from source.api.components.change_score import ChangeScore
from source.api.components.collider import PolygonCollider
from source.api.components.mesh import PolygonMesh
from source.api.components.renderer import Renderer
from source.api.management.options_manager import OptionsManager
from source.api.objects.game_object import GameObject
from data.constants import ASSETS_PATH


class TargetBase(GameObject):
    """
    A class to represent a TargetBase. A TargetBase is a GameObject that is hit by the ball. When the TargetBase is hit, the score is increased.

    Attributes:
        add_to_score: int, the amount of score to add when the spring is hit
        hit_sound: pygame.mixer.Sound, the sound to play when the spring is hit
        was_hit: bool, whether the target was hit

    Methods:
        __init__(self, scene, pos: Vector2, width: float = 20, height: float = 75, color: Color = Color(255, 0, 0), add_to_score: int = 25, rotation: float=0)
        on_trigger_enter(self, other: GameObject) -> None
    """

    def __init__(self, scene, pos: Vector2 = Vector2(), width: float = 15, height: float = 50, rotation: float = 0, base_color: Color = Color(255, 0, 0), hit_color: Color = Color(0, 255, 0)):
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
        self.base_color = base_color
        self.hit_color = hit_color
        self.width = width
        self.height = height

        super().__init__(pos, -1, scene)
        self.hit_sound: pygame.mixer.Sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/target_base.wav"))
        self.was_hit = False

        asf = OptionsManager().asf
        self.mesh = PolygonMesh(base_color, [
            Vector2(-width/2, -height/2)*asf,
            Vector2(width/2, -height/2)*asf,
            Vector2(width/2, height/2)*asf,
            Vector2(-width/2, height/2)*asf
        ])
        self.add_components(
            self.mesh,
            PolygonCollider(is_trigger=True),
            Renderer(),
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
        if self.was_hit:
            return
        self.sound_manager.play_sfx(self.hit_sound)
        self.mesh.color = self.hit_color
        self.was_hit = True
        return super().on_trigger_enter(other)

    def reset(self) -> None:
        """
        Resets the target to its base color and sets was_hit to False

        Returns:
            None
        """
        self.mesh.color = self.base_color
        self.was_hit = False

    def change_color(self, color: Color) -> None:
        """
        Changes the color of the target

        Arguments:
            color: Color, the new color of the target

        Returns:
            None
        """
        self.mesh.color = color

    def serialize(self) -> dict:
        """
        Serializes the TargetBase

        Returns:
            dict: the serialized TargetBase
        """
        asf = OptionsManager().asf
        return {
            "pos": {
                "x": self.transform.pos.x/asf,
                "y": self.transform.pos.y/asf
            },
            "width": self.width/asf,
            "height": self.height/asf,
            "rotation": self.transform.rot.get_value(),
            "base_color": {
                "r": self.base_color.r,
                "g": self.base_color.g,
                "b": self.base_color.b
            },
            "hit_color": {
                "r": self.hit_color.r,
                "g": self.hit_color.g,
                "b": self.hit_color.b
            },
            "was_hit": self.was_hit,
            "components": {c.__class__.__name__: c.serialize() for c in self.components}
        }

    def deserialize(self, data: dict) -> 'TargetBase':
        """
        Deserializes the TargetBase

        Arguments:
            data: dict, the data to deserialize

        Returns:
            TargetBase: the deserialized TargetBase
        """
        asf = OptionsManager().asf
        self.transform.pos = Vector2(data["pos"]["x"], data["pos"]["y"]) * asf
        self.width = data["width"] * asf
        self.height = data["height"] * asf
        self.transform.rotate(data["rotation"])
        self.base_color = Color(data["base_color"]["r"], data["base_color"]["g"], data["base_color"]["b"])
        self.hit_color = Color(data["hit_color"]["r"], data["hit_color"]["g"], data["hit_color"]["b"])
        self.was_hit = data["was_hit"]
        self.mesh.color = self.hit_color if self.was_hit else self.base_color
        return self


class TargetGroup(GameObject):
    """
    A class to represent a TargetGroup. A TargetGroup is a GameObject that is hit by the ball. When all targets in the group are hit, the score is increased.

    Attributes:
        targets: list[TargetBase], the targets in the group
        add_to_score: int, the amount of score to add when the group is hit
        all_hit_sound: pygame.mixer.Sound, the sound to play when the group is hit

    Methods:
        __init__(self, scene, targets: list[TargetBase], add_to_score: int = 5000)
        on_update(self, delta_time: float) -> None
    """

    def __init__(self, scene, targets: list[TargetBase], add_to_score: int = 5000, delay: float = .25) -> None:
        """
        Inits TargetGroup with targets and add_to_score

        Arguments:
            scene: Scene, the scene of the TargetGroup
            targets: list[TargetBase], the targets in the group
            add_to_score: int, the amount of score to add when the group is hit

        Returns:
            None
        """
        super().__init__(Vector2(), 0, scene)
        self.all_hit_sound: pygame.mixer.Sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/target_group.wav"))

        self.targets = targets
        self.add_to_score = add_to_score
        self.delay = delay*1000  # in ms
        self.color_change_count = 0
        self.color_change_state = 0
        self.start_time = 0
        self.init_reset = False

    def on_update(self, delta_time: float) -> None:
        """
        Checks if all targets are hit and plays the all_hit_sound if they are

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """
        if not self.init_reset and all(target.was_hit for target in self.targets):
            self.sound_manager.play_sfx(self.all_hit_sound)
            self.scene.score += self.add_to_score
            self.start_time = get_ticks()
            self.color_change_count = 0
            self.color_change_state = 0
            self.init_reset = True

        if not self.init_reset:
            return super().on_update(delta_time)

        if self.color_change_count < 3 and get_ticks() - self.start_time > self.delay:
            colors = {0: Color(255, 255, 0), 1: Color(0, 255, 0)}
            for target in self.targets:
                target.change_color(colors[self.color_change_state])
            self.color_change_state = 1 - self.color_change_state
            self.color_change_count += self.color_change_state
            self.start_time = get_ticks()
        elif self.color_change_count >= 3:
            self.init_reset = False
            for target in self.targets:
                target.reset()
        return super().on_update(delta_time)

    def on_destroy(self) -> None:
        """
        Destroys the TargetGroup

        Returns:
            None
        """
        for target in self.targets:
            if target in self.scene.all_active_gos:
                target.on_destroy()
        self.targets.clear()
        return super().on_destroy()

    def serialize(self) -> dict:
        """
        Serializes the TargetGroup

        Returns:
            dict: the serialized TargetGroup
        """
        return {
            self.__class__.__name__: {
                "targets": [target.serialize() for target in self.targets],
                "add_to_score": self.add_to_score,
                "delay": self.delay
            }
        }

    def deserialize(self, data: dict) -> 'TargetGroup':
        """
        Deserializes the TargetGroup

        Arguments:
            data: dict, the data to deserialize

        Returns:
            TargetGroup: the deserialized TargetGroup
        """
        targets = [TargetBase(self.scene).deserialize(target) for target in data["targets"]]
        self.scene.add_gameobjects(*targets)
        self.targets = targets

        self.add_to_score = data["add_to_score"]
        self.delay = data["delay"]
        return self
