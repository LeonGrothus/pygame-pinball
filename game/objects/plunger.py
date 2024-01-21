import random
from pygame import Color, Vector2
from api.components.collider import PolygonCollider
from api.components.mesh import PolygonMesh
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject
from options import Options


class Plunger(GameObject):
    def __init__(self, first_point: Vector2, second_point: Vector2, impuls_range: tuple[int, int]= (1000, 1000)):
        self.first_point = first_point
        self.second_point = second_point
        self.impuls_range = impuls_range
        self.options = Options()
        super().__init__(Vector2(), 0)
    
    def on_awake(self):
        points = [self.first_point, self.second_point]

        self.mesh: PolygonMesh = PolygonMesh(Color(0, 0, 0), points)
        self.collider: PolygonCollider = PolygonCollider()

        # Add the necessary components
        self.add_components(
            self.mesh,
            self.collider,
        )

        return super().on_awake()
    
    def on_collision(self, other, point, normal):
        other_rb = other.get_component_by_class(Rigidbody)
        other_rb.velocity.x = 0 # type: ignore
        impuls = random.randrange(self.impuls_range[0], self.impuls_range[1])
        print(impuls)
        other_rb.apply_impuls(normal * impuls * self.options.asf) # type: ignore
        return super().on_collision(other, point, normal)