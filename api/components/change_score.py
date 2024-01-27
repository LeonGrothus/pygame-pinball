from pygame import Vector2
from api.components.component import Component
from api.objects.game_object import GameObject


class ChangeScore(Component):
    """
    A class to represent a ChangeScore. A ChangeScore is a component that changes the score by a given amount when it is hit. 

    Attributes:
        add_to_score: int, score to add

    Methods:
        __init__(self, add_to_score: int = 10)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'ChangeScore'
    """

    def __init__(self, add_to_score: int = 10) -> None:
        """
        Inits ChangeScore with add_to_score

        Arguments:
            add_to_score: int, score to add
        """

        self.add_to_score = add_to_score
        super().__init__()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        """
        Adds add_to_score to the score

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
        """

        self.parent.scene.score += self.add_to_score
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        """
        Serializes the ChangeScore

        Returns:
            dict: a dictionary containing the ChangeScore's data
        """

        return {
            "add_to_score": self.add_to_score
        }

    def deserialize(self, data: dict) -> 'ChangeScore':
        """
        Deserializes the ChangeScore

        Arguments:
            data: dict, the data to deserialize

        Returns:
            ChangeScore: the modified ChangeScore instance
        """
        self.add_to_score = data["add_to_score"]
        return self