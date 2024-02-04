import os
from pathlib import Path
import pygame

class BackgroundManager:
    """
    A class to manage the background images in a game.

    Attributes:
        images (list[Path]): A list of paths to the image files.
        delay (float): The delay in seconds between image changes.
        screen (pygame.Surface): The screen to draw the image on.
        current_image (int): The index of the current image.
        last_update (float): The time in seconds since the last image change.

    Methods:
        __init__(self, images: list[Path], delay: float): Initializes the BackgroundManager.
        update(self, delta_time): Updates the current image if the delay has passed.
        draw(self, screen): Draws the current image to the given screen.
    """

    def __init__(self, image_dir: Path, delay: float, screen: pygame.Surface) -> None:
        """
        Initializes the BackgroundManager with a list of images and a delay. 

        Arguments:
            image_dir (Path): The directory containing the images.
            delay (float): The delay in seconds between image changes. If -1, the image will not change.
            screen (pygame.Surface): The screen to draw the image on. 
        """
        # Load the images and scale them to the screen size
        self.image_dir = image_dir
        self.screen = screen
        
        self.delay = delay
        self.current_image = 0
        self.last_update = 0
        
        self.load_images()

    def update(self, delta_time) -> None:
        """
        Updates the current image if the delay has passed. If the delay is -1, the image will not change.

        Arguments:
            delta_time (float): The time in seconds since the last update.
        """
        self.screen.blit(self.images[self.current_image], (0, 0))
        if self.delay == -1:
            return

        self.last_update += delta_time
        if self.last_update > self.delay:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.last_update = 0

    def load_images(self) -> None:
        """
        Loads the images from the specified directory and scales them to the screen size. 
        Modifies the images in place.
        """
        image_files = sorted([image for image in os.listdir(self.image_dir) if image.endswith('.jpg')])
        self.images = []
        for image_file in image_files:
            image_path = os.path.join(self.image_dir, image_file)
            pygame_image = pygame.image.load(image_path).convert()
            self.images.append(pygame.transform.scale(pygame_image, (self.screen.get_width(), self.screen.get_height())))