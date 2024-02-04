from pathlib import Path
from pygame import Color, Surface
from pygame import Vector2 as V2
import pygame
from pygame.event import Event
from source.api.components.bumper import Bumper
from source.api.components.change_score import ChangeScore
from source.api.components.life_timer import LifeTimer
from source.api.components.scale_renderer import ScaleRenderer
from source.api.components.simple_movement import SimpleMovement
from source.api.management.background_manager import BackgroundManager
from source.api.scene.scene import Scene
from source.api.ui.text import Text
from source.api.ui.ui_element_base import UIElementBase
from data.constants import ASSETS_PATH
from source.game.objects.ball import Ball
from source.game.objects.flipper import Flipper
from source.game.objects.plunger import Plunger
from source.game.objects.spring import Spring
from source.game.objects.target import TargetBase, TargetGroup
from source.game.objects.teleporter import Teleporter
from source.game.objects.wall import CircleWall, PolygonWall
from source.game.scenes.submenus.end_menu import EndMenu
from source.game.scenes.submenus.pause_menu import PauseMenu
from source.api.management.options_manager import OptionsManager
from scipy.ndimage.filters import gaussian_filter
from source.api.utils import utils


class MainPinball(Scene):
    """
    A class to represent the main pinball scene. This class is used to create the main pinball scene.

    Attributes:
        screen (Surface): The screen to draw the scene on.
        scene_manager (SceneManager): The scene manager.
        ui_elements (list): A list of UI elements.
        left_flipper (Flipper): The left flipper.
        right_flipper (Flipper): The right flipper.
        blured (Surface): The blured background.
        flipper_sound (pygame.mixer.Sound): The sound to play when the flipper is hit.
        spawn_ball_sound (pygame.mixer.Sound): The sound to play when a ball is spawned.
        game_over_sound (pygame.mixer.Sound): The sound to play when the game is over.
        bonus_ball_sound (pygame.mixer.Sound): The sound to play when a bonus ball is spawned.
        score_threshold (int): The score threshold to spawn a bonus ball.

    Methods:
        __init__(self, screen: Surface, scene_manager)
        awake(self)
        update(self, delta_time: float, events: list[Event])
        add_ball(self)
        pause(self, events: list[Event])
        unpause(self)
        change_scene(self, scene_name: str)
        get_blured(self, events: list[Event])
        game_ended(self, events: list[Event])
        unload(self)
    """

    def __init__(self, screen: pygame.Surface, scene_manager, background_manager: BackgroundManager):
        """
        Creates the main pinball scene.

        Arguments:
            screen (Surface): The screen to draw the scene on.
            scene_manager (SceneManager): The scene manager.
        """

        super().__init__(screen, scene_manager, background_manager)

        self.left_flipper: Flipper = None  # type: ignore
        self.right_flipper: Flipper = None  # type: ignore

        self.blured: Surface = None  # type: ignore
        self.ui_elements: list[UIElementBase] = []

        self.flipper_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/flipper.wav"))
        self.spawn_ball_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/spawn_ball.wav"))
        self.game_over_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/game_over.wav"))
        self.bonus_ball_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bonus_ball.wav"))

        self.score_scaling = 2

    def awake(self) -> None:
        """
        Creates the main pinball scene.

        Returns:
            None
        """

        bumper_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bumper.wav"))
        bumper_sound01 = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/bumper01.wav"))

        options = OptionsManager()
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
        scale_duration = .075
        scale_strength = .25

        self.add_gameobject(Plunger(self, V2(width - self.ball_radius*3, height),
                            V2(width, height), impuls_range=(int(1500*asf**(2/3)), int(1700*asf**(2/3)))))

        self.left_flipper = Flipper(self, V2(300*asf - 130 * asf, height - 125*asf), 30)
        self.right_flipper = Flipper(self, V2(300*asf + 130 * asf, height - 125*asf), 150)
        self.add_gameobject(self.right_flipper)
        self.add_gameobject(self.left_flipper)
        # ball spawn container
        rel_points = [V2(0, 125*asf), V2(0, 0), V2(125*asf, -125*asf), V2(125*asf, -250*asf)]
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction,
                            pos=V2(width, height-125*asf), visible=False))

        # right wall
        rel_points = [V2(0, -125*asf - self.ball_radius*4), V2(0, -height/2), V2(0, -height)]
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, pos=V2(width, height), visible=False))
        # left wall
        rel_points = [V2(0, 0), V2(0, height/2), V2(0, height)]
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, pos=V2(0, 0), visible=False))
        # top wall
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(666, 297), V2(666, 0), V2(0, 0), V2(0, 267), V2(21, 217), V2(47, 176), V2(
            96, 124), V2(165, 78), V2(244, 51), V2(336, 42), V2(423, 51), V2(504, 80), V2(558, 113), V2(596, 148), V2(620, 178), V2(639, 208), V2(652, 240)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=0, visible=True))

        # plunger cap wall with left outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(616, 1000), V2(619, 341), V2(603, 265), V2(568, 203), V2(524, 163), V2(474, 130), V2(459, 131), V2(447, 137), V2(439, 149), V2(
            441, 164), V2(449, 174), V2(498, 207), V2(532, 241), V2(556, 289), V2(563, 334), V2(543, 407), V2(517, 461), V2(518, 482), V2(557, 482), V2(602, 522), V2(600, 900), V2(555, 915), V2(361, 1000)]))

        self.add_gameobject(PolygonWall(self, rel_points, friction=0, visible=True))
        # left bottom outlet
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf),
                          [V2(0, 900), V2(45, 915), V2(241, 1000), V2(0, 1000)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=0, visible=True))

        # upper thing of left side ball guidence
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf), [V2(136, 510), V2(145, 510), V2(149, 503), V2(146, 494), V2(115, 424), V2(104, 354), V2(114, 288), V2(145, 236), V2(186, 199), V2(
            225, 171), V2(231, 157), V2(226, 141), V2(210, 131), V2(191, 133), V2(165, 149), V2(114, 191), V2(80, 242), V2(62, 298), V2(60, 359), V2(75, 424), V2(100, 474), V2(118, 497)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))
        # lower thing of left side ball guidence
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(0, 666), V2(34, 610), V2(70, 578), V2(78, 562), V2(70, 545), V2(35, 496), V2(11, 435), V2(0, 326)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))

        # left flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(44, 787), V2(43, 821), V2(53, 838), V2(162, 889), V2(177, 862), V2(63, 807), V2(56, 800), V2(53, 787), V2(49, 785)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))
        # right flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(
            x*asf), [V2(555, 787), V2(557, 821), V2(546, 838), V2(437, 889), V2(423, 862), V2(536, 807), V2(543, 800), V2(546, 787), V2(550, 785)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))

        # obstacle above the left flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(105, 729), V2(109, 745), V2(120, 754), V2(161, 774), V2(175, 779), V2(187, 774), V2(193, 766), V2(193, 754), V2(143, 656), V2(134, 646), V2(123, 643), V2(111, 647), V2(104, 659)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True, hit_sound=bumper_sound).add_components(
            Bumper(bumper_strength), ChangeScore(20), ScaleRenderer(scale_duration, scale_strength)))
        # obstacle above the right flipper extension
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf), [V2(495, 729), V2(491, 745), V2(479, 754), V2(439, 774), V2(425, 779), V2(413, 774), V2(407, 766), V2(407, 754), V2(457, 656), V2(466, 646), V2(477, 643), V2(489, 647), V2(496, 659)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True, hit_sound=bumper_sound).add_components(
            Bumper(bumper_strength), ChangeScore(20), ScaleRenderer(scale_duration, scale_strength)))

        # center obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf), [V2(260, 556), V2(255, 567), V2(262, 578), V2(
            305, 598), V2(320, 600), V2(334, 598), V2(375, 579), V2(382, 568), V2(377, 556), V2(330, 535), V2(307, 535)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True, hit_sound=bumper_sound).add_components(
            Bumper(bumper_strength), ChangeScore(10), ScaleRenderer(scale_duration, scale_strength)))
        # left side obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(169, 411), V2(174, 398), V2(185, 393), V2(199, 397), V2(232, 457), V2(228, 473), V2(216, 479), V2(201, 471)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True, hit_sound=bumper_sound)
                            .add_components(Bumper(bumper_strength), ChangeScore(10), ScaleRenderer(scale_duration, scale_strength)))
        # right side obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(481, 411), V2(476, 398), V2(465, 393), V2(451, 397), V2(418, 457), V2(422, 473), V2(434, 479), V2(449, 471)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True, hit_sound=bumper_sound).add_components(
            Bumper(bumper_strength), ChangeScore(10), ScaleRenderer(scale_duration, scale_strength)))
        # top left obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(291, 108), V2(285, 117), V2(285, 177), V2(292, 186), V2(303, 186), V2(309, 176), V2(309, 117), V2(304, 108)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))
        # top right obstacle
        rel_points = list(map(lambda x: utils.ceil_vector((x)*asf),
                          [V2(379, 108), V2(385, 117), V2(385, 177), V2(378, 186), V2(367, 186), V2(361, 176), V2(361, 117), V2(366, 108)]))
        self.add_gameobject(PolygonWall(self, rel_points, friction=friction, visible=True))

        # bumpers
        self.add_gameobject(CircleWall(self, V2(320, 420)*asf, 40*asf, color=Color(255, 0, 0), hit_sound=bumper_sound01
                                       ).add_components(Bumper(bumper_strength), ScaleRenderer(scale_duration, scale_strength), ChangeScore(200, True, 2, 2)))
        self.add_gameobject(CircleWall(self, V2(388, 292)*asf, 35*asf, color=Color(240, 212, 88), hit_sound=bumper_sound01
                                       ).add_components(Bumper(bumper_strength), ScaleRenderer(scale_duration, scale_strength), ChangeScore(100, True, 2, 2)))
        self.add_gameobject(CircleWall(self, V2(250, 282)*asf, 30*asf, color=Color(100, 201, 231), hit_sound=bumper_sound01
                                       ).add_components(Bumper(bumper_strength), ScaleRenderer(scale_duration, scale_strength), ChangeScore(50, True, 2, 2)))
        self.add_gameobject(CircleWall(self, V2(300, 700)*asf, 20*asf, color=Color(100, 201, 231), hit_sound=bumper_sound01).add_components(Bumper(
            bumper_strength), ScaleRenderer(scale_duration, scale_strength, True), ChangeScore(150, True, 2, 2), SimpleMovement(V2(250, 700)*asf, V2(350, 700)*asf, .75)))
        # life bumpers
        colors: list[Color] = [Color(54, 54, 54), Color(63, 75, 77), Color(64, 92, 97), Color(
            59, 108, 117), Color(48, 130, 145), Color(28, 151, 173), Color(6, 165, 194), Color(2, 132, 207)]
        self.add_gameobject(CircleWall(self, V2(25, 760)*asf, 15*asf, ).add_components(
                            Bumper((bumper_strength[0]*2, bumper_strength[1]*2)), ScaleRenderer(scale_duration, scale_strength), ChangeScore(50, True, 2, 2), LifeTimer(colors, 6)))
        self.add_gameobject(CircleWall(self, V2(578, 760)*asf, 15*asf).add_components(
                            Bumper((bumper_strength[0]*2, bumper_strength[1]*2)), ScaleRenderer(scale_duration, scale_strength), ChangeScore(50, True, 2, 2), LifeTimer(colors, 6)))

        # teleporter
        rel_points = list(map(lambda x: utils.ceil_vector(x*asf),
                          [V2(518, 482), V2(557, 482), V2(602, 522), V2(601, 565)]))
        self.add_gameobject(Teleporter(self, rel_points, V2(337, 100)*asf))

        # springs
        # left
        self.add_gameobject(Spring(self, V2(23, 700)*asf, width=10*asf, height=50 *
                            asf, color=Color(150, 150, 150), add_to_score=25))
        self.add_gameobject(Spring(self, V2(70, 650)*asf, width=10*asf, height=50 *
                            asf, color=Color(150, 150, 150), add_to_score=25))
        # right
        self.add_gameobject(Spring(self, V2(580, 700)*asf, width=10*asf, height=50 *
                            asf, color=Color(150, 150, 150), add_to_score=25))
        self.add_gameobject(Spring(self, V2(532, 650)*asf, width=10*asf, height=50 *
                            asf, color=Color(150, 150, 150), add_to_score=25))
        # center
        self.add_gameobject(Spring(self, V2(300, 800)*asf, width=10*asf, height=50 *
                            asf, color=Color(150, 150, 150), add_to_score=25))
        # tube
        self.add_gameobject(Spring(self, V2(70, 493)*asf, width=10*asf, height=50*asf,
                            color=Color(150, 150, 150), add_to_score=25, rotation=-35))
        
        # target
        targets = [
            TargetBase(self, V2(132,259)*asf, rotation=30),
            TargetBase(self, V2(107,357)*asf, rotation=2),
            TargetBase(self, V2(128,450)*asf, rotation=-28)
        ]
        self.add_gameobjects(*targets)

        self.add_gameobject(TargetGroup(self, targets))

        # text
        self.score_text = Text(self.screen, (.01, .01), (0, 0), text=f"Score: {self.score}", font_size=50*asf)
        self.ui_elements.append(self.score_text)
        self.balls_text = Text(self.screen, (.97, .01), (1, 0), text=f"Balls: {self.remaining_balls}", font_size=50*asf)
        self.ui_elements.append(self.balls_text)

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Updates the main pinball scene.

        Arguments:
            delta_time (float): The time since the last frame.
            events (list): A list of pygame events.

        Returns:
            None
        """
        super().update(0 if (self.paused or self.end_game) else delta_time, events)  # update the scene

        if self.score >= self.score_threshold:
            self.add_ball(True)
            self.sound_manager.play_sfx(self.bonus_ball_sound)
            self.score_threshold *= self.score_scaling

        self.score_text.text.set_value(f"Score: {self.score}")
        self.balls_text.text.set_value(f"Balls: {self.remaining_balls}")
        if (self.remaining_balls <= 0 and self.active_balls <= 0) and not self.end_game:
            self.game_ended(events)

        for event in events:
            if event.type == pygame.KEYDOWN:  # flipper rotation
                if event.key == pygame.K_ESCAPE:  # pause
                    if self.paused:
                        self.unpause()
                    else:
                        self.pause(events)

                elif event.key == pygame.K_LEFT:  # left flipper
                    self.left_flipper.transform.init_smooth_rotation(-10)
                    self.sound_manager.play_sfx(self.flipper_sound)
                elif event.key == pygame.K_RIGHT:  # right flipper
                    self.right_flipper.transform.init_smooth_rotation(190)
                    self.sound_manager.play_sfx(self.flipper_sound)
                elif event.key == pygame.K_SPACE:  # plunger
                    if self.remaining_balls > 0 and self.active_balls <= 0:  # if there are balls left and no active balls
                        self.add_ball()

            elif event.type == pygame.KEYUP:  # stop flipper rotation
                if event.key == pygame.K_LEFT:  # left flipper
                    self.left_flipper.transform.init_smooth_rotation(30)

                elif event.key == pygame.K_RIGHT:  # right flipper
                    self.right_flipper.transform.init_smooth_rotation(150)

        if self.paused:  # if the game is paused, update the pause menu
            return self.pause_menu.update(events, self.blured)

        if self.end_game:  # if the game is over, update the end menu
            return self.end_menu.update(events, self.blured)

        if self.paused:  # if the game is paused, return
            return

        for element in self.ui_elements:  # update the ui elements
            element.update_events(events)
            element.draw()

    def add_ball(self, forced_spawn=False) -> None:
        """
        Adds a ball to the scene.

        Arguments:
            froced_spawn (bool): If the ball should be spawned even if there are no balls left.

        Returns:
            None
        """

        self.sound_manager.play_sfx(self.spawn_ball_sound)
        if not forced_spawn:
            self.remaining_balls -= 1
        width = self.screen.get_width()
        height = self.screen.get_height()
        asf = OptionsManager().asf
        # .add_components(Tray(5, Color(200,200,200)))
        self.add_gameobject(Ball(self, V2(width + self.ball_radius*2, height-250*asf),
                            radius=self.ball_radius, forced_spawn=forced_spawn))

    def pause(self, events: list[Event]) -> None:
        """
        Pauses the game.

        Arguments:
            events (list): A list of pygame events.

        Returns:
            None
        """

        # Update need to be called so that all objects are visible in the background
        self.blured = self.get_blured(events)  # get the blured background
        self.paused = True  # pause the game

    def unpause(self) -> None:
        """
        Unpauses the game.

        Returns:
            None
        """

        self.paused = False

    def change_scene(self, scene_name: str) -> None:
        """
        Changes the scene.

        Arguments:
            scene_name (str): The name of the scene to change to.

        Returns:
            None
        """

        self.serialize()
        self.scene_manager.change_scene(scene_name)

    def get_blured(self, events: list[Event]) -> Surface:
        """
        Gets the blured background.

        Arguments:
            events (list): A list of pygame events.

        Returns:
            Surface: The blured background.
        """

        # Update need to be called so that all objects are visible in the background
        super().update(0, events)  # update the scene
        for element in self.ui_elements:  # update the ui elements
            element.update_events(events)  # update the ui elements
            element.draw()  # draw the ui elements
        background = self.screen.copy()  # copy the screen to a surface
        radius = OptionsManager().asf * 10

        # Convert the surface to an array
        array = pygame.surfarray.pixels3d(background)

        # Apply a Gaussian blur to the array
        blurred_array = gaussian_filter(array, sigma=(radius, radius, 0))

        # Convert the blurred array back to a surface
        blurred_surface = pygame.surfarray.make_surface(blurred_array)
        return blurred_surface  # return the blurred surface

    def game_ended(self, events: list[Event]) -> None:
        """
        Ends the game.

        Arguments:
            events (list): A list of pygame events.

        Returns:
            None
        """

        self.end_menu = EndMenu(self.screen, self.scene_manager, self.score)
        self.end_game = True
        self.blured = self.get_blured(events)
        self.save_score()
        self.sound_manager.play_sfx(self.game_over_sound)

    def unload(self) -> None:
        """
        Unloads the main pinball scene.

        Returns:
            None
        """
        self.ui_elements.clear()
        return super().unload()
