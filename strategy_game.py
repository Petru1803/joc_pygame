import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1792, 1024
HEX_SIZE = 25
BG_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (200, 50, 50)
GRAY = (150, 150, 150)

# Load background image
BACKGROUND_IMAGE = pygame.image.load("background2.jpg")
BACKGROUND_IMAGE = pygame.transform.smoothscale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Game states
MENU = "menu"
GAME = "game"
PAUSED = "paused"
state = MENU
selected_hex = None

# Button class
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BG_COLOR)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# Hexagon class
import pygame
import random

class Hexagon:
    def __init__(self, x, y, owner="neutral"):
        self.x, self.y = x, y
        self.owner = owner
        self.stats = {"Power": random.randint(1, 10), "Defense": random.randint(1, 10)}

    # Factory levels
        self.factory_levels = {
            "armor_factory": 0,
            "barracks": 0,
            "airplane_factory": 0,
            "food_factory": 0,
            "resource_gathering": 0
        }
        
        # Unit counts
        self.units = {
            "guards": 0,
            "motorized_guards": 0,
            "infantry": 0,
            "motorized_infantry": 0,
            "recon": 0,
            "motorized_recon": 0,
            "light_armor": 0,
            "medium_armor": 0,
            "heavy_armor": 0,
            "fighter_squadron": 0,
            "paratroopers": 0
        }
        
        # Stats
        self.stats = {"Power": random.randint(1, 10), "Defense": random.randint(1, 10)}
        self.x, self.y = x, y
        self.owner = owner
        self.stats = {"Power": random.randint(1, 10), "Defense": random.randint(1, 10)}

    def draw(self):
        color = BLUE if self.owner == "player" else RED if self.owner == "ai" else GRAY
        points = self.get_hex_points()
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color + (150,), points)
        screen.blit(surface, (0, 0))  # Semi-transparent
        pygame.draw.polygon(screen, color, points, 2)

    def get_hex_points(self):
        """Calculate the six corners of the hexagon with a 45-degree top-down effect."""
        points = []
        for i in range(6):
            angle = pygame.math.Vector2(HEX_SIZE, 0).rotate(60 * i)
            angle.y *= 0.5  # Squash the Y-axis for the perspective effect
            points.append((self.x + angle.x, self.y + angle.y))
        return points

    def check_click(self, pos):
        """Check if a point is inside the hexagon."""
        points = self.get_hex_points()
        
        # First, create a bounding box for a quick pre-check
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        
        # Quick bounding box check (improves performance)
        if not (min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y):
            return False

        # Use pygame’s polygon collision detection
        polygon = pygame.draw.polygon(screen, (0, 0, 0), points)
        return polygon.collidepoint(pos)


# Menu actions
def start_game():
    global state
    state = GAME

def pause_game():
    global state
    state = PAUSED

def quit_game():
    pygame.quit()
    exit()

def close_hex_menu():
    global selected_hex
    selected_hex = None

# Create menu buttons
start_button = Button("Start", WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, start_game)
quit_button = Button("Quit", WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, quit_game)

# Create hexagons grid
hexagons = []

# Define the rectangular area to fully cover with hexagons
hex_width = HEX_SIZE * 2
hex_height = int(HEX_SIZE * 1.732)  # Height of a hexagon in a staggered grid

# Define the bounding box from the top-most and bottom-most hexagons
min_x, min_y = 100 + 3 * hex_width, 250
max_x, max_y = 800 - 3 * hex_width, 750

# Generate hexagons to fully cover the bounding box
for y in range(min_y, max_y + hex_height, hex_height):
    for x in range(min_x, max_x + hex_width, hex_width):
        if (y // hex_height) % 2 == 1:
            x += hex_width // 2  # Offset every other row
        owner = "neutral"
        hexagons.append(Hexagon(x, y, owner))

# Set exactly two hexagons to be blue (player-owned)
if len(hexagons) > 2:
    hexagons[0].owner = "player"
    hexagons[1].owner = "player"

# Land hexagons detected from the image
#land_hex_positions = [(x, y) for (x, y) in [
    #(100, 150), (200, 250), (300, 350), (400, 450), (500, 550), (600, 650), (700, 750), (800, 850)]]  # Replace with detected hex positions
#for x, y in land_hex_positions:
    #owner = random.choice(["player", "neutral", "ai"])
    #hexagons.append(Hexagon(x, y, owner))

# Main loop
running = True
while running:
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if state == GAME:
                state = PAUSED
            elif state == PAUSED:
                state = GAME
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == MENU or state == PAUSED:
                start_button.check_click(event.pos)
                quit_button.check_click(event.pos)
            elif state == GAME:
                clicked_hex = None
                for hexagon in hexagons:
                    if hexagon.check_click(event.pos):
                        clicked_hex = hexagon
                        break
                if clicked_hex and clicked_hex.owner == "player":
                    selected_hex = clicked_hex
                else:
                    selected_hex = None
                    
                #else:
                    #if selected_hex and pygame.Rect(WIDTH - 200, HEIGHT//2 - 100, 150, 150).collidepoint(event.pos):
                        #if pygame.Rect(WIDTH - 70, HEIGHT//2 - 100, 20, 20).collidepoint(event.pos):
                           # close_hex_menu()
    
    if state == MENU or state == PAUSED:
        start_button.draw()
        quit_button.draw()
    elif state == GAME:
        for hexagon in hexagons:
            hexagon.draw()
        
        if selected_hex:
            pygame.draw.rect(screen, WHITE, (WIDTH - 200, HEIGHT//2 - 100, 150, 150))
            text = small_font.render(f"Power: {selected_hex.stats['Power']}", True, BG_COLOR)
            screen.blit(text, (WIDTH - 190, HEIGHT//2 - 80))
            text = small_font.render(f"Defense: {selected_hex.stats['Defense']}", True, BG_COLOR)
            screen.blit(text, (WIDTH - 190, HEIGHT//2 - 50))
            
            close_button = pygame.Rect(WIDTH - 70, HEIGHT//2 - 100, 20, 20)
            pygame.draw.rect(screen, RED, close_button)
            pygame.draw.line(screen, WHITE, (WIDTH - 68, HEIGHT//2 - 98), (WIDTH - 52, HEIGHT//2 - 82), 3)
            pygame.draw.line(screen, WHITE, (WIDTH - 52, HEIGHT//2 - 98), (WIDTH - 68, HEIGHT//2 - 82), 3)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
