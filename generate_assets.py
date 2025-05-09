import pygame
import os
from assets.images.player_car import create_player_car, create_lamborghini_car
from assets.images.enemy_cars import create_enemy_car
from assets.images.scenery import create_road, create_tree, create_cloud, create_bush

# Initialize pygame
pygame.init()

# Create directories if they don't exist
os.makedirs(os.path.join('assets', 'images'), exist_ok=True)
os.makedirs(os.path.join('assets', 'sounds'), exist_ok=True)

# Generate and save player car
player_car = create_player_car()
pygame.image.save(player_car, os.path.join('assets', 'images', 'player_car.png'))

# Generate and save Lamborghini car
lamborghini = create_lamborghini_car()
pygame.image.save(lamborghini, os.path.join('assets', 'images', 'lamborghini.png'))

# Generate and save enemy cars
enemy_car1 = create_enemy_car((0, 0, 255))  # Blue
pygame.image.save(enemy_car1, os.path.join('assets', 'images', 'enemy_car1.png'))

enemy_car2 = create_enemy_car((0, 255, 0))  # Green
pygame.image.save(enemy_car2, os.path.join('assets', 'images', 'enemy_car2.png'))

enemy_car3 = create_enemy_car((255, 165, 0))  # Orange
pygame.image.save(enemy_car3, os.path.join('assets', 'images', 'enemy_car3.png'))

# Generate and save road
road = create_road()
pygame.image.save(road, os.path.join('assets', 'images', 'road.png'))

# Generate and save tree
tree = create_tree()
pygame.image.save(tree, os.path.join('assets', 'images', 'tree.png'))

# Generate and save bush
bush = create_bush()
pygame.image.save(bush, os.path.join('assets', 'images', 'bush.png'))

# Generate and save cloud
cloud = create_cloud()
pygame.image.save(cloud, os.path.join('assets', 'images', 'cloud.png'))

# Generate and save heart (for lives)
heart_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
# Draw a heart shape
pygame.draw.polygon(heart_surface, (255, 0, 0), [
    (15, 27),  # Bottom point
    (5, 15),   # Left middle
    (0, 8),    # Left top
    (7, 0),    # Left curve
    (15, 7),   # Middle top
    (23, 0),   # Right curve
    (30, 8),   # Right top
    (25, 15)   # Right middle
])
pygame.image.save(heart_surface, os.path.join('assets', 'images', 'heart.png'))

print("All game assets have been generated successfully!")