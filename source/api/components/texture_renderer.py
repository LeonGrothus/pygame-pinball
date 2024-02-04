from pathlib import Path
import pygame
from source.api.components.component import Component

from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh

class TextureRenderer(Component):
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

    def __init__(self, texture_path: Path, width: float, height: float, visible: bool = True, alpha: int = 200) -> None:
        """
        Initializes the renderer component.

        Arguments:
            visible (bool, optional): Whether the renderer is visible or not. Defaults to True.
        """

        super().__init__()

        self.width = width
        self.height = height
        self.textur_path = texture_path
        self.texture = pygame.image.load(texture_path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (int(width), int(height)))
        self.texture.set_alpha(alpha)
        self.visible: bool = visible
        self.screen = pygame.display.get_surface()

    def on_init(self) -> None:
        """
        Called when the renderer component is initialized.

        Returns:
            None
        """
        self.rotate(self.parent.transform.rot.get_value())
        self.parent.transform.rot.subscribe(self.rotate)
        return super().on_init()

    def on_late_update(self, delta_time: float) -> None:
        """
        Called when the renderer component is updated.

        Arguments:
            delta_time (float): The time since the last frame.
        
        Returns:
            None
        """
        self.screen.blit(self.rotated_texture, self.rotated_rect.topleft)
        return super().on_update(delta_time)
    

    def rotate(self, angle: float) -> None:
        """
        Rotates the renderer component by the given angle.

        Arguments:
            angle (float): The angle to rotate the renderer by.
        
        Returns:
            None
        """
        self.rotated_texture = pygame.transform.rotate(self.texture, -angle)
        self.rotated_rect = self.rotated_texture.get_rect(center = self.texture.get_rect(center = (self.parent.transform.pos.x, self.parent.transform.pos.y)).center)

    def serialize(self) -> dict:
        """
        Serializes the renderer component data into a dictionary.

        Returns:
            dict: The serialized renderer data.
        """
        return {
            "textur_path": self.textur_path,
            "width": self.width,
            "height": self.height,
            "visible": self.visible
        }

    def deserialize(self, data: dict) -> 'TextureRenderer':
        """
        Deserializes the renderer component data from a dictionary.

        Arguments:
            data (dict): The serialized renderer data.

        Returns:
            Renderer: The deserialized renderer component.
        """
        self.textur_path = data["textur_path"]
        self.width = data["width"]
        self.height = data["height"]
        self.visible = data["visible"]
        self.texture = pygame.image.load(self.textur_path).convert_alpha()
        return self