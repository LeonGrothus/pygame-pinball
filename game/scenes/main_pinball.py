from math import ceil
from typing import Callable
from unittest.mock import DEFAULT
from pygame import Color, Surface
from pygame import Vector2 as V2
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
from game.objects.bumper import Bumper
from game.objects.flipper import Flipper
from game.objects.plunger import Plunger
from game.objects.wall import Wall
from options import Options
from scipy.ndimage.filters import gaussian_filter
from api.utils import utils


class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)
        self.ball_radius = 20 * Options().asf

        self.left_flipper: Flipper = None  # type: ignore
        self.right_flipper: Flipper = None  # type: ignore

        self.blured: Surface = None  # type: ignore

    def awake(self) -> None:

        width = self.screen.get_width()
        height = self.screen.get_height()

        self.pause_menu = PauseMenu(self.screen, lambda: self.change_scene("options_menu"),
                                    lambda: self.unpause(), lambda: self.change_scene("main_menu"))
        self.paused = False

        asf = Options().asf

        self.left_flipper = Flipper(V2(580*asf / 2 - 125 * asf, height - 175*asf), 30)
        self.right_flipper = Flipper(V2(580*asf / 2 + 125 * asf, height - 175*asf), 150)
        self.add_gameobject(self.left_flipper)
        self.add_gameobject(self.right_flipper)

        self.add_gameobject(Plunger(V2(width - self.ball_radius*3, height), V2(width, height)))

        # ball spawn container
        rel_points = [V2(0, 125*asf), V2(0, 0), V2(125*asf, -125*asf), V2(125*asf, -250*asf)]
        self.add_gameobject(Wall(rel_points, friction=0, pos=V2(width, height-125*asf), visible=False))

        # right wall
        rel_points = [V2(0, -125*asf - self.ball_radius*4), V2(0, -height/2), V2(0, -height)]
        print(rel_points)
        self.add_gameobject(Wall(rel_points, friction=0, pos=V2(width, height), visible=False))
        # left wall
        rel_points = [V2(0, 0), V2(0, height/2), V2(0, height)]
        self.add_gameobject(Wall(rel_points, friction=0, pos=V2(0, 0), visible=False))
        # plunger cap wall
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(580, 1000), V2(580, 275), V2(600, 275), V2(600, 1000)]))
        self.add_gameobject(Wall(rel_points, visible=True))
        # top wall
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(665, 300), V2(666, 0), V2(0, 0), V2(0, 398), V2(0, 540), V2(42, 517), V2(76, 482), V2(142, 454), V2(145, 439), V2(78, 324), V2(63, 239), V2(63, 150), V2(79, 98), V2(129, 59), V2(212, 27), V2(291, 14), V2(362, 13), V2(449, 24), V2(534, 60), V2(611, 124), V2(639, 164), V2(655, 217)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))

        # left bottom outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(50, 865), V2(180, 935), V2(210, 963), V2(225, 1000), V2(0, 1000), V2(0, 805), V2(10, 835), V2(30, 850)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # right bottom outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(530, 865), V2(400, 935), V2(370, 963), V2(355, 1000), V2(580, 1000), V2(580, 805), V2(570, 835), V2(550, 850)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))

        # center top obstacle
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(290, 129), V2(295, 122), V2(325, 122), V2(330, 129), V2(330, 218), V2(325, 224), V2(295, 224), V2(290, 218)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # first obstacle to the left of the center obstacle
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(200, 150), V2(210, 140), V2(220, 150), V2(220, 200), V2(210, 210), V2(200, 200)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # second obstacle to the left of the center obstacle
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(200-70, 150), V2(210-70, 140), V2(220-70, 150), V2(220-70, 200), V2(210-70, 210), V2(200-70, 200)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))


        # top right obstacle
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(485, 137), V2(451, 170), V2(448, 176), V2(451, 183), V2(505, 255), V2(511, 259), V2(517, 255), V2(557, 206), V2(557, 199), V2(550, 188), V2(504, 143), V2(494, 137)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # other top right obstacle
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(580, 275), V2(482, 393), V2(482, 412), V2(580, 485)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # center obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x+V2(20,00))*asf), [V2(193, 499), V2(193, 484), V2(246, 461), V2(264, 461), V2(319, 483), V2(320, 500), V2(267, 523), V2(247, 523)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))


        # left plunger extension
        rel_points = list(map(lambda x: utils.ceil_vector((x+V2(0,74))*asf), [V2(50, 641), V2(65, 721), V2(157, 762), V2(171, 739), V2(113, 715), V2(86, 689)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # right plunger extension
        rel_points = list(map(lambda x: utils.ceil_vector((x+V2(0,74))*asf), [V2(530, 641), V2(515, 721), V2(423, 762), V2(409, 739), V2(467, 715), V2(494, 689)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))


        # obstacle on top of the left plunger extension
        rel_points = list(map(lambda x: utils.ceil_vector((x+V2(30,45))*asf), [V2(123, 564), V2(104, 555), V2(88, 567), V2(87, 638), V2(99, 655), V2(151, 679), V2(169, 675), V2(175, 656)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))
        # obstacle on top of the right plunger extension
        rel_points = list(map(lambda x: utils.ceil_vector((x+V2(-30,45))*asf), [V2(457, 564), V2(476, 555), V2(492, 567), V2(492, 638), V2(481, 655), V2(428, 679), V2(410, 675), V2(404, 656)]))
        self.add_gameobject(Wall(rel_points, friction=0, visible=True))

        # bumpers
        self.add_gameobject(Bumper(V2(65, 290)*asf, 20*asf, 100*asf, color=Color(255, 0, 0)))
        self.add_gameobject(Bumper(V2(237, 322)*asf, 20*asf, 100*asf, color=Color(200, 0, 0)))
        self.add_gameobject(Bumper(V2(380, 280)*asf, 30*asf, 100*asf, color=Color(255, 0, 0)))
        # self.add_gameobject(Bumper(V2(65, 290)*asf, 20*asf, 250*asf, color=Color(255, 0, 0)))
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
                    self.left_flipper.transform.init_smooth_rotation(-10)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(190)
                elif event.key == pygame.K_SPACE:
                    self.add_ball()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(30)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(150)

        if self.paused:
            return self.pause_menu.update(events, self.blured)

        return super().update(0 if self.paused else delta_time, events)

    def add_ball(self) -> None:
        width = self.screen.get_width()
        height = self.screen.get_height()
        asf = Options().asf
        self.add_gameobject(Ball(V2(width + self.ball_radius*2, height-250*asf), radius=self.ball_radius))

    def pause(self, events: list[Event]) -> None:
        # Update need to be called so that all objects are visible in the background
        super().update(0, events)
        self.blured = self.get_blured()
        self.paused = True

    def unpause(self) -> None:
        self.paused = False

    def change_scene(self, scene_name: str) -> None:
        self.serialize()
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
