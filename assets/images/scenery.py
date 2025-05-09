import pygame
import random

def create_road():
    """
    Creates a road image with lane markings and enhanced greenery
    """
    road_width = 800
    road_height = 800
    
    road_surface = pygame.Surface((road_width, road_height))
    
    # Green background for grass
    road_surface.fill((34, 139, 34))  # Forest green for grass
    
    # Gray road in the middle
    pygame.draw.rect(road_surface, (100, 100, 100), (150, 0, road_width - 300, road_height))
    
    # Road edges
    pygame.draw.rect(road_surface, (255, 255, 255), (150, 0, 5, road_height))  # Left edge
    pygame.draw.rect(road_surface, (255, 255, 255), (road_width - 155, 0, 5, road_height))  # Right edge
    
    # Lane markings
    lane_mark_length = 50
    gap_length = 30
    total_length = lane_mark_length + gap_length
    
    for y in range(0, road_height, total_length):
        pygame.draw.rect(road_surface, (255, 255, 255), (road_width // 2 - 5, y, 10, lane_mark_length))
    
    # Add random small details to the grass (flowers, rocks, etc.)
    for _ in range(100):
        # Left side details
        x = random.randint(10, 140)
        y = random.randint(0, road_height)
        size = random.randint(2, 5)
        color = random.choice([
            (255, 255, 0),    # Yellow flowers
            (255, 0, 255),    # Purple flowers
            (255, 255, 255),  # White flowers
            (255, 0, 0),      # Red flowers
            (139, 69, 19)     # Brown rocks
        ])
        pygame.draw.circle(road_surface, color, (x, y), size)
        
        # Right side details
        x = random.randint(road_width - 140, road_width - 10)
        y = random.randint(0, road_height)
        size = random.randint(2, 5)
        color = random.choice([
            (255, 255, 0),    # Yellow flowers
            (255, 0, 255),    # Purple flowers
            (255, 255, 255),  # White flowers
            (255, 0, 0),      # Red flowers
            (139, 69, 19)     # Brown rocks
        ])
        pygame.draw.circle(road_surface, color, (x, y), size)
    
    # Add some grass texture (lines)
    for _ in range(200):
        # Left side grass lines
        x = random.randint(0, 145)
        y = random.randint(0, road_height)
        length = random.randint(3, 8)
        pygame.draw.line(road_surface, (0, 100, 0), (x, y), (x, y + length), 1)
        
        # Right side grass lines
        x = random.randint(road_width - 145, road_width)
        y = random.randint(0, road_height)
        length = random.randint(3, 8)
        pygame.draw.line(road_surface, (0, 100, 0), (x, y), (x, y + length), 1)
    
    return road_surface

def create_tree():
    """
    Creates a simple tree image
    """
    tree_surface = pygame.Surface((100, 150), pygame.SRCALPHA)
    
    # Tree trunk
    pygame.draw.rect(tree_surface, (139, 69, 19), (40, 80, 20, 70))  # Brown trunk
    
    # Tree leaves
    pygame.draw.circle(tree_surface, (34, 139, 34), (50, 60), 40)  # Green leaves
    pygame.draw.circle(tree_surface, (34, 139, 34), (30, 40), 30)
    pygame.draw.circle(tree_surface, (34, 139, 34), (70, 40), 30)
    
    return tree_surface

def create_bush():
    """
    Creates a simple bush image
    """
    bush_surface = pygame.Surface((60, 40), pygame.SRCALPHA)
    
    # Bush leaves
    pygame.draw.circle(bush_surface, (34, 139, 34), (30, 20), 20)  # Green leaves
    pygame.draw.circle(bush_surface, (34, 139, 34), (15, 20), 15)
    pygame.draw.circle(bush_surface, (34, 139, 34), (45, 20), 15)
    
    # Add some flowers to the bush
    for _ in range(5):
        x = random.randint(10, 50)
        y = random.randint(5, 35)
        size = random.randint(2, 4)
        color = random.choice([(255, 0, 0), (255, 255, 0), (255, 0, 255)])  # Red, yellow, purple flowers
        pygame.draw.circle(bush_surface, color, (x, y), size)
    
    return bush_surface

def create_cloud():
    """
    Creates a simple cloud image
    """
    cloud_surface = pygame.Surface((150, 80), pygame.SRCALPHA)
    
    # Cloud puffs
    pygame.draw.circle(cloud_surface, (255, 255, 255), (50, 40), 30)
    pygame.draw.circle(cloud_surface, (255, 255, 255), (80, 30), 35)
    pygame.draw.circle(cloud_surface, (255, 255, 255), (110, 40), 30)
    pygame.draw.circle(cloud_surface, (255, 255, 255), (70, 50), 25)
    
    return cloud_surface