# Kids Car Racing Adventure

A simple and fun car racing game designed for children, built with Python and Pygame.

## Game Features

- Colorful, realistic-looking cars
- Simple controls using arrow keys
- Scrolling road with enhanced nature scenery and greenery
- 4 lives system with visual heart indicators
- Background music and sound effects
- Increasing difficulty as you progress

## How to Play

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   python run_game.py
   ```

3. Game Controls:
   - LEFT ARROW: Move car left
   - RIGHT ARROW: Move car right
   - SPACE: Restart game after game over
   - ESC: Quit game

## Game Objective

Avoid the oncoming cars for as long as possible to achieve a high score. You have 4 lives, and each collision with another car will cost you one life. As your score increases, the game will become more challenging with additional cars appearing on the road.

## Project Structure

- `run_game.py`: Main entry point to start the game
- `game.py`: Contains the main game logic and classes
- `generate_assets.py`: Generates the game images
- `sound_generator.py`: Generates the game sound effects
- `assets/`: Directory containing game resources
  - `images/`: Game images (cars, road, scenery)
  - `sounds/`: Game sound effects

## Technical Details

The game uses procedurally generated graphics and sound effects, making it lightweight and easy to run on most computers. The game automatically generates all required assets when first run.

Enjoy the game!