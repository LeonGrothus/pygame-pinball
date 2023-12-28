from pygame import Vector2
from components.collider import CircleCollider, Collider, PolygonCollider
from components.component import Component
from objects.gameObject import GameObject
from utils.transform import Transform
from constants import GRAVITY


class Rigidbody(Component):
    def __init__(self, mass: float = 1, is_kinematic: bool = False):
        super().__init__()

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
        if collider:
            self.collider = collider

    def apply_force(self, force) -> None:
        if not self.is_kinematic:
            self.acceleration += force / self.mass

    def on_update(self, delta_time) -> None:
        if self.collider and not self.is_kinematic:
            self.resolve_collisions()
        else:
            self.set_collider()

        if not self.is_kinematic:

            self.acceleration += GRAVITY

            self.velocity += self.acceleration * delta_time
            self.parent.transform.pos += self.velocity * delta_time
            
            self.acceleration = Vector2(0, 0)

    def resolve_collisions(self):
        game_object: GameObject
        for game_object in self.parent.all_active_gos:
            if game_object == self.parent:
                continue

            collision_point, normal = None, None
            other_collider = game_object.get_component_by_class(Collider)
            if other_collider:
                if type(other_collider) is CircleCollider:
                    collision_point, normal = self.check_circle_circle_collision(other_collider)
                elif type(other_collider) is PolygonCollider:
                    collision_point, normal = self.check_circle_polygon_collision(other_collider)

            if collision_point is None or normal is None:
                continue
            
            self.apply_force(normal * (self.velocity.length()+5) * 100)
        return False

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

            to_circle = other.parent.transform.pos - p1
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
