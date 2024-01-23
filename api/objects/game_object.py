from abc import ABC
from pygame import Surface, Vector2
from api.management.sound_manager import SoundManager
from api.utils.transform import Transform

class GameObject(ABC):
    def __init__(self, pos: Vector2, render_layer: int, scene) -> None:
        self.render_layer: int = render_layer
        self.components: list = []
        self.transform: Transform = Transform(self)
        self.transform.pos = pos

        self.scene = scene
        self.sound_manager: SoundManager = scene.sound_manager
    
    def add_components(self, *args) -> 'GameObject':
        for c in args:
            self._add_component(c)
        for c in args:
            c.on_init()
        return self

    def _add_component(self, comp) -> bool:
        comp.set_parent(self)

        if self.get_component_by_class(type(comp)) is not None:
            return False
        self.components.append(comp)
        return True
    
    def remove_component(self, comp) -> bool:
        if self.get_component_by_class(type(comp)) is not None:
            self.components.remove(comp)
            return True
        return False

    def get_component_by_class(self, comp_type: type):
        for c in self.components:
            if isinstance(c, comp_type):
                return c
        return None
    
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
        self.scene = parent

    def get_scene(self):
        return self.scene
    
    # To be overriden
    
    def on_destroy(self) -> None:
        self.scene.all_active_gos.remove(self)
        for c in self.components:
            c.on_destroy()
    
    def on_update(self, delta_time: float) -> None:
        self.transform.update(delta_time)
        for c in self.components:
            c.on_update(delta_time)

    def on_late_update(self, delta_time: float) -> None:
        for c in self.components:
            c.on_late_update(delta_time)

    def on_awake(self) -> None:
        pass
    
    def on_collision(self, other: 'GameObject', point: Vector2, normal: Vector2) -> None:
        for c in self.components:
            c.on_collision(other, point, normal)

    def on_trigger_enter(self, other: 'GameObject') -> None:
        pass

    def on_trigger_exit(self, other: 'GameObject') -> None:
        pass