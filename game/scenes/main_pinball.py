from pygame import Color, Surface
from pygame import Vector2 as V2
import pygame
from pygame.event import Event
from api.components.bumper import Bumper
from api.management.scene import Scene
from api.ui.text import Text
from api.ui.ui_element_base import UIElementBase
from game.objects.ball import Ball
from game.objects.flipper import Flipper
from game.objects.plunger import Plunger
from game.objects.wall import CircleWall, PolygonWall
from game.scenes.submenus.end_menu import EndMenu
from game.scenes.submenus.pause_menu import PauseMenu
from options import Options
from scipy.ndimage.filters import gaussian_filter
from api.utils import utils


class MainPinball(Scene):
    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.left_flipper: Flipper = None  # type: ignore
        self.right_flipper: Flipper = None  # type: ignore

        self.blured: Surface = None  # type: ignore
        self.ui_elements: list[UIElementBase] = []

    def awake(self) -> None:
        options = Options()
        asf = options.asf
        
        self.ball_radius = 15 * asf
        

        bumper_strength = (100*asf, 125*asf)

        width = self.screen.get_width()
        height = self.screen.get_height()

        self.pause_menu = PauseMenu(self.screen, lambda: self.change_scene("options_menu"),
                                    lambda: self.unpause(), lambda: self.change_scene("main_menu"))

        self.paused = False
        self.end_game = False
        friction = 0.1

        self.left_flipper = Flipper(V2(300*asf - 130 * asf, height - 125*asf), 30)
        self.right_flipper = Flipper(V2(300*asf + 130 * asf, height - 125*asf), 150)
        self.add_gameobject(self.left_flipper)
        self.add_gameobject(self.right_flipper)

        self.add_gameobject(Plunger(V2(width - self.ball_radius*3, height),
                            V2(width, height), impuls_range=(1300*asf, 1400*asf)))

        # ball spawn container
        rel_points = [V2(0, 125*asf), V2(0, 0), V2(125*asf, -125*asf), V2(125*asf, -250*asf)]
        self.add_gameobject(PolygonWall(rel_points, friction=friction, pos=V2(width, height-125*asf), visible=False))

        # right wall
        rel_points = [V2(0, -125*asf - self.ball_radius*4), V2(0, -height/2), V2(0, -height)]
        self.add_gameobject(PolygonWall(rel_points, friction=friction, pos=V2(width, height), visible=False))
        # left wall
        rel_points = [V2(0, 0), V2(0, height/2), V2(0, height)]
        self.add_gameobject(PolygonWall(rel_points, friction=friction, pos=V2(0, 0), visible=False))
        # top wall
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(666, 297), V2(666, 0), V2(0, 0), V2(0, 267), V2(21, 217), V2(47, 176), V2(
            96, 124), V2(165, 78), V2(244, 51), V2(336, 42), V2(423, 51), V2(504, 80), V2(558, 113), V2(596, 148), V2(620, 178), V2(639, 208), V2(652, 240)]))
        self.add_gameobject(PolygonWall(rel_points, friction=0, visible=True))

        # plunger cap wall with left outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(616, 1000), V2(619, 341), V2(603, 265), V2(568, 203), V2(526, 163), V2(474, 130), V2(451, 134), V2(440, 152), V2(447, 172), V2(498, 207), V2(
            532, 241), V2(556, 289), V2(563, 334), V2(543, 407), V2(518, 456), V2(520, 481), V2(535, 504), V2(557, 482), V2(598, 521), V2(578, 546), V2(600, 570), V2(600, 900), V2(555, 915), V2(361, 1000)]))
        self.add_gameobject(PolygonWall(rel_points, friction=0, visible=True))
        # left bottom outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf),
                          [V2(0, 900), V2(45, 915), V2(241, 1000), V2(0, 1000)]))
        self.add_gameobject(PolygonWall(rel_points, friction=0, visible=True))

        # upper thing of left side ball guidence
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf), [V2(135, 512), V2(146, 508), V2(147, 497), V2(115, 424), V2(104, 354), V2(115, 289), V2(145, 236), V2(186, 199), V2(
            222, 173), V2(232, 156), V2(223, 138), V2(202, 131), V2(165, 149), V2(114, 191), V2(80, 242), V2(62, 298), V2(60, 359), V2(72, 416), V2(101, 480), V2(124, 506)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))
        # lower thing of left side ball guidence
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(0, 666), V2(34, 610), V2(70, 578), V2(78, 562), V2(70, 545), V2(35, 496), V2(11, 435), V2(0, 326)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))

        # left flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(45, 758), V2(43, 821), V2(51, 832), V2(162, 888), V2(177, 862), V2(68, 806), V2(53, 792)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))
        # right flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(559, 757), V2(558, 825), V2(548, 837), V2(437, 890), V2(423, 860), V2(538, 804), V2(550, 792)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))

        # obstacle above the left flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(105, 729), V2(110, 746), V2(163, 774), V2(
            179, 779), V2(191, 769), V2(193, 754), V2(140, 650), V2(127, 645), V2(114, 646), V2(105, 656)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True,
                            add_to_score=20).add_components(Bumper(bumper_strength)))
        # obstacle above the right flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(498, 734), V2(491, 747), V2(433, 780), V2(
            422, 779), V2(411, 770), V2(410, 752), V2(462, 653), V2(475, 645), V2(489, 647), V2(496, 658)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True,
                            add_to_score=20).add_components(Bumper(bumper_strength)))

        # center obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf), [V2(260, 556), V2(255, 567), V2(262, 578), V2(
            305, 598), V2(320, 600), V2(334, 598), V2(375, 579), V2(382, 568), V2(377, 556), V2(330, 535), V2(307, 535)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True,
                            add_to_score=10).add_components(Bumper(bumper_strength)))
        # left side obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(169, 410), V2(177, 394), V2(199, 396), V2(232, 457), V2(223, 476), V2(201, 473)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True,
                            add_to_score=10).add_components(Bumper(bumper_strength)))
        # right side obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(480, 412), V2(471, 394), V2(451, 397), V2(417, 457), V2(426, 476), V2(447, 475)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True,
                            add_to_score=10).add_components(Bumper(bumper_strength)))
        # top left obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(298, 104), V2(286, 116), V2(285, 174), V2(297, 188), V2(308, 175), V2(309, 116)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))
        # top right obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(375, 106), V2(363, 118), V2(362, 175), V2(374, 188), V2(387, 177), V2(387, 119)]))
        self.add_gameobject(PolygonWall(rel_points, friction=friction, visible=True))

        # bumpers
        self.add_gameobject(CircleWall(V2(320, 420)*asf, 40*asf, color=Color(255, 0, 0),
                            add_to_score=100).add_components(Bumper(bumper_strength)))
        self.add_gameobject(CircleWall(V2(388, 292)*asf, 35*asf, color=Color(240, 212, 88),
                            add_to_score=50).add_components(Bumper(bumper_strength)))
        self.add_gameobject(CircleWall(V2(250, 282)*asf, 30*asf, color=Color(100, 201, 231),
                            add_to_score=25).add_components(Bumper(bumper_strength)))

        # text
        self.score_text = Text(self.screen, (.01, .01), (0, 0), text=f"Score: {self.score}", font_size=50*asf)
        self.ui_elements.append(self.score_text)
        self.balls_text = Text(self.screen, (.97, .01), (1, 0), text=f"Balls: {self.remaining_balls}", font_size=50*asf)
        self.ui_elements.append(self.balls_text)
        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        self.score_text.text.set_value(f"Score: {self.score}")
        self.balls_text.text.set_value(f"Balls: {self.remaining_balls}")
        if (self.remaining_balls <= 0 and self.active_balls <= 0) and not self.end_game:
            self.game_ended(events)

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
                    if self.remaining_balls > 0 and self.active_balls <= 0:
                        self.add_ball()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_flipper.transform.init_smooth_rotation(30)

                elif event.key == pygame.K_RIGHT:
                    self.right_flipper.transform.init_smooth_rotation(150)

        if self.paused:
            return self.pause_menu.update(events, self.blured)
        
        if self.end_game:
            return self.end_menu.update(events, self.blured)

        super().update(0 if (self.paused or self.end_game) else delta_time, events)
        if self.paused:
            return

        for element in self.ui_elements:
            element.update_events(events)
            element.draw()

    def add_ball(self) -> None:
        self.remaining_balls -= 1
        width = self.screen.get_width()
        height = self.screen.get_height()
        asf = Options().asf
        self.add_gameobject(Ball(V2(width + self.ball_radius*2, height-250*asf), radius=self.ball_radius))

    def pause(self, events: list[Event]) -> None:
        # Update need to be called so that all objects are visible in the background
        self.blured = self.get_blured(events)
        self.paused = True

    def unpause(self) -> None:
        self.paused = False

    def change_scene(self, scene_name: str) -> None:
        self.serialize()
        self.scene_manager.change_scene(scene_name)

    def get_blured(self, events: list[Event]) -> Surface:
        super().update(0, events)
        for element in self.ui_elements:
            element.update_events(events)
            element.draw()
        background = self.screen.copy()
        radius = Options().asf * 10

        # Convert the surface to a numpy array
        array = pygame.surfarray.pixels3d(background)

        # Apply a Gaussian blur to the array
        blurred_array = gaussian_filter(array, sigma=(radius, radius, 0))

        # Convert the blurred array back to a surface
        blurred_surface = pygame.surfarray.make_surface(blurred_array)
        return blurred_surface

    def game_ended(self, events: list[Event]) -> None:
        self.end_menu = EndMenu(self.screen, self.scene_manager, self.score)
        self.end_game = True
        self.blured = self.get_blured(events)
        self.save_score()

    def unload(self) -> None:
        self.ui_elements.clear()
        return super().unload()
