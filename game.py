import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
FPS_CAP = 100
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAND_SIZE = 4
FONT = pygame.font.SysFont(None, 36) 

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Sandbox")
pygame.font.init()  # Initialize Pygame's font system

sand_positions = []
active_sand = set() 

def draw_text(text, x, y, color=WHITE):
    """Helper function to render and draw text onto the screen."""
    text_surf = FONT.render(text, True, color)
    screen.blit(text_surf, (x, y))

def is_adjacent_free(x, y):
    """Check if any adjacent position is free"""
    positions = [
        (x, y + SAND_SIZE),          # below
        (x, y - SAND_SIZE),          # above
        (x + SAND_SIZE, y),          # right
        (x - SAND_SIZE, y),          # left
        (x + SAND_SIZE, y + SAND_SIZE), # diagonal bottom right
        (x - SAND_SIZE, y + SAND_SIZE), # diagonal bottom left
        (x + SAND_SIZE, y - SAND_SIZE), # diagonal top right
        (x - SAND_SIZE, y - SAND_SIZE)  # diagonal top left
    ]
    for pos in positions:
        if pos not in sand_positions:
            return True
    return False

def drop_sand():
    global active_sand
    new_positions = set(sand_positions)
    next_active_sand = set()

    for x, y in list(active_sand):  # Convert set to list to safely iterate
        if (x, y) not in new_positions:  # Ensure position exists before processing
            continue
        
        below = (x, y + SAND_SIZE)
        below_left = (x - SAND_SIZE, y + SAND_SIZE)
        below_right = (x + SAND_SIZE, y + SAND_SIZE)
        
        moved = False
        if below not in new_positions and 0 <= below[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.remove((x, y))
            new_positions.add(below)
            moved = True
        elif below_left not in new_positions and 0 <= below_left[0] < SCREEN_WIDTH and 0 <= below_left[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.remove((x, y))
            new_positions.add(below_left)
            moved = True
        elif below_right not in new_positions and 0 <= below_right[0] < SCREEN_WIDTH and 0 <= below_right[1] < SCREEN_HEIGHT - SAND_SIZE:
            new_positions.remove((x, y))
            new_positions.add(below_right)
            moved = True

        if moved:
            # Check positions adjacent to the new position to see if they should be marked as active
            for dx in [-SAND_SIZE, 0, SAND_SIZE]:
                for dy in [-SAND_SIZE, 0, SAND_SIZE]:
                    adj_x = x + dx
                    adj_y = y + dy
                    if (adj_x, adj_y) in new_positions and is_adjacent_free(adj_x, adj_y):
                        next_active_sand.add((adj_x, adj_y))

    active_sand = next_active_sand
    sand_positions[:] = list(new_positions)



def draw_sand():
    """Draw the sand particles"""
    for pos in sand_positions:
        pygame.draw.rect(screen, YELLOW, (pos[0], pos[1], SAND_SIZE, SAND_SIZE))

def main():
    clock = pygame.time.Clock()
    placing_sand = False  # Track if we're currently placing sand

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    placing_sand = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Release left click
                    placing_sand = False

        if placing_sand:
            x, y = pygame.mouse.get_pos()
            x = (x // SAND_SIZE) * SAND_SIZE
            y = (y // SAND_SIZE) * SAND_SIZE
            if (x, y) not in sand_positions:
                sand_positions.append((x, y))
                active_sand.add((x, y))
                # Also, check the surrounding particles to activate them
                for dx in [-SAND_SIZE, 0, SAND_SIZE]:
                    for dy in [-SAND_SIZE, 0, SAND_SIZE]:
                        adj_x = x + dx
                        adj_y = y + dy
                        if (adj_x, adj_y) in sand_positions:
                            active_sand.add((adj_x, adj_y))

        drop_sand()
        
        screen.fill(BLACK)
        draw_sand()

        # Drawing the counter and FPS
        num_sand_particles = len(sand_positions)
        draw_text(f"Sand Particles: {num_sand_particles}", 10, 10)
        fps = int(clock.get_fps())
        draw_text(f"FPS: {fps}", 10, 50)

        pygame.display.flip()
        clock.tick(FPS_CAP)



if __name__ == "__main__":
    main()