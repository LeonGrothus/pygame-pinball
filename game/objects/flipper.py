from pygame import Vector2, Color
import pygame
from api.objects.game_object import GameObject
from api.components.mesh import PolygonMesh
from api.components.collider import PolygonCollider
from api.components.ridigbody import Rigidbody
from api.components.renderer import Renderer

class Flipper(GameObject):
    def __init__(self, pos: Vector2, initial_angle: float, color: Color = Color(255, 255, 255)):
        super().__init__(pos, 10)
        self.transform.rotate(initial_angle)

        # Define the points for the plunger polygon
        points = [
            pygame.Vector2(-24, -3),
            pygame.Vector2(-23, -6),
            pygame.Vector2(-22, -10),
            pygame.Vector2(-21, -12),
            pygame.Vector2(-20, -14),
            pygame.Vector2(-15, -19),
            pygame.Vector2(-10, -22),
            pygame.Vector2(-6, -24),
            pygame.Vector2(0, -25),
            pygame.Vector2(20, -24),
            pygame.Vector2(40, -24),
            pygame.Vector2(60, -23),
            pygame.Vector2(80, -22),
            pygame.Vector2(100, -21),
            pygame.Vector2(120, -19),
            pygame.Vector2(140, -17),
            pygame.Vector2(160, -14),
            pygame.Vector2(180, -10),
            pygame.Vector2(200, -6),
            pygame.Vector2(207, -4),
            pygame.Vector2(210, 0),
            pygame.Vector2(207, 4),
            pygame.Vector2(200, 6),
            pygame.Vector2(180, 10),
            pygame.Vector2(160, 14),
            pygame.Vector2(140, 17),
            pygame.Vector2(120, 19),
            pygame.Vector2(100, 21),
            pygame.Vector2(80, 22),
            pygame.Vector2(60, 23),
            pygame.Vector2(40, 24),
            pygame.Vector2(20, 25),
            pygame.Vector2(0, 25),
            pygame.Vector2(-6, 24),
            pygame.Vector2(-10, 22),
            pygame.Vector2(-15, 19),
            pygame.Vector2(-20, 14),
            pygame.Vector2(-21, 12),
            pygame.Vector2(-22, 10),
            pygame.Vector2(-23, 6),
            pygame.Vector2(-24, 3),
        ]
        
        # Add the necessary components
        self.add_components(
            PolygonMesh(color, points),
            PolygonCollider(),
            Renderer()
        )
