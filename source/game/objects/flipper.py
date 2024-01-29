from pygame import Color
from pygame import Vector2 as V2
from source.api.objects.game_object import GameObject
from source.api.components.mesh import PolygonMesh
from source.api.components.collider import PolygonCollider
from source.api.components.renderer import Renderer
from source.api.management.options_manager import OptionsManager


class Flipper(GameObject):
    """
    A class to represent a Flipper. A Flipper is a GameObject that is used to hit the ball.

    Attributes:
        scene: Scene, the scene of the Flipper
        pos: V2, the position of the Flipper
        color: Color, the color of the Flipper
        initial_angle: float, the initial angle of the Flipper

    Methods:
        __init__(self, scene, pos: V2, color: Color = Color(255, 255, 255), radius=25)
        on_destroy(self)
        on_update(self, delta_time: float)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Ball'
        hide_ball(self)
    """

    def __init__(self, scene, pos: V2, initial_angle: float, color: Color = Color(255, 255, 255)) -> None:
        """
        Inits Flipper with pos, color and radius

        Arguments:
            scene: Scene, the scene of the Flipper
            pos: V2, the position of the Flipper
            color: Color, the color of the Flipper
            initial_angle: float, the initial angle of the Flipper
        """
        super().__init__(pos, 10, scene)

        points: list[V2] = [V2(76, 97), V2(80, 86), V2(90, 78), V2(100, 75), V2(140, 76), V2(180, 78), V2(220, 81), V2(260, 86), V2(300, 94), V2(307, 96), V2(310, 100), V2(307, 104), V2(300, 106), V2(260, 114), V2(220, 119), V2(180, 122), V2(140, 124), V2(100, 125), V2(90, 122), V2(80, 114), V2(76, 103)]
        points = [point - V2(100, 100) for point in points]
        asf = OptionsManager().asf

        for point in points:
            point *= (asf * 0.55)

        # Add the necessary components
        self.add_components(
            PolygonMesh(color, points),
            PolygonCollider(friction=0 ),
            Renderer()
        )

        self.transform.rotate(initial_angle)