from abc import ABC
from api.components.component import Component
from api.components.mesh import CircleMesh, Mesh, PolygonMesh


class Collider(Component, ABC):
    def __init__(self, is_trigger) -> None:
        self.is_trigger: bool = is_trigger

        self.mesh: Mesh = None  # type: ignore
        super().__init__()

    def on_init(self) -> None:
        self.get_mesh()
        return super().on_init()

    def get_mesh(self) -> None:
        mesh = self.parent.get_component_by_class(Mesh)
        if not mesh:
            raise Exception(f"No Mesh found on {self.parent}")

        self.mesh = mesh
        self.mesh_type = type(mesh)

    def serialize(self) -> dict:
        return {
            "is_trigger": self.is_trigger
        }

    def deserialize(self, data: dict) -> 'Collider':
        self.is_trigger = data["is_trigger"]
        return self


class CircleCollider(Collider):
    def __init__(self, is_trigger: bool = False) -> None:
        super().__init__(is_trigger)

        self.mesh: CircleMesh = None  # type: ignore


class PolygonCollider(Collider):
    def __init__(self, is_trigger: bool = False) -> None:
        super().__init__(is_trigger)

        self.mesh: PolygonMesh = None  # type: ignore
