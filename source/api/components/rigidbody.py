import math
from pygame import Vector2
from source.api.components.collider import CircleCollider, Collider, PolygonCollider
from source.api.components.component import Component
from source.api.objects.game_object import GameObject
from data.constants import GRAVITY, AIR_FRICTION, PADDLE_COLLISION_DAMPING, PTPF
from source.api.management.options_manager import OptionsManager
from source.api.utils.utils import clamp


class Rigidbody(Component):
    """
    A class to represent a Rigidbody. This class is responsible for the physics of the game.
    It handles collisions and applies gravity and air friction.

    Attributes:
        currently_in_trigger: list, list of all objects currently in trigger
        is_kinematic: bool, whether the rigidbody is kinematic
        velocity: Vector2, the velocity of the rigidbody
        acceleration: Vector2, the acceleration of the rigidbody
        collider: CircleCollider, the collider of the rigidbody

    Methods:
        __init__(self, is_kinematic: bool = False)
        set_parent(self, parent: GameObject)
        on_init(self)
        on_destroy(self)
        set_collider(self)
        apply_impuls(self, impuls)
        on_update(self, scaled_delta_time)
        resolve_collisions(self)
        resolve_collision(self, collision_point: Vector2, normal: Vector2, other_collider: Collider)
        check_circle_circle_collision(self, other: CircleCollider)
        check_circle_polygon_collision(self, other: PolygonCollider)
        serialize(self) -> dict
        deserialize(self, data: dict) -> 'Rigidbody'
    """

    def __init__(self, is_kinematic: bool = False) -> None:
        """
        Inits Rigidbody with is_kinematic

        Arguments:
            is_kinematic: bool, whether the rigidbody is kinematic
        """

        super().__init__()

        self.currently_in_trigger: list = []

        self.is_kinematic: bool = is_kinematic
        self.velocity: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)

        self.collider: CircleCollider = None  # type: ignore
        self.asf = OptionsManager().asf

    def set_parent(self, parent: GameObject) -> None:
        """
        Sets the parent of the component

        Arguments:
            parent: GameObject, the parent of the component
        """
        return super().set_parent(parent)

    def on_init(self) -> None:
        """
        Sets the collider

        Returns:
            None
        """
        self.set_collider()
        return super().on_init()

    def set_collider(self) -> None:
        """
        Sets the collider

        Returns:
            None
        """

        collider = self.parent.get_component_by_class(Collider)
        if not collider:
            raise Exception(f"No Collider found on {self.parent}")

        self.collider = collider

    def apply_impuls(self, impuls) -> None:
        """
        Applies an impuls to the rigidbody

        Arguments:
            impuls: Vector2, the impuls to apply
        """

        if not self.is_kinematic:
            self.velocity += impuls

    def on_update(self, scaled_delta_time) -> None:
        """
        Updates the rigidbody

        Arguments:
            scaled_delta_time: float, the time since the last frame

        Returns:
            None
        """

        if not self.is_kinematic:
            self.handle_collisions()

            self.acceleration += GRAVITY * self.asf

            self.velocity += (self.acceleration * scaled_delta_time)
            self.velocity *= (1 - (AIR_FRICTION/PTPF)/max(self.asf, 1))

            self.parent.transform.pos += (self.velocity * scaled_delta_time)

        self.acceleration = Vector2(0, 0)

    def handle_collisions(self) -> None:
        """
        Resolves all collisions

        Returns:
            None
        """
        game_object: GameObject 
        for game_object in self.parent.scene.all_active_gos: 
            if game_object == self.parent:
                continue

            collision_point, normal = None, None
            other_collider: Collider = game_object.get_component_by_class(Collider)  # type: ignore
            if other_collider:
                if type(other_collider) is CircleCollider: # If the other object is a CircleCollider, check for a circle-circle collision
                    collision_point, normal = self.check_circle_circle_collision(other_collider)
                elif type(other_collider) is PolygonCollider: # If the other object is a PolygonCollider, check for a circle-polygon collision
                    collision_point, normal = self.check_circle_polygon_collision(other_collider)
            else:
                continue

            if collision_point is None or normal is None: # If there is no collision, continue
                if other_collider.is_trigger and (game_object in self.currently_in_trigger): # If the other object is a trigger and the ball is in it, remove it from the list
                    self.currently_in_trigger.remove(game_object) 
                    other_collider.parent.on_trigger_exit(self.parent)
                continue

            if other_collider.is_trigger: # If the other object is a trigger, add it to the list if it is not already in it
                if game_object not in self.currently_in_trigger:
                    self.currently_in_trigger.append(game_object)
                    other_collider.parent.on_trigger_enter(self.parent)
                continue

            self.resolve_collision(collision_point, normal, other_collider) # Resolve the collision
            self.parent.on_collision(other_collider.parent, collision_point, normal) # Call the on_collision method of this object
            other_collider.parent.on_collision(self.parent, collision_point, normal) # Call the on_collision method of the other object

    def resolve_collision(self, collision_point: Vector2, normal: Vector2, other_collider: Collider) -> None:
        """
        Resolves a collision

        Arguments:
            collision_point: Vector2, the point of collision
            normal: Vector2, the normal of the collision
            other_collider: Collider, the other collider

        Returns:
            None
        """

        # If the other object is a RigidBody, calculate the impulse
        if (other_rb := other_collider.parent.get_component_by_class(Rigidbody)):
            v_rel = self.velocity - other_rb.velocity # Relative velocity
            j = -v_rel.dot(normal) # Calculate the impulse magnitude
            # Apply the impulse
            self.velocity += j * normal
            other_rb.velocity -= j * normal
        else:
            # Calculate the new velocity of the ball after the collision
            reflected_velocity = self.velocity.reflect(normal)
            # Calculate the angle of impact
            angle_of_impact = abs(normal.dot(self.velocity.normalize()))
            # Calculate the velocity magnitude
            velocity_magnitude = self.velocity.length()
            # Adjust the friction based on the velocity and the angle of impact 
            adjusted_friction = other_collider.friction * (clamp(velocity_magnitude / (500*self.asf), .2, 1)) * (1 + angle_of_impact/10)
            reflected_velocity *= clamp(1 - adjusted_friction, 0.5, 1)
            
            # If the other object has a rotation speed, calculate the angular momentum
            if other_collider.parent.transform.do_smooth_rotation:
                # Calculate the angular velocity vector
                angular_velocity = normal * ((other_collider.parent.transform.rotation_speed*self.asf)/PADDLE_COLLISION_DAMPING) * (self.asf**(1/2))
                
                # Add the angular momentum to the velocity of the ball
                self.velocity = reflected_velocity + angular_velocity
            else:
                self.velocity = reflected_velocity

        # Calculate the overlap between the ball and the other object
        overlap = self.collider.mesh.radius - collision_point.distance_to(self.parent.transform.pos)
        if other_rb:
            overlap = self.collider.mesh.radius + other_collider.mesh.radius - collision_point.distance_to(self.parent.transform.pos) # type: ignore

        # If there is an overlap, move the ball by the overlap amount along the collision normal
        if overlap > 0:
            self.parent.transform.pos += normal * overlap
        
    def check_circle_circle_collision(self, other: CircleCollider) -> tuple:
        distance_squared = self.parent.transform.pos.distance_squared_to(other.parent.transform.pos)
        if distance_squared < (self.collider.mesh.radius + other.mesh.radius)**2: # If the distance between the two objects is smaller than the sum of their radii, there is a collision
            if distance_squared == 0: # If the distance is 0, return the normal as (1, 0)
                return None, None
            normal = (self.parent.transform.pos-other.parent.transform.pos) / math.sqrt(distance_squared) # Calculate the normal
            collision_point = self.parent.transform.pos + self.collider.mesh.radius * normal # Calculate the collision point
            return collision_point, normal 
        return None, None

    def check_circle_polygon_collision(self, other: PolygonCollider) -> tuple:
        for i in range(len(other.mesh.points)): # For each edge of the polygon
            p1: Vector2 = other.mesh.points[i] # Get the first point of the edge
            p2: Vector2 = other.mesh.points[(i + 1) % len(other.mesh.points)] # Get the second point of the edge
            edge: Vector2 = p2 - p1 # Calculate the edge vector
            edge_length: float = edge.length() # Calculate the length of the edge
            edge_direction: Vector2 = edge / edge_length # Calculate the direction of the edge

            to_circle: Vector2 = self.parent.transform.pos - p1 # Calculate the vector from the first point of the edge to the ball
            projection_length: float = to_circle.dot(edge_direction) # Calculate the length of the projection of the vector from the first point of the edge to the ball onto the edge
            if 0 <= projection_length <= edge_length: # If the projection is on the edge 
                closest_point: Vector2 = p1 + projection_length * edge_direction # Calculate the closest point on the edge to the ball
            else:
                continue

            distance: float = closest_point.distance_to(self.parent.transform.pos) # Calculate the distance between the closest point and the ball
            if distance < self.collider.mesh.radius: # If the distance is smaller than the radius of the ball, there is a collision 
                if math.isclose(distance, 0, abs_tol=1e-5): # If the distance is 0, return the normal as (1, 0)
                    normal: Vector2 = edge_direction
                    return closest_point, normal
                normal: Vector2 = (self.parent.transform.pos - closest_point) / distance # Calculate the normal
                return closest_point, normal
        return None, None

    def serialize(self) -> dict:
        """
        Serializes the Rigidbody

        Returns:
            dict: a dictionary containing the Rigidbody's data
        """

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
        """
        Deserializes the Rigidbody

        Arguments:
            data: dict, a dictionary containing the Rigidbody's data

        Returns:
            Rigidbody: the modified Rigidbody instance
        """

        self.is_kinematic = data["is_kinematic"]
        self.velocity = Vector2(data["velocity"][0], data["velocity"][1]) * self.asf
        self.acceleration = Vector2(data["acceleration"][0], data["acceleration"][1]) * self.asf
        return self
