import pygame
from pygame import Vector2, Color
from source.api.components.mesh import PolygonMesh
from source.api.components.collider import PolygonCollider
from source.api.components.renderer import Renderer
from source.api.components.rigidbody import Rigidbody
from source.api.objects.game_object import GameObject
from source.game.objects.ball import Ball


class Teleporter(GameObject):
    """
    A class to represent a Teleporter. A Teleporter is a GameObject that is used to teleport the ball to another location.

    Attributes:
        teleport_location: Vector2, the location to teleport the ball to
        delay: float, the delay before teleporting the ball
        objects_to_teleport: list[tuple[Ball, float]], the list of objects to teleport

    Methods:
        __init__(self, scene, rel_points: list[Vector2], teleport_location: Vector2, pos: Vector2 = Vector2(0, 0), color: Color = Color(80, 80, 80), delay=2)
        on_collision(self, other: Ball, point: Vector2, normal: Vector2) -> None
        on_update(self, delta_time)
    """

    def __init__(self, scene, rel_points: list[Vector2], teleport_location: Vector2, pos: Vector2 = Vector2(0, 0), color: Color = Color(80, 80, 80), delay=2):
        """
        Inits Teleporter with pos, color and radius

        Arguments:
            scene: Scene, the scene of the Teleporter
            rel_points: list[Vector2], the relative points of the Teleporter
            teleport_location: Vector2, the location to teleport the ball to
            pos: Vector2, the position of the Teleporter
            color: Color, the color of the Teleporter
            delay: float, the delay before teleporting the ball
        """
        super().__init__(pos, 0, scene)
        self.teleport_location = teleport_location
        self.delay = delay
        self.objects_to_teleport: list[tuple[Ball, float]] = []

        self.on_teleport_sound = pygame.mixer.Sound("assets/sounds/teleport.wav")
        self.exit_teleport_sound = pygame.mixer.Sound("assets/sounds/exit_teleport.wav")

        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(),
            Renderer()
        )

    def on_collision(self, other: Ball, point: Vector2, normal: Vector2) -> None:
        """
        Teleports the ball to the teleport_location

        Arguments:
            other: Ball, the ball
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
        """

        if any(obj == other for obj, _ in self.objects_to_teleport): # if the ball is already in the list,
            return # don't teleport it again
        self.sound_manager.play_sfx(self.on_teleport_sound) # play the teleport sound
        self.objects_to_teleport.append((other, self.delay)) # add the ball to the list
        other.hide_ball() # hide the ball
        return super().on_collision(other, point, normal) 

    def on_update(self, delta_time) -> None:
        """
        Teleports the ball to the teleport_location

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """

        for i in range(len(self.objects_to_teleport) - 1, -1, -1):
            obj, time = self.objects_to_teleport[i]
            time -= delta_time
            if time <= 0:
                obj.transform.pos = self.teleport_location.copy()
                obj.hide = False
                obj.get_component_by_class(Rigidbody).velocity = Vector2(0, 0) # type: ignore
                self.objects_to_teleport.pop(i)
                self.sound_manager.play_sfx(self.exit_teleport_sound)
            else:
                self.objects_to_teleport[i] = (obj, time)
        return super().on_update(delta_time)
