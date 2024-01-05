from abc import ABC
from pygame import Surface, Vector2
from api.utils.transform import Transform

class GameObject(ABC):
    def __init__(self, pos: Vector2, render_layer: float) -> None:
        self.render_layer = render_layer
        self.components = []
        self.transform = Transform(self)
        self.transform.pos = pos

        self.scene: Scene = None # type: ignore
    
    def add_components(self, *args):
        for c in args:
            self.__add_component(c)
        for c in args:
            c.on_init()

    def __add_component(self, comp):
        comp.set_parent(self)

        if self.get_component_by_class(type(comp)) is not None:
            return False
        self.components.append(comp)
        return True
    
    def remove_component(self, comp):
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
    
    def set_scene(self, parent):
        self.scene = parent

    def get_scene(self):
        return self.scene
    
    def destroy(self):
        self.scene.all_active_gos.remove(self)
        for c in self.components:
            c.on_distroy()
    
    def update(self, delta_time: float):
        for c in self.components:
            c.on_update(delta_time)
    
    def on_trigger_enter(self, other):
        pass

    def on_trigger_exit(self, other):
        pass