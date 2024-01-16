from abc import ABC
from json import load
from pathlib import Path
from typing import Callable
import pygame
from pygame.event import Event
from api.management.json_manager import JsonManager

from api.objects.game_object import GameObject
from api.components.rigidbody import Rigidbody
from constants import PROJECT_PATH
from game.objects.ball import Ball

class BaseDisplay(ABC):
    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        self.screen: pygame.Surface = screen
        self.scene_manager = scene_manager

    ### Methods to be overriden by the user ###

    def awake(self) -> None:
        pass

    def update(self, delta_time: float, events: list[Event]) -> None:
        pass

    def unload(self) -> None:
        pass


class Scene(BaseDisplay, ABC):
    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        super().__init__(screen, scene_manager)

        self.active_ball_count: int = 0
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
        game_object.on_awake()

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

    def serialize(self) -> None:
        data = {
            "active_ball_count": self.active_ball_count,
            "object_counter": self.object_counter,
            "all_balls": [go.serialize() for go in self.all_active_gos if isinstance(go, Ball)],
        }
        jm = JsonManager(PROJECT_PATH / Path("data.json"))
        current_data = jm.load_json()
        current_data["save_game"] = data
        jm.save_json(current_data)
    
    def deserialize(self, data: dict):
        self.active_ball_count = data["active_ball_count"]
        self.object_counter = data["object_counter"]
        for ball_data in data["all_balls"]:
            ball_class = list(ball_data.keys())[0]
            game_object = globals()[ball_class](pygame.Vector2(0,0)).deserialize(ball_data[ball_class])
            self.add_gameobject(game_object)
        return self

    ### Methods to be extended by the user ###

    def update(self, delta_time: float, events: list[Event]) -> None:
        for game_object in self.all_active_gos:
            game_object.on_update(delta_time)

    def unload(self) -> None:
        for game_object in self.all_active_gos:
            game_object.on_destroy()
        self.all_active_gos.clear()
        self.all_active_rbs.clear()
