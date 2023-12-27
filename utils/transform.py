from pygame import Vector2


class Transform:
    def __init__(self) -> None:
        self.scale: Vector2 = Vector2()
        self.pos: Vector2 = Vector2()
        self.rot: float = 0

    def get_origin(self) -> Vector2:
        return Vector2(self.pos.x - self.scale.x / 2, self.pos.y - self.scale.y / 2)
