import pygame

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

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Tile Game with Camera")

# Load player
player = pygame.Rect(100, 100, TILE_SIZE, TILE_SIZE)
player_speed = 5

# Camera
camera_x = 0
camera_y = 0

# Generate a simple tile map (0 - empty, 1 - wall)
game_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
for x in range(MAP_WIDTH):
    game_map[0][x] = 1  # Top wall
    game_map[MAP_HEIGHT - 1][x] = 1  # Bottom wall
for y in range(MAP_HEIGHT):
    game_map[y][0] = 1  # Left wall
    game_map[y][MAP_WIDTH - 1] = 1  # Right wall

def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_x = x * TILE_SIZE - camera_x
            tile_y = y * TILE_SIZE - camera_y
            if game_map[y][x] == 1:
                pygame.draw.rect(screen, GREEN, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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
