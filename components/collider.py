from components.component import Component


class Collider(Component):
    def __init__(self) -> None:
        super().__init__()

    pass


class CircleCollider(Collider):
    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius = radius


class PolygonCollider(Collider):
    def __init__(self, relative_points: list) -> None:
        super().__init__()
        self.points = relative_points

    def on_init(self) -> None:
        self.points = [self.parent.transform.pos + p for p in self.points]
        
        return super().on_init()
