import pygame
import json
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32  # Size of each tile
MAP_WIDTH = 30  # Number of tiles in width
MAP_HEIGHT = 20  # Number of tiles in height

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Tile types
EMPTY_TILE = 0
WALL_TILE = 1
CHANGED_TILE = 2

# Save/Load files
MAP_FILE = "saved_map.json"
PLAYER_FILE = "player_data.json"

def save_game():
    with open(MAP_FILE, "w") as file:
        json.dump(game_map, file)
    with open(PLAYER_FILE, "w") as file:
        json.dump({"x": player.x, "y": player.y}, file)

def load_map():
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, "r") as file:
            return json.load(file)
    else:
        return [[EMPTY_TILE for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def load_player():
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as file:
            data = json.load(file)
            return pygame.Rect(data["x"], data["y"], TILE_SIZE, TILE_SIZE)
    else:
        return pygame.Rect(100, 100, TILE_SIZE, TILE_SIZE)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Tile Game with Camera")

# Load player and map
game_map = load_map()
player = load_player()
player_speed = 5

# Camera
camera_x = 0
camera_y = 0

# Ensure walls are placed
for x in range(MAP_WIDTH):
    game_map[0][x] = WALL_TILE  # Top wall
    game_map[MAP_HEIGHT - 1][x] = WALL_TILE  # Bottom wall
for y in range(MAP_HEIGHT):
    game_map[y][0] = WALL_TILE  # Left wall
    game_map[y][MAP_WIDTH - 1] = WALL_TILE  # Right wall

def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_x = x * TILE_SIZE - camera_x
            tile_y = y * TILE_SIZE - camera_y
            if game_map[y][x] == WALL_TILE:
                pygame.draw.rect(screen, GREEN, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
            elif game_map[y][x] == CHANGED_TILE:
                pygame.draw.rect(screen, RED, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Convert player's position to tile coordinates
                tile_x = player.x // TILE_SIZE
                tile_y = player.y // TILE_SIZE
                # Change the tile type if it's empty
                if game_map[tile_y][tile_x] == EMPTY_TILE:
                    game_map[tile_y][tile_x] = CHANGED_TILE
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - player_speed >= TILE_SIZE:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x + player_speed + TILE_SIZE <= (MAP_WIDTH * TILE_SIZE) - TILE_SIZE:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y - player_speed >= TILE_SIZE:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y + player_speed + TILE_SIZE <= (MAP_HEIGHT * TILE_SIZE) - TILE_SIZE:
        player.y += player_speed
    
    # Camera follows player but stays within boundaries
    camera_x = max(0, min(player.x - SCREEN_WIDTH // 2 + TILE_SIZE // 2, (MAP_WIDTH * TILE_SIZE) - SCREEN_WIDTH))
    camera_y = max(0, min(player.y - SCREEN_HEIGHT // 2 + TILE_SIZE // 2, (MAP_HEIGHT * TILE_SIZE) - SCREEN_HEIGHT))
    
    # Draw game world
    draw_map()
    pygame.draw.rect(screen, BLUE, (player.x - camera_x, player.y - camera_y, TILE_SIZE, TILE_SIZE))
    
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
