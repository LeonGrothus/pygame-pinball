from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer
from options import Options


class Flipper(GameObject):
    def __init__(self, scene, pos: Vector2, initial_angle: float, color: Color = Color(255, 255, 255)):
        super().__init__(pos, 10, scene)

        points: list[Vector2] = [
            Vector2(-24, -3),
            Vector2(-23, -6),
            Vector2(-22, -10),
            Vector2(-21, -12),
            Vector2(-20, -14),
            Vector2(-15, -19),
            Vector2(-10, -22),
            Vector2(-6, -24),
            Vector2(0, -25),
            Vector2(20, -24),
            Vector2(40, -24),
            Vector2(60, -23),
            Vector2(80, -22),
            Vector2(100, -21),
            Vector2(120, -19),
            Vector2(140, -17),
            Vector2(160, -14),
            Vector2(180, -10),
            Vector2(200, -6),
            Vector2(207, -4),
            Vector2(210, 0),
            Vector2(207, 4),
            Vector2(200, 6),
            Vector2(180, 10),
            Vector2(160, 14),
            Vector2(140, 17),
            Vector2(120, 19),
            Vector2(100, 21),
            Vector2(80, 22),
            Vector2(60, 23),
            Vector2(40, 24),
            Vector2(20, 25),
            Vector2(0, 25),
            Vector2(-6, 24),
            Vector2(-10, 22),
            Vector2(-15, 19),
            Vector2(-20, 14),
            Vector2(-21, 12),
            Vector2(-22, 10),
            Vector2(-23, 6),
            Vector2(-24, 3),
        ]
        asf = Options().asf

        for point in points:
            point *= (asf * 0.55)

        # Add the necessary components
        self.add_components(
            PolygonMesh(color, points),
            PolygonCollider(friction=0 ),
            Renderer()
        )

        self.transform.rotate(initial_angle)