from pygame import Vector2, Vector3
import pygame
from api.components.collider import CircleCollider, Collider, PolygonCollider
from api.components.component import Component
from api.objects.game_object import GameObject
from constants import GRAVITY, AIR_FRICTION, COLLISION_FRICTION, PADDLE_COLLISION_DAMPING


class Rigidbody(Component):
    def __init__(self, is_kinematic: bool = False) -> None:
        super().__init__()

        self.currently_in_trigger: list = []

        self.is_kinematic: bool = is_kinematic
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)

        self.collider: CircleCollider = None  # type: ignore

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
            print(self.velocity)

    def on_update(self, delta_time) -> None:
        if not self.is_kinematic:
            self.resolve_collisions()

            self.acceleration += GRAVITY

            self.velocity += self.acceleration * delta_time
            # print(self.velocity)
            self.velocity *= (1 - AIR_FRICTION)

            self.parent.transform.pos += self.velocity * delta_time

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
            other_collider.parent.on_collision(self.parent, collision_point, normal)

    def resolve_collision(self, collision_point: Vector2, normal: Vector2, other_collider: Collider) -> None:
        self.velocity = self.velocity.reflect(normal) * (1-COLLISION_FRICTION)
        self.parent.transform.pos += normal * (self.collider.mesh.radius -
                                               collision_point.distance_to(self.parent.transform.pos))

        if other_collider.parent.transform.do_smooth_rotation:
            # Calculate the vector from the center of rotation to the point of contact
            rotation_vector = collision_point - other_collider.parent.transform.pos

            # Calculate the angular velocity vector
            angular_velocity_vector = Vector3(0, 0, other_collider.parent.transform.rotation_speed)

            # Calculate the 3D rotation vector
            rotation_vector_3d = Vector3(rotation_vector.x, rotation_vector.y, 0)

            # Calculate the rotational velocity as the cross product of the angular velocity vector and the rotation vector
            rotational_velocity_3d = angular_velocity_vector.cross(rotation_vector_3d)

            # Convert the 3D rotational velocity back to 2D
            rotational_velocity = Vector2(rotational_velocity_3d.x, rotational_velocity_3d.y)

            # Calculate the alignment of the normal vector with the rotational velocity vector
            alignment = normal.dot(rotational_velocity.normalize())

            # Scale the rotational velocity based on the alignment
            self.velocity += rotational_velocity * alignment / PADDLE_COLLISION_DAMPING

            # pygame.draw.line(self.parent.scene.screen, (255, 0, 255),
            #                  collision_point, collision_point + normal * 100, 5)

    def check_circle_circle_collision(self, other: CircleCollider) -> tuple:
        distance = self.parent.transform.pos.distance_to(other.parent.transform.pos)
        if distance < self.collider.mesh.radius + other.mesh.radius:
            if distance == 0:
                print(f"{self.parent.transform.pos} {other.parent.transform.pos}")
                return None, None
            normal = (self.parent.transform.pos - other.parent.transform.pos) / distance
            return self.parent.transform.pos + other.mesh.radius * normal, normal
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
                normal: Vector2 = (self.parent.transform.pos - closest_point) / distance
                return closest_point, normal
        return None, None

    def serialize(self) -> dict:
        return {
            "is_kinematic": self.is_kinematic,
            "velocity": [
                self.velocity.x,
                self.velocity.y
            ],
            "acceleration": [
                self.acceleration.x,
                self.acceleration.y
            ]
        }

    def deserialize(self, data: dict) -> 'Rigidbody':
        self.is_kinematic = data["is_kinematic"]
        self.velocity = Vector2(data["velocity"][0], data["velocity"][1])
        self.acceleration = Vector2(data["acceleration"][0], data["acceleration"][1])
        return self