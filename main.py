import pygame
from pathlib import Path
from api.management.scene_manager import SceneManager
import constants

# Initialize PyGame
pygame.init()

# Making display screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()
bg = pygame.transform.scale(bg_orig, (screen.get_width(), screen.get_height()))  # scales background image to fit screen size

# Setup 
running = True

scene_manager = SceneManager(screen, "main_pinball")

# Main event loop
while running:
    screen.blit(bg, pygame.Vector2())  # redraws background image

    events = pygame.event.get()  # Get all events
    for event in events:
        if event.type == pygame.QUIT:  
            running = False
            break

    scene_manager.active_scene.update(constants.DELTA_TIME, events)  # Update the scene

    pygame.display.flip()  # Update the display
    clock.tick(constants.FRAMERATE)  # Limit the framerate
