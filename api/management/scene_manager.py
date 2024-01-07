from pygame import Surface
from game.scenes.main_menu import MainMenu
from game.scenes.main_pinball import MainPinball
from game.scenes.options_menu import OptionsMenu
from game.scenes.scoreboard_menu import ScoreboardMenu


class SceneManager:
    def __init__(self, screen: Surface, default: str) -> None:
        self.screen: Surface = screen

        self.scenes: dict = {
            "main_menu": MainMenu(self.screen, self),
            "main_pinball": MainPinball(self.screen, self),
            "options_menu": OptionsMenu(self.screen, self),
        }
        self.active_scene = self.scenes[default]
        self.active_scene.awake()

    def change_scene(self, scene_name: str) -> None:
        self.active_scene.unload()
        self.active_scene = self.scenes[scene_name]
        self.active_scene.awake()