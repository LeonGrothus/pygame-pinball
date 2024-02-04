from abc import ABC
from pygame import Surface, Vector2
from source.api.management.sound_manager import SoundManager
from source.api.utils.transform import Transform
from data.constants import PTPF

class GameObject(ABC):
    """
    A class to represent a GameObject. A GameObject is an object in the game. A GameObject can have components. 
    A GameObject can be serialized and deserialized. A GameObject can be initialized

    Attributes:
        render_layer: int, the render layer of the GameObject
        components: list, the components of the GameObject
        transform: Transform, the transform of the GameObject

    Methods:
        __init__(self, pos: Vector2, render_layer: int, scene)
        add_components(self, *args) -> 'GameObject'
        _add_component(self, comp) -> bool
        remove_component(self, comp) -> bool
        get_component_by_class(self, comp_type: type)
        has_component_by_class(self, comp_type: type) -> bool
        get_components_by_class_scuffed(self, *class_names: str)
        set_scene(self, parent) -> None
        get_scene(self)
        on_destroy(self) -> None
        on_update(self, delta_time: float) -> None
        on_late_update(self, delta_time: float) -> None
        on_awake(self) -> None
        on_collision(self, other: 'GameObject', point: Vector2, normal: Vector2) -> None
        on_trigger_enter(self, other: 'GameObject') -> None
        on_trigger_exit(self, other: 'GameObject') -> None
    """

    def __init__(self, pos: Vector2, render_layer: int, scene) -> None:
        """
        Inits GameObject with pos, render_layer and scene

        Arguments:
            pos: Vector2, the position of the GameObject
            render_layer: int, the render layer of the GameObject
            scene: Scene, the scene of the GameObject
        """

        self.render_layer: int = render_layer
        self.components: list = []
        self.transform: Transform = Transform(self)
        self.transform.pos = pos

        self.scene = scene
        self.sound_manager: SoundManager = scene.sound_manager
        self.rigidbody = None
    
    def add_components(self, *args) -> 'GameObject':
        """
        Adds the given components to the GameObject

        Arguments:
            *args: the components to add
        
        Returns:
            self
        """
        for c in args:
            self._add_component(c)
        for c in args:
            c.on_init()
        return self

    def _add_component(self, comp) -> bool:
        """
        Adds the given component to the GameObject

        Arguments:
            comp: the component to add

        Returns:  
            bool: True if the component was added, False if not
        """

        if comp.__class__.__name__ == "Rigidbody": # scuffed because of circular import
            self.rigidbody = comp 
        comp.set_parent(self) # Set the parent of the component

        if self.get_component_by_class(type(comp)) is not None: # If the component is already on the GameObject
            return False # Don't add it again
        self.components.append(comp) # Add the component
        return True # Return True to indicate that the component was added
    
    def remove_component(self, comp) -> bool:
        """
        Removes the given component from the GameObject

        Arguments:
            comp: the component to remove

        Returns:
            bool: True if the component was removed, False if not
        """
        if self.get_component_by_class(type(comp)) is not None: # If the component is on the GameObject
            self.components.remove(comp) # Remove the component
            return True # Return True to indicate that the component was removed
        return False # Return False to indicate that the component was not removed

    def get_component_by_class(self, comp_type: type): 
        """
        Returns the first component that matches the given type.

        Arguments:
            comp_type (type): The type of the component to match.
        
        Returns:
            component: The first component that matches the given type, or None if no match is found.
        """
        for c in self.components: # For every component on the GameObject 
            if isinstance(c, comp_type): # If the component is of the given type
                return c # Return the component
        return None # Return None to indicate that no component was found
    
    def has_component_by_class(self, comp_type: type) -> bool:
        """
        Returns whether the GameObject has a component that matches the given type.

        Arguments:
            comp_type: type, the type of the component to match

        Returns:
            bool: True if the GameObject has a component that matches the given type, False if not
        """

        return self.get_component_by_class(comp_type) is not None
    
    def get_components_by_class_scuffed(self, *class_names: str):
        """
        Returns the first component that matches the given class name.

        This method should only be used in cases where the type cannot be used.
        It checks for an exact match with the class name, and does not check if the class inherits from other classes.

        Parameters:
            class_name (str): The name of the class to match.

        Returns:
            The first component that matches the given class name, or None if no match is found.
        """
        for c in self.components:
            for class_name in class_names:
                if c.__class__.__name__ == class_name:
                    return c
        return None
    
    def set_scene(self, parent) -> None:
        """
        Sets the scene of the GameObject

        Arguments:
            parent: Scene, the scene of the GameObject

        Returns:
            None
        """
        self.scene = parent

    def get_scene(self):
        return self.scene
    
    ### Methods to be extended by the user ###
    
    def on_destroy(self) -> None:
        """
        on_destroy is called when the GameObject is destroyed

        Returns:
            None
        """
        
        self.scene.all_active_gos.remove(self)
        for c in self.components:
            c.on_destroy()
    
    def on_update(self, delta_time: float) -> None:
        """
        on_update is called every frame

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """
        for c in self.components:
            if c == self.rigidbody:
                continue
            c.on_update(delta_time) # Update the component
        
        scaled_delta_time = delta_time / PTPF # Scale the delta time to the application scale factor 
        for _ in range(PTPF): # For every physics tick per frame 
            self.transform.update(scaled_delta_time) # Update the transform
            if self.rigidbody: # If the GameObject has a Rigidbody 
                self.rigidbody.on_update(scaled_delta_time) # Update the Rigidbody

    def on_late_update(self, delta_time: float) -> None:
        """
        on_late_update is called every frame after on_update

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """

        for c in self.components:
            c.on_late_update(delta_time)

    def on_awake(self) -> None:
        """
        on_awake is called when the GameObject is initialized

        Returns:
            None
        """

        pass
    
    def on_collision(self, other: 'GameObject', point: Vector2, normal: Vector2) -> None:
        """
        on_collision is called when the parent collides with another object

        Arguments:
            other: GameObject, the other object
            point: Vector2, the point of collision
            normal: Vector2, the normal of the collision

        Returns:
            None
        """
        for c in self.components:
            c.on_collision(other, point, normal)

    def on_trigger_enter(self, other: 'GameObject') -> None:
        """
        on_trigger_enter is called when the parent enters a trigger collider

        Arguments:
            other: GameObject, the other object
        
        Returns:
            None
        """
        pass

    def on_trigger_exit(self, other: 'GameObject') -> None:
        """
        on_trigger_exit is called when the parent exits a trigger collider

        Arguments:
            other: GameObject, the other object

        Returns:
            None
        """
        pass