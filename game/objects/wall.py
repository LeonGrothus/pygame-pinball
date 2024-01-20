from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer
from constants import COLLISION_FRICTION
from options import Options


class Wall(GameObject):
    def __init__(self, rel_points: list[Vector2], friction: float = COLLISION_FRICTION, pos: Vector2 = Vector2(0,0), color: Color = Color(100, 100, 100), visible: bool = True):
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
            PolygonCollider(friction=self.friction)
        )
        if self.visible:
            self.add_components(Renderer())
        

        return super().on_awake()