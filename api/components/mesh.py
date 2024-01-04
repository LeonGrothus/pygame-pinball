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
        self.target_rotation = self.parent.transform.rot
        return super().on_init()

    def on_update(self, delta_time: float) -> None:
        if self.parent.transform.rot != self.target_rotation:
            self.rotate_towards(self.rotation_speed * delta_time)

        return super().on_update(delta_time)

    def init_rotation(self, target: float, speed: float) -> None:
        if target == self.target_rotation:
            return
        self.target_rotation = target
        self.rotation_speed = abs(speed)

    def rotate_towards(self, rotation_speed) -> None:
        rotation_difference = self.target_rotation - self.parent.transform.rot
        if abs(rotation_difference) <= rotation_speed:
            rotation = rotation_difference
            self.rotation_speed = 0
        else:
            rotation = rotation_speed if rotation_difference > 0 else -rotation_speed
        self.rotate(rotation)
    
    @abstractmethod
    def rotate(self, angle: float) -> None:
        self.parent.transform.rot += angle


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
        self.points = [self.parent.transform.pos + p.rotate(angle + self.parent.transform.rot) for p in self.__relative_points]
        return super().rotate(angle)
