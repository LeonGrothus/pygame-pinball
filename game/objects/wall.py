from pygame import Vector2, Color
from api.components.bumper import Bumper
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh, PolygonMesh
from api.components.collider import CircleCollider, PolygonCollider
from api.components.renderer import Renderer
from constants import COLLISION_FRICTION as CF
from options import Options


class PolygonWall(GameObject):
    def __init__(self, rel_points: list[Vector2], friction: float = CF, pos: Vector2 = Vector2(0, 0), color: Color = Color(100, 100, 100), visible: bool = True):
        self.color = color
        self.rel_points = rel_points
        self.pos = pos
        self.visible = visible
        self.friction = friction
        super().__init__(pos, 0)

    def on_awake(self):
        # Add the necessary components
        self.add_components(
            PolygonMesh(self.color, self.rel_points),
            PolygonCollider(friction=self.friction),
        )
        if self.visible:
            self.add_components(Renderer())

        return super().on_awake()


class CircleWall(GameObject):
    def __init__(self, pos: Vector2, radius: float, friction: float = CF, color: Color = Color(100, 100, 100), visible: bool = True):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.visible = visible
        self.friction = friction
        super().__init__(pos, 0)

    def on_awake(self):
        # Add the necessary components
        self.add_components(
            CircleMesh(self.color, radius=self.radius),
            CircleCollider(friction=self.friction),
        )
        if self.visible:
            self.add_components(Renderer())

        return super().on_awake()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        return super().on_collision(other, point, normal)
