from pygame import Vector2
import pygame
from scipy import constants
from components.collider import CircleCollider, Collider, PolygonCollider
from components.component import Component
from objects.gameObject import GameObject
from utils.transform import Transform
from constants import GRAVITY, AIR_FRICTION, COLLISION_FRICTION


class Rigidbody(Component):
    def __init__(self, mass: float = 1, is_kinematic: bool = False) -> None:
        super().__init__()

        self.currently_in_trigger: list = []

        self.mass: float = mass
        self.is_kinematic: bool = is_kinematic
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)

        self.collider: CircleCollider = None # type: ignore

    def set_parent(self, parent: GameObject) -> None:
        return super().set_parent(parent)

    def on_init(self) -> None:
        self.parent.all_active_rbs.append(self)
        self.set_collider()
        return super().on_init()

    def on_destroy(self) -> None:
        self.parent.all_active_rbs.remove(self)
        return super().on_destroy()

    def set_collider(self) -> None:
        collider = self.parent.get_component_by_class(Collider)
        if not collider:
            raise Exception(f"No Collider found on {self.parent}")
        
        self.collider = collider

    def apply_force(self, force) -> None:
        if not self.is_kinematic:
            self.acceleration += force / self.mass

    def on_update(self, delta_time) -> None:
        if not self.is_kinematic:
            self.resolve_collisions()

        if not self.is_kinematic:

            self.acceleration += GRAVITY

            self.velocity += self.acceleration * delta_time
            self.velocity *= (1 - AIR_FRICTION)

            self.parent.transform.pos += self.velocity * delta_time
            
            self.acceleration = Vector2(0, 0)

    def resolve_collisions(self):
        game_object: GameObject
        for game_object in self.parent.all_active_gos:
            if game_object == self.parent:
                continue

            collision_point, normal = None, None
            other_collider: Collider = game_object.get_component_by_class(Collider) # type: ignore
            if other_collider:
                if type(other_collider) is CircleCollider:
                    collision_point, normal = self.check_circle_circle_collision(other_collider)
                elif type(other_collider) is PolygonCollider:
                    collision_point, normal = self.check_circle_polygon_collision(other_collider)

            if collision_point is None or normal is None:
                if other_collider.is_trigger and (game_object in self.currently_in_trigger):
                    self.currently_in_trigger.remove(game_object)
                    other_collider.parent.on_trigger_exit(self.parent)
                continue
            
            if other_collider.is_trigger:
                if game_object not in self.currently_in_trigger:
                    self.currently_in_trigger.append(game_object)
                    other_collider.parent.on_trigger_enter(self.parent)
                continue

            self.reflect_velocity(normal)
        return False
    
    def reflect_velocity(self, normal: Vector2) -> None:
        print(f"reflecting {self.velocity} with {normal}")
        self.velocity = self.velocity.reflect(normal) * (1-COLLISION_FRICTION)

    def check_circle_circle_collision(self, other: CircleCollider):
        distance = self.parent.transform.pos.distance_to(other.parent.transform.pos)
        if distance < self.collider.radius + other.radius:
            if distance == 0:
                print(f"{self.parent.transform.pos} {other.parent.transform.pos}")
                return None, None
            normal = (self.parent.transform.pos - other.parent.transform.pos) / distance
            return self.parent.transform.pos + other.radius * normal, normal
        return None, None

    def check_circle_polygon_collision(self, other: PolygonCollider):
        for i in range(len(other.points)):
            p1: Vector2 = other.points[i]
            p2: Vector2 = other.points[(i + 1) % len(other.points)]
            edge = p2 - p1
            edge_length = edge.length()
            edge_direction = edge / edge_length

            to_circle = self.parent.transform.pos - p1
            projection_length = to_circle.dot(edge_direction)
            if 0 <= projection_length <= edge_length:
                closest_point = p1 + projection_length * edge_direction
                
            else:
                continue

            distance = closest_point.distance_to(self.parent.transform.pos)
            if distance < self.collider.radius:
                normal = (self.parent.transform.pos - closest_point) / distance
                return closest_point, normal
        return None, None