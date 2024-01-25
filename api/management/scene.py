from abc import ABC
from json import load
from pathlib import Path
import pygame
from pygame.event import Event
from api.components.life_timer import LifeTimer
from api.management.json_manager import JsonManager
from api.management.sound_manager import SoundManager

from api.objects.game_object import GameObject
from api.components.rigidbody import Rigidbody
from constants import PROJECT_PATH
from game.objects.ball import Ball
from game.objects.wall import CircleWall
from options import Options

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
        options = Options()

        self.active_balls = 0
        self.remaining_balls: int = 5
        self.score: int = 0
        self.user_name: str = options.user_name
        self.object_counter: int = 0
        self.all_active_gos: list = []
        self.all_active_rbs: list = []

        self.game_manager: GameManager = None  # type: ignore
        self.sound_manager: SoundManager = SoundManager()

    def add_gameobject(self, game_object: GameObject) -> None:
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
        self.save_score()
        data = {
            "user_name": self.user_name,
            "score": self.score,
            "remaining_balls": self.remaining_balls,
            "object_counter": self.object_counter,
            "all_balls": [go.serialize() for go in self.all_active_gos if isinstance(go, Ball)],
            "all_life_time_bumpers": [go.serialize() for go in self.all_active_gos if go.has_component_by_class(LifeTimer)],
        }
        jm = JsonManager(PROJECT_PATH / Path("data.json"))
        current_data = jm.load_json()
        current_data["save_game"] = data
        jm.save_json(current_data)

    def save_score(self) -> None:
        jm = JsonManager(PROJECT_PATH / Path("data.json"))
        current_data = jm.load_json()
        if "scoreboard" not in current_data:
            current_data["scoreboard"] = {}
        current_data["scoreboard"][self.user_name] = self.score
        jm.save_json(current_data)

    
    def deserialize(self, data: dict):
        for game_object in self.all_active_gos:
            if game_object.has_component_by_class(LifeTimer):
                game_object.on_destroy()

        self.user_name = data["user_name"]
        self.score = data["score"]
        self.remaining_balls = data["remaining_balls"]
        self.object_counter = data["object_counter"]
        for ball_data in data["all_balls"]:
            ball_class = list(ball_data.keys())[0]
            game_object = globals()[ball_class](self, pygame.Vector2(0,0)).deserialize(ball_data[ball_class])
            self.add_gameobject(game_object)

        for bumper_data in data["all_life_time_bumpers"]:
            bumper_class = list(bumper_data.keys())[0]
            game_object = globals()[bumper_class](self, pygame.Vector2(0,0), 0).deserialize(bumper_data[bumper_class])
            self.add_gameobject(game_object)
        return self

    ### Methods to be extended by the user ###

    def update(self, delta_time: float, events: list[Event]) -> None:
        for game_object in self.all_active_gos:
            game_object.on_update(delta_time)
        for game_object in self.all_active_gos:
            game_object.on_late_update(delta_time)
        return super().update(delta_time, events)

    def unload(self) -> None:
        for game_object in self.all_active_gos:
            game_object.on_destroy()
        self.all_active_gos.clear()
        self.all_active_rbs.clear()
        self.object_counter = 0
        self.active_balls = 0
        self.remaining_balls: int = 5
        self.score: int = 0

