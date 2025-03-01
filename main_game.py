import pygame
import json
import os

# Initialize pygame
pygame.init()

# Get the screen resolution
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
TILE_SIZE = 32  # Size of each tile

# Calculate map dimensions based on screen size
MAP_WIDTH = max(1, SCREEN_WIDTH // TILE_SIZE)
MAP_HEIGHT = max(1, SCREEN_HEIGHT // TILE_SIZE)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128, 100)  # Semi-transparent gray

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

# Create screen in full-screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("2D Tile Game with Camera")

# Load player and map
game_map = load_map()
player = load_player()
player_speed = 5

# Pause menu state
paused = False

# Ensure game_map has the correct dimensions
while len(game_map) < MAP_HEIGHT:
    game_map.append([EMPTY_TILE] * MAP_WIDTH)
for row in game_map:
    while len(row) < MAP_WIDTH:
        row.append(EMPTY_TILE)

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

def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))  # Adjust alpha for better visibility
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 60)
    resume_text = font.render("Resume", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    screen.blit(resume_text, resume_rect)
    screen.blit(quit_text, quit_rect)
    return resume_rect, quit_rect

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
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state
        elif event.type == pygame.MOUSEBUTTONDOWN and paused:
            mouse_pos = pygame.mouse.get_pos()
            if resume_rect.collidepoint(mouse_pos):
                paused = False
            elif quit_rect.collidepoint(mouse_pos):
                save_game()
                running = False
    
    if not paused:
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
    else:
        resume_rect, quit_rect = draw_pause_menu()
    
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
