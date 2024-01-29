from abc import ABC
from pathlib import Path
import pygame
from pygame.event import Event

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
    def __init__(self, screen: pygame.Surface, scene_manager, background_path: Path) -> None:
        """
        Inits BaseDisplay with screen and scene_manager

        Arguments:
            screen: pygame.Surface, the screen to draw on
            scene_manager: SceneManager, the scene manager
        """
        self.background = pygame.image.load(background_path).convert() # Load background image

        self.screen: pygame.Surface = screen
        self.scene_manager = scene_manager

    ### Methods to be extended by the user ###

    def awake(self) -> None:
        """
        Awake is called when the scene is initialized

        Returns:
            None
        """
        self.scaled_background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))  # scales background image to fit screen size

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Update is called every frame

        Arguments:
            delta_time: float, the time between frames
            events: list[Event], the events of the frame

        Returns:
            None
        """
        self.screen.blit(self.scaled_background, pygame.Vector2())  # redraws background image

    def unload(self) -> None:
        """
        Unload is called when the scene is unloaded

        Returns:
            None
        """

        pass

