from components.component import Component
from components.mesh import CircleMesh, Mesh, PolygonMesh


class Collider(Component):
    def __init__(self) -> None:
        self.mesh: Mesh = None  # type: ignore
        super().__init__()

    def on_init(self) -> None:
        self.get_mesh()
        return super().on_init()

    def get_mesh(self) -> None:
        mesh = self.parent.get_component_by_class(Mesh)
        if mesh:
            self.mesh = mesh
            self.mesh_type = type(mesh)
        else:
            print(f"No mesh to Render found on {self.parent}")


class CircleCollider(Collider):
    def __init__(self) -> None:
        super().__init__()
        self.radius: float = None  # type: ignore

    def on_init(self) -> None:
        self.get_mesh()

        if (self.mesh_type == CircleMesh):
            self.radius = self.mesh.radius  # type: ignore
        else:
            print(f"No mesh to form Collider found on {self.parent} with Mesh type {type(self.mesh)}")


class PolygonCollider(Collider):
    def __init__(self) -> None:
        super().__init__()
        self.points: list = None # type: ignore

    def on_init(self) -> None:
        self.get_mesh()

        if (self.mesh_type == PolygonMesh):
            self.points = self.mesh.points  # type: ignore
        else:
            print(f"No mesh to form Collider found on {self.parent} with Mesh type {type(self.mesh)}")
