import math
from pygame import Vector2
from api.components.collider import CircleCollider, Collider, PolygonCollider
from api.components.component import Component
from api.objects.game_object import GameObject
from constants import GRAVITY, AIR_FRICTION, PADDLE_COLLISION_DAMPING, PTPF
from options import Options
from api.utils.utils import clamp


class Rigidbody(Component):
    def __init__(self, is_kinematic: bool = False) -> None:
        super().__init__()

        self.currently_in_trigger: list = []

        self.is_kinematic: bool = is_kinematic
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)

        self.collider: CircleCollider = None  # type: ignore
        self.asf = Options().asf

    def set_parent(self, parent: GameObject) -> None:
        return super().set_parent(parent)

    def on_init(self) -> None:
        self.set_collider()
        return super().on_init()

    def on_destroy(self) -> None:
        return super().on_destroy()

    def set_collider(self) -> None:
        collider = self.parent.get_component_by_class(Collider)
        if not collider:
            raise Exception(f"No Collider found on {self.parent}")

        self.collider = collider

    def apply_impuls(self, impuls) -> None:
        if not self.is_kinematic:
            self.velocity += impuls

    def on_update(self, scaled_delta_time) -> None:
        if not self.is_kinematic:
            self.resolve_collisions()

            self.acceleration += GRAVITY * self.asf

            self.velocity += (self.acceleration * scaled_delta_time)
            self.velocity *= (1 - AIR_FRICTION/(PTPF/self.asf))

            self.parent.transform.pos += (self.velocity * scaled_delta_time)

        self.acceleration = Vector2(0, 0)

    def resolve_collisions(self) -> None:
        game_object: GameObject
        for game_object in self.parent.scene.all_active_gos:
            if game_object == self.parent:
                continue

            collision_point, normal = None, None
            other_collider: Collider = game_object.get_component_by_class(Collider)  # type: ignore
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

            self.resolve_collision(collision_point, normal, other_collider)
            self.parent.on_collision(other_collider.parent, collision_point, normal)
            other_collider.parent.on_collision(self.parent, collision_point, normal)

    def resolve_collision(self, collision_point: Vector2, normal: Vector2, other_collider: Collider) -> None:
        # Calculate the new velocity of the ball after the collision
        reflected_velocity = self.velocity.reflect(normal)
        # Calculate the angle of impact
        angle_of_impact = abs(normal.dot(self.velocity.normalize()))
        # Calculate the velocity magnitude
        velocity_magnitude = self.velocity.length()
        # Adjust the friction based on the velocity and the angle of impact
        adjusted_friction = other_collider.friction * (1 + velocity_magnitude / 5000) * (1 + angle_of_impact/10)
        reflected_velocity *= clamp(1 - adjusted_friction, 0.5, 1)
        
        # If the other object has a rotation speed, calculate the angular momentum
        if other_collider.parent.transform.do_smooth_rotation:
            # Calculate the distance from the collision point to the center of the other object
            r = collision_point - other_collider.parent.transform.pos
            
            # Calculate the angular velocity vector
            angular_velocity = normal * other_collider.parent.transform.rotation_speed/PADDLE_COLLISION_DAMPING * self.asf
            
            # Add the angular momentum to the velocity of the ball
            self.velocity = reflected_velocity + angular_velocity
        else:
            self.velocity = reflected_velocity

        # Calculate the overlap between the ball and the other object
        overlap = self.collider.mesh.radius - collision_point.distance_to(self.parent.transform.pos)

        # If there is an overlap, move the ball by the overlap amount along the collision normal
        if overlap > 0:
            self.parent.transform.pos += normal * overlap
        
    def check_circle_circle_collision(self, other: CircleCollider) -> tuple:
        distance_squared = self.parent.transform.pos.distance_squared_to(other.parent.transform.pos)
        if distance_squared < (self.collider.mesh.radius + other.mesh.radius)**2:
            if distance_squared == 0:
                return None, None
            normal = (self.parent.transform.pos-other.parent.transform.pos) / math.sqrt(distance_squared)
            collision_point = self.parent.transform.pos + self.collider.mesh.radius * normal
            return collision_point, normal
        return None, None

    def check_circle_polygon_collision(self, other: PolygonCollider) -> tuple:
        for i in range(len(other.mesh.points)):
            p1: Vector2 = other.mesh.points[i]
            p2: Vector2 = other.mesh.points[(i + 1) % len(other.mesh.points)]
            edge: Vector2 = p2 - p1
            edge_length: float = edge.length()
            edge_direction: Vector2 = edge / edge_length

            to_circle: Vector2 = self.parent.transform.pos - p1
            projection_length: float = to_circle.dot(edge_direction)
            if 0 <= projection_length <= edge_length:
                closest_point: Vector2 = p1 + projection_length * edge_direction
            else:
                continue

            distance: float = closest_point.distance_to(self.parent.transform.pos)
            if distance < self.collider.mesh.radius:
                if math.isclose(distance, 0, abs_tol=1e-5):
                    normal: Vector2 = edge_direction
                    return closest_point, normal
                normal: Vector2 = (self.parent.transform.pos - closest_point) / distance
                return closest_point, normal
        return None, None

    def serialize(self) -> dict:
        return {
            "is_kinematic": self.is_kinematic,
            "velocity": [
                self.velocity.x/self.asf,
                self.velocity.y/self.asf
            ],
            "acceleration": [
                self.acceleration.x/self.asf,
                self.acceleration.y/self.asf
            ]
        }

    def deserialize(self, data: dict) -> 'Rigidbody':
        self.is_kinematic = data["is_kinematic"]
        self.velocity = Vector2(data["velocity"][0], data["velocity"][1]) * self.asf
        self.acceleration = Vector2(data["acceleration"][0], data["acceleration"][1]) * self.asf
        return self
