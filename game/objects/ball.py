from pygame import Vector2, Color
from objects.gameObject import GameObject
from components.mesh import CircleMesh
from components.collider import CircleCollider
from components.ridigbody import Rigidbody
from components.renderer import Renderer

class Ball(GameObject):
    def __init__(self, pos: Vector2, screen, all_active_gos: list, all_active_rbs: list, radius: float = 50, color: Color = Color(255, 255, 255)):
        super().__init__(pos, screen, all_active_gos, all_active_rbs)
        
        # Add the necessary components
        self.add_components(
            CircleMesh(color, radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )