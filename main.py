import sys
import pygame
from source.api.management.scene_manager import SceneManager
from source.api.management.sound_manager import SoundManager
import constants
from source.api.management.options import Options

# Initialize PyGame
pygame.init()

options = Options() # Load options
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