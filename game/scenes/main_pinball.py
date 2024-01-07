from pygame import Vector2, Color
import pygame
from pygame.event import Event
from api.management.scene import Scene
from game.objects.ball import Ball
from game.objects.boundry import Boundry
from game.objects.flipper import Flipper

class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.left_flipper: Flipper = None # type: ignore
        self.right_flipper: Flipper = None # type: ignore
        
    def awake(self) -> None:
        self.left_flipper = Flipper(Vector2(self.screen.get_width() / 2 - 230, self.screen.get_height() - 140), 30)
        self.right_flipper = Flipper(Vector2(self.screen.get_width() / 2 + 230, self.screen.get_height() - 140), 150)
        self.add_gameobject(self.left_flipper)
        self.add_gameobject(self.right_flipper)

        self.add_gameobject(Ball(Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)))
        self.add_gameobject(Boundry())
        return super().awake()
    
    def update(self, delta_time: float, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.change_scene("main_menu")

                elif event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(0)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(180)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(30)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(150)

        return super().update(delta_time, events)