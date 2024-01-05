import pygame
from pathlib import Path
from game.objects.flipper import Flipper
from api.objects.gameObject import GameObject
import constants
from game.scenes.main_pinball import MainPinball

# Initialize PyGame
pygame.init()

# Making display screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

scene = MainPinball(screen)
scene.awake()

# Main event loop
while running:
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0))  # redraws background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # Rotate all game objects 90 degrees to the right
                game_object: GameObject
                for game_object in scene.all_active_gos:
                    if type(game_object) == Flipper:
                        game_object.transform.rotate_towards(180, constants.PADDLE_SPEED)
            elif event.key == pygame.K_LEFT:
                # Rotate all game objects 90 degrees to the left
                for game_object in scene.all_active_gos:
                    if type(game_object) == Flipper:
                        game_object.transform.rotate_towards(0, constants.PADDLE_SPEED)
        continue

    scene.update(constants.DELTA_TIME)

    pygame.display.flip()  # Update the display of the full screen
    clock.tick(constants.FRAMERATE)  # 60 frames per second
