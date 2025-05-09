import pygame
import math
import random

def create_enemy_car(color=None):
    """
    Creates a realistic-looking car image for enemies - oriented vertically
    """
    if color is None:
        # Random car colors
        color = random.choice([
            (0, 0, 180),    # Blue
            (0, 120, 0),    # Green
            (180, 0, 180),  # Purple
            (180, 100, 0)   # Orange
        ])
    
    # Create different car models
    car_type = random.randint(1, 3)
    
    if car_type == 1:
        return create_sedan_car(color)
    elif car_type == 2:
        return create_suv_car(color)
    else:
        return create_sports_car(color)

def create_sedan_car(color):
    """
    Creates a realistic sedan car
    """
    car_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
    
    # Adjust colors for highlights and shadows
    r, g, b = color
    highlight_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
    shadow_color = (max(r - 60, 0), max(g - 60, 0), max(b - 60, 0))
    
    # Main body shape
    pygame.draw.rect(car_surface, color, (10, 20, 40, 80), border_radius=8)
    
    # Hood
    pygame.draw.rect(car_surface, color, (15, 10, 30, 20), border_radius=5)
    
    # Trunk
    pygame.draw.rect(car_surface, color, (15, 90, 30, 20), border_radius=5)
    
    # Roof
    pygame.draw.rect(car_surface, color, (15, 40, 30, 30), border_radius=3)
    
    # Windows
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 42, 26, 26), border_radius=2)  # Main window
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 25, 26, 15), border_radius=2)  # Front windshield
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 70, 26, 15), border_radius=2)  # Rear windshield
    
    # Body highlights
    pygame.draw.line(car_surface, highlight_color, (10, 30), (10, 90), 2)  # Left side highlight
    pygame.draw.line(car_surface, shadow_color, (50, 30), (50, 90), 2)     # Right side shadow
    
    # Wheels - realistic with rims
    wheel_color = (30, 30, 30)
    rim_color = (200, 200, 200)
    
    # Left front wheel
    pygame.draw.circle(car_surface, wheel_color, (8, 35), 8)
    pygame.draw.circle(car_surface, rim_color, (8, 35), 4)
    
    # Right front wheel
    pygame.draw.circle(car_surface, wheel_color, (52, 35), 8)
    pygame.draw.circle(car_surface, rim_color, (52, 35), 4)
    
    # Left rear wheel
    pygame.draw.circle(car_surface, wheel_color, (8, 85), 8)
    pygame.draw.circle(car_surface, rim_color, (8, 85), 4)
    
    # Right rear wheel
    pygame.draw.circle(car_surface, wheel_color, (52, 85), 8)
    pygame.draw.circle(car_surface, rim_color, (52, 85), 4)
    
    # Wheel details - spokes
    for wheel_x, wheel_y in [(8, 35), (52, 35), (8, 85), (52, 85)]:
        for i in range(0, 360, 60):
            rad = i * math.pi / 180
            x1 = wheel_x + 4 * math.cos(rad)
            y1 = wheel_y + 4 * math.sin(rad)
            x2 = wheel_x + 1 * math.cos(rad)
            y2 = wheel_y + 1 * math.sin(rad)
            pygame.draw.line(car_surface, wheel_color, (int(x1), int(y1)), (int(x2), int(y2)), 1)
    
    # Headlights
    pygame.draw.circle(car_surface, (255, 255, 200), (20, 15), 5)  # Left headlight
    pygame.draw.circle(car_surface, (255, 255, 200), (40, 15), 5)  # Right headlight
    
    # Taillights
    pygame.draw.rect(car_surface, (255, 0, 0), (15, 100, 10, 5), border_radius=2)  # Left taillight
    pygame.draw.rect(car_surface, (255, 0, 0), (35, 100, 10, 5), border_radius=2)  # Right taillight
    
    # Door lines
    pygame.draw.line(car_surface, (0, 0, 0), (15, 50), (45, 50), 1)
    pygame.draw.line(car_surface, (0, 0, 0), (15, 70), (45, 70), 1)
    
    # Door handles
    pygame.draw.rect(car_surface, (200, 200, 200), (42, 55, 5, 2), border_radius=1)
    pygame.draw.rect(car_surface, (200, 200, 200), (42, 75, 5, 2), border_radius=1)
    
    # Grille
    for i in range(17, 44, 4):
        pygame.draw.line(car_surface, (50, 50, 50), (i, 18), (i, 22), 1)
    
    return car_surface

def create_suv_car(color):
    """
    Creates a realistic SUV car
    """
    car_surface = pygame.Surface((65, 130), pygame.SRCALPHA)
    
    # Adjust colors for highlights and shadows
    r, g, b = color
    highlight_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
    shadow_color = (max(r - 60, 0), max(g - 60, 0), max(b - 60, 0))
    
    # Main body shape - taller for SUV
    pygame.draw.rect(car_surface, color, (10, 20, 45, 90), border_radius=8)
    
    # Hood
    pygame.draw.rect(car_surface, color, (15, 10, 35, 20), border_radius=5)
    
    # Trunk/rear
    pygame.draw.rect(car_surface, color, (15, 100, 35, 20), border_radius=5)
    
    # Roof - longer for SUV
    pygame.draw.rect(car_surface, color, (15, 30, 35, 60), border_radius=3)
    
    # Windows - larger for SUV
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 35, 31, 50), border_radius=2)  # Main window
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 20, 31, 15), border_radius=2)  # Front windshield
    pygame.draw.rect(car_surface, (100, 200, 255), (17, 85, 31, 15), border_radius=2)  # Rear windshield
    
    # Body highlights
    pygame.draw.line(car_surface, highlight_color, (10, 30), (10, 100), 2)  # Left side highlight
    pygame.draw.line(car_surface, shadow_color, (55, 30), (55, 100), 2)     # Right side shadow
    
    # Wheels - larger for SUV
    wheel_color = (30, 30, 30)
    rim_color = (200, 200, 200)
    
    # Left front wheel
    pygame.draw.circle(car_surface, wheel_color, (10, 40), 10)
    pygame.draw.circle(car_surface, rim_color, (10, 40), 5)
    
    # Right front wheel
    pygame.draw.circle(car_surface, wheel_color, (55, 40), 10)
    pygame.draw.circle(car_surface, rim_color, (55, 40), 5)
    
    # Left rear wheel
    pygame.draw.circle(car_surface, wheel_color, (10, 90), 10)
    pygame.draw.circle(car_surface, rim_color, (10, 90), 5)
    
    # Right rear wheel
    pygame.draw.circle(car_surface, wheel_color, (55, 90), 10)
    pygame.draw.circle(car_surface, rim_color, (55, 90), 5)
    
    # Wheel details - spokes
    for wheel_x, wheel_y in [(10, 40), (55, 40), (10, 90), (55, 90)]:
        for i in range(0, 360, 60):
            rad = i * math.pi / 180
            x1 = wheel_x + 5 * math.cos(rad)
            y1 = wheel_y + 5 * math.sin(rad)
            x2 = wheel_x + 2 * math.cos(rad)
            y2 = wheel_y + 2 * math.sin(rad)
            pygame.draw.line(car_surface, wheel_color, (int(x1), int(y1)), (int(x2), int(y2)), 1)
    
    # Headlights
    pygame.draw.circle(car_surface, (255, 255, 200), (20, 15), 6)  # Left headlight
    pygame.draw.circle(car_surface, (255, 255, 200), (45, 15), 6)  # Right headlight
    
    # Taillights
    pygame.draw.rect(car_surface, (255, 0, 0), (15, 110, 12, 6), border_radius=2)  # Left taillight
    pygame.draw.rect(car_surface, (255, 0, 0), (38, 110, 12, 6), border_radius=2)  # Right taillight
    
    # Door lines
    pygame.draw.line(car_surface, (0, 0, 0), (15, 50), (50, 50), 1)
    pygame.draw.line(car_surface, (0, 0, 0), (15, 70), (50, 70), 1)
    
    # Door handles
    pygame.draw.rect(car_surface, (200, 200, 200), (47, 55, 5, 2), border_radius=1)
    pygame.draw.rect(car_surface, (200, 200, 200), (47, 75, 5, 2), border_radius=1)
    
    # Grille - larger for SUV
    pygame.draw.rect(car_surface, (50, 50, 50), (20, 18, 25, 8), border_radius=2)
    for i in range(22, 44, 5):
        pygame.draw.line(car_surface, (100, 100, 100), (i, 19), (i, 25), 1)
    
    # Roof rack - typical for SUV
    pygame.draw.line(car_surface, (50, 50, 50), (17, 35), (48, 35), 2)
    pygame.draw.line(car_surface, (50, 50, 50), (17, 80), (48, 80), 2)
    
    return car_surface

def create_sports_car(color):
    """
    Creates a realistic sports car
    """
    car_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
    
    # Adjust colors for highlights and shadows
    r, g, b = color
    highlight_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
    shadow_color = (max(r - 60, 0), max(g - 60, 0), max(b - 60, 0))
    
    # Main body shape - sleeker for sports car
    points = [
        (30, 10),   # Front nose
        (15, 25),   # Front left
        (45, 25),   # Front right
        (10, 40),   # Left front fender
        (50, 40),   # Right front fender
        (10, 80),   # Left rear fender
        (50, 80),   # Right rear fender
        (15, 100),  # Rear left
        (45, 100),  # Rear right
        (30, 110)   # Rear center
    ]
    pygame.draw.polygon(car_surface, color, points)
    
    # Hood lines
    pygame.draw.line(car_surface, shadow_color, (15, 25), (30, 10), 2)
    pygame.draw.line(car_surface, highlight_color, (30, 10), (45, 25), 2)
    
    # Side body lines
    pygame.draw.line(car_surface, shadow_color, (10, 40), (10, 80), 2)
    pygame.draw.line(car_surface, highlight_color, (50, 40), (50, 80), 2)
    
    # Windshield
    pygame.draw.polygon(car_surface, (100, 200, 255), [(20, 30), (40, 30), (35, 45), (25, 45)])
    
    # Side windows
    pygame.draw.polygon(car_surface, (100, 200, 255), [(15, 50), (45, 50), (45, 65), (15, 65)])
    
    # Rear window
    pygame.draw.polygon(car_surface, (100, 200, 255), [(20, 70), (40, 70), (35, 85), (25, 85)])
    
    # Wheels - sporty with larger rims
    wheel_color = (30, 30, 30)
    rim_color = (220, 220, 220)
    
    # Left front wheel
    pygame.draw.circle(car_surface, wheel_color, (10, 40), 9)
    pygame.draw.circle(car_surface, rim_color, (10, 40), 5)
    
    # Right front wheel
    pygame.draw.circle(car_surface, wheel_color, (50, 40), 9)
    pygame.draw.circle(car_surface, rim_color, (50, 40), 5)
    
    # Left rear wheel
    pygame.draw.circle(car_surface, wheel_color, (10, 80), 9)
    pygame.draw.circle(car_surface, rim_color, (10, 80), 5)
    
    # Right rear wheel
    pygame.draw.circle(car_surface, wheel_color, (50, 80), 9)
    pygame.draw.circle(car_surface, rim_color, (50, 80), 5)
    
    # Wheel details - spokes
    for wheel_x, wheel_y in [(10, 40), (50, 40), (10, 80), (50, 80)]:
        for i in range(0, 360, 45):
            rad = i * math.pi / 180
            x1 = wheel_x + 5 * math.cos(rad)
            y1 = wheel_y + 5 * math.sin(rad)
            x2 = wheel_x + 2 * math.cos(rad)
            y2 = wheel_y + 2 * math.sin(rad)
            pygame.draw.line(car_surface, wheel_color, (int(x1), int(y1)), (int(x2), int(y2)), 1)
    
    # Headlights - sleek
    pygame.draw.polygon(car_surface, (255, 255, 200), [(20, 20), (30, 15), (40, 20), (35, 25), (25, 25)])
    
    # Taillights - sporty
    pygame.draw.rect(car_surface, (255, 0, 0), (20, 95, 20, 5), border_radius=1)
    
    # Air intakes
    pygame.draw.rect(car_surface, (20, 20, 20), (25, 25, 10, 5), border_radius=1)
    
    # Spoiler
    pygame.draw.polygon(car_surface, color, [(15, 90), (45, 90), (40, 100), (20, 100)])
    
    return car_surface