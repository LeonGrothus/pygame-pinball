import pygame
import math
from api.components.component import Component
from options import Options

class SimpleMovement(Component):
    def __init__(self, start_pos, end_pos, speed, move_type='sine'):
        super().__init__()
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        self.speed = speed
        self.move_type = move_type
        self.direction = 1
        self.t = 0
        self.asf = Options().asf

    def on_update(self, delta_time):
        if self.move_type == 'linear':
            self.linear_move(delta_time)
        elif self.move_type == 'sine':
            self.sine_move(delta_time)

    def linear_move(self, delta_time):
        direction = (self.end_pos - self.start_pos).normalize()
        self.parent.transform.pos += direction * self.speed * self.asf * delta_time
        if self.parent.transform.pos.distance_squared_to(self.end_pos) < 1:
            self.start_pos, self.end_pos = self.end_pos, self.start_pos

    def sine_move(self, delta_time):
        self.t += self.speed * delta_time
        sine_val = math.sin(self.t) / 2 + 0.5
        self.parent.transform.pos = self.start_pos.lerp(self.end_pos, sine_val)

    def serialize(self):
        return {
            'start_pos': self.start_pos,
            'end_pos': self.end_pos,
            'speed': self.speed,
            'move_type': self.move_type
        }
    
    def deserialize(self, data):
        self.start_pos = data['start_pos']
        self.end_pos = data['end_pos']
        self.speed = data['speed']
        self.move_type = data['move_type']
        return self