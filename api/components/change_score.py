import random
from pygame import Vector2
from api.components.component import Component
from api.components.rigidbody import Rigidbody
from api.objects.game_object import GameObject


class ChangeScore(Component):
    def __init__(self, add_to_score: int = 10) -> None:
        self.add_to_score = add_to_score
        super().__init__()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        self.parent.scene.score += self.add_to_score
        return super().on_collision(other, point, normal)

    def serialize(self) -> dict:
        return {
            "add_to_score": self.add_to_score
        }

    def deserialize(self, data: dict) -> 'ChangeScore':
        self.add_to_score = data["add_to_score"]
        return self