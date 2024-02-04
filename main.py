import sys
import pygame
from source.api.management.scene_manager import SceneManager
from source.api.management.sound_manager import SoundManager
import data.constants as constants
from source.api.management.options_manager import OptionsManager

"""
This is the main file of the game. It initializes PyGame and creates the screen and clock. It also creates the sound manager and scene manager.
The main event loop is also located here.
"""

def main():
    """
    The main function of the game. It initializes PyGame and creates the screen and clock. It also creates the sound manager and scene manager.
    The main event loop is also located here.
    """

    # Initialize PyGame
    pygame.init()

    options = OptionsManager() # Load options
    screen = pygame.display.set_mode(options.resolution) # Create the screen
    clock = pygame.time.Clock() # Create clock

    sound_manager = SoundManager() # Create sound manager
    sound_manager.set_options(options) # Set options
    sound_manager.load_music() # Load music
    sound_manager.play_music() # Play music

    scene_manager = SceneManager(screen, "main_menu") # Create scene manager and set default scene to main_menu

    # Main event loop
    while True:
        events = pygame.event.get() # Get all events
        sound_manager.update(events) # Update sound manager
        for event in events:
            if event.type == pygame.QUIT:   
                pygame.quit()
                sys.exit()
            
        scene_manager.active_scene.update(constants.DELTA_TIME, events)  # Update the scene

        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAMERATE)  # Limit the framerate

if __name__ == "__main__":
    main()  # Run the main function