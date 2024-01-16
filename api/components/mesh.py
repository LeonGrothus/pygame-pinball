from abc import ABC, abstractmethod

from pygame import Color, Vector2
from api.components.component import Component


class Mesh(Component, ABC):
    def __init__(self, color: Color) -> None:
        self.color: Color = color

        self.target_rotation: float = 0
        self.rotation_speed: float = 0
        super().__init__()

    def on_init(self) -> None:
        self.parent.transform.rot.subscribe(self.rotate)
        return super().on_init()

    def on_destroy(self) -> None:
        self.parent.transform.rot.unsubscribe(self.rotate)
        return super().on_destroy()

    @abstractmethod
    def rotate(self, angle: float) -> None:
        pass


class CircleMesh(Mesh):
    def __init__(self, color: Color, radius: float) -> None:
        super().__init__(color)
        self.radius = radius

    # def serialize(self) -> dict:
    #     return {
    #         "radius": self.radius
    #     }

    # def deserialize(self, data: dict) -> None:
    #     self.radius = data["radius"]

    def rotate(self, angle: float) -> None:
        return super().rotate(angle)


class PolygonMesh(Mesh):
    def __init__(self, color: Color, relative_points: list[Vector2]) -> None:
        super().__init__(color)

        self._relative_points: list[Vector2] = relative_points
        self.points: list[Vector2] = relative_points

    def on_init(self) -> None:
        self.points = [self.parent.transform.pos + p for p in self.points]
        return super().on_init()

    def serialize(self) -> dict:
        return {
            "relative_points": [
                {
                    "x": p.x,
                    "y": p.y
                } for p in self._relative_points
            ]
        }

    def deserialize(self, data: dict) -> None:
        self._relative_points = [Vector2(p["x"], p["y"]) for p in data["relative_points"]]

    def rotate(self, angle: float) -> None:
        self.points = [self.parent.transform.pos + p.rotate(angle) for p in self._relative_points]
        return super().rotate(angle)
