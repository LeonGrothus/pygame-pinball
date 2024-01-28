import random
from pygame import Vector2
from source.api.components.component import Component
from source.api.components.rigidbody import Rigidbody
from source.api.objects.game_object import GameObject


class Bumper(Component):
    """
    A class to represent a Bumper. A Bumper is a component that applies a random force to the other object when it is hit.

    Attributes:
        bumper_force: tuple[int, int], force range applied by the bumper

    Methods:
        __init__(self, bumper_force: tuple[int, int] = (100,100))
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Bumper'
    """

    def __init__(self, bumper_force: tuple[int, int] = (100,100)) -> None:
        """
        Inits Bumper with bumper_force

        Arguments:
            bumper_force: tuple[int, int], force range applied by the bumper
        """

        self.bumper_force = bumper_force
        super().__init__()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        """
        Applies a random force to the other object

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
        """

        other_rb = other.get_component_by_class(Rigidbody)
        impuls = random.randrange(int(self.bumper_force[0]), int(self.bumper_force[1]))
        other_rb.apply_impuls(normal * impuls) # type: ignore
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        """
        Serializes the Bumper

        Returns:
            dict: a dictionary containing the Bumper's data
        """
        
        return {
            "bumper_force": self.bumper_force
        }

    def deserialize(self, data: dict) -> 'Bumper':
        """
        Deserializes the Bumper

        Arguments:
            data: dict, a dictionary containing the Bumper's data
        
        Returns:
            Bumper: the modified Bumper instance
        """

        self.bumper_force = data["bumper_force"]
        return self