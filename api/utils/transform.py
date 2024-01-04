from pygame import Vector2


class Transform:
    def __init__(self, parent) -> None:
        self.parent = parent

        self.scale: Vector2 = Vector2() # should be deprecated
        self.pos: Vector2 = Vector2()
        self.rot: float = 0

        self.__mesh = None

    def get_origin(self) -> Vector2: # should be deprecated
        return Vector2(self.pos.x - self.scale.x / 2, self.pos.y - self.scale.y / 2)

    def rotate_towards(self, target: float, speed: float) -> None:
        if not self.__mesh:
            self.__mesh = self.parent.get_components_by_class_scuffed("PolygonMesh", "CircleMesh")
            if not self.__mesh:
                raise Exception(f"No Mesh found on {self.parent}")

        self.__mesh.init_rotation(target, speed)