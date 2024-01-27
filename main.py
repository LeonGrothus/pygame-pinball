import sys
from typing import Callable
import pygame
from pathlib import Path
from api.management.scene_manager import SceneManager
from api.management.sound_manager import SoundManager
import constants
from data.options import Options

# Initialize PyGame
pygame.init()

options = Options() # Load options
screen = pygame.display.set_mode(options.resolution) # Create the screen
bg_orig = pygame.image.load(constants.ASSETS_PATH / Path("images/background.jpg")).convert() # Load background image
clock = pygame.time.Clock() # Create clock

sound_manager = SoundManager() # Create sound manager
sound_manager.set_options(options) # Set options
sound_manager.load_music() # Load music
sound_manager.play_music() # Play music

scene_manager = SceneManager(screen, "main_menu") # Create scene manager and set default scene to main_menu

# Main event loop
while True:
    bg = pygame.transform.scale(bg_orig, (screen.get_width(), screen.get_height()))  # scales background image to fit screen size
    screen.blit(bg, pygame.Vector2())  # redraws background image

    events = pygame.event.get() # Get all events
    sound_manager.update(events) # Update sound manager
    for event in events:
        if event.type == pygame.QUIT:   
            pygame.quit()
            sys.exit()
        
    scene_manager.active_scene.update(constants.DELTA_TIME, events)  # Update the scene

    pygame.display.flip()  # Update the display
    clock.tick(constants.FRAMERATE)  # Limit the framerate