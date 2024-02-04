from pygame import Color, Surface, Vector2
import pygame
from data.constants import DEFAULT_FONT
from source.api.components.component import Component
from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh
from source.api.management.options_manager import OptionsManager
from source.api.objects.game_object import GameObject
from pygame.freetype import Font


class TextObject:
    """
    This class should only be used as a parameter for the ChangeScore class.

    Arguments:
        alpha (int): The transparency value of the text object.
        pos (Vector2): The position of the text object.

    Attributes:
        alpha (int): The transparency value of the text object.
        pos (Vector2): The position of the text object.
    """

    def __init__(self, alpha: int, pos: Vector2) -> None:
        """
        Initialize the ChangeScore component.

        Args:
            alpha (int): The alpha value.
            pos (Vector2): The position vector.
        """
        self.alpha = alpha
        self.pos = pos


class ChangeScore(Component):
    """
    A class to represent a ChangeScore. A ChangeScore is a component that changes the score by a given amount when it is hit. 

    Attributes:
        add_to_score (int): The score to add when a collision occurs.
        speed (float): The speed at which the score text moves upwards.
        alpha_decrease (int): The amount by which the alpha of the score text decreases each frame.
        font (pygame.font.Font): The font used to render the score text.
        text_surface (pygame.Surface): The pre-rendered text surface.
        text_objects (list[TextObject]): The list of text objects currently being displayed.

    Methods:
        __init__(self, add_to_score: int = 10, speed: float = 1.0, alpha_decrease: int = 1)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
        on_update(self, delta_time: float) -> None
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'ChangeScore'
    """

    def __init__(self, add_to_score: int = 10, show_text: bool = False, text_size: float = 1, speed: float = 1, alpha_decrease: int = 10, text_color: Color = Color(255, 255, 255)) -> None:
        """
        Inits ChangeScore with add_to_score, speed, and alpha_decrease.

        Arguments:
            add_to_score (int): The score to add when a collision occurs.
            speed (float): The speed at which the score text moves upwards.
            alpha_decrease (int): The amount by which the alpha of the score text decreases each frame.
        """
        super().__init__()
        self.add_to_score = add_to_score
        self.speed = speed
        self.alpha_decrease = alpha_decrease

        self.show_text = show_text
        if not self.show_text:
            return

        self.font = Font(DEFAULT_FONT, 20*OptionsManager().asf * text_size)
        text = str(self.add_to_score)
        self.text_size = self.font.get_rect(text).size
        self.text_surface = pygame.Surface(self.text_size, pygame.SRCALPHA)
        self.font.render_to(self.text_surface, (0, 0), text, text_color)
        self.text_objects: list[TextObject] = []

    def on_init(self) -> None:
        """
        Called when the renderer component is initialized.

        Returns:
            None
        """
        self.get_mesh()
        if self.mesh_type == PolygonMesh:
            self.cms = (sum(x for x, _ in self.mesh.points) / len(self.mesh.points),
                        sum(y for _, y in self.mesh.points) / len(self.mesh.points))
        if self.mesh_type == CircleMesh:
            self.cms = None
        return super().on_init()

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2):
        """
        Adds add_to_score to the score and creates a new text object.

        Arguments:
            other (GameObject): The other object.
            point (Vector2): The point of collision.
            normal (Vector2): The normal of the collision.
        """
        self.parent.scene.score += self.add_to_score

        if not self.show_text:
            return super().on_collision(other, point, normal)
        text_object = TextObject(255, Vector2(self.cms if self.cms else self.parent.transform.pos))
        self.text_objects.append(text_object)
        return super().on_collision(other, point, normal)

    def on_late_update(self, delta_time: float) -> None:
        """
        Moves the text objects upwards and decreases their alpha.

        Arguments:
            delta_time (float): The time since the last frame.

        Returns:
            None
        """
        if not self.show_text:
            return super().on_late_update(delta_time)

        for text_object in self.text_objects:
            text_object.pos.y -= self.speed
            text_object.alpha -= self.alpha_decrease
            self.text_surface.set_alpha(text_object.alpha)
            self.parent.scene.screen.blit(self.text_surface, text_object.pos - Vector2(self.text_size) / 2)
        self.text_objects = [text_object for text_object in self.text_objects if text_object.alpha > 0]
        return super().on_late_update(delta_time)

    def serialize(self) -> dict:
        """
        Serializes the ChangeScore

        Returns:
            dict: a dictionary containing the ChangeScore's data
        """

        return {
            "add_to_score": self.add_to_score
        }

    def deserialize(self, data: dict) -> 'ChangeScore':
        """
        Deserializes the ChangeScore

        Arguments:
            data: dict, the data to deserialize

        Returns:
            ChangeScore: the modified ChangeScore instance
        """
        self.add_to_score = data["add_to_score"]
        return self

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
