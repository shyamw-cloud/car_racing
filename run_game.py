import os
import sys
import pygame

# Check if assets exist, if not generate them
if not os.path.exists(os.path.join('assets', 'images', 'player_car.png')):
    print("Generating game assets...")
    try:
        import generate_assets
    except ImportError as e:
        print(f"Error importing generate_assets: {e}")
        sys.exit(1)

# Check if sounds exist, if not generate them
if not os.path.exists(os.path.join('assets', 'sounds', 'crash.wav')):
    print("Generating sound effects...")
    try:
        import sound_generator
        sound_generator.generate_sounds()
    except ImportError as e:
        print(f"Error importing sound_generator: {e}")
        sys.exit(1)

# Import and run the game
try:
    from game import Game
    
    print("Starting Kids Car Racing Adventure...")
    print("Use LEFT and RIGHT arrow keys to control your car.")
    print("Avoid the other cars to score points!")
    print("Press ESC to quit the game.")
    
    game = Game()
    game.run()
except ImportError as e:
    print(f"Error importing game: {e}")
    sys.exit(1)