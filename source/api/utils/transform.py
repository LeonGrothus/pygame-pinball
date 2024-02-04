from pygame import Vector2

from source.api.utils.event_value import EventValue
from data.constants import PADDLE_SPEED, PTPF
from source.api.management.options_manager import OptionsManager

class Transform:
    """
    A class to represent a Transform. A Transform is the position and rotation of a GameObject.

    Attributes:
        parent: GameObject, the parent of the Transform
        pos: Vector2, the position of the Transform
        rotation_speed: float, the rotation speed of the Transform
        do_smooth_rotation: bool, whether the Transform should rotate smoothly
        target_smooth_rotation: float, the target rotation of the smooth rotation
        rot: EventValue[float], the rotation of the Transform

    Methods:
        __init__(self, parent)
        rotate(self, angle: float)
        update(self, scaled_delta_time: float)
        init_smooth_rotation(self, target: float)
        _rotate_towards(self, rotation_speed)
        serialize(self) -> dict
        deserialize(self, data: dict) -> None
    """

    def __init__(self, parent) -> None:
        """
        Inits Transform with parent

        Arguments:
            parent: GameObject, the parent of the Transform
        """

        self.parent = parent

        self.pos: Vector2 = Vector2()

        self.rotation_speed: float = PADDLE_SPEED / max(OptionsManager().asf, 1)
        self.do_smooth_rotation: bool = False
        self.target_smooth_rotation: float = float("inf")
        self.rot: EventValue[float] = EventValue(0)
    
    def rotate(self, angle: float) -> None:
        """
        Rotates the Transform by angle

        Arguments:
            angle: float, the angle to rotate by
        """

        self.rot.set_value(self.rot.get_value() + angle)

    def update(self, scaled_delta_time: float) -> None:
        """
        Updates the Transform

        Arguments:
            scaled_delta_time: float, the time since the last frame
        """

        if self.do_smooth_rotation:
            self._rotate_towards(self.rotation_speed * scaled_delta_time)

    def init_smooth_rotation(self, target: float) -> None:
        """
        Initializes a smooth rotation

        Arguments:
            target: float, the target rotation of the smooth rotation
        """
        if target == self.target_smooth_rotation:
            return
        self.do_smooth_rotation = True
        self.target_smooth_rotation = target

    def _rotate_towards(self, rotation_speed) -> None:
        """
        Rotates the Transform towards the target rotation

        Arguments:
            rotation_speed: float, the rotation speed of the Transform
        """

        rotation_difference = self.target_smooth_rotation - self.rot.get_value() # Calculate the rotation difference
        if abs(rotation_difference) <= rotation_speed: # If the rotation is smaller than the rotation speed
            self.do_smooth_rotation = False # Stop rotating
            angle = rotation_difference # Rotate the remaining rotation 
        else:
            angle = rotation_speed if rotation_difference > 0 else -rotation_speed # Rotate the rotation speed
        self.rotate(angle) # Rotate the Transform

    def serialize(self) -> dict:
        """
        Serializes the Transform

        Returns:
            dict: the serialized Transform
        """

        asf = OptionsManager().asf
        return {
            "pos": [self.pos.x/asf, self.pos.y/asf], # Divide by asf to get the position in pixels
            "rot": self.rot.get_value() # Get the rotation
        }
    
    def deserialize(self, data: dict) -> None:
        """
        Deserializes the Transform

        Arguments:
            data: dict, the serialized Transform
        """

        self.pos = Vector2(data["pos"]) * OptionsManager().asf # Multiply by asf to get the position in meters
        self.rot.set_value(data["rot"]) # Set the rotation