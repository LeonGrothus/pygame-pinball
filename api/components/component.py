from abc import ABC, abstractmethod

from pygame import Vector2

from api.objects.game_object import GameObject


class Component(ABC):
    def __init__(self):
        self.parent: GameObject = None # type: ignore

    def set_parent(self, parent: GameObject) -> None:
        self.parent = parent
    

    def on_init(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        pass

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @abstractmethod
    def deserialize(self, data: dict) -> 'Component':
        pass
