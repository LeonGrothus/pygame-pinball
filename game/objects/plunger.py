from pygame import Vector2, Color
from objects.gameObject import GameObject
from components.mesh import PolygonMesh
from components.collider import PolygonCollider
from components.ridigbody import Rigidbody
from components.renderer import Renderer

class Plunger(GameObject):
    def __init__(self, pos: Vector2, screen, all_active_gos: list, all_active_rbs: list, color: Color = Color(255, 255, 255)):
        super().__init__(pos, screen, all_active_gos, all_active_rbs)
        
        # Define the points for the plunger polygon
        points = [Vector2(-10, -50), Vector2(-10, 50), Vector2(10, 50), Vector2(10, -50)]
        
        # Add the necessary components
        self.add_components(
            PolygonMesh(color, points),
            PolygonCollider(),
            Rigidbody(),
            Renderer()
        )