from pygame import Vector2, Color
import pygame
from pygame.event import Event
from api.management.scene import Scene
from game.objects.ball import Ball
from game.objects.boundry import Boundry
from game.objects.flipper import Flipper
from constants import PADDLE_SPEED

class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.left_flipper = None
        self.right_flipper = None
        
    def awake(self) -> None:
        self.left_flipper = Flipper(Vector2(self.screen.get_width() / 2 - 230, self.screen.get_height() - 140), 30/2)
        self.right_flipper = Flipper(Vector2(self.screen.get_width() / 2 + 230, self.screen.get_height() - 140), 150/2)
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
                    self.left_flipper.transform.rotate_towards(0, PADDLE_SPEED) # type: ignore

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.rotate_towards(180, PADDLE_SPEED) # type: ignore

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_flipper.transform.rotate_towards(30, PADDLE_SPEED) # type: ignore

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.rotate_towards(150, PADDLE_SPEED) # type: ignore

        return super().update(delta_time, events)