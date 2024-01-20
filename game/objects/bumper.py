import random
from pygame import Color, Vector2
import pygame
from api.components.collider import CircleCollider
from api.components.mesh import CircleMesh
from api.components.renderer import Renderer
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject

class Bumper(GameObject):
    def __init__(self, pos: Vector2, radius: float, impact: float, color: Color = Color(255, 255, 255)):
        super().__init__(pos, 0)
        self.color = color
        self.pos = pos
        self.radius = radius
        self.impact = impact
    
    def on_awake(self):

        # Add the necessary components
        self.add_components(
            CircleMesh(self.color, self.radius),
            CircleCollider(friction=0),
            Renderer()
        )

        return super().on_awake()
    
    def on_collision(self, other: GameObject, point, normal):
        normal.rotate_ip(random.randint(-10, 10))
        other_rigidbody = other.get_component_by_class(Rigidbody)
        other_rigidbody.apply_impuls(normal * self.impact) # type: ignore
        return super().on_collision(other, point, -normal)