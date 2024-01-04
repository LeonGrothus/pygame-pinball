from pygame import Vector2, Color
from api.objects.gameObject import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.renderer import Renderer

class Boundry(GameObject):
    def __init__(self, pos: Vector2, screen, all_active_gos: list, all_active_rbs: list, color: Color = Color(255, 255, 255)):
        super().__init__(pos, screen, all_active_gos, all_active_rbs)
        
        self.mesh = PolygonMesh(color, [])
        self.collider: PolygonCollider = PolygonCollider()
        
        # Add the necessary components
        self.add_components(
            self.mesh,
            self.collider,
        )

    def update(self, delta_time: float):
        super().update(delta_time)
        
        # Update the points of the mesh and collider to match the current screen size
        width, height = self.screen.get_size()
        points = [Vector2(0, 0), Vector2(width, 0), Vector2(width, height), Vector2(0, height)]
        self.mesh.points = points