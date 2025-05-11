import os
import sys
import subprocess
import shutil
import webbrowser
import time

def check_requirements():
    """Check if required packages are installed, install if not"""
    print("Checking requirements...")
    
    try:
        import pygbag
        print("✓ pygbag is already installed")
    except ImportError:
        print("Installing pygbag...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
        print("✓ pygbag installed successfully")

def build_game():
    """Build the game using pygbag"""
    print("\nBuilding game with pygbag...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pygbag with the simplified main file
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pygbag",
            "--app", "main:app",
            os.path.join(current_dir, "web_main.py")
        ])
        print("\n✓ Game built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building game: {e}")
        return False

def start_local_server():
    """Start a local web server to test the game"""
    print("\nStarting local web server...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Check if build directory exists
    if not os.path.exists(build_dir):
        print("Error: Build directory not found. Please build the game first.")
        return False
    
    # Change to the build directory
    os.chdir(build_dir)
    
    # Determine an available port
    port = 8000
    
    print(f"Starting server at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{port}")
    
    # Start the server
    try:
        # Use the http.server module
        server_command = [sys.executable, "-m", "http.server", str(port)]
        subprocess.run(server_command)
        return True
    except KeyboardInterrupt:
        print("\nServer stopped")
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

def main():
    print("===== Simple Car Racing Game Deployment =====")
    
    # Check requirements
    check_requirements()
    
    # Build the game
    if not build_game():
        print("Failed to build the game. Exiting.")
        return
    
    # Ask if user wants to start a local server
    response = input("\nDo you want to start a local server to test the game? (y/n): ")
    if response.lower() == 'y':
        start_local_server()
    else:
        print("\nTo test the game later, run:")
        print("cd build/web")
        print("python -m http.server 8000")
        print("And open http://localhost:8000 in your browser")
    
    print("\n===== Deployment Instructions =====")
    print("To deploy to Vercel:")
    print("1. Install Node.js from https://nodejs.org/")
    print("2. Install Vercel CLI: npm install -g vercel")
    print("3. Navigate to the build directory: cd build/web")
    print("4. Deploy: vercel")
    print("5. Follow the prompts to complete deployment")

if __name__ == "__main__":
    main()