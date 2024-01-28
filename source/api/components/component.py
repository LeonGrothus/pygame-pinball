from abc import ABC, abstractmethod

from pygame import Vector2

from source.api.objects.game_object import GameObject


class Component(ABC):
    """
    A class to represent a Component. A component is a part of a GameObject. A component can be added to a GameObject.
    The component is updated every frame. A component can be serialized and deserialized. A component can be initialized

    Attributes:
        parent: GameObject, the parent of the component

    Methods:
        __init__(self)
        set_parent(self, parent: GameObject)
        on_init(self)
        on_destroy(self)
        on_update(self, delta_time: float)
        on_late_update(self, delta_time: float)
        on_collision(self, other: GameObject, point: Vector2, normal: Vector2)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Component'
    """

    def __init__(self) -> None:
        """
        Inits Component with parent

        Arguments:  
            parent: GameObject, the parent of the component
        """

        self.parent: GameObject = None # type: ignore

    def set_parent(self, parent: GameObject) -> None:
        """
        Sets the parent of the component

        Arguments:
            parent: GameObject, the parent of the component
        """
    
        self.parent = parent
    

    def on_init(self) -> None:
        """
        on_init is called when the component is initialized

        Returns:
            None
        """
        pass

    def on_destroy(self) -> None:
        """
        on_destroy is called when the component is destroyed

        Returns:
            None
        """
        pass

    def on_update(self, delta_time: float) -> None:
        """
        on_update is called every frame

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """
        pass

    def on_late_update(self, delta_time: float) -> None:
        """
        on_late_update is called every frame after on_update

        Arguments:
            delta_time: float, the time since the last frame
        
        Returns:
            None
        """

        pass

    def on_collision(self, other: GameObject, point: Vector2, normal: Vector2) -> None:
        """
        on_collision is called when the parent collides with another object

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision

        Returns:
            None
        """
        pass

    ### Abstract Methods ###

    @abstractmethod
    def serialize(self) -> dict:
        """
        serialize is called when the component is serialized

        Returns:
            dict: a dictionary containing the component's data
        """
        pass

    @abstractmethod
    def deserialize(self, data: dict) -> 'Component':
        """
        deserialize is called when the component is deserialized

        Arguments:
            data: dict, the data to deserialize

        Returns:    
            Component: the deserialized component
        """
        pass
