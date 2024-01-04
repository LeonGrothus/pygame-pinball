import pygame
from pathlib import Path
from game.objects.ball import Ball
from game.objects.flipper import Flipper
from api.objects.gameObject import GameObject
import constants

# Initialize PyGame
pygame.init()

all_active_gos: list = []
all_active_rbs: list = []

# Making display screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

Ball(pygame.Vector2(100, 100), screen, all_active_gos, all_active_rbs)
Flipper(pygame.Vector2(100, 400), screen, all_active_gos, all_active_rbs)

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
                for game_object in all_active_gos:
                    game_object.transform.rotate_towards(90, constants.PADDLE_SPEED)
            elif event.key == pygame.K_LEFT:
                # Rotate all game objects 90 degrees to the left
                for game_object in all_active_gos:
                    game_object.transform.rotate_towards(-90, constants.PADDLE_SPEED)
        continue

    go: GameObject
    for go in all_active_gos:
        go.update(constants.DELTA_TIME)

    pygame.display.flip()  # Update the display of the full screen
    clock.tick(constants.FRAMERATE)  # 60 frames per second
