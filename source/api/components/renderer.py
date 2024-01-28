import pygame
from source.api.components.component import Component

from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh

class Renderer(Component):
    """
    The Renderer class is responsible for rendering the visual representation of an entity in the game scene.

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

    def __init__(self, visible: bool = True) -> None:
        """
        Initializes the renderer component.

        Arguments:
            visible (bool, optional): Whether the renderer is visible or not. Defaults to True.
        """

        super().__init__()

        self.visible: bool = visible

        self.mesh: Mesh = None  # type: ignore
        self.mesh_type: type = None  # type: ignore

    def on_init(self) -> None:
        """
        Called when the renderer component is initialized.

        Returns:
            None
        """

        self.get_mesh()
        return super().on_init()

    def on_late_update(self, delta_time: float) -> None:
        """
        Called when the renderer component is updated.

        Arguments:
            delta_time (float): The time since the last frame.
        
        Returns:
            None
        """

        if not self.visible:
            return super().on_update(delta_time)

        if self.mesh_type == CircleMesh:
            self.mesh: CircleMesh = self.mesh  # type: ignore
            pygame.draw.circle(
                self.parent.scene.screen,
                self.mesh.color,
                (self.parent.transform.pos.x, self.parent.transform.pos.y),
                self.mesh.radius, # type: ignore
            )

        elif self.mesh_type == PolygonMesh:
            self.mesh: PolygonMesh = self.mesh  # type: ignore
            pygame.draw.polygon(
                self.parent.scene.screen,
                self.mesh.color,
                self.mesh.points,
            )

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
        return {}

    def deserialize(self, data: dict) -> 'Renderer':
        """
        Deserializes the renderer component data from a dictionary.

        Arguments:
            data (dict): The serialized renderer data.

        Returns:
            Renderer: The deserialized renderer component.
        """
        return self