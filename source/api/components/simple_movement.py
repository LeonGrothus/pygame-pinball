import pygame
import math

from source.api.components.component import Component
from source.api.management.options_manager import OptionsManager

class SimpleMovement(Component):
    """
    A class to represent a SimpleMovement. This component moves the parent from start_pos to end_pos with speed.
    The movement can be linear or sine.

    Attributes:
        start_pos: Vector2, the start position of the movement
        end_pos: Vector2, the end position of the movement
        speed: float, the speed of the movement
        move_type: str, the type of the movement
        direction: int, the direction of the movement
        asf: float, the application scale factor

    Methods:
        __init__(self, start_pos: Vector2, end_pos: Vector2, speed: float, move_type: str = 'sine')
        on_update(self, delta_time: float)
        linear_move(self, delta_time: float)
        sine_move(self, delta_time: float)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'SimpleMovement'
    """

    def __init__(self, start_pos: pygame.Vector2, end_pos: pygame.Vector2, speed: float, move_type: str='sine'):
        """
        Inits SimpleMovement with start_pos, end_pos, speed and move_type

        Arguments:
            start_pos: Vector2, the start position of the movement
            end_pos: Vector2, the end position of the movement
            speed: float, the speed of the movement
            move_type: str, the type of the movement
        """

        super().__init__()
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        self.speed = speed
        self.move_type = move_type
        self.direction = 1
        self.t = 0
        self.asf = OptionsManager().asf

    def on_update(self, delta_time: float) -> None:
        """
        Moves the parent from start_pos to end_pos with speed

        Arguments:
            delta_time: float, the time since the last frame
        """

        if self.move_type == 'linear':
            self.linear_move(delta_time)
        elif self.move_type == 'sine':
            self.sine_move(delta_time)

    def linear_move(self, delta_time: float) -> None:
        """
        Moves the parent from start_pos to end_pos with speed using linear movement

        Arguments:
            delta_time: float, the time since the last frame

        Returns:
            None
        """
        direction = (self.end_pos - self.start_pos).normalize()
        self.parent.transform.pos += direction * self.speed * self.asf * delta_time
        if self.parent.transform.pos.distance_squared_to(self.end_pos) < 1:
            self.start_pos, self.end_pos = self.end_pos, self.start_pos

    def sine_move(self, delta_time: float):
        """
        Moves the parent from start_pos to end_pos with speed using sine

        Arguments:
            delta_time: float, the time since the last frame
        """
        self.t += self.speed * delta_time
        sine_val = math.sin(self.t) / 2 + 0.5
        self.parent.transform.pos = self.start_pos.lerp(self.end_pos, sine_val)

    def serialize(self) -> dict:
        """
        Serializes the SimpleMovement

        Returns:
            dict: the serialized SimpleMovement
        """

        return {
            'start_pos': self.start_pos,
            'end_pos': self.end_pos,
            'speed': self.speed,
            'move_type': self.move_type
        }
    
    def deserialize(self, data: dict) -> 'SimpleMovement':
        """
        Deserializes the SimpleMovement

        Arguments:
            data: dict, the serialized SimpleMovement

        Returns:
            SimpleMovement: the modified SimpleMovement instance
        """

        self.start_pos = data['start_pos']
        self.end_pos = data['end_pos']
        self.speed = data['speed']
        self.move_type = data['move_type']
        return self