from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer
from options import Options


class Wall(GameObject):
    def __init__(self, pos: Vector2, rel_points: list[Vector2], color: Color = Color(255, 255, 255), visible: bool = True):
        self.color = color
        self.rel_points = rel_points
        self.pos = pos
        self.visible = visible
        super().__init__(pos, 0)
    
    def on_awake(self):
        # Add the necessary components
        self.add_components(
            PolygonMesh(Color(0, 0, 0), self.rel_points),
            PolygonCollider()
        )
        if self.visible:
            self.add_components(Renderer())
        

        return super().on_awake()