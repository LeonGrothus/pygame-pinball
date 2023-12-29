from pygame import Color
from components.component import Component


class Mesh(Component):
    def __init__(self, color: Color) -> None:
        self.color: Color = color
        super().__init__()


class CircleMesh(Mesh):
    def __init__(self, color: Color, radius: float) -> None:
        super().__init__(color)
        self.radius = radius


class PolygonMesh(Mesh):
    def __init__(self, color: Color, relative_points: list) -> None:
        super().__init__(color)
        self.points = relative_points

    def on_init(self) -> None:
        self.points = [self.parent.transform.pos + p for p in self.points]
        
        return super().on_init()
