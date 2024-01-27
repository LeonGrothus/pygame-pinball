from pathlib import Path
from pygame import Vector2

GRAVITY = Vector2(0, 666)

COLLISION_FRICTION = 0.1
AIR_FRICTION = 0.008

PADDLE_SPEED = 666  # degrees per second
PADDLE_COLLISION_DAMPING = .66


FRAMERATE = 60
PTPF = 12 # Physics ticks per frame
DELTA_TIME = (1 / FRAMERATE)

PROJECT_PATH: Path = Path(__file__).parents[0]
ASSETS_PATH = PROJECT_PATH / Path("assets")

DEFAULT_BUTTON_STYLE = ASSETS_PATH / Path("buttons/default_style")
DEFAULT_FONT = ASSETS_PATH / Path("fonts/Tektur-Regular.ttf")
