import pygame
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load the uploaded terrain texture and heightmap
ground_texture = pygame.image.load("map_texture.png").convert()
heightmap = pygame.image.load("heightmap.png").convert()  # Grayscale heightmap

texture_width, texture_height = ground_texture.get_size()
heightmap_width, heightmap_height = heightmap.get_size()

# Camera settings
camera_x, camera_y = texture_width // 2, texture_height // 2  # Start in the center of the map
camera_angle = 0  # Rotation angle
camera_height = 150  # How high the camera is
elevation_scale = 80  # Increased elevation multiplier for better mountains
view_distance = 500  # Increase perspective depth
horizon = HEIGHT // 2 - 70  # Lower the horizon for better perspective

def get_height(x, y):
    """Gets height from the heightmap (0-255 grayscale)."""
    x = int(x) % heightmap_width
    y = int(y) % heightmap_height
    height_value = heightmap.get_at((x, y)).r / 255.0 * elevation_scale  # Scale height

    # Debugging: Print some height values
    if x % 200 == 0 and y % 200 == 0:
        print(f"Height at ({x}, {y}): {height_value}")

    return height_value

def draw_terrain():
    """Simulates Mode 7 with heightmap-based elevation adjustment."""
    for y in range(horizon, HEIGHT):  # Render from the horizon down
        depth = (y - horizon) / (HEIGHT - horizon)  # Normalize depth
        if depth == 0:
            continue  # Avoid division by zero

        # Perspective scaling with small offset to prevent extreme shrinking
        row_scale = view_distance / (depth + 0.5)  
        row_offset_y = camera_y + row_scale * math.sin(camera_angle)

        for x in range(WIDTH):  # Iterate through screen columns
            col_offset_x = camera_x + (x - WIDTH // 2) * row_scale * math.cos(camera_angle)

            # Sample height from heightmap
            height_at_point = get_height(col_offset_x, row_offset_y)

            # Adjust y-coordinate based on height
            adjusted_y = y - height_at_point

            # Convert to texture coordinates
            tex_x = int(col_offset_x) % texture_width
            tex_y = int(row_offset_y) % texture_height
            color = ground_texture.get_at((tex_x, tex_y))

            # Draw pixel or small block (to improve performance)
            pygame.draw.rect(screen, color, (x, adjusted_y, 1, 1))

running = True
while running:
    screen.fill((135, 206, 235))  # Sky color

    # Render pseudo-3D terrain
    draw_terrain()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_angle -= 0.05
    if keys[pygame.K_RIGHT]:
        camera_angle += 0.05
    if keys[pygame.K_UP]:
        camera_x += math.cos(camera_angle) * 5
        camera_y += math.sin(camera_angle) * 5
    if keys[pygame.K_DOWN]:
        camera_x -= math.cos(camera_angle) * 5
        camera_y -= math.sin(camera_angle) * 5

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
