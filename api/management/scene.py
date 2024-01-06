from abc import ABC
from json import load
import pygame
from pygame.event import Event

from api.objects.game_object import GameObject
from api.components.ridigbody import Rigidbody

class BaseDisplay(ABC):
    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        self.screen: pygame.Surface = screen
        self.scene_manager = scene_manager

    ### Methods to be overriden by the user ###

    def awake(self) -> None:
        pass

    def update(self, delta_time: float, events: list[Event]) -> None:
        pass


class Scene(BaseDisplay, ABC):
    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        super().__init__(screen, scene_manager)

        self.object_counter: int = 0
        self.all_active_gos: list = []
        self.all_active_rbs: list = []

        self.game_manager: GameManager = None  # type: ignore

    def add_gameobject(self, game_object: GameObject) -> None:
        game_object.set_scene(self)
        self.all_active_gos.append(game_object)
        self.all_active_gos.sort(key=lambda x: x.render_layer)
        self.object_counter += 1

        if game_object.get_component_by_class(Rigidbody) is not None:
            self.all_active_rbs.append(game_object)

    def add_gameobjects(self, *game_objects: GameObject) -> None:
        for go in game_objects:
            self.add_gameobject(go)

    def remove_gameobject(self, game_object: GameObject) -> None:
        game_object.set_scene(None)
        if (game_object is None):
            return

        if (game_object in self.all_active_gos):
            self.all_active_gos.remove(game_object)
        if (game_object in self.all_active_rbs):
            self.all_active_rbs.remove(game_object)

    ### Methods to be extended by the user ###

    def update(self, delta_time: float, events: list[Event]) -> None:
        for game_object in self.all_active_gos:
            game_object.update(delta_time)
