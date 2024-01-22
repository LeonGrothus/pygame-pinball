import pygame
from pygame import Vector2, Color
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject


class Teleporter(GameObject):
    def __init__(self, scene, rel_points: list[Vector2], teleport_location: Vector2, pos: Vector2 = Vector2(0, 0), color: Color = Color(80, 80, 80), delay=.5):
        super().__init__(pos, 0, scene)
        self.teleport_location = teleport_location
        self.delay = delay
        self.objects_to_teleport = []

        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(),
            Renderer()
        )

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        if any(obj == other for obj, _ in self.objects_to_teleport):
            return
        self.objects_to_teleport.append((other, self.delay))
        return super().on_collision(other, point, normal)

    def on_update(self, delta_time):
        for i in range(len(self.objects_to_teleport) - 1, -1, -1):
            obj, time = self.objects_to_teleport[i]
            time -= delta_time
            if time <= 0:
                obj.transform.pos = self.teleport_location.copy()
                obj.get_component_by_class(Rigidbody).velocity = Vector2(0, 0)
                self.objects_to_teleport.pop(i)
            else:
                self.objects_to_teleport[i] = (obj, time)
        return super().on_update(delta_time)
