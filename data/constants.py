from pathlib import Path
from pygame import Vector2

"""
A file to store constants in
"""

GRAVITY = Vector2(0, 666) # Gravity applied to all objects

COLLISION_FRICTION = 0.13 # Friction applied when the object is colliding
AIR_FRICTION = 0.012 # Friction applied when the object is in the air

PADDLE_SPEED = 666  # degrees per second
PADDLE_COLLISION_DAMPING = .66 # Factor to scale the velocity with when the paddle is hit


FRAMERATE = 60 # Frames per second
PTPF = 10 # Physics ticks per frame
DELTA_TIME = (1 / FRAMERATE) # Delta time for updates

PROJECT_PATH: Path = Path(__file__).parents[1] # Path to the project directory
ASSETS_PATH = PROJECT_PATH / Path("assets") # Path to the assets directory

DEFAULT_BUTTON_STYLE = ASSETS_PATH / Path("buttons/default_style") # Path to the default button style
DEFAULT_FONT = ASSETS_PATH / Path("fonts/Tektur-Regular.ttf") # Path to the default font
