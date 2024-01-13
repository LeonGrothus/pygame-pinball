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
        self.tiles = [pygame.image.load(folder_path / f"{i}.png") for i in range(1, 10)]

    def create_button(self, size: Tuple[int, int], left_sided=False, right_sided=False, top_sided=False, bottom_sided=False, tint=None, gamma: float=0) -> Surface:
        """
        Creates a new button with the specified size and sides.

        This method creates a new button by blitting the appropriate tile onto each part of the button. The tiles are blitted in a grid pattern, with the corners and edges using the appropriate tiles and the center using the center tile. If a tint is specified, it is applied to all tiles. The brightness of the tiles can be adjusted using the gamma parameter.

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
        button = pygame.Surface(size)

        tile_size = self.tiles[0].get_size()
        scale_factor = min(size[0] / 100, size[1] / 100, 1)  # don't scale up
        scaled_tile_size = (int(tile_size[0] * scale_factor), int(tile_size[1] * scale_factor))


        rows = size[1] // scaled_tile_size[1]
        cols = size[0] // scaled_tile_size[0]

        for i in range(rows):
            for j in range(cols):
                tile = self.tiles[4]  # default to center tile
                if i == 0 and not top_sided:  # top row
                    if j == 0 and not left_sided:  # left corner
                        tile = self.tiles[0]
                    elif j == cols - 1 and not right_sided:  # right corner
                        tile = self.tiles[2]
                    else:  # top middle
                        tile = self.tiles[1]
                elif i == rows - 1 and not bottom_sided:  # bottom row
                    if j == 0 and not left_sided:  # left corner
                        tile = self.tiles[6]
                    elif j == cols - 1 and not right_sided:  # right corner
                        tile = self.tiles[8]
                    else:  # bottom middle
                        tile = self.tiles[7]
                elif j == 0 and not left_sided:  # left middle
                    tile = self.tiles[3]
                elif j == cols - 1 and not right_sided:  # right middle
                    tile = self.tiles[5]

                if tint:
                    tile = tile.copy()  # create a copy to not modify the original tile
                    tile.fill(tint, special_flags=pygame.BLEND_RGBA_MULT)

                if gamma != 0:
                    arr = surfarray.array3d(tile)
                    arr = np.clip(arr * (1 - gamma), 0, 255).astype(np.uint8)
                    tile = surfarray.make_surface(arr)

                if scale_factor != 1:
                    tile = pygame.transform.scale(tile, scaled_tile_size)

                button.blit(tile, (j * scaled_tile_size[0], i * scaled_tile_size[1]))

        return button


#############
### Debug ###
#############

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    button_manager = ButtonStyle(
        Path("/home/leon/Schreibtisch/Studium/Programmieren und Algorithmen/Pinball/assets/buttons/default_style"))
    button = button_manager.create_button((20, 20), gamma=-.2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(button, (300, 250))
        pygame.display.flip()

    pygame.quit()
