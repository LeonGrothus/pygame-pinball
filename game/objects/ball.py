from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh
from api.components.collider import CircleCollider
from api.components.ridigbody import Rigidbody
from api.components.renderer import Renderer

class Ball(GameObject):
    def __init__(self, pos: Vector2, radius: float = 50, color: Color = Color(255, 255, 255)):
        super().__init__(pos, 5)
        
        # Add the necessary components
        self.add_components(
            CircleMesh(color, radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )