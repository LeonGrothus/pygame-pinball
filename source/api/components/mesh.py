from abc import ABC, abstractmethod

from pygame import Color, Vector2
from source.api.components.component import Component
from source.api.management.options_manager import OptionsManager


class Mesh(Component, ABC):
    """
    A class to represent a Mesh. A mesh is a visual representation of a GameObject.

    Attributes:
        color: Color, the color of the mesh
        target_rotation: float, the target rotation of the mesh
        rotation_speed: float, the rotation speed of the mesh

    Methods:
        __init__(self, color: Color)
        on_init(self)
        on_destroy(self)
        rotate(self, angle: float)
        _set_size(self) -> Vector2
    """

    def __init__(self, color: Color) -> None:
        """
        Inits Mesh with color

        Arguments:
            color: Color, the color of the mesh
        """
        self.color: Color = color

        self.target_rotation: float = 0
        self.rotation_speed: float = 0
        super().__init__()

    def on_init(self) -> None:
        """
        Initializes the mesh and subscribes to the rotation of the parent

        Returns:
            None
        """

        self.parent.transform.rot.subscribe(self.rotate)
        self.size = self._set_size()
        return super().on_init()

    def on_destroy(self) -> None:
        """
        Unsubscribes from the rotation of the parent

        Returns:
            None
        """
        self.parent.transform.rot.unsubscribe(self.rotate)
        return super().on_destroy()
    
    ### Abstract methods ###

    @abstractmethod
    def rotate(self, angle: float) -> None:
        """
        Rotates the mesh

        Arguments:
            angle: float, the angle to rotate the mesh by

        Returns:
            None
        """
        pass

    @abstractmethod
    def _set_size(self) -> Vector2:
        """
        Sets the size of the mesh

        Returns:
            Vector2: the size of the mesh
        """
        pass


class CircleMesh(Mesh):
    """
    A class representing a circle mesh. A circle mesh is a visual representation of a circle.

    Attributes:
        color (Color): The color of the circle.
        radius (float): The radius of the circle.
    """

    def __init__(self, color: Color = Color(255, 255, 255), radius: float = 25) -> None:
        """
        Initialize a CircleMesh object.

        Arguments:
            color (Color, optional): The color of the circle. Defaults to Color(255, 255, 255).
            radius (float, optional): The radius of the circle. Defaults to 25.
        """
        super().__init__(color)
        self.radius = radius

    def serialize(self) -> dict:
        """
        Serialize the CircleMesh object.

        Returns:
            dict: The serialized representation of the CircleMesh object.
        """
        return {
            "radius": self.radius/OptionsManager().asf
        }

    def deserialize(self, data: dict) -> 'CircleMesh':
        """
        Deserialize the CircleMesh object.

        Args:
            data (dict): The serialized data of the CircleMesh object.

        Returns:
            CircleMesh: The deserialized CircleMesh object.
        """
        self.radius = data["radius"]*OptionsManager().asf
        return self

    def rotate(self, angle: float) -> None:
        """
        Rotate the CircleMesh object.

        Args:
            angle (float): The angle to rotate the circle by.
        """
        return super().rotate(angle)
    
    def _set_size(self) -> Vector2:
        """
        Calculate and set the size of the CircleMesh object.

        Returns:
            Vector2: The size of the CircleMesh object.
        """
        return Vector2(self.radius*2, self.radius*2)


class PolygonMesh(Mesh):
    """
    A class to represent a PolygonMesh. A PolygonMesh is a visual representation of a polygon.

    Attributes:
        color: Color, the color of the mesh
        points: list[Vector2], the points of the mesh
        _relative_points: list[Vector2], the relative points of the mesh

    Methods:
        __init__(self, color: Color, relative_points: list[Vector2])
        on_init(self)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'PolygonMesh'
        rotate(self, angle: float)
        _set_size(self) -> Vector2
    """

    def __init__(self, color: Color, relative_points: list[Vector2]) -> None:
        """
        Initialize a PolygonMesh object.

        Arguments:
            color (Color): The color of the mesh.
            relative_points (list[Vector2]): The list of relative points that define the shape of the mesh.
        """
        super().__init__(color)

        self._relative_points: list[Vector2] = relative_points
        self.points: list[Vector2] = relative_points

    def on_init(self) -> None:
        """
        Perform initialization tasks for the mesh.

        Returns:
            None
        """
        self.points = [self.parent.transform.pos + p for p in self.points]
        return super().on_init()

    def serialize(self) -> dict:
        """
        Serialize the mesh object into a dictionary.

        Returns:
            dict: The serialized mesh object.
        """
        return {
            "relative_points": [
                {
                    "x": p.x,
                    "y": p.y
                } for p in self._relative_points
            ],
            "color": {
                "r": self.color.r,
                "g": self.color.g,
                "b": self.color.b,
                "a": self.color.a
            }
        }

    def deserialize(self, data: dict) -> 'PolygonMesh':
        """
        Deserialize the mesh object from a dictionary.

        Arguments:
            data (dict): The dictionary containing the serialized mesh data.

        Returns:
            PolygonMesh: The deserialized mesh object.
        """
        self._relative_points = [Vector2(p["x"], p["y"]) for p in data["relative_points"]]
        self.color = Color(data["color"]["r"], data["color"]["g"], data["color"]["b"], data["color"]["a"])
        return self

    def rotate(self, angle: float) -> None:
        """
        Rotate the mesh by a given angle.

        Arguments:
            angle (float): The angle of rotation in degrees.

        Returns:
            None
        """
        self.points = [self.parent.transform.pos + p.rotate(angle) for p in self._relative_points]
        return super().rotate(angle)
    
    def _set_size(self) -> Vector2:
        """
        Calculate and return the size of the mesh.

        Returns:
            Vector2: The size of the mesh.
        """
        return Vector2(max(p.x for p in self.points) - min(p.x for p in self.points),
                            max(p.y for p in self.points) - min(p.y for p in self.points))
