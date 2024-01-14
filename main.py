from typing import Callable
import pygame
from pathlib import Path
from api.management.scene_manager import SceneManager
import constants
from options import Options

# Initialize PyGame
pygame.init()

# Making display screen
options = Options()
screen = pygame.display.set_mode(options.resolution)
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

scene_manager = SceneManager(screen, "main_menu")
# Main event loop
while running:
    bg = pygame.transform.scale(bg_orig, (screen.get_width(), screen.get_height()))  # scales background image to fit screen size
    screen.blit(bg, pygame.Vector2())  # redraws background image

    events = pygame.event.get()  # Get all events
    for event in events:
        if event.type == pygame.QUIT:  
            running = False
            break
        
    scene_manager.active_scene.update(constants.DELTA_TIME, events)  # Update the scene

    pygame.display.flip()  # Update the display
    clock.tick(constants.FRAMERATE)  # Limit the framerate