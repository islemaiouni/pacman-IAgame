import pygame
import random
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 10  # Game Speed

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Initialize entities
pacman_pos = None
food_positions = []
enemy_positions = []

# BFS Algorithm to find the shortest path while avoiding enemies and reaching food
def bfs(grid, start, goals, enemies):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [])])  # Store (current position, path taken)
    visited = set([start])

    while queue:
        current, path = queue.popleft()
        
        if current in goals:  # If we've reached a food goal, return the path
            return path + [current]

        # Explore all possible movements
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            
            if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and next_pos not in visited and next_pos not in enemies:
                visited.add(next_pos)
                queue.append((next_pos, path + [current]))

    return []  # If no valid path found

# Function to draw the grid and game elements
def draw_grid(screen, pacman_pos, food_positions, enemy_positions):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Grid lines

    # Draw Pacman
    px, py = pacman_pos
    pygame.draw.circle(screen, YELLOW, (py * CELL_SIZE + CELL_SIZE // 2, px * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw Food
    for fx, fy in food_positions:
        pygame.draw.circle(screen, GREEN, (fy * CELL_SIZE + CELL_SIZE // 2, fx * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    # Draw Enemies
    for ex, ey in enemy_positions:
        pygame.draw.circle(screen, RED, (ey * CELL_SIZE + CELL_SIZE // 2, ex * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

# Function to place Pacman, food, and enemies randomly
def place_entities():
    global pacman_pos, food_positions, enemy_positions

    # Pacman Position
    pacman_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

    # Food Positions
    food_positions = []
    while len(food_positions) < 2:
        food_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food_pos != pacman_pos and food_pos not in food_positions:
            food_positions.append(food_pos)

    # Enemy Positions
    enemy_positions = []
    while len(enemy_positions) < 2:
        enemy_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if enemy_pos != pacman_pos and enemy_pos not in food_positions and enemy_pos not in enemy_positions:
            enemy_positions.append(enemy_pos)

    return food_positions, enemy_positions

# Main Game Loop
def main():
    global pacman_pos, food_positions, enemy_positions
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman with BFS AI")
    clock = pygame.time.Clock()
    running = True

    # Place entities on the grid
    food_positions, enemy_positions = place_entities()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # BFS for AI Movement (Pacman moves to the nearest food while avoiding enemies)
        path = []
        if food_positions:
            # Compute the shortest path to all food goals
            food_paths = []
            for food in food_positions:
                food_paths.append(bfs([[0] * GRID_SIZE for _ in range(GRID_SIZE)], pacman_pos, [food], enemy_positions))
            
            # Find the path that reaches any of the food
            valid_paths = [p for p in food_paths if p]
            if valid_paths:
                path = min(valid_paths, key=lambda p: len(p))  # Shortest path to food

        # Move Pacman along the path if a path exists
        if path:
            pacman_pos = path[1]  # Move Pacman to the next step in the path

        # Check if food is eaten
        if pacman_pos in food_positions:
            food_positions.remove(pacman_pos)  # Remove food from the list

            # If all food is eaten, place new food and enemies
            if not food_positions:
                print("All food eaten!")
                food_positions, enemy_positions = place_entities()

        # Check if Pacman touches any enemies (game over)
        if pacman_pos in enemy_positions:
            print("Game Over! Pacman was caught by an enemy.")
            running = False

        # Draw
        screen.fill(BLACK)
        draw_grid(screen, pacman_pos, food_positions, enemy_positions)
        pygame.display.flip()
        clock.tick(FPS)  # Control game speed

    pygame.quit()

if __name__ == "__main__":
    main()
