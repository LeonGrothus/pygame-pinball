import pygame
import sys
import re
from pathlib import Path

"""
This file is ONLY intended to be used to create the mesh from the image_fit.png file. It has no other purpose.
"""

# Initialize Pygame
pygame.init()

# Define constants
scale = 2
SCREEN_WIDTH = int(666 * scale)
SCREEN_HEIGHT = int(1000 * scale)
IMAGE_PATH = Path("level_design/image_fit.png")
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

flip_x = 300 * scale

# Default list of vectors
default_vectors_str = "[V2(-24, -3),V2(-23, -6),V2(-22, -10),V2(-21, -12),V2(-20, -14),V2(-15, -19),V2(-10, -22),V2(-6, -24),V2(0, -25),V2(20, -24),V2(40, -24),V2(60, -23),V2(80, -22),V2(100, -21),V2(120, -19),V2(140, -17),V2(160, -14),V2(180, -10),V2(200, -6),V2(207, -4),V2(210, 0),V2(207, 4),V2(200, 6),V2(180, 10),V2(160, 14),V2(140, 17),V2(120, 19),V2(100, 21),V2(80, 22),V2(60, 23),V2(40, 24),V2(20, 25),V2(0, 25),V2(-6, 24),V2(-10, 22),V2(-15, 19),V2(-20, 14),V2(-21, 12),V2(-22, 10),V2(-23, 6),V2(-24, 3),]"

# Extract the numbers from the string
matches = re.findall(r'V2\((-?\d+), (-?\d+)\)', default_vectors_str)
default_vectors = [pygame.Vector2(int(x)+100, int(y)+100)*scale for x, y in matches]

# Use the default vectors as the initial click positions
click_positions = default_vectors
dragged_point = None
show_circles = True

def point_line_distance(point, line_start, line_end) -> float:
    """
    Calculate the distance between a point and a line segment.

    Arguments:
        point (Vector2): The point
        line_start (Vector2): The start of the line segment
        line_end (Vector2): The end of the line segment

    Returns:
        float: The distance between the point and the line segment
    """
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
        elif event.type == pygame.MOUSEBUTTONDOWN: # If the mouse is clicked
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # Get the mouse position
            for i, pos in enumerate(click_positions): # Loop through all the points
                if (pos - mouse_pos).length() <= POINT_RADIUS: # If the mouse is close to a point
                    dragged_point = i # Set the dragged point to the index of the point
                    break
            else:
                # Save the mouse position when clicking
                click_positions.append(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP: # If the mouse is released
            dragged_point = None # Stop dragging the point
        elif event.type == pygame.MOUSEMOTION and dragged_point is not None: # If the mouse is moved and a point is being dragged
            click_positions[dragged_point] = pygame.Vector2(pygame.mouse.get_pos()) # Set the position of the dragged point to the mouse position
        elif event.type == pygame.KEYDOWN: # If a key is pressed
            if event.key == pygame.K_DELETE or event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS: # If the delete key is pressed
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # Get the mouse position
                for i, pos in enumerate(click_positions): # Loop through all the points 
                    if (pos - mouse_pos).length() <= POINT_RADIUS: # If the mouse is close to a point
                        del click_positions[i] # Delete the point
                        break # Stop looping
            elif event.key == pygame.K_h:
                # Toggle the value of show_circles
                show_circles = not show_circles 
            elif event.key == pygame.K_RETURN: # If the enter key is pressed 
                positions_str = ', '.join(f'V2({int(pos.x/scale)}, {int(pos.y/scale)})' for pos in click_positions) # Create a string of all the positions
                print(f"[{positions_str}]") # Print the string
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS: # If the plus key is pressed
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # Get the mouse position
                min_distance = float('inf') # Set the minimum distance to infinity
                insert_index = None # Set the insert index to None
                for i in range(len(click_positions)): # Loop through all the points
                    start, end = click_positions[i], click_positions[(i+1)%len(click_positions)] # Get the start and end of the line segment
                    distance = point_line_distance(mouse_pos, start, end) # Calculate the distance between the mouse and the line segment
                    if distance < min_distance: # If the distance is smaller than the minimum distance
                        min_distance = distance # Set the minimum distance to the distance
                        insert_index = i + 1 # Set the insert index to the index of the point after the start point 
                if insert_index is not None:
                    click_positions.insert(insert_index, mouse_pos)
            elif event.key == pygame.K_f:  # Flip the inputs around the specified x position
                click_positions = [pygame.Vector2(2*flip_x - pos.x, pos.y) for pos in click_positions]
            elif event.key == pygame.K_c:  # Clear the inputs
                click_positions = []
            elif event.key == pygame.K_SPACE:
                print(pygame.mouse.get_pos()[0]/scale, pygame.mouse.get_pos()[1]/scale) # Print the mouse position

    screen.blit(image, pygame.Vector2(0, 0)) # Draw the image

    if len(click_positions) > 2: # If there are more than 2 points
        pygame.draw.polygon(screen, POLYGON_COLOR, click_positions, 1) # Draw the polygon

    if show_circles: # If the circles should be shown
        for pos in click_positions: # Loop through all the points
            pygame.draw.circle(screen, POINT_COLOR, pos, POINT_RADIUS) # Draw the point

    # Update the screen
    pygame.display.flip()