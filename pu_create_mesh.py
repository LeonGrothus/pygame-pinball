from pathlib import Path
import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Definiere Konstanten
scale = 1.5
SCREEN_WIDTH = 666 * scale
SCREEN_HEIGHT = 1000 * scale
IMAGE_PATH = Path("image.png")
STRETCH_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Erstelle das Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Rendering Scene")

# Lade das Bild
image = pygame.image.load(IMAGE_PATH)
image = pygame.transform.scale(image, STRETCH_SIZE)

# Liste für die Positionen der Klicks
click_positions = []

# Haupt-Event-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Speichere die Mausposition beim Klicken
            click_positions.append(pygame.Vector2(pygame.mouse.get_pos())//scale)
            print("Click Positions:", *click_positions)

    screen.blit(image, pygame.Vector2(0, 0))

    # Aktualisiere den Bildschirm
    pygame.display.flip()