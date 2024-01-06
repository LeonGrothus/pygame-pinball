from pygame import Surface
from game.scenes.main_menu import MainMenu
from game.scenes.main_pinball import MainPinball
from game.scenes.options_menu import OptionsMenu
from game.scenes.scoreboard_menu import ScoreboardMenu
from api.management.scene import BaseDisplay, Scene


class SceneManager:
    def __init__(self, screen: Surface, default: str) -> None:
        self.screen: Surface = screen

        self.scenes: dict[str, BaseDisplay] = {
            "main_menu": MainMenu(self.screen),
            "main_pinball": MainPinball(self.screen),
            "options": OptionsMenu(self.screen),
            "scoreboard": ScoreboardMenu(self.screen)
        }
        self.active_scene: BaseDisplay = self.scenes[default]
        self.active_scene.awake()

    def change_scene(self, scene_name: str) -> None:
        self.active_scene = self.scenes[scene_name]
        self.active_scene.awake()