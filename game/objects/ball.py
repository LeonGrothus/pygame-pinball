from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh
from api.components.collider import CircleCollider
from api.components.ridigbody import Rigidbody
from api.components.renderer import Renderer
from options import Options

class Ball(GameObject):
    def __init__(self, pos: Vector2, color: Color = Color(255, 255, 255)):
        self.color = color
        self.radius = 25 * Options().asf
        super().__init__(pos, 5)

    def awake(self):
        # Add the necessary components
        self.add_components(
            CircleMesh(self.color, self.radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )
        return super().awake()

    def destroy(self) -> None:
        self.scene.active_ball_count -= 1
        return super().destroy()
    
    def update(self, delta_time: float):
        if self.transform.pos.y > self.scene.screen.get_height() + self.radius/2:
            self.destroy()
        return super().update(delta_time)