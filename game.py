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
    """Update the sand positions so they fall down and spread out"""
    new_positions = []
    for x, y in sand_positions:
        below = (x, y + SAND_SIZE)
        below_left = (x - SAND_SIZE, y + SAND_SIZE)
        below_right = (x + SAND_SIZE, y + SAND_SIZE)

        # Check directly below first
        if below not in sand_positions and 0 <= below[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.append(below)
        # If that's occupied, check below-left
        elif below_left not in sand_positions and 0 <= below_left[0] < SCREEN_WIDTH and 0 <= below_left[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.append(below_left)
        # If that's occupied too, check below-right
        elif below_right not in sand_positions and 0 <= below_right[0] < SCREEN_WIDTH and 0 <= below_right[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.append(below_right)
        # If all three are occupied, the sand particle doesn't move
        else:
            new_positions.append((x, y))

    sand_positions[:] = new_positions  # Update the sand positions



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