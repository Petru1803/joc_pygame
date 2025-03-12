import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
HEX_SIZE = int(WIDTH * 0.014)
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
        font = pygame.font.Font(None, 24)  # Small font for coordinates
        color = BLUE if self.owner == "player" else RED if self.owner == "ai" else GRAY
        points = self.get_hex_points()
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color + (150,), points)
        screen.blit(surface, (0, 0))  # Semi-transparent
        pygame.draw.polygon(screen, color, points, 2)
        text_surface = font.render(f'({int(self.x)}, {int(self.y)})', True, WHITE)
        screen.blit(text_surface, (self.x - HEX_SIZE // 2, self.y - HEX_SIZE // 2))

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

# Green area positions extracted from the map
hex_positions = [(x * WIDTH / 1792, y * HEIGHT / 1024) for x, y in [
    (x, y) for x, y in [
        (800, 1022), (42, 1022), (1567, 1022), (736, 1019), (395, 1020),
        (1674, 1017), (1441, 1017), (601, 1020), (1235, 1013), (528, 1007),
        (661, 1005), (324, 1002), (1513, 992), (114, 993), (443, 990),
        (1773, 989), (267, 982), (1633, 977), (166, 960), (1726, 959),
        (1559, 960), (727, 960), (57, 960), (846, 960), (557, 955),
        (391, 951), (614, 948), (1475, 938), (670, 947), (255, 925),
        (1016, 924), (1422, 914), (345, 912), (192, 909), (510, 908),
        (897, 899), (571, 899), (445, 891), (761, 892), (1777, 880),
        (637, 883), (296, 881), (1604, 878), (1276, 877), (995, 872),
        (1662, 864), (701, 860), (42, 859), (371, 853), (867, 848),
        (461, 836), (94, 829), (1032, 830), (806, 826),
        (637, 827), (274, 826), (201, 827), (1772, 822), (1135, 821),
        (1198, 818), (1630, 813), (1716, 812), (741, 804), (86, 894),
        (323, 794), (983, 799), (49, 793), (603, 780), (1586, 776),
        (673, 780), (1082, 775), (1524, 774), (898, 768), (548, 765),
        (1658, 765), (1789, 764), (801, 752), (1134, 750), (226, 751),
        (1729, 742), (1477, 734), (1014, 726), (664, 722), (751, 714),
        (1627, 711), (442, 707), (870, 712), (554, 701), (1557, 696),
        (251, 700), (174, 689), (810, 687), (1480, 678),
        (706, 676), (369, 679), (311, 671), (238, 644), (1678, 638),
        (1571, 630), (789, 630), (910, 629), (1783, 624), (1008, 616),
        (173, 610), (1510, 605), (331, 608), (1640, 586), (705, 578),
        (890, 572), (382, 571), (1584, 572), (784, 568), (439, 567),
        (1699, 562), (145, 558), (201, 554), (1651, 531), (1785, 526),
        (848, 521), (1560, 517), (752, 517), (259, 515), (164, 474),
        (1667, 470), (295, 470), (229, 467), (1728, 464), (886, 461),
        (1769, 424), (837, 433), (666, 402), (179, 401), (269, 394),
        (1721, 366), (26, 381), (131, 364), (607, 349), (180, 326),
        (64, 319), (1769, 294), (540, 284), (424, 258), (282, 232),
        (1769, 215), (229, 212), (96, 191), (339, 181), (162, 162),
        (252, 155), (1747, 146), (1583, 130), (82, 126), (1638, 107),
        (682, 96), (1701, 95), (1518, 94), (1761, 86), (755, 79),
        (39, 69), (167, 66), (962, 71), (833, 59), (1472, 46),
        (1635, 35), (1576, 29), (94, 29), (247, 25), (1741, 25),
        (1222, 24), (774, 26), (682, 24), (906, 27), (1507, 2),
        (840, 3), (946, 446), (178, 1),(720, 350), (880, 350), (1120, 350), (1200, 350),
        (600, 420), (1000, 420), (1080, 420), (1240, 420),
        (640, 490), (800, 490), (880, 490), (960, 490), (1040, 490), (1200, 490),
        (720, 560), (880, 560), (1040, 560), (1120, 560),
        (640, 630), (720, 630), (800, 630), (880, 630), (1040, 630), (1120, 630),
        (680, 700), (760, 700), (920, 700), (1000, 700), (1080, 700), (1160, 700),(1330, 200), (1490, 200), (1650, 200),
        (1290, 270), (1450, 270), (1610, 270), (1770, 270),
        (1250, 340), (1330, 340), (1490, 340), (1650, 340),
        (1370, 410), (1530, 410), (1690, 410),
        (1250, 480), (1410, 480), (1570, 480), (1730, 480),
        (1290, 550), (1370, 550), (1530, 550), (1690, 550),
        (1250, 620), (1410, 620), (1570, 620), (1730, 620),
        (1330, 690), (1490, 690), (1650, 690)
    ] if 5 <= x <= 1499 and 10 <= y <= 799]]

hex_width = HEX_SIZE * 2
hex_height = int(HEX_SIZE * 1.732)
min_x, min_y = 100 + 3 * hex_width, 250
max_x, max_y = 800 - 3 * hex_width, 750

for x, y in hex_positions:
    if (y // hex_height) % 2 == 1:
        x += hex_width // 2
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
