import pygame
from api.components.component import Component

from api.components.mesh import CircleMesh, Mesh, PolygonMesh

class Renderer(Component):
    def __init__(self, visible:bool = True) -> None:
        super().__init__()

        self.visible: bool = visible

        self.mesh: Mesh = None # type: ignore
        self.mesh_type: type = None # type: ignore

    def on_init(self) -> None:
        self.get_mesh()
        return super().on_init()
    
    def on_late_update(self, delta_time: float) -> None:
        if not self.visible:
            return super().on_update(delta_time)

        if(self.mesh_type == CircleMesh):
            self.mesh: CircleMesh = self.mesh # type: ignore
            pygame.draw.circle(self.parent.scene.screen, self.mesh.color, (self.parent.transform.pos.x, self.parent.transform.pos.y), self.mesh.radius) # type: ignore
        
        elif(self.mesh_type == PolygonMesh):
            self.mesh: PolygonMesh = self.mesh # type: ignore
            pygame.draw.polygon(self.parent.scene.screen, self.mesh.color, self.mesh.points)

        return super().on_update(delta_time)

    def get_mesh(self) -> None:
        mesh = self.parent.get_component_by_class(Mesh)
        if not mesh:
            raise Exception(f"No Mesh found on {self.parent}")

        self.mesh = mesh
        self.mesh_type = type(mesh)

    def serialize(self) -> dict:
        return {
        }
    
    def deserialize(self, data: dict) -> 'Renderer':
        return self
