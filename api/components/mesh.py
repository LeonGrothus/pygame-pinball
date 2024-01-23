from abc import ABC, abstractmethod

from pygame import Color, Vector2
from api.components.component import Component
from options import Options


class Mesh(Component, ABC):
    def __init__(self, color: Color) -> None:
        self.color: Color = color

        self.target_rotation: float = 0
        self.rotation_speed: float = 0
        super().__init__()

    def on_init(self) -> None:
        self.parent.transform.rot.subscribe(self.rotate)
        self.size = self._set_size()
        return super().on_init()

    def on_destroy(self) -> None:
        self.parent.transform.rot.unsubscribe(self.rotate)
        return super().on_destroy()

    @abstractmethod
    def rotate(self, angle: float) -> None:
        pass

    @abstractmethod
    def _set_size(self) -> Vector2:
        pass


class CircleMesh(Mesh):
    def __init__(self, color: Color = Color(255, 255, 255), radius: float = 25) -> None:
        super().__init__(color)
        self.radius = radius

    def serialize(self) -> dict:
        return {
            "radius": self.radius/Options().asf
        }

    def deserialize(self, data: dict) -> 'CircleMesh':
        self.radius = data["radius"]*Options().asf
        return self

    def rotate(self, angle: float) -> None:
        return super().rotate(angle)
    
    def _set_size(self) -> Vector2:
        return Vector2(self.radius*2, self.radius*2)


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

    def deserialize(self, data: dict) -> 'PolygonMesh':
        self._relative_points = [Vector2(p["x"], p["y"]) for p in data["relative_points"]]
        return self

    def rotate(self, angle: float) -> None:
        self.points = [self.parent.transform.pos + p.rotate(angle) for p in self._relative_points]
        return super().rotate(angle)
    
    def _set_size(self) -> Vector2:
        return Vector2(max(p.x for p in self.points) - min(p.x for p in self.points),
                            max(p.y for p in self.points) - min(p.y for p in self.points))
