from abc import ABC, abstractmethod

from pygame import Color
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

    def rotate(self, angle: float) -> None:
        return super().rotate(angle)


class PolygonMesh(Mesh):
    def __init__(self, color: Color, relative_points: list) -> None:
        super().__init__(color)

        self.__relative_points = relative_points
        self.points = relative_points

    def on_init(self) -> None:
        self.points = [self.parent.transform.pos + p for p in self.points]
        
        return super().on_init()
    
    def rotate(self, angle: float) -> None:
        self.points = [self.parent.transform.pos + p.rotate(angle) for p in self.__relative_points]
        return super().rotate(angle)