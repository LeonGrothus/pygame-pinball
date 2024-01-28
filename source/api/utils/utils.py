import math
import pygame

"""
Utility functions should not be used but are here for convenience reasons.
"""


def map_range(value: float, i_min: float, i_max: float, o_min: float, o_max: float):
    """
    Maps a value from one range to another.

    Arguments:
        value (float): The value to map.
        i_min (float): The minimum of the input range.
        i_max (float): The maximum of the input range.
        o_min (float): The minimum of the output range.
        o_max (float): The maximum of the output range.
    """
    return o_min + (float(value - i_min) / float(i_max - i_min) * (o_max - o_min))


def lerp(first: float, second: float, percentage: float):
    """
    Linearly interpolates between two values.

    Arguments:
        first (float): The first value.
        second (float): The second value.
        percentage (float): The percentage to interpolate by.
    """
    return first + (second - first) * percentage

# def normalize_image_size(image: pygame.Surface, max_width: int=NORMALIZED_IMAGE_SIZE[0], max_height: int=NORMALIZED_IMAGE_SIZE[1]):
#     width, height = image.get_size()
#     aspect_ratio = width / height

#     if width > height:
#         new_width = min(max_width, width)
#         new_height = int(new_width / aspect_ratio)
#     else:
#         new_height = min(max_height, height)
#         new_width = int(new_height * aspect_ratio)

#     return pygame.transform.scale(image, (new_width, new_height))


def clamp(value: float, min_value: float, max_value: float):
    """
    Clamps a value between a minimum and a maximum value.

    Arguments:
        value (float): The value to clamp.
        min_value (float): The minimum value.
        max_value (float): The maximum value.
    """
    return max(min(value, max_value), min_value)


def ceil_vector(v: pygame.Vector2):
    """
    Ceils a vector.

    Arguments:
        v (Vector2): The vector to ceil.
    """
    return pygame.Vector2(math.ceil(v.x), math.ceil(v.y))
