import pygame
import random
import os
import sys
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kids Car Racing Adventure")
clock = pygame.time.Clock()

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(os.path.join('assets', 'images', name))
        image = pygame.transform.scale(image, 
                                      (int(image.get_width() * scale), 
                                       int(image.get_height() * scale)))
        return image
    except pygame.error as e:
        print(f"Couldn't load image: {name}")
        print(e)
        return pygame.Surface((50, 50))

# Load sounds
def load_sound(name):
    try:
        sound = mixer.Sound(os.path.join('assets', 'sounds', name))
        return sound
    except:
        print(f"Couldn't load sound: {name}")
        return None

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('lamborghini.png', 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 6  # Slightly faster for a Lamborghini
        self.score = 0
        self.lives = 4  # Player starts with 4 lives
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH - 150:
            self.rect.x += self.speed
            
        # Update invulnerability timer
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
            
    def draw(self, surface):
        # Make the car blink when invulnerable
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            return  # Skip drawing to create blinking effect
        surface.blit(self.image, self.rect)
        
    def make_invulnerable(self, duration=120):  # 2 seconds at 60 FPS
        self.invulnerable = True
        self.invulnerable_timer = duration

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly select one of the enemy car images
        car_images = ['enemy_car1.png', 'enemy_car2.png', 'enemy_car3.png']
        self.image = load_image(random.choice(car_images), 1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(150, SCREEN_WIDTH - 200)
        self.rect.y = random.randint(-500, -100)
        self.speed = random.randint(3, 7)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(150, SCREEN_WIDTH - 200)
            self.rect.y = random.randint(-500, -100)
            self.speed = random.randint(3, 7)
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Road:
    def __init__(self):
        self.image = load_image('road.png', 1)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.scroll_speed = 5
        
    def update(self):
        self.rect.y += self.scroll_speed
        if self.rect.y >= 0:
            self.rect.y = -self.rect.height + SCREEN_HEIGHT
            
    def draw(self, surface):
        surface.blit(self.image, (0, self.rect.y))
        surface.blit(self.image, (0, self.rect.y + self.rect.height))

class Scenery:
    def __init__(self):
        # Load trees and bushes for enhanced greenery
        self.trees = [load_image('tree.png', 1) for _ in range(5)]
        self.bushes = [load_image('bush.png', 1) for _ in range(8)]
        
        # Position trees on both sides of the road
        self.tree_positions = [(random.randint(20, 100), random.randint(0, SCREEN_HEIGHT)) for _ in range(5)]
        self.tree_positions += [(random.randint(SCREEN_WIDTH - 120, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT)) for _ in range(5)]
        
        # Position bushes on both sides of the road
        self.bush_positions = [(random.randint(30, 120), random.randint(0, SCREEN_HEIGHT)) for _ in range(8)]
        self.bush_positions += [(random.randint(SCREEN_WIDTH - 140, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT)) for _ in range(8)]
        
        # Clouds in the sky
        self.clouds = [load_image('cloud.png', 1) for _ in range(3)]
        self.cloud_positions = [(random.randint(0, SCREEN_WIDTH), random.randint(0, 200)) for _ in range(3)]
        
        self.scroll_speed = 2
        
    def update(self):
        # Update tree positions
        for i in range(len(self.tree_positions)):
            x, y = self.tree_positions[i]
            y += self.scroll_speed
            if y > SCREEN_HEIGHT:
                if i < 5:  # Left side trees
                    y = -100
                    x = random.randint(20, 100)
                else:  # Right side trees
                    y = -100
                    x = random.randint(SCREEN_WIDTH - 120, SCREEN_WIDTH - 40)
            self.tree_positions[i] = (x, y)
        
        # Update bush positions
        for i in range(len(self.bush_positions)):
            x, y = self.bush_positions[i]
            y += self.scroll_speed
            if y > SCREEN_HEIGHT:
                if i < 8:  # Left side bushes
                    y = -50
                    x = random.randint(30, 120)
                else:  # Right side bushes
                    y = -50
                    x = random.randint(SCREEN_WIDTH - 140, SCREEN_WIDTH - 30)
            self.bush_positions[i] = (x, y)
            
        # Update cloud positions
        for i in range(len(self.cloud_positions)):
            x, y = self.cloud_positions[i]
            y += self.scroll_speed / 2  # Clouds move slower
            if y > SCREEN_HEIGHT:
                y = -100
                x = random.randint(0, SCREEN_WIDTH)
            self.cloud_positions[i] = (x, y)
            
    def draw(self, surface):
        # Draw clouds
        for i, cloud in enumerate(self.clouds):
            surface.blit(cloud, self.cloud_positions[i])
            
        # Draw trees
        for i, tree in enumerate(self.trees):
            surface.blit(tree, self.tree_positions[i])
            
        # Draw bushes
        for i, bush in enumerate(self.bushes):
            surface.blit(bush, self.bush_positions[i])

class Game:
    def __init__(self):
        self.player = Player()
        self.road = Road()
        self.scenery = Scenery()
        self.enemies = pygame.sprite.Group()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_count = 2  # Reduced to 2 cars initially
        self.heart_image = load_image('heart.png', 1)
        
        # Load sounds
        self.crash_sound = load_sound('crash.wav')
        self.point_sound = load_sound('point.wav')
        self.life_lost_sound = load_sound('life_lost.wav')
        
        # Load and play background music
        self.background_music = load_sound('background_music.wav')
        if self.background_music:
            self.background_music.play(-1)  # Loop indefinitely
        
        # Create initial enemies
        for _ in range(self.enemy_count):
            self.enemies.add(Enemy())
            
        # Font for text
        self.font = pygame.font.Font(None, 36)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True
    
    def update(self):
        if not self.game_over:
            self.player.update()
            self.road.update()
            self.scenery.update()
            self.enemies.update()
            
            # Check for collisions
            if not self.player.invulnerable:
                for enemy in self.enemies:
                    if pygame.sprite.collide_rect(self.player, enemy):
                        self.player.lives -= 1
                        
                        # Play appropriate sound
                        if self.player.lives <= 0:
                            if self.crash_sound:
                                self.crash_sound.play()
                            self.game_over = True
                        else:
                            if self.life_lost_sound:
                                self.life_lost_sound.play()
                            self.player.make_invulnerable()
                            
                        # Reset enemy position
                        enemy.rect.x = random.randint(150, SCREEN_WIDTH - 200)
                        enemy.rect.y = random.randint(-500, -100)
                    
            # Update score
            self.score += 1
            if self.score % 1000 == 0:
                if self.point_sound:
                    self.point_sound.play()
                self.level += 1
                if self.level % 2 == 0 and self.enemy_count < 4:  # Add a new enemy every 2 levels, max 4
                    self.enemy_count += 1
                    self.enemies.add(Enemy())
    
    def draw(self):
        # Fill background
        screen.fill((135, 206, 235))  # Sky blue
        
        # Draw scenery
        self.scenery.draw(screen)
        
        # Draw road
        self.road.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        screen.blit(level_text, (10, 50))
        
        # Draw lives
        for i in range(self.player.lives):
            screen.blit(self.heart_image, (SCREEN_WIDTH - 40 - i * 35, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press SPACE to restart", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            
        pygame.display.flip()
        
    def reset_game(self):
        self.player = Player()
        self.enemies.empty()
        for _ in range(self.enemy_count):
            self.enemies.add(Enemy())
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_count = 2  # Reset to 2 cars
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        # Stop music when game ends
        if self.background_music:
            self.background_music.stop()
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()