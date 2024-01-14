from pathlib import Path
from pygame import Vector2

GRAVITY = Vector2(0, 1000)

COLLISION_FRICTION = 0.1
AIR_FRICTION = 0.0015

PADDLE_SPEED = 1080 # degrees per second
PADDLE_COLLISION_DAMPING = 100


FRAMERATE = 120
DELTA_TIME = (1 / FRAMERATE)

PROJECT_PATH = Path(__file__).parents[0]
ASSETS_PATH = PROJECT_PATH / Path("assets")

NORMALIZED_IMAGE_SIZE = (500, 500)