import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
TILE_SIZE = 80
GRID_PADDING = 10
BACKGROUND_COLOR = (187, 173, 160)
GRID_COLOR = (205, 193, 180)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 40)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Function to draw the game grid and tiles
def draw():
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window, GRID_COLOR, (GRID_PADDING, 100, WIDTH - 2 * GRID_PADDING, HEIGHT - 100 - GRID_PADDING))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = grid[i][j]
            tile_color = get_tile_color(tile_value)
            pygame.draw.rect(window, tile_color, (GRID_PADDING + j * (TILE_SIZE + GRID_PADDING),
                                                  100 + GRID_PADDING + i * (TILE_SIZE + GRID_PADDING),
                                                  TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                text = FONT.render(str(tile_value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(GRID_PADDING + j * (TILE_SIZE + GRID_PADDING) + TILE_SIZE // 2,
                                                  100 + GRID_PADDING + i * (TILE_SIZE + GRID_PADDING) + TILE_SIZE // 2))
                window.blit(text, text_rect)
    
    # Display score
    score_text = FONT.render(f"Score: {score}", True, TEXT_COLOR)
    window.blit(score_text, (20, 20))
    
    pygame.display.update()

# Function to get tile color based on tile value
def get_tile_color(value):
    colors = {
        0: (205, 193, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121), 
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46)
    }
    return colors.get(value, (255, 255, 255))  # Default color for unknown values


# Function to add a new tile (2 or 4) to a random empty cell
def add_new_tile(grid):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Initialize the game grid and score
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
add_new_tile(grid)
add_new_tile(grid)

# Function to merge tiles and update the score
def merge_tiles(value):
    global score
    score += value

# Function to move tiles based on keyboard input
def move_tiles(key):
    global grid
    if key == pygame.K_UP:
        grid = move_up(grid)
    elif key == pygame.K_DOWN:
        grid = move_down(grid)
    elif key == pygame.K_LEFT:
        grid = move_left(grid)
    elif key == pygame.K_RIGHT:
        grid = move_right(grid)
    
    # After moving tiles, add a new tile to the grid
    add_new_tile(grid)

# Function to move tiles upwards
def move_up(grid):
    for j in range(GRID_SIZE):
        # Shifting tiles upwards
        for i in range(1, GRID_SIZE):
            if grid[i][j] != 0:
                k = i
                while k > 0 and grid[k - 1][j] == 0:
                    grid[k - 1][j] = grid[k][j]
                    grid[k][j] = 0
                    k -= 1

        # Merging tiles if the side-most numbers are equal
        for i in range(GRID_SIZE - 1):
            if grid[i][j] != 0 and grid[i][j] == grid[i + 1][j]:
                merged_value = grid[i][j] * 2
                merge_tiles(merged_value)  # Update the score
                grid[i][j] = merged_value
                grid[i + 1][j] = 0
                k = i + 1
                while k < GRID_SIZE - 1:
                    grid[k][j] = grid[k + 1][j]
                    k += 1
                grid[k][j] = 0

    return grid

# Function to move tiles downwards
def move_down(grid):
    for j in range(GRID_SIZE):
        # Shifting tiles downwards
        for i in range(GRID_SIZE - 2, -1, -1):
            if grid[i][j] != 0:
                k = i
                while k < GRID_SIZE - 1 and grid[k + 1][j] == 0:
                    grid[k + 1][j] = grid[k][j]
                    grid[k][j] = 0
                    k += 1

        # Merging tiles if the side-most numbers are equal
        for i in range(GRID_SIZE - 1, 0, -1):
            if grid[i][j] != 0 and grid[i][j] == grid[i - 1][j]:
                merged_value = grid[i][j] * 2
                merge_tiles(merged_value)  # Update the score
                grid[i][j] = merged_value
                grid[i - 1][j] = 0
                k = i - 1
                while k > 0:
                    grid[k][j] = grid[k - 1][j]
                    k -= 1
                grid[k][j] = 0

    return grid

# Function to move tiles to the left
def move_left(grid):
    for i in range(GRID_SIZE):
        for j in range(1, GRID_SIZE):  # Start from the second column and move towards left
            if grid[i][j] != 0:
                # Move tile to the left as far as possible
                k = j
                while k > 0 and grid[i][k - 1] == 0:
                    grid[i][k - 1] = grid[i][k]
                    grid[i][k] = 0
                    k -= 1
                
                # Merge tiles with the same value
                if k > 0 and grid[i][k - 1] == grid[i][k]:
                    merged_value = grid[i][k] * 2
                    merge_tiles(merged_value)  # Update the score
                    grid[i][k - 1] = merged_value
                    grid[i][k] = 0

    return grid

# Function to move tiles to the right
def move_right(grid):
    for i in range(GRID_SIZE):
        # Shifting tiles to the right
        for j in range(GRID_SIZE - 2, -1, -1):
            if grid[i][j] != 0:
                k = j
                while k < GRID_SIZE - 1 and grid[i][k + 1] == 0:
                    grid[i][k + 1] = grid[i][k]
                    grid[i][k] = 0
                    k += 1

        # Merging tiles if the side-most numbers are equal
        for j in range(GRID_SIZE - 1, 0, -1):
            if grid[i][j] != 0 and grid[i][j] == grid[i][j - 1]:
                merged_value = grid[i][j] * 2
                merge_tiles(merged_value)  # Update the score
                grid[i][j] = merged_value
                k = j - 1
                while k > 0:
                    grid[i][k] = grid[i][k - 1]
                    k -= 1
                grid[i][k] = 0

    return grid


# Function to check if the game is over
def check_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False  # Game is not over as there is an empty cell

            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False  # Game is not over as there are still mergeable tiles vertically

            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False  # Game is not over as there are still mergeable tiles horizontally

    return True  # Game is over as there are no empty cells and no mergeable tiles

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                move_tiles(event.key)
                if check_game_over():
                    # If game is over, update the display to show "Game Over"
                    game_over_text = FONT.render("Game Over", True, TEXT_COLOR)
                    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    window.blit(game_over_text, game_over_rect)
                    pygame.display.update()
                    pygame.time.wait(5000)  # Wait for 5 seconds before quitting
                    running = False

    draw()

# Quit Pygame properly
pygame.quit()