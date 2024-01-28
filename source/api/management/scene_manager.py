from pathlib import Path
from pygame import Surface
from api.management.scene import Scene
from constants import ASSETS_PATH
from game.scenes.main_menu import MainMenu
from game.scenes.main_pinball import MainPinball
from game.scenes.options_menu import OptionsMenu


class SceneManager:
    """
    A class to represent a SceneManager. A SceneManager is responsible for managing the scenes of the game.

    Attributes:
        screen (Surface): The screen to render the game on.
        scenes (dict): A dictionary containing all the scenes.
        active_scene (Scene): The active scene.

    Methods:
        __init__(self, screen: Surface, default: str)
        change_scene(self, scene_name: str)
    """

    def __init__(self, screen: Surface, default: str) -> None:
        """
        Inits SceneManager with screen and default

        Arguments:
            screen (Surface): The screen to render the game on.
            default (str): The default scene.
        """
        self.screen: Surface = screen

        self.scenes: dict = {
            "main_menu": MainMenu(self.screen, self, Path(ASSETS_PATH / Path("images/main_background.jpg"))),
            "main_pinball": MainPinball(self.screen, self, Path(ASSETS_PATH / Path("images/pinball_background.jpg"))),
            "options_menu": OptionsMenu(self.screen, self, Path(ASSETS_PATH / Path("images/main_background.jpg"))),
        }
        self.active_scene = self.scenes[default]
        self.active_scene.awake()

    def change_scene(self, scene_name: str) -> Scene:
        """
        Changes the active scene

        Arguments:
            scene_name (str): The name of the scene to change to.

        Returns:
            Scene: The new active scene.
        """

        self.active_scene.unload()
        self.active_scene = self.scenes[scene_name]
        self.active_scene.awake()
        return self.active_scene