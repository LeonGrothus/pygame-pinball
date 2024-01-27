from abc import ABC
from pathlib import Path
import pygame
from pygame.event import Event
from api.components.life_timer import LifeTimer
from api.management.image_manager import ImageManager
from api.management.sound_manager import SoundManager

from api.objects.game_object import GameObject
from api.components.rigidbody import Rigidbody
from constants import PROJECT_PATH
from game.objects.wall import CircleWall
from game.objects.ball import Ball
from data.options import Options

class BaseDisplay(ABC):
    """
    Base class for all scenes. A scene is a collection of GameObjects. A scene can be serialized and deserialized. A scene can be initialized

    Attributes:
        screen: pygame.Surface, the screen to draw on
        scene_manager: SceneManager, the scene manager

    Methods:
        __init__(self, screen: pygame.Surface, scene_manager)
        awake(self)
        update(self, delta_time: float, events: list[Event])
        unload(self)
    """
    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        """
        Inits BaseDisplay with screen and scene_manager

        Arguments:
            screen: pygame.Surface, the screen to draw on
            scene_manager: SceneManager, the scene manager
        """

        self.screen: pygame.Surface = screen
        self.scene_manager = scene_manager

    ### Methods to be overriden by the user ###

    def awake(self) -> None:
        """
        Awake is called when the scene is initialized

        Returns:
            None
        """
        pass

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Update is called every frame

        Arguments:
            delta_time: float, the time between frames
            events: list[Event], the events of the frame

        Returns:
            None
        """
        pass

    def unload(self) -> None:
        """
        Unload is called when the scene is unloaded

        Returns:
            None
        """

        pass


class Scene(BaseDisplay, ABC):
    """
    A class to represent a Scene. A scene is a collection of GameObjects. A scene can be serialized and deserialized. A scene can be initialized

    Attributes:
        screen: pygame.Surface, the screen to draw on
        scene_manager: SceneManager, the scene manager
        active_balls: int, the number of active balls
        remaining_balls: int, the number of remaining balls
        score: int, the score of the player
        object_counter: int, the number of objects in the scene

    Methods:
        __init__(self, screen: pygame.Surface, scene_manager)
        awake(self)
        add_gameobject(self, game_object: GameObject)
        add_gameobjects(self, *game_objects: GameObject)
        remove_gameobject(self, game_object: GameObject)
        serialize(self) -> None
        save_score(self) -> None
        deserialize(self)
    """

    def __init__(self, screen: pygame.Surface, scene_manager) -> None:
        """
        Inits Scene with screen and scene_manager

        Arguments:
            screen: pygame.Surface, the screen to draw on
            scene_manager: SceneManager, the scene manager
        """
        super().__init__(screen, scene_manager)
        self.active_balls = 0
        self.remaining_balls: int = 5
        self.score: int = 0
        self.object_counter: int = 0
        self.all_active_gos: list = []
        self.all_active_rbs: list = []

        self.game_manager: GameManager = None  # type: ignore
        self.sound_manager: SoundManager = SoundManager()

        self.image_manager = ImageManager(PROJECT_PATH / Path("data/data.png"))

    def awake(self) -> None:
        """
        Awake is called when the scene is initialized

        Returns:
            None
        """
        self.user_name: str = Options().user_name
        return super().awake()

    def add_gameobject(self, game_object: GameObject) -> None:
        """
        Adds a gameobject to the scene

        Arguments:
            game_object: GameObject, the gameobject to add

        Returns:
            None
        """

        self.all_active_gos.append(game_object)
        self.all_active_gos.sort(key=lambda x: x.render_layer)
        self.object_counter += 1

        if game_object.get_component_by_class(Rigidbody) is not None:
            self.all_active_rbs.append(game_object)
        game_object.on_awake()

    def add_gameobjects(self, *game_objects: GameObject) -> None:
        """
        Adds multiple gameobjects to the scene at once

        Arguments:
            *game_objects: GameObject, the gameobjects to add

        Returns:
            None
        """
        for go in game_objects:
            self.add_gameobject(go)

    def remove_gameobject(self, game_object: GameObject) -> None:
        """
        Removes a gameobject from the scene

        Arguments:
            game_object: GameObject, the gameobject to remove

        Returns:
            None
        """
        game_object.set_scene(None)
        if (game_object is None):
            return

        if (game_object in self.all_active_gos):
            self.all_active_gos.remove(game_object)
        if (game_object in self.all_active_rbs):
            self.all_active_rbs.remove(game_object)

    def serialize(self) -> None:
        """
        Serializes the scene

        Returns:
            None
        """

        self.save_score()
        data = {
            "user_name": self.user_name,
            "score": self.score,
            "remaining_balls": self.remaining_balls,
            "object_counter": self.object_counter,
            "all_balls": [go.serialize() for go in self.all_active_gos if isinstance(go, Ball)],
            "all_life_time_bumpers": [go.serialize() for go in self.all_active_gos if go.has_component_by_class(LifeTimer)],
        }
        
        current_data = self.image_manager.load_json()
        current_data["save_game"] = data
        self.image_manager.save_json(current_data)

    def save_score(self) -> None:
        """
        Saves the score to the scoreboard

        Returns:
            None
        """
        current_data = self.image_manager.load_json()

        user_score = current_data.get("scoreboard", {}).get(self.user_name, 0)
        if user_score < self.score:
            current_data.setdefault("scoreboard", {})[self.user_name] = self.score

        self.image_manager.save_json(current_data)

    
    def deserialize(self):
        """
        Deserializes the scene

        Returns:
            Scene: the modified Scene instance
        """

        json = self.image_manager.load_json()
        data = json["save_game"]
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
        
        json["save_game"] = {}
        self.image_manager.save_json(json)
        return self

    ### Methods to be extended by the user ###

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Update is called every frame

        Arguments:
            delta_time: float, the time between frames
            events: list[Event], the events of the frame

        Returns:
            None
        """
        for game_object in self.all_active_gos:
            game_object.on_update(delta_time)
        for game_object in self.all_active_gos:
            game_object.on_late_update(delta_time)
        return super().update(delta_time, events)

    def unload(self) -> None:
        """
        Unload is called when the scene is unloaded

        Returns:
            None
        """

        for game_object in self.all_active_gos:
            game_object.on_destroy()
        self.all_active_gos.clear()
        self.all_active_rbs.clear()
        self.object_counter = 0
        self.active_balls = 0
        self.remaining_balls: int = 5
        self.score: int = 0

