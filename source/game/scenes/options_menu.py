from pathlib import Path
from pygame import Surface
import pygame
from source.api.management.background_manager import BackgroundManager
from source.api.scene.scene import BaseDisplay
from pygame.event import Event
from pygame.freetype import Font
from source.api.ui.button import Button
from source.api.ui.button_style import ButtonStyle
from source.api.ui.slider import Slider
from source.api.ui.text import Text
from source.api.ui.ui_element_base import UIElementBase

from data.constants import DEFAULT_BUTTON_STYLE, DEFAULT_FONT
from source.api.management.options_manager import OptionsManager


class OptionsMenu(BaseDisplay):
    """
    A class to represent the options menu.

    This class extends the BaseDisplay class and adds functionality for the options menu.

    Attributes:
        button_style (ButtonStyle): The button style to use for the menu.
        font (Font): The font to use for the menu.
        ui_elements (list): The list of UI elements in the menu.
        options (Options): The options.
        new_master_volume (float): The new master volume.
        new_music_volume (float): The new music volume.
        new_sfx_volume (float): The new sfx volume.
        asf (float): The global scale.

    Methods:
        __init__(self, screen: Surface, scene_manager)
        awake(self)
        update(self, delta_time: float, events: list[Event])
        unload(self)
        set_master_volume(self, value: float)
        set_music_volume(self, value: float)
        set_sfx_volume(self, value: float)
        set_global_scale(self, value: float)
        _apply_changes(self)
    """

    def __init__(self, screen: Surface, scene_manager, background_manager: BackgroundManager) -> None:
        """
        Initializes the options menu.

        Parameters:
            screen (Surface): The screen to draw the menu on.
            scene_manager (SceneManager): The scene manager.
        """

        self.button_style = ButtonStyle(DEFAULT_BUTTON_STYLE)

        self.font = Font(DEFAULT_FONT, 75)
        self.ui_elements: list[UIElementBase] = []

        self.options = OptionsManager()
        self.new_master_volume = self.options.master_volume
        self.new_music_volume = self.options.music_volume
        self.new_sfx_volume = self.options.sfx_volume
        self.asf = self.options.asf

        super().__init__(screen, scene_manager, background_manager)

    def awake(self) -> None:
        """
        Creates the menu.

        Returns:
            None
        """
        button_width = int(250 * self.asf)
        button_height = int(125 * self.asf)
        button_font_size = int(50 * self.asf)

        text_relativ_x = .05
        text_font_size = int(40 * self.asf)

        self.ui_elements.append(Text(self.screen, (.5, .05), (.5, 0), text="Options",
                          width=self.options.resolution[0]*7/8, font=self.font))

        # Sliders
        slider_relativ_x = .75
        slider_width = int(250 * self.asf)
        slider_height = int(50 * self.asf)

        self.ui_elements.append(Text(self.screen, (.5, .25), (.5, .5), text="Resolution",
                                font=self.font, font_size=text_font_size*2))

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .35), (0, .5),
                                text="Global Scale", font=self.font, font_size=text_font_size))
        gloabl_scale_slider = Slider(self.screen, (slider_relativ_x, .35), (.5, .5),
                                     slider_width, slider_height, min=0.5, max=2.0, step=0.5, initial_value=self.asf)
        gloabl_scale_slider.value.subscribe(lambda value: self.set_global_scale(value))
        self.ui_elements.append(gloabl_scale_slider)

        self.ui_elements.append(Text(self.screen, (.5, .5), (.5, .5), text="Sound",
                                font=self.font, font_size=text_font_size*2))

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .6), (0, .5),
                                text="Master Volume", font=self.font, font_size=text_font_size))
        master_volume_slider = Slider(self.screen, (slider_relativ_x, .6), (.5, .5),
                                      slider_width, slider_height, min=0, max=100, step=1, initial_value=self.new_master_volume)
        master_volume_slider.value.subscribe(lambda value: self.set_master_volume(value))
        self.ui_elements.append(master_volume_slider)

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .7), (0, .5),
                                text="Music Volume", font=self.font, font_size=text_font_size))
        music_volume_slider = Slider(self.screen, (slider_relativ_x, .7), (.5, .5),
                                     slider_width, slider_height, min=0, max=100, step=1, initial_value=self.new_music_volume)
        music_volume_slider.value.subscribe(lambda value: self.set_music_volume(value))
        self.ui_elements.append(music_volume_slider)

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .8), (0, .5),
                                text="SFX Volume", font=self.font, font_size=text_font_size))
        sfx_volume_slider = Slider(self.screen, (slider_relativ_x, .8), (.5, .5),
                                   slider_width, slider_height, min=0, max=100, step=1, initial_value=self.new_sfx_volume)
        sfx_volume_slider.value.subscribe(lambda value: self.set_sfx_volume(value))
        self.ui_elements.append(sfx_volume_slider)

        back_button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, left_sided=True, bottom_sided=True)
        apply_button = self.button_style.create_button_set(
            (button_width, button_height), 0.03, 3, right_sided=True, bottom_sided=True)

        self.ui_elements.append(Button(self.screen, (0, 1), (0, 1), button_width, button_height,
                                       inactive_button=back_button[0], hover_button=back_button[1], pressed_button=back_button[2],
                                       text="Back", font_size=button_font_size, on_click=lambda: self.scene_manager.change_scene("main_menu")))

        self.ui_elements.append(Button(self.screen, (1, 1), (1, 1), button_width, button_height,
                                       inactive_button=apply_button[0], hover_button=apply_button[1], pressed_button=apply_button[2],
                                       text="Apply", font_size=button_font_size, on_click=lambda: self._apply_changes()))

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        """
        Updates the menu.

        Parameters:
            delta_time (float): The time since the last frame.
            events (list): The list of pygame events.

        Returns:
            None
        """
        super().update(delta_time, events)

        for element in self.ui_elements:
            element.draw()
            element.update_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.change_scene("main_menu")
    
    def unload(self) -> None:
        """
        Unloads the menu.

        Returns:
            None
        """
        self.options.save()
        self.ui_elements.clear()
        return super().unload()

    def set_master_volume(self, value: float) -> None:
        """
        Sets the master volume.

        Parameters:
            value (float): The new value.

        Returns:
            None
        """
        self.new_master_volume = value

    def set_music_volume(self, value: float) -> None:
        """
        Sets the music volume.

        Parameters:
            value (float): The new value.

        Returns:
            None
        """
        self.new_music_volume = value

    def set_sfx_volume(self, value: float) -> None:
        """
        Sets the sfx volume.

        Parameters:
            value (float): The new value.

        Returns:
            None
        """
        self.new_sfx_volume = value

    def set_global_scale(self, value: float) -> None:
        """
        Sets the global scale.

        Parameters:
            value (float): The new value.

        Returns:
            None
        """
        self.asf = value

    def _apply_changes(self):
        """
        Applies the changes.

        Returns:
            None
        """
        self.options.master_volume = self.new_master_volume
        self.options.music_volume = self.new_music_volume
        self.options.sfx_volume = self.new_sfx_volume
        self.options.asf = self.asf
        self.options.save()

        pygame.display.set_mode(self.options.resolution)
        self.scene_manager.change_scene("options_menu")
