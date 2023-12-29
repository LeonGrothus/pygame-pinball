from pygame import Surface, Vector2
from utils.transform import Transform

class GameObject():
    def __init__(self, pos: Vector2, sreen: Surface, all_active_gos: list, all_active_rbs: list) -> None:
        all_active_gos.append(self)

        self.screen = sreen
        self.all_active_gos = all_active_gos
        self.all_active_rbs = all_active_rbs

        self.render_layer = 0
        self.components = []
        self.transform = Transform()
        self.transform.pos = pos
    
    def add_components(self, *args):
        for c in args:
            self.add_component(c)

    def add_component(self, comp):
        comp.set_parent(self)

        if self.get_component_by_class(type(comp)) is not None:
            return False
        self.components.append(comp)
        
        comp.on_init()
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
    
    def destroy(self):
        self.all_active_gos.remove(self)
        for c in self.components:
            c.on_distroy()
    
    def update(self, delta_time: float):
        for c in self.components:
            c.on_update(delta_time)