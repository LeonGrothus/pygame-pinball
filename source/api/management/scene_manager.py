from pathlib import Path
from pygame import Surface
from source.api.management.background_manager import BackgroundManager
from source.api.scene.scene import Scene
from data.constants import ASSETS_PATH
from source.game.scenes.main_menu import MainMenu
from source.game.scenes.main_pinball import MainPinball
from source.game.scenes.options_menu import OptionsMenu


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

        default_background = BackgroundManager(Path(ASSETS_PATH / Path("images/main_background")), -1, screen)
        pinball_background = BackgroundManager(Path(ASSETS_PATH / Path("images/pinball_background")), 1, screen)

        self.scenes: dict = {
            "main_menu": MainMenu(self.screen, self, default_background),
            "main_pinball": MainPinball(self.screen, self, pinball_background),
            "options_menu": OptionsMenu(self.screen, self, default_background),
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