import pygame
import math

def create_player_car():
    """
    Creates a realistic-looking car image for the player - oriented vertically
    """
    car_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
    
    # Car body - metallic red
    body_color = (180, 0, 0)
    highlight_color = (220, 30, 30)
    shadow_color = (120, 0, 0)
    
    # Main body shape
    pygame.draw.rect(car_surface, body_color, (10, 20, 40, 80), border_radius=8)
    
    # Hood
    pygame.draw.rect(car_surface, body_color, (15, 10, 30, 20), border_radius=5)
    
    # Trunk
    pygame.draw.rect(car_surface, body_color, (15, 90, 30, 20), border_radius=5)
    
    # Roof
    pygame.draw.rect(car_surface, body_color, (15, 40, 30, 30), border_radius=3)
    
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

def create_lamborghini_car():
    """
    Creates a realistic Lamborghini-style sports car - oriented vertically
    """
    car_surface = pygame.Surface((70, 140), pygame.SRCALPHA)
    
    # Car body - Lamborghini yellow
    body_color = (255, 215, 0)  # Golden yellow
    highlight_color = (255, 235, 100)
    shadow_color = (200, 160, 0)
    
    # Main body shape - very low and sleek
    points = [
        (35, 15),   # Front nose
        (25, 20),   # Front left
        (45, 20),   # Front right
        (20, 30),   # Left front fender
        (50, 30),   # Right front fender
        (15, 50),   # Left door front
        (55, 50),   # Right door front
        (15, 90),   # Left door rear
        (55, 90),   # Right door rear
        (20, 110),  # Left rear fender
        (50, 110),  # Right rear fender
        (25, 125),  # Rear left
        (45, 125),  # Rear right
        (35, 130)   # Rear center
    ]
    pygame.draw.polygon(car_surface, body_color, points)
    
    # Add some details to make it look more like a Lamborghini
    
    # Hood lines - sharp angles
    pygame.draw.line(car_surface, shadow_color, (25, 20), (35, 15), 2)
    pygame.draw.line(car_surface, highlight_color, (35, 15), (45, 20), 2)
    
    # Side body lines - distinctive Lamborghini sharp edges
    pygame.draw.line(car_surface, shadow_color, (20, 30), (15, 90), 2)
    pygame.draw.line(car_surface, highlight_color, (50, 30), (55, 90), 2)
    pygame.draw.line(car_surface, shadow_color, (15, 90), (20, 110), 2)
    pygame.draw.line(car_surface, highlight_color, (55, 90), (50, 110), 2)
    
    # Windshield - angled
    pygame.draw.polygon(car_surface, (100, 200, 255), [(25, 25), (45, 25), (40, 40), (30, 40)])
    
    # Side windows - low profile
    pygame.draw.polygon(car_surface, (100, 200, 255), [(20, 45), (50, 45), (50, 60), (20, 60)])
    
    # Rear window
    pygame.draw.polygon(car_surface, (100, 200, 255), [(25, 100), (45, 100), (40, 115), (30, 115)])
    
    # Door line - distinctive Lamborghini door
    pygame.draw.line(car_surface, (0, 0, 0), (20, 60), (50, 60), 1)
    pygame.draw.line(car_surface, (0, 0, 0), (20, 70), (50, 70), 1)
    
    # Wheels - larger for sports car look with realistic rims
    wheel_color = (30, 30, 30)
    rim_color = (220, 220, 220)
    
    # Left front wheel
    pygame.draw.circle(car_surface, wheel_color, (12, 40), 10)
    pygame.draw.circle(car_surface, rim_color, (12, 40), 6)
    
    # Right front wheel
    pygame.draw.circle(car_surface, wheel_color, (58, 40), 10)
    pygame.draw.circle(car_surface, rim_color, (58, 40), 6)
    
    # Left rear wheel
    pygame.draw.circle(car_surface, wheel_color, (12, 100), 10)
    pygame.draw.circle(car_surface, rim_color, (12, 100), 6)
    
    # Right rear wheel
    pygame.draw.circle(car_surface, wheel_color, (58, 100), 10)
    pygame.draw.circle(car_surface, rim_color, (58, 100), 6)
    
    # Wheel details - spokes
    for wheel_x, wheel_y in [(12, 40), (58, 40), (12, 100), (58, 100)]:
        for i in range(0, 360, 45):
            rad = i * math.pi / 180
            x1 = wheel_x + 6 * math.cos(rad)
            y1 = wheel_y + 6 * math.sin(rad)
            x2 = wheel_x + 2 * math.cos(rad)
            y2 = wheel_y + 2 * math.sin(rad)
            pygame.draw.line(car_surface, wheel_color, (int(x1), int(y1)), (int(x2), int(y2)), 2)
    
    # Headlights - angular Lamborghini style
    pygame.draw.polygon(car_surface, (255, 255, 200), [(25, 20), (35, 15), (45, 20), (40, 25), (30, 25)])
    
    # Taillights - distinctive Lamborghini style
    pygame.draw.rect(car_surface, (255, 0, 0), (25, 120, 20, 5), border_radius=1)
    
    # Air intakes on sides - multiple
    pygame.draw.rect(car_surface, (20, 20, 20), (15, 70, 5, 15), border_radius=1)
    pygame.draw.rect(car_surface, (20, 20, 20), (50, 70, 5, 15), border_radius=1)
    pygame.draw.rect(car_surface, (20, 20, 20), (15, 50, 5, 10), border_radius=1)
    pygame.draw.rect(car_surface, (20, 20, 20), (50, 50, 5, 10), border_radius=1)
    
    # Front air intake - large
    pygame.draw.rect(car_surface, (20, 20, 20), (30, 20, 10, 5), border_radius=1)
    
    # Spoiler - large rear wing
    pygame.draw.polygon(car_surface, body_color, [(20, 115), (50, 115), (55, 125), (15, 125)])
    pygame.draw.line(car_surface, shadow_color, (20, 115), (15, 125), 2)
    pygame.draw.line(car_surface, highlight_color, (50, 115), (55, 125), 2)
    
    # Lamborghini logo (simplified)
    pygame.draw.circle(car_surface, (0, 0, 0), (35, 80), 4)
    pygame.draw.polygon(car_surface, (255, 215, 0), [(31, 80), (39, 80), (35, 76)])
    
    return car_surface