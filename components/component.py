from abc import abstractmethod
from objects.gameObject import GameObject


class Component:
    def __init__(self):
        self.parent: GameObject = None # type: ignore

    @abstractmethod
    def on_init(self) -> None:
        pass

    def set_parent(self, parent: GameObject) -> None:
        self.parent = parent

    @abstractmethod
    def on_destroy(self) -> None:
        pass

    @abstractmethod
    def on_update(self, delta_time: float) -> None:
        pass
