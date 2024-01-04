from abc import ABC

from api.objects.gameObject import GameObject


class Component(ABC):
    def __init__(self):
        self.parent: GameObject = None # type: ignore

    def set_parent(self, parent: GameObject) -> None:
        self.parent = parent
    

    def on_init(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass
