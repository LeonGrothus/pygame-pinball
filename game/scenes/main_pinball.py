from typing import Callable
from unittest.mock import DEFAULT
from pygame import Surface, Vector2
import pygame
from pygame.event import Event
from pygame.freetype import Font
from api.management.scene import Scene
from api.ui.button import Button
from api.ui.button_style import ButtonStyle
from api.ui.text import Text
from api.ui.ui_element_base import UIElementBase
from constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from game.objects.ball import Ball
from game.objects.boundry import Boundry
from game.objects.flipper import Flipper
from options import Options
from scipy.ndimage.filters import gaussian_filter


class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.pause_menu = PauseMenu(self.screen, lambda: self.change_scene("options_menu"),
                                    lambda: self.unpause(), lambda: self.change_scene("main_menu"))

        self.left_flipper: Flipper = None  # type: ignore
        self.right_flipper: Flipper = None  # type: ignore

        self.blured: Surface = None  # type: ignore

    def awake(self) -> None:
        self.paused = False

        asf = Options().asf
        self.left_flipper = Flipper(Vector2(self.screen.get_width() / 2 - 125 *
                                    asf, self.screen.get_height() - 175*asf), 30)
        self.right_flipper = Flipper(Vector2(self.screen.get_width() / 2 + 125 *
                                     asf, self.screen.get_height() - 175*asf), 150)
        self.add_gameobject(self.left_flipper)
        self.add_gameobject(self.right_flipper)

        self.add_gameobject(Ball(Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)))

        # open_side="bottom"
        self.add_gameobject(Boundry())
        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.unpause()
                    else:
                        self.pause(events)

                elif event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(0)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(180)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(30)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(150)

        if self.paused:
            return self.pause_menu.update(events, self.blured)

        return super().update(0 if self.paused else delta_time, events)

    def pause(self, events: list[Event]) -> None:
        # Update need to be called so that all objects are visible in the background
        super().update(0, events)
        self.blured = self.get_blured()
        self.paused = True

    def unpause(self) -> None:
        self.paused = False

    def change_scene(self, scene_name: str) -> None:
        # self.serialize()
        self.scene_manager.change_scene(scene_name)

    def get_blured(self) -> Surface:
        background = self.screen.copy()
        radius = Options().asf * 10

        # Convert the surface to a numpy array
        array = pygame.surfarray.pixels3d(background)

        # Apply a Gaussian blur to the array
        blurred_array = gaussian_filter(array, sigma=(radius, radius, 0))

        # Convert the blurred array back to a surface
        blurred_surface = pygame.surfarray.make_surface(blurred_array)
        return blurred_surface


class PauseMenu:
    def __init__(self, screen: Surface, options_action: Callable, resume_action: Callable, main_menu_action: Callable) -> None:
        self.screen: Surface = screen

        self.ui_elements: list[UIElementBase] = []

        self.font = Font(DEFAULT_FONT, 75)
        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        asf = Options().asf
        button_width = int(250 * asf)
        button_height = int(125 * asf)
        button_font_size = int(50 * asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Pause",
                                     width=Options().resolution[0]*7/8, font=self.font))

        button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True)

        self.ui_elements.append(Button(self.screen, (1, .3), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Resume", font_size=button_font_size, on_click=resume_action))

        self.ui_elements.append(Button(self.screen, (1, .45), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Options", font_size=button_font_size, on_click=options_action))

        self.ui_elements.append(Button(self.screen, (1, .60), (1, 0), button_width, button_height,
                                       inactive_button=button[0], hover_button=button[1], pressed_button=button[2],
                                       text="Menu", font_size=button_font_size, on_click=main_menu_action))

    def update(self, events: list[Event], background: Surface) -> None:
        self.screen.blit(background, (0, 0))
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()
