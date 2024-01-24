import random
from pygame import Vector2
from api.components.component import Component
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject


class Bumper(Component):
    def __init__(self, bumper_force: tuple[int, int] = (100,100)) -> None:
        self.bumper_force = bumper_force
        super().__init__()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        other_rb = other.get_component_by_class(Rigidbody)
        impuls = random.randrange(int(self.bumper_force[0]), int(self.bumper_force[1]))
        other_rb.apply_impuls(normal * impuls) # type: ignore
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        return {
            "bumper_force": self.bumper_force
        }

    def deserialize(self, data: dict) -> 'Bumper':
        self.bumper_force = data["bumper_force"]
        return self