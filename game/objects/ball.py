from pathlib import Path
from pygame import Vector2, Color
import pygame
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh
from api.components.collider import CircleCollider
from api.components.rigidbody import Rigidbody
from api.components.renderer import Renderer
from constants import ASSETS_PATH
from options import Options

class Ball(GameObject):
    def __init__(self, scene, pos: Vector2, color: Color = Color(255, 255, 255), radius=25):
        self.radius = radius
        self.hide = False
        super().__init__(pos, 5, scene)

        self.add_components(
            CircleMesh(color, self.radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )
        self.scene.active_balls += 1

        self.ball_destroyed_sound = pygame.mixer.Sound(ASSETS_PATH / Path("sounds/ball_destroyed.wav"))
    
    def on_destroy(self):
        self.sound_manager.play_sfx(self.ball_destroyed_sound)
        self.scene.active_balls -= 1
        return super().on_destroy()
    
    def on_update(self, delta_time: float):
        if self.hide:
            return
        if self.transform.pos.y > self.scene.screen.get_height() + self.radius/2:
            self.on_destroy()
        return super().on_update(delta_time)
    
    def serialize(self):
        return {
            self.__class__.__name__: {
                "components": {c.__class__.__name__: c.serialize() for c in self.components},
                "transform": self.transform.serialize()
            }
        }

    def deserialize(self, data):
        self.components.clear()
        self.transform.deserialize(data["transform"])
        components = []
        component_data = data["components"]
        for component_class in data["components"]:
            component = globals()[component_class]().deserialize(component_data[component_class])
            components.append(component)
        self.add_components(*components)
        return self
    
    def hide_ball(self):
        self.transform.pos = Vector2(-100, -100)
        self.hide = True
    
    
