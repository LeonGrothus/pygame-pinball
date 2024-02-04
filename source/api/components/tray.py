import pygame
from source.api.components.component import Component
from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh
from source.api.components.renderer import Renderer
from data.constants import DELTA_TIME


class Tray(Component):
    """
    The Tray class is responsible for rendering the visual representation of an entity in the game scene.
    It also adds a tray effect to the entity. But the tray effect with alpha is extremly slow because the pygame build
    does not support the AVX2 extension and the bilt can not be computed efficiently.

    Attributes:
        visible (bool): Whether the renderer is visible or not.
        mesh (Mesh): The mesh component of the parent entity.
        mesh_type (type): The type of the mesh component of the parent entity.
        capture_interval (int): The interval in which the tray is captured
        color (pygame.Color): The color of the tray
        fade_out_time (float): The time it takes for the tray to fade out
        delta_alpha (float): The change in alpha per frame
        frame_counter (int): The frame counter
        pos_and_alpha_values (list[tuple[tuple[int, int], float]]): The list of positions and alpha values of the tray
        screen (pygame.Surface): The screen of the game
        surface (pygame.Surface): The surface of the tray

    Methods:
        __init__(self, visible: bool = True)
        on_init(self)
        on_late_update(self, delta_time: float)
        get_mesh(self)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Renderer'
    """

    def __init__(self, capture_interval: int, color: pygame.Color, fade_out_time: float = .5) -> None:
        """
        Initializes the tray component.

        Arguments:
            capture_interval (int): The interval in which the tray is captured
            color (pygame.Color): The color of the tray
            fade_out_time (float): The time it takes for the tray to fade out
        """

        super().__init__()
        self.capture_interval = capture_interval
        self.color = color
        self.delta_alpha = 255/fade_out_time*DELTA_TIME

        self.frame_counter = 0
        self.pos_and_alpha_values: list[tuple[tuple[int, int], float]] = []
        self.screen = None
        self.surface = None

    def on_init(self) -> None:
        """
        Called when the tray component is initialized.

        Returns:
            None
        """
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
        """
        Called when the tray component is updated.

        Arguments:
            delta_time (float): The time since the last frame.

        Returns:
            None
        """

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
        """
        Serializes the tray component data into a dictionary.

        Returns:
            dict: The serialized tray data.
        """

        return {
            "capture_interval": self.capture_interval,
            "color": self.color
        }

    def deserialize(self, data: dict) -> 'Tray':
        """
        Deserializes the tray component data from a dictionary.

        Arguments:
            data (dict): The serialized tray data.

        Returns:
            Tray: The deserialized tray component.
        """
        
        self.capture_interval = data["capture_interval"]
        self.color = data["color"]
        return self
