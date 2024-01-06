from pathlib import Path
from pygame import Vector2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY = Vector2(0, 1000)

COLLISION_FRICTION = 0.1
AIR_FRICTION = 0.0015

PADDLE_SPEED = 1080 # degrees per second
PADDLE_COLLISION_DAMPING = 60


FRAMERATE = 120
DELTA_TIME = (1 / FRAMERATE)

PROJECT_PATH = Path(__file__).parents[0]

