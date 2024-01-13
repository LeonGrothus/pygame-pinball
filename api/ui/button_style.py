import math
import os
import numpy as np
import pygame
from pygame import Surface
import pygame.surfarray as surfarray
from pathlib import Path

from typing import Tuple


class ButtonStyle:
    def __init__(self, folder_path: Path):
        """
        Initializes a new instance of the ButtonStyle class.

        This method loads the tiled images from the specified folder.

        Parameters:
            folder_path (Path): The path to the folder containing the tile images.
        """
        self.tiles = [(pygame.image.load(folder_path / f"{i}.png").convert_alpha()) for i in range(1, 10)]

    def create_button(self, size: Tuple[int, int], left_sided=False, right_sided=False, top_sided=False, bottom_sided=False, tint=None, gamma: float=0) -> Surface:
        """
        Creates a new button with the specified size and sides.

        This method creates a new button by blitting the appropriate tile onto each part of the button. 
        The tiles are blitted in a grid pattern, with the corners and edges using the appropriate tiles 
        and the center using the center tile. If a tint is specified, it is applied to all tiles. 
        The brightness of the tiles can be adjusted using the gamma parameter.

        Parameters:
            size (Tuple[int, int]): The size of the button.
            left_sided (bool, optional): Whether the button should be left-sided. Defaults to False.
            right_sided (bool, optional): Whether the button should be right-sided. Defaults to False.
            top_sided (bool, optional): Whether the button should be top-sided. Defaults to False.
            bottom_sided (bool, optional): Whether the button should be bottom-sided. Defaults to False.
            tint (Tuple[int, int, int], optional): The RGB values of the tint to apply to the tiles. Defaults to None.
            gamma (float, optional): The gamma correction to apply to the tiles. A value of 0 means no change, -1 means maximum brightness, and 1 means maximum darkness. Defaults to 0.

        Returns:
            Surface: The created button.
        """
        button = pygame.Surface(size, pygame.SRCALPHA, 32)

        tile_size = self.tiles[0].get_size()

        # if the minimum size is less than 100, scale the tiles down because the tiles are 50x50
        scale_factor = min(size[0] / 100, size[1] / 100, 1)  # don't scale up
        scaled_tile_size = (int(tile_size[0] * scale_factor), int(tile_size[1] * scale_factor))

        # calculate the number of rows and columns of tiles
        rows = math.ceil(size[1] / scaled_tile_size[1])
        cols = math.ceil(size[0] / scaled_tile_size[0])
 
        # blit the tiles onto the button
        for i in range(rows):
            for j in range(cols):
                # default to center tile
                tile = self.tiles[4]
                tile_size = scaled_tile_size

                if i == 0 and not top_sided:  # top row
                    if j == 0 and not left_sided:  # left corner
                        tile = self.tiles[0] # top left
                    elif j == cols - 1 and not right_sided:  # right corner
                        tile = self.tiles[2] # top right
                    else:  # top middle
                        tile = self.tiles[1] # top middle
                        tile_size = (size[0] - tile_size[0] * (cols - 1), tile_size[1])
                elif i == rows - 1 and not bottom_sided:  # bottom row
                    if j == 0 and not left_sided:  # left corner
                        tile = self.tiles[6] # bottom left
                    elif j == cols - 1 and not right_sided:  # right corner
                        tile = self.tiles[8] # bottom right
                    else:  # bottom middle
                        tile = self.tiles[7] # bottom middle
                        tile_size = (size[0] - tile_size[0] * (cols - 1), tile_size[1])
                elif j == 0 and not left_sided:  # left middle
                    tile = self.tiles[3] # left middle
                    tile_size = (tile_size[0], size[1] - tile_size[1] * (rows - 1))
                elif j == cols - 1 and not right_sided:  # right middle
                    tile = self.tiles[5] # right middle
                    tile_size = (tile_size[0], size[1] - tile_size[1] * (rows - 1))
                else:  # middle middle
                    tile_size = (size[0] - tile_size[0] * (cols - 1), size[1] - tile_size[1] * (rows - 1))

                # apply tint to the tile if necessary
                if tint:
                    tile = tile.copy()  # create a copy to not modify the original tile
                    tile.fill(tint, special_flags=pygame.BLEND_RGBA_MULT)

                # apply gamma correction to the tile if necessary
                if gamma != 0:
                    tile = tile.copy()  # create a copy to not modify the original tile
                    # apply gamma correction to each pixel
                    for x in range(tile.get_width()):
                        for y in range(tile.get_height()):
                            r, g, b, a = tile.get_at((x, y))
                            r = min(max(int(r + gamma * 255), 0), 255)
                            g = min(max(int(g + gamma * 255), 0), 255)
                            b = min(max(int(b + gamma * 255), 0), 255)
                            tile.set_at((x, y), pygame.Color(r, g, b, a))
                
                # scale the tile if necessary
                if scale_factor != 1 or tile_size != scaled_tile_size:
                    tile = pygame.transform.scale(tile, tile_size)

                # calculate the position of the tile
                pos_x = min(j * scaled_tile_size[0], size[0] - tile_size[0])
                pos_y = min(i * scaled_tile_size[1], size[1] - tile_size[1])
                button.blit(tile, (pos_x, pos_y))
        return button


#############
### Debug ###
#############

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    button_manager = ButtonStyle(
        Path(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'buttons', 'default_style')))
    button = button_manager.create_button((200, 125))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((127, 0, 127))
        screen.blit(button, (300, 250))
        pygame.display.flip()

    pygame.quit()
