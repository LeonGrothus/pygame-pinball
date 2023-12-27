from objects.gameObject import GameObject


class Component:
    def __init__(self):
        self.parent: GameObject = None

    def on_start(self) -> None:
        pass

    def set_parent(self, parent: GameObject) -> None:
        self.parent = parent

    def on_destroy(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass
