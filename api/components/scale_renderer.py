import pygame
import math
from api.components.component import Component
from api.components.mesh import CircleMesh, Mesh, PolygonMesh

class ScaleRenderer(Component):
    def __init__(self, duration: float, strength: float, overlay_effect = True, overlay_effect_size = 1) -> None:
        super().__init__()
        self.original_duration: float = duration
        self.strength: float = strength
        self.duration: float = 0.0

        self.mesh: Mesh = None # type: ignore
        self.mesh_type: type = None # type: ignore

        self.overlay_effect = overlay_effect  
        self.overlay_alpha = 75  # Set the alpha value for the white overlay
        self.overlay_color = (255, 255, 255)  # White color
        self.overlay_effect_size = overlay_effect_size

    def on_init(self) -> None:
        self.get_mesh()
        if self.mesh_type == PolygonMesh:
            self.avg_point = (sum(x for x, _ in self.mesh.points) / len(self.mesh.points), 
                            sum(y for _, y in self.mesh.points) / len(self.mesh.points))
        return super().on_init()
    

    def on_collision(self, other, point, normal) -> None:
        self.duration = self.original_duration
        return super().on_collision(other, point, normal)

    def on_update(self, delta_time: float) -> None:
        if self.duration <= 0:
            return super().on_update(delta_time)
        
        self.duration -= delta_time
        scale = 1 + abs(math.sin(math.pi * (self.original_duration - self.duration) / self.original_duration)) * self.strength

        if self.mesh_type == CircleMesh:
            self.mesh: CircleMesh = self.mesh # type: ignore
            pygame.draw.circle(self.parent.scene.screen, self.mesh.color, (self.parent.transform.pos.x, self.parent.transform.pos.y), self.mesh.radius * scale) # type: ignore

            if self.overlay_effect:
                # Create a new surface for the overlay
                size = self.mesh.radius * self.overlay_effect_size * 2 * scale # type: ignore
                overlay_surface = pygame.Surface((size, size), pygame.SRCALPHA) # type: ignore
                pygame.draw.circle(overlay_surface, self.overlay_color + (self.overlay_alpha,), (size / 2, size / 2), size / 2) # type: ignore
                self.parent.scene.screen.blit(overlay_surface, (self.parent.transform.pos.x - size / 2, self.parent.transform.pos.y - size / 2)) # type: ignore
        
        elif self.mesh_type == PolygonMesh:
            self.mesh: PolygonMesh = self.mesh # type: ignore
            scaled_points = [((x - self.avg_point[0]) * scale + self.avg_point[0], 
                                (y - self.avg_point[1]) * scale + self.avg_point[1]) for x, y in self.mesh.points]
            pygame.draw.polygon(self.parent.scene.screen, self.mesh.color, scaled_points)

            if self.overlay_effect:
                # Create a new surface for the overlay
                overlay_surface = pygame.Surface((self.parent.scene.screen.get_width(), self.parent.scene.screen.get_height()), pygame.SRCALPHA)
                scaled_points_overlay = [((x - self.avg_point[0]) * scale * self.overlay_effect_size + self.avg_point[0], 
                                          (y - self.avg_point[1]) * scale * self.overlay_effect_size + self.avg_point[1]) for x, y in self.mesh.points]
                pygame.draw.polygon(overlay_surface, self.overlay_color + (self.overlay_alpha,), scaled_points_overlay)
                self.parent.scene.screen.blit(overlay_surface, (0, 0))

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
    
    def deserialize(self, data: dict) -> 'ScaleRenderer':
        return self