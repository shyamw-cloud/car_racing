import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("Building web version of the game...")
    
    # Make sure pygbag is installed
    try:
        import pygbag
        print("pygbag is installed.")
    except ImportError:
        print("Installing pygbag...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
        print("pygbag installed successfully.")
    
    # Run pygbag with build option only (don't start server yet)
    print("Building game with pygbag...")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pygbag", 
            "--build",
            "web_main.py"
        ])
        print("Game built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error building game: {e}")
        return
    
    # Check if build directory exists
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")
    if not os.path.exists(build_dir):
        print(f"Error: Build directory not found at {build_dir}")
        return
    
    # Start a local server
    print(f"Starting local server at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    # Change to the build directory
    os.chdir(build_dir)
    
    # Open browser
    webbrowser.open("http://localhost:8000")
    
    # Start server
    try:
        subprocess.run([sys.executable, "-m", "http.server", "8000"])
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    main()
