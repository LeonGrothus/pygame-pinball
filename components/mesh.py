from abc import ABC, abstractmethod
import math
import numpy as np
from pygame import Color, Vector2
from components.component import Component


class Mesh(Component, ABC):
    def __init__(self, color: Color) -> None:
        self.color: Color = color

        self.target_rot: float = 0
        self.rotation_speed: float = 0
        super().__init__()

    def on_init(self) -> None:
        self.target_rot = self.parent.transform.rot
        return super().on_init()

    def on_update(self, delta_time: float) -> None:
        if self.parent.transform.rot != self.target_rot:
            self.rotate(np.clip(self.rotation_speed * delta_time + self.parent.transform.rot, -math.inf, self.target_rot) - self.parent.transform.rot)

        return super().on_update(delta_time)

    def rotate_towards(self, target: float, speed: float) -> None:
        self.target_rot = target
        self.rotation_speed = speed

        self.parent.transform.rot += speed

        if self.parent.transform.rot > target:
            self.parent.transform.rot = target
    
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
        self.points = relative_points

    def on_init(self) -> None:
        self.points = [self.parent.transform.pos + p for p in self.points]
        
        return super().on_init()
    
    def rotate(self, angle: float) -> None:
        p: Vector2
        for p in self.points:
            p.rotate_ip(angle)
        return super().rotate(angle)
