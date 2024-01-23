import pygame
from api.components.component import Component
from api.components.mesh import CircleMesh, Mesh, PolygonMesh
from api.components.renderer import Renderer
from constants import DELTA_TIME


class Tray(Component):
    def __init__(self, capture_interval: int, color: pygame.Color, fade_out_time: float = .5):
        super().__init__()
        self.capture_interval = capture_interval
        self.color = color
        self.delta_alpha = 255/fade_out_time*DELTA_TIME

        self.frame_counter = 0
        self.pos_and_alpha_values: list[tuple[tuple[int, int], float]] = []
        self.screen = None
        self.surface = None

    def on_init(self) -> None:
        self.mesh = self.parent.get_component_by_class(Mesh)  # type: ignore
        self.mesh_type = type(self.mesh)
        self.renderer = self.parent.get_component_by_class(Renderer)
        if not self.mesh or not self.renderer:
            raise Exception(f"No Mesh or Renderer found on {self.parent}")

        # Create the surface and draw the shape
        self.surface = pygame.Surface(self.mesh.size, pygame.SRCALPHA)
        if self.mesh_type == CircleMesh:
            self.mesh: CircleMesh = self.mesh  # type: ignore
            pygame.draw.circle(self.surface, self.color, (self.mesh.radius,
                               self.mesh.radius), self.mesh.radius)  # type: ignore
        elif self.mesh_type == PolygonMesh:
            self.mesh: PolygonMesh = self.mesh  # type: ignore
            pygame.draw.polygon(self.surface, self.color, self.mesh.points)

    def on_update(self, delta_time: float) -> None:
        self.frame_counter += 1
        if self.frame_counter % self.capture_interval == 0:
            self.frame_counter = 0
            self.pos_and_alpha_values.append(((int(self.parent.transform.pos.x-self.mesh.size.x/2), int(self.parent.transform.pos.y-self.mesh.size.y/2)), 255))

        for pos, alpha in self.pos_and_alpha_values:
            # Update the alpha value of the surface
            self.surface.set_alpha(int(alpha))  # type: ignore
            self.parent.scene.screen.blit(self.surface, pos)

        # Decrease the alpha value of all surfaces
        self.pos_and_alpha_values = [(pos, alpha-self.delta_alpha) for pos, alpha in self.pos_and_alpha_values if alpha-self.delta_alpha > 0]
        return super().on_update(delta_time)

    def serialize(self) -> dict:
        return {
            "capture_interval": self.capture_interval,
            "color": self.color
        }

    def deserialize(self, data: dict) -> 'Tray':
        self.capture_interval = data["capture_interval"]
        self.color = data["color"]
        return self
