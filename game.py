import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAND_SIZE = 4

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Sandbox")

sand_positions = []

def drop_sand():
    """Update the sand positions so they fall down"""
    for i in range(len(sand_positions) - 1, -1, -1):
        x, y = sand_positions[i]
        if y + SAND_SIZE < SCREEN_HEIGHT and (x, y + SAND_SIZE) not in sand_positions:
            sand_positions[i] = (x, y + SAND_SIZE)

def draw_sand():
    """Draw the sand particles"""
    for pos in sand_positions:
        pygame.draw.rect(screen, YELLOW, (pos[0], pos[1], SAND_SIZE, SAND_SIZE))

def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                x, y = pygame.mouse.get_pos()
                x = (x // SAND_SIZE) * SAND_SIZE  # Make the sand placement grid-aligned
                y = (y // SAND_SIZE) * SAND_SIZE
                sand_positions.append((x, y))

        drop_sand()

        screen.fill(BLACK)
        draw_sand()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()