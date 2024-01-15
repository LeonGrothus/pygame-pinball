from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer


class Boundry(GameObject):
    def __init__(self, open_side=None):
        self.open_side = open_side
        super().__init__(Vector2(), 0)
    
    def awake(self):
        width, height = self.scene.screen.get_size()

        # Create the points for the boundary
        points = [Vector2(0, 0), Vector2(width, 0), Vector2(width, height), Vector2(0, height)]

        # Remove the points for the open side
        if self.open_side == 'top':
            points.remove(Vector2(0, 0))
            points.remove(Vector2(width, 0))
        elif self.open_side == 'right':
            points.remove(Vector2(width, 0))
            points.remove(Vector2(width, height))
        elif self.open_side == 'bottom':
            points.remove(Vector2(width, height))
            points.remove(Vector2(0, height))
        elif self.open_side == 'left':
            points.remove(Vector2(0, height))
            points.remove(Vector2(0, 0))

        self.mesh: PolygonMesh = PolygonMesh(Color(0, 0, 0), points)
        self.collider: PolygonCollider = PolygonCollider()

        # Add the necessary components
        self.add_components(
            self.mesh,
            self.collider,
        )

        return super().awake()