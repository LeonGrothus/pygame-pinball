import math
import pygame



def map_range(value, i_min, i_max, o_min, o_max):
  return o_min + (float(value - i_min) / float(i_max - i_min) * (o_max - o_min))

def lerp(first, second, percentage):
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

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def ceil_vector(v):
    return pygame.Vector2(math.ceil(v.x), math.ceil(v.y))