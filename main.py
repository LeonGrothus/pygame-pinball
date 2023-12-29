import pygame
from pathlib import Path
from components.collider import CircleCollider, Collider, PolygonCollider
from components.mesh import CircleMesh, PolygonMesh
from components.renderer import Renderer
from components.ridigbody import Rigidbody
from objects.gameObject import GameObject
import constants

# Initialize PyGame
pygame.init()

# Define spacetime

all_active_gos: list = []
all_active_rbs: list = []

# Making display screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE)
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

# You could declare components (the initial ball, the other items, ...) here
x = GameObject(pygame.Vector2(100, 100), screen, all_active_gos, all_active_rbs)
x.add_components(CircleMesh(pygame.Color(255, 255, 255), 50), CircleCollider(), Rigidbody(), Renderer())

y = GameObject(pygame.Vector2(100, 400), screen, all_active_gos, all_active_rbs)
y.add_components(PolygonMesh(pygame.Color(255, 255, 0), [pygame.Vector2(-100,-50),pygame.Vector2(-100,50),pygame.Vector2(100,50)]),
                  PolygonCollider(True), Renderer())

#,pygame.Vector2(100,-10)

# PolygonCollider([pygame.Vector2(-100,-10),pygame.Vector2(-100,10),pygame.Vector2(100,10),pygame.Vector2(100,-10)])

# Main event loop
while running:
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0))  # redraws background image

    for event in pygame.event.get():
        # Get's all the user action (keyboard, mouse, joysticks, ...)
        continue

    go: GameObject
    for go in all_active_gos:
        go.update(constants.DELTA_TIME)  # Use the DELTA_TIME constant
    # Adjust screen

    # Here the action could take place

    # s = s0 + v0*t + 1/2a*t**2

    pygame.display.flip()  # Update the display of the full screen
    clock.tick(60)  # 60 frames per second

# Done! Time to quit.
