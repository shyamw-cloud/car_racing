import asyncio
import pygame
import sys
import os
import math

# Add this to make imports work in web context
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Global variables for analytics
total_plays = 0
current_players = 0

# Touch controls
touch_buttons = {
    'left': pygame.Rect(50, 500, 100, 80),
    'right': pygame.Rect(650, 500, 100, 80)
}

class WebGame:
    def __init__(self):
        global total_plays, current_players
        total_plays += 1
        current_players += 1
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Game window dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # Create game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Kids Car Racing Adventure")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.loading_progress = 0
        self.loading_complete = False
        self.assets_loaded = False
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_count = 2
        self.font = pygame.font.Font(None, 36)
        
        # Game objects
        self.player = None
        self.road = None
        self.scenery = None
        self.enemies = pygame.sprite.Group()
        self.heart_image = None
        
        # Sounds
        self.crash_sound = None
        self.point_sound = None
        self.life_lost_sound = None
        self.background_music = None
    
    def load_image(self, name, scale=1):
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

    def load_sound(self, name):
        try:
            sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', name))
            return sound
        except:
            print(f"Couldn't load sound: {name}")
            return None
    
    def load_assets(self):
        # Simulate progressive loading
        if self.loading_progress < 100:
            self.loading_progress += 2
            return False
        
        # Once loading reaches 100%, initialize the actual game
        if not self.assets_loaded:
            # Load images
            self.heart_image = self.load_image('heart.png', 1)
            
            # Initialize player
            self.player = Player(self)
            
            # Initialize road and scenery
            self.road = Road(self)
            self.scenery = Scenery(self)
            
            # Load sounds
            self.crash_sound = self.load_sound('crash.wav')
            self.point_sound = self.load_sound('point.wav')
            self.life_lost_sound = self.load_sound('life_lost.wav')
            self.background_music = self.load_sound('background_music.wav')
            
            # Play background music
            if self.background_music:
                self.background_music.play(-1)  # Loop indefinitely
            
            # Create initial enemies
            for _ in range(self.enemy_count):
                self.enemies.add(Enemy(self))
            
            self.assets_loaded = True
            self.loading_complete = True
        
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global current_players
                current_players -= 1
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_players -= 1
                    return False
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                    
            # Handle touch events for mobile
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if touch_buttons['left'].collidepoint(pos):
                    # Simulate left arrow key press
                    if self.player.rect.left > 150:
                        self.player.rect.x -= self.player.speed * 3
                elif touch_buttons['right'].collidepoint(pos):
                    # Simulate right arrow key press
                    if self.player.rect.right < self.SCREEN_WIDTH - 150:
                        self.player.rect.x += self.player.speed * 3
                    
                # Check if game over and touch anywhere to restart
                if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
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
                        enemy.rect.x = random.randint(150, self.SCREEN_WIDTH - 200)
                        enemy.rect.y = random.randint(-500, -100)
                    
            # Update score
            self.score += 1
            if self.score % 1000 == 0:
                if self.point_sound:
                    self.point_sound.play()
                self.level += 1
                if self.level % 2 == 0 and self.enemy_count < 4:  # Add a new enemy every 2 levels, max 4
                    self.enemy_count += 1
                    self.enemies.add(Enemy(self))
    
    def draw_loading_screen(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw loading bar
        bar_width = 400
        bar_height = 30
        bar_x = (self.SCREEN_WIDTH - bar_width) // 2
        bar_y = self.SCREEN_HEIGHT // 2
        
        # Outer rectangle
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # Inner progress rectangle
        progress_width = int(bar_width * (self.loading_progress / 100))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, progress_width, bar_height), border_radius=5)
        
        # Loading text
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        
        loading_text = self.font.render(f"Loading... {self.loading_progress}%", True, (0, 0, 0))
        text_rect = loading_text.get_rect(center=(self.SCREEN_WIDTH // 2, bar_y - 40))
        self.screen.blit(loading_text, text_rect)
        
        # Game title
        title_text = self.font.render("Kids Car Racing Adventure", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, bar_y - 100))
        self.screen.blit(title_text, title_rect)
        
        pygame.display.flip()
    
    def draw_touch_controls(self):
        # Draw left button
        pygame.draw.rect(self.screen, (200, 200, 200, 150), touch_buttons['left'], border_radius=10)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(80, 540), (60, 520), (60, 560)])
        
        # Draw right button
        pygame.draw.rect(self.screen, (200, 200, 200, 150), touch_buttons['right'], border_radius=10)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(720, 540), (740, 520), (740, 560)])
    
    def draw(self):
        # Fill background
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw scenery
        self.scenery.draw(self.screen)
        
        # Draw road
        self.road.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, self.BLACK)
        self.screen.blit(level_text, (10, 50))
        
        # Draw lives
        for i in range(self.player.lives):
            self.screen.blit(self.heart_image, (self.SCREEN_WIDTH - 40 - i * 35, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("Game Over! Tap to restart", True, self.RED)
            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2))
        
        # Add touch controls for mobile
        self.draw_touch_controls()
        
        # Draw player count
        players_text = self.font.render(f"Players Online: {current_players}", True, (0, 0, 0))
        self.screen.blit(players_text, (10, 90))
        
        total_plays_text = self.font.render(f"Total Plays: {total_plays}", True, (0, 0, 0))
        self.screen.blit(total_plays_text, (10, 120))
        
        pygame.display.flip()
    
    def reset_game(self):
        self.player = Player(self)
        self.enemies.empty()
        for _ in range(self.enemy_count):
            self.enemies.add(Enemy(self))
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_count = 2  # Reset to 2 cars
    
    def run(self):
        running = True
        while running:
            if not self.loading_complete:
                self.load_assets()
                self.draw_loading_screen()
                self.clock.tick(30)
                continue
                
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        # Stop music when game ends
        if self.background_music:
            self.background_music.stop()

# Game classes
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = game.load_image('lamborghini.png', 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = game.SCREEN_WIDTH // 2
        self.rect.bottom = game.SCREEN_HEIGHT - 20
        self.speed = 6  # Slightly faster for a Lamborghini
        self.score = 0
        self.lives = 4  # Player starts with 4 lives
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.game.SCREEN_WIDTH - 150:
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
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Randomly select one of the enemy car images
        car_images = ['enemy_car1.png', 'enemy_car2.png', 'enemy_car3.png']
        self.image = game.load_image(random.choice(car_images), 1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(150, game.SCREEN_WIDTH - 200)
        self.rect.y = random.randint(-500, -100)
        self.speed = random.randint(3, 7)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.game.SCREEN_HEIGHT:
            self.rect.x = random.randint(150, self.game.SCREEN_WIDTH - 200)
            self.rect.y = random.randint(-500, -100)
            self.speed = random.randint(3, 7)
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Road:
    def __init__(self, game):
        self.game = game
        self.image = game.load_image('road.png', 1)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.scroll_speed = 5
        
    def update(self):
        self.rect.y += self.scroll_speed
        if self.rect.y >= 0:
            self.rect.y = -self.rect.height + self.game.SCREEN_HEIGHT
            
    def draw(self, surface):
        surface.blit(self.image, (0, self.rect.y))
        surface.blit(self.image, (0, self.rect.y + self.rect.height))

class Scenery:
    def __init__(self, game):
        self.game = game
        # Load trees and bushes for enhanced greenery
        self.trees = [game.load_image('tree.png', 1) for _ in range(5)]
        self.bushes = [game.load_image('bush.png', 1) for _ in range(8)]
        
        # Position trees on both sides of the road
        self.tree_positions = [(random.randint(20, 100), random.randint(0, game.SCREEN_HEIGHT)) for _ in range(5)]
        self.tree_positions += [(random.randint(game.SCREEN_WIDTH - 120, game.SCREEN_WIDTH - 40), random.randint(0, game.SCREEN_HEIGHT)) for _ in range(5)]
        
        # Position bushes on both sides of the road
        self.bush_positions = [(random.randint(30, 120), random.randint(0, game.SCREEN_HEIGHT)) for _ in range(8)]
        self.bush_positions += [(random.randint(game.SCREEN_WIDTH - 140, game.SCREEN_WIDTH - 30), random.randint(0, game.SCREEN_HEIGHT)) for _ in range(8)]
        
        # Clouds in the sky
        self.clouds = [game.load_image('cloud.png', 1) for _ in range(3)]
        self.cloud_positions = [(random.randint(0, game.SCREEN_WIDTH), random.randint(0, 200)) for _ in range(3)]
        
        self.scroll_speed = 2
        
    def update(self):
        # Update tree positions
        for i in range(len(self.tree_positions)):
            x, y = self.tree_positions[i]
            y += self.scroll_speed
            if y > self.game.SCREEN_HEIGHT:
                if i < 5:  # Left side trees
                    y = -100
                    x = random.randint(20, 100)
                else:  # Right side trees
                    y = -100
                    x = random.randint(self.game.SCREEN_WIDTH - 120, self.game.SCREEN_WIDTH - 40)
            self.tree_positions[i] = (x, y)
        
        # Update bush positions
        for i in range(len(self.bush_positions)):
            x, y = self.bush_positions[i]
            y += self.scroll_speed
            if y > self.game.SCREEN_HEIGHT:
                if i < 8:  # Left side bushes
                    y = -50
                    x = random.randint(30, 120)
                else:  # Right side bushes
                    y = -50
                    x = random.randint(self.game.SCREEN_WIDTH - 140, self.game.SCREEN_WIDTH - 30)
            self.bush_positions[i] = (x, y)
            
        # Update cloud positions
        for i in range(len(self.cloud_positions)):
            x, y = self.cloud_positions[i]
            y += self.scroll_speed / 2  # Clouds move slower
            if y > self.game.SCREEN_HEIGHT:
                y = -100
                x = random.randint(0, self.game.SCREEN_WIDTH)
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

async def main():
    game = WebGame()
    game.run()

if __name__ == "__main__":
    asyncio.run(main())