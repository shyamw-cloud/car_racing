import asyncio
import pygame
import sys
import os

# Add this to make imports work in web context
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Global variables for analytics
total_plays = 0
current_players = 0

# Import your game
from game import Game

class WebGame(Game):
    def __init__(self):
        super().__init__()
        global total_plays, current_players
        total_plays += 1
        current_players += 1
        self.loading_progress = 0
        self.loading_complete = False
        self.assets_loaded = False
        self.font = None
        self.touch_buttons = {
            'left': pygame.Rect(50, 500, 100, 80),
            'right': pygame.Rect(650, 500, 100, 80)
        }
        
    def load_assets(self):
        # Simulate progressive loading
        if self.loading_progress < 100:
            self.loading_progress += 2
            return False
        
        # Once loading reaches 100%, initialize the actual game
        if not self.assets_loaded:
            super().__init__()  # Initialize the actual game
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
                if self.touch_buttons['left'].collidepoint(pos):
                    # Simulate left arrow key press
                    self.player.rect.x -= self.player.speed * 3
                elif self.touch_buttons['right'].collidepoint(pos):
                    # Simulate right arrow key press
                    self.player.rect.x += self.player.speed * 3
                    
                # Check if game over and touch anywhere to restart
                if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                    
        return True
        
    def draw_loading_screen(self):
        screen = pygame.display.get_surface()
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw loading bar
        bar_width = 400
        bar_height = 30
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() // 2
        
        # Outer rectangle
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # Inner progress rectangle
        progress_width = int(bar_width * (self.loading_progress / 100))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, progress_width, bar_height), border_radius=5)
        
        # Loading text
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        
        loading_text = self.font.render(f"Loading... {self.loading_progress}%", True, (0, 0, 0))
        text_rect = loading_text.get_rect(center=(screen.get_width() // 2, bar_y - 40))
        screen.blit(loading_text, text_rect)
        
        # Game title
        title_text = self.font.render("Kids Car Racing Adventure", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, bar_y - 100))
        screen.blit(title_text, title_rect)
        
        pygame.display.flip()
        
    def draw_touch_controls(self):
        screen = pygame.display.get_surface()
        
        # Draw left button
        pygame.draw.rect(screen, (200, 200, 200, 150), self.touch_buttons['left'], border_radius=10)
        pygame.draw.polygon(screen, (0, 0, 0), [(80, 540), (60, 520), (60, 560)])
        
        # Draw right button
        pygame.draw.rect(screen, (200, 200, 200, 150), self.touch_buttons['right'], border_radius=10)
        pygame.draw.polygon(screen, (0, 0, 0), [(720, 540), (740, 520), (740, 560)])
        
    def draw(self):
        super().draw()
        
        # Add touch controls for mobile
        self.draw_touch_controls()
        
        # Draw player count
        screen = pygame.display.get_surface()
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            
        players_text = self.font.render(f"Players Online: {current_players}", True, (0, 0, 0))
        screen.blit(players_text, (10, 90))
        
        total_plays_text = self.font.render(f"Total Plays: {total_plays}", True, (0, 0, 0))
        screen.blit(total_plays_text, (10, 120))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            if not self.loading_complete:
                self.load_assets()
                self.draw_loading_screen()
                clock.tick(30)
                continue
                
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        # Stop music when game ends
        if self.background_music:
            self.background_music.stop()
            
        # Don't quit pygame in web context
        if not pygame.get_init():
            pygame.quit()
            sys.exit()

async def main():
    pygame.init()
    pygame.display.set_mode((800, 600))
    game = WebGame()
    game.run()

if __name__ == "__main__":
    asyncio.run(main())