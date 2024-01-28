import pygame
import math
from source.api.components.component import Component
from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh

class ScaleRenderer(Component):
    """
    The ScaleRenderer class is responsible for rendering the visual representation of an entity in the game scene.
    It also adds a scale effect to the entity. The scale effect is triggered when the entity collides with another entity.

    Attributes:
        visible (bool): Whether the renderer is visible or not.
        mesh (Mesh): The mesh component of the parent entity.
        mesh_type (type): The type of the mesh component of the parent entity.

    Methods:
        __init__(self, visible: bool = True)
        on_init(self)
        on_late_update(self, delta_time: float)
        get_mesh(self)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Renderer'
    """

    def __init__(self, duration: float = .1, strength: float = .2, overlay_effect = True, overlay_effect_size = 1) -> None:
        """
        Initializes the renderer component.

        Arguments:
            visible (bool, optional): Whether the renderer is visible or not. Defaults to True.
        """

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
        """
        Called when the renderer component is initialized.

        Returns:
            None
        """
        self.get_mesh()
        if self.mesh_type == PolygonMesh:
            self.avg_point = (sum(x for x, _ in self.mesh.points) / len(self.mesh.points), 
                            sum(y for _, y in self.mesh.points) / len(self.mesh.points))
        return super().on_init()
    

    def on_collision(self, other, point, normal) -> None:
        """
        Override the on_collision method to reset the duration of the scale effect.
        
        Arguments:
            other: GameObject, the other game object
            point: Vector2, the point of collision
            normal: Vector2, the normal of collision

        Returns:
            None
        """

        self.duration = self.original_duration
        return super().on_collision(other, point, normal)

    def on_late_update(self, delta_time: float) -> None:
        """
        Called when the renderer component is updated.

        Arguments:
            delta_time (float): The time since the last frame.

        Returns:
            None
        """

        if self.duration <= 0:
            return super().on_update(delta_time)
        
        self.duration -= delta_time # Update the duration
        # Calculate the scale based on the duration
        scale = 1 + abs(math.sin(math.pi * (self.original_duration - self.duration) / self.original_duration)) * self.strength

        if self.mesh_type == CircleMesh: # If the mesh is a circle
            self.mesh: CircleMesh = self.mesh # type: ignore
            # Draw the circle
            pygame.draw.circle(self.parent.scene.screen, self.mesh.color, (self.parent.transform.pos.x, self.parent.transform.pos.y), self.mesh.radius * scale) # type: ignore

            if self.overlay_effect: # If the overlay effect is enabled
                # Create a new surface for the overlay
                size = self.mesh.radius * self.overlay_effect_size * 2 * scale # type: ignore
                # Draw the overlay
                overlay_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                # Draw the circle on the overlay surface
                pygame.draw.circle(overlay_surface, self.overlay_color + (self.overlay_alpha,), (size / 2, size / 2), size / 2) # type: ignore
                # Blit the overlay surface to the screen
                # Inefficient, but it works
                self.parent.scene.screen.blit(overlay_surface, (self.parent.transform.pos.x - size / 2, self.parent.transform.pos.y - size / 2)) # type: ignore
        
        elif self.mesh_type == PolygonMesh:
            # Draw the polygon
            self.mesh: PolygonMesh = self.mesh # type: ignore
            # Calculate the scaled points
            scaled_points = [((x - self.avg_point[0]) * scale + self.avg_point[0], 
                                (y - self.avg_point[1]) * scale + self.avg_point[1]) for x, y in self.mesh.points]
            pygame.draw.polygon(self.parent.scene.screen, self.mesh.color, scaled_points)

            if self.overlay_effect: # If the overlay effect is enabled
                # Create a new surface for the overlay
                overlay_surface = pygame.Surface((self.parent.scene.screen.get_width(), self.parent.scene.screen.get_height()), pygame.SRCALPHA)
                # Calculate the scaled points
                scaled_points_overlay = [((x - self.avg_point[0]) * scale * self.overlay_effect_size + self.avg_point[0], 
                                          (y - self.avg_point[1]) * scale * self.overlay_effect_size + self.avg_point[1]) for x, y in self.mesh.points]
                # Draw the overlay
                pygame.draw.polygon(overlay_surface, self.overlay_color + (self.overlay_alpha,), scaled_points_overlay)
                # Blit the overlay surface to the screen
                # Inefficient, but it works
                self.parent.scene.screen.blit(overlay_surface, (0, 0))

        return super().on_update(delta_time)
    
    def get_mesh(self) -> None:
        """
        Gets the mesh of the parent.

        Returns:
            None
        """
        
        mesh = self.parent.get_component_by_class(Mesh)
        if not mesh:
            raise Exception(f"No Mesh found on {self.parent}")

        self.mesh = mesh
        self.mesh_type = type(mesh)

    def serialize(self) -> dict:
        """
        Serializes the renderer component data into a dictionary.

        Returns:
            dict: The serialized renderer data.
        """
        return {
        }
    
    def deserialize(self, data: dict) -> 'ScaleRenderer':
        """
        Deserializes the renderer component data from a dictionary.

        Arguments:
            data (dict): The serialized renderer data.

        Returns:
            Renderer: The deserialized renderer component.
        """
        return self