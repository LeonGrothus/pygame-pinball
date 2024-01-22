import random
from pygame import Color, Vector2
from api.components.collider import PolygonCollider
from api.components.mesh import PolygonMesh
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject
from options import Options


class Plunger(GameObject):
    def __init__(self, scene, first_point: Vector2, second_point: Vector2, impuls_range: tuple[int, int]= (1000, 1000)):
        self.impuls_range = impuls_range
        super().__init__(Vector2(), 0, scene)

        points = [first_point, second_point]
        self.add_components(
            PolygonMesh(Color(0, 0, 0), points),
            PolygonCollider(),
        )


    def on_collision(self, other, point, normal):
        other_rb = other.get_component_by_class(Rigidbody)
        other_rb.velocity.x = 0 # type: ignore
        impuls = random.randrange(self.impuls_range[0], self.impuls_range[1])
        other_rb.apply_impuls(normal * impuls) # type: ignore
        return super().on_collision(other, point, normal)