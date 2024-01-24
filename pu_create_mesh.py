import pygame
import sys
import re
from pathlib import Path

# Initialize Pygame
pygame.init()

# Define constants
scale = 2
SCREEN_WIDTH = int(666 * scale)
SCREEN_HEIGHT = int(1000 * scale)
IMAGE_PATH = Path("image_fit.png")
STRETCH_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
POINT_RADIUS = 10  # Radius of the points
POINT_COLOR = (255, 0, 0)  # Color of the points (red)
POLYGON_COLOR = (0, 255, 0)  # Color of the polygon (green)

# Create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Rendering Scene")

# Load the image
image = pygame.image.load(IMAGE_PATH)
image = pygame.transform.scale(image, STRETCH_SIZE)

flip_x = 600/2 * scale

# Default list of vectors
default_vectors_str = "[V2(616, 1000), V2(619, 341), V2(603, 265), V2(568, 203), V2(526, 163), V2(474, 130), V2(451, 134), V2(440, 152), V2(447, 172), V2(498, 207), V2(532, 241), V2(556, 289), V2(563, 334), V2(543, 407), V2(518, 456), V2(520, 481), V2(535, 504), V2(557, 482), V2(598, 521), V2(578, 546), V2(600, 570), V2(600, 900), V2(555, 915), V2(361, 1000)]"

# Extract the numbers from the string
matches = re.findall(r'V2\((\d+), (\d+)\)', default_vectors_str)
default_vectors = [pygame.Vector2(int(x), int(y))*scale for x, y in matches]

# Use the default vectors as the initial click positions
click_positions = default_vectors
dragged_point = None
show_circles = True

def point_line_distance(point, line_start, line_end):
    """Calculate the minimum distance between a point and a line segment."""
    line_length = (line_end - line_start).length()
    if line_length == 0:
        return (point - line_start).length()
    t = max(0, min(1, (point - line_start).dot(line_end - line_start) / line_length**2))
    projection = line_start + t * (line_end - line_start)
    return (point - projection).length()

# Main event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            for i, pos in enumerate(click_positions):
                if (pos - mouse_pos).length() <= POINT_RADIUS:
                    dragged_point = i
                    break
            else:
                # Save the mouse position when clicking
                click_positions.append(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragged_point = None
        elif event.type == pygame.MOUSEMOTION and dragged_point is not None:
            click_positions[dragged_point] = pygame.Vector2(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                for i, pos in enumerate(click_positions):
                    if (pos - mouse_pos).length() <= POINT_RADIUS:
                        del click_positions[i]
                        break
            elif event.key == pygame.K_h:
                # Toggle the value of show_circles
                show_circles = not show_circles
            elif event.key == pygame.K_RETURN:
                positions_str = ', '.join(f'V2({int(pos.x/scale)}, {int(pos.y/scale)})' for pos in click_positions)
                print(f"[{positions_str}]")
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                min_distance = float('inf')
                insert_index = None
                for i in range(len(click_positions)):
                    start, end = click_positions[i], click_positions[(i+1)%len(click_positions)]
                    distance = point_line_distance(mouse_pos, start, end)
                    if distance < min_distance:
                        min_distance = distance
                        insert_index = i + 1
                if insert_index is not None:
                    click_positions.insert(insert_index, mouse_pos)
            elif event.key == pygame.K_f:  # Flip the inputs around the specified x position
                click_positions = [pygame.Vector2(2*flip_x - pos.x, pos.y) for pos in click_positions]
            elif event.key == pygame.K_c:  # Clear the inputs
                click_positions = []
            elif event.key == pygame.K_SPACE:
                print(pygame.mouse.get_pos()[0]/scale, pygame.mouse.get_pos()[1]/scale)

    screen.blit(image, pygame.Vector2(0, 0))

    if len(click_positions) > 2:
        pygame.draw.polygon(screen, POLYGON_COLOR, click_positions, 1)

    if show_circles:
        for pos in click_positions:
            pygame.draw.circle(screen, POINT_COLOR, pos, POINT_RADIUS)

    # Update the screen
    pygame.display.flip()