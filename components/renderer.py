import pygame
from components.collider import CircleCollider, Collider, PolygonCollider
from components.component import Component
from pygame.color import Color

class Renderer(Component):
    def __init__(self, color: Color) -> None:
        super().__init__()

        self.color: Color = color
        self.collider = None # type: ignore
        self.collider_type = None

    def on_init(self) -> None:
        self.get_collider()
        return super().on_init()
    
    def on_update(self, delta_time: float) -> None:
        if(self.collider_type == CircleCollider):
            self.collider: CircleCollider = self.collider # type: ignore
            pygame.draw.circle(self.parent.screen, self.color, (self.parent.transform.pos.x, self.parent.transform.pos.y), self.collider.radius) # type: ignore
        
        elif(self.collider_type == PolygonCollider):
            self.collider: PolygonCollider = self.collider # type: ignore
            
            pygame.draw.polygon(self.parent.screen, self.color, self.collider.points)

        else:
            self.get_collider()
            print(f"No collider found {self.collider}")

        return super().on_update(delta_time)

    def get_collider(self) -> None:
        collider = self.parent.get_component_by_class(Collider)
        if collider:
            self.collider = collider
            self.collider_type = type(collider)
