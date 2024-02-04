from abc import ABC
from source.api.components.component import Component
from source.api.components.mesh import CircleMesh, Mesh, PolygonMesh
from data.constants import COLLISION_FRICTION


class Collider(Component, ABC):
    """
    A class to represent a Collider. A collider is a component that can collide with other colliders. 

    Attributes:
        is_trigger: bool, whether the collider is a trigger
        friction: float, the friction of the collider
        mesh: Mesh, the mesh of the collider

    Methods:
        __init__(self, is_trigger: bool, friction: float)
        on_init(self)
        get_mesh(self)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Collider'
    """

    def __init__(self, is_trigger: bool, friction: float) -> None:
        """
        Inits Collider with is_trigger and friction
        
        Arguments:
            is_trigger: bool, whether the collider is a trigger
            friction: float, the friction of the collider
        """

        self.is_trigger: bool = is_trigger
        self.friction: float = friction

        self.mesh: Mesh = None  # type: ignore
        super().__init__()

    def on_init(self) -> None:
        """
        Gets the mesh of the parent

        Returns:
            None
        """

        self.get_mesh()
        return super().on_init()

    def get_mesh(self) -> None:
        """
        Gets the mesh of the parent

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
        Serializes the Collider

        Returns:
            dict: a dictionary containing the Collider's data
        """

        return {
            "is_trigger": self.is_trigger
        }

    def deserialize(self, data: dict) -> 'Collider':
        """
        Deserializes the Collider

        Arguments:
            data: dict, a dictionary containing the Collider's data

        Returns:
            Collider: the modified Collider instance
        """

        self.is_trigger = data["is_trigger"]
        return self


class CircleCollider(Collider):
    """
    CircleCollider inherits from Collider

    Attributes:
        is_trigger: bool, whether the collider is a trigger
        friction: float, the friction of the collider
        mesh: CircleMesh, the mesh of the collider

    Methods:
        __init__(self, is_trigger: bool, friction: float)
    """

    def __init__(self, is_trigger = False, friction: float = COLLISION_FRICTION) -> None:
        """
        Inits CircleCollider with is_trigger and friction

        Arguments:
            is_trigger: bool, whether the collider is a trigger
            friction: float, the friction of the collider
        """

        super().__init__(is_trigger, friction)

        self.mesh: CircleMesh = None  # type: ignore


class PolygonCollider(Collider):
    """
    PolygonCollider inherits from Collider

    Attributes:
        is_trigger: bool, whether the collider is a trigger
        friction: float, the friction of the collider
        mesh: PolygonMesh, the mesh of the collider

    Methods:
        __init__(self, is_trigger: bool, friction: float)
    """

    def __init__(self, is_trigger = False, friction: float = COLLISION_FRICTION) -> None:
        """
        Inits PolygonCollider with is_trigger and friction

        Arguments:
            is_trigger: bool, whether the collider is a trigger
            friction: float, the friction of the collider
        """
    
        super().__init__(is_trigger, friction)

        self.mesh: PolygonMesh = None  # type: ignore
