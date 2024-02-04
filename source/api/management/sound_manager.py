import os
from pathlib import Path
import random

import pygame
from pygame.mixer import Sound
from data.constants import ASSETS_PATH

# Singelton


class SoundManager:
    """
    A class to represent the options.

    This class is a singleton and can be accessed by calling SoundManager().

    Attributes:
        music_files (list): A list of music files.
        current_music (str): The current music file.
        options (Options): The options.

    Methods:
        __new__(cls) -> 'SoundManager'
        set_options(self, options) -> None
        init(self) -> None
        load_music(self) -> None
        play_music(self) -> None
        update(self, events: list[pygame.event.Event]) -> None
        play_sfx(self, sound: Sound) -> None
        update_volume(self) -> None
    """

    _instance = None

    def __new__(cls) -> 'SoundManager':
        """
        Create a new instance of the Options class if it does not exist yet.

        Returns:
            Options: The instance of the Options class.
        """
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def set_options(self, options):
        """
        Sets the options. This method is needed, because of circular imports.

        Parameters:
            options (Options): The options.
        """
        self.options = options
        self.update_volume()

    def init(self):
        pygame.mixer.init()
        self.music_files = []
        self.current_music = None
        self.channel = 0

    def load_music(self):
        """
        Loads all music files from the specified directory.
        """
        music_dir = ASSETS_PATH / Path('music')
        for file in os.listdir(music_dir):
            self.music_files.append(os.path.join(music_dir, file))

    def play_music(self):
        """
        Plays a music file randomly.
        """
        if not self.music_files:
            print("No music files loaded.")
            return

        # Choose a music file randomly
        self.current_music = random.choice(self.music_files)

        # Load and play the music file
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.play(1)

        # Set the end music event
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume((self.options.music_volume / 100) * (self.options.master_volume / 100))

    def update(self, events: list[pygame.event.Event]) -> None:
        """
        Handles the end of a music track.
        """
        for event in events:
            if event.type == pygame.USEREVENT:
                self.play_music()

    def play_sfx(self, sound: Sound) -> None:
        """
        Plays a sound effect.

        Parameters:
            sound (str): The sound to play.

        Returns:
            None
        """
        self.channel = (self.channel+1) % 8
        sound.set_volume((self.options.sfx_volume / 100) * (self.options.master_volume / 100))
        pygame.mixer.Channel(self.channel).play(sound)

    def update_volume(self) -> None:
        """
        Updates the volume.

        Returns:
            None
        """
        pygame.mixer.music.set_volume((self.options.music_volume / 100) * (self.options.master_volume / 100))
