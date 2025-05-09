import os
import sys
import subprocess
import shutil

def check_pygbag():
    """Check if pygbag is installed, install if not"""
    try:
        import pygbag
        print("pygbag is already installed.")
    except ImportError:
        print("pygbag is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
        print("pygbag installed successfully.")

def build_game():
    """Build the game using pygbag"""
    print("Building game with pygbag...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pygbag
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pygbag", 
        "--build", 
        "--ume_block=0",
        os.path.join(current_dir, "web_wrapper.py")
    ])
    
    print("Game built successfully with pygbag!")
    
    # Copy the index.html to the build directory
    build_dir = os.path.join(current_dir, "build", "web")
    shutil.copy2(os.path.join(current_dir, "index.html"), build_dir)
    print("Copied custom index.html to build directory.")
    
    print(f"\nBuild completed! Files are in: {build_dir}")
    print("You can now deploy these files to a web server.")

if __name__ == "__main__":
    check_pygbag()
    build_game()