from pygame import Vector2, Color
from api.components.bumper import Bumper
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh, PolygonMesh
from api.components.collider import CircleCollider, PolygonCollider
from api.components.renderer import Renderer
from constants import COLLISION_FRICTION as CF
from options import Options


class PolygonWall(GameObject):
    def __init__(self, scene, rel_points: list[Vector2], friction: float = CF, pos: Vector2 = Vector2(0, 0), color: Color = Color(100, 100, 100), visible: bool = True):
        super().__init__(pos, 0, scene)

        self.add_components(
            PolygonMesh(color, rel_points),
            PolygonCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())


class CircleWall(GameObject):
    def __init__(self, scene, pos: Vector2, radius: float, friction: float = CF, color: Color = Color(100, 100, 100), visible: bool = True):
        super().__init__(pos, 0, scene)

        self.add_components(
            CircleMesh(color, radius=radius),
            CircleCollider(friction=friction),
        )
        if visible:
            self.add_components(Renderer())

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        return super().on_collision(other, point, normal)
