import os
import sys
import subprocess
import shutil
import webbrowser
import time
import platform

def check_requirements():
    """Check if required packages are installed, install if not"""
    required_packages = ['pygbag', 'pillow']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"+ {package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"+ {package} installed successfully.")

def build_game():
    """Build the game using pygbag"""
    print("\n=== Building game with pygbag ===")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pygbag
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pygbag", 
            "--build",
            "--ume_block=0",
            os.path.join(current_dir, "main.py")
        ])
        print("+ Game built successfully with pygbag!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building game: {e}")
        return False

def optimize_images():
    """Optimize images for web deployment"""
    print("\n=== Optimizing images ===")
    try:
        from PIL import Image
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets", "images")
        build_assets_dir = os.path.join(current_dir, "build", "web", "assets", "images")
        
        # Create directory if it doesn't exist
        os.makedirs(build_assets_dir, exist_ok=True)
        
        # Optimize each image
        for filename in os.listdir(assets_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                input_path = os.path.join(assets_dir, filename)
                output_path = os.path.join(build_assets_dir, filename)
                
                try:
                    with Image.open(input_path) as img:
                        # Resize if too large
                        max_size = (800, 600)
                        if img.width > max_size[0] or img.height > max_size[1]:
                            img.thumbnail(max_size, Image.LANCZOS)
                        
                        # Save with optimization
                        img.save(output_path, optimize=True, quality=85)
                    
                    original_size = os.path.getsize(input_path)
                    optimized_size = os.path.getsize(output_path)
                    savings = original_size - optimized_size
                    
                    print(f"Optimized {filename}: {original_size/1024:.1f}KB -> {optimized_size/1024:.1f}KB (saved {savings/1024:.1f}KB)")
                except Exception as e:
                    print(f"Error optimizing {filename}: {e}")
                    # If optimization fails, just copy the original
                    shutil.copy2(input_path, output_path)
        
        print("+ Images optimized successfully!")
        return True
    except ImportError:
        print("Pillow is not installed. Skipping image optimization.")
        return False
    except Exception as e:
        print(f"Error during image optimization: {e}")
        return False

def copy_html_files():
    """Copy custom HTML and other files to the build directory"""
    print("\n=== Copying custom files ===")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Copy index.html
    try:
        shutil.copy2(os.path.join(current_dir, "index.html"), build_dir)
        print("+ Copied index.html to build directory")
    except Exception as e:
        print(f"Error copying index.html: {e}")
    
    # Copy privacy_policy.html
    try:
        shutil.copy2(os.path.join(current_dir, "privacy_policy.html"), build_dir)
        print("+ Copied privacy_policy.html to build directory")
    except Exception as e:
        print(f"Error copying privacy_policy.html: {e}")
    
    # Create assets directories if they don't exist
    os.makedirs(os.path.join(build_dir, "assets", "sounds"), exist_ok=True)
    
    # Copy sound files
    sounds_dir = os.path.join(current_dir, "assets", "sounds")
    build_sounds_dir = os.path.join(build_dir, "assets", "sounds")
    
    if os.path.exists(sounds_dir):
        for filename in os.listdir(sounds_dir):
            if filename.lower().endswith(('.wav', '.mp3', '.ogg')):
                try:
                    shutil.copy2(os.path.join(sounds_dir, filename), build_sounds_dir)
                    print(f"+ Copied sound file: {filename}")
                except Exception as e:
                    print(f"Error copying sound file {filename}: {e}")

def start_local_server():
    """Start a local web server to test the game"""
    print("\n=== Starting local web server ===")
    
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
    print("===== Kids Car Racing Adventure - Web Build Tool =====")
    
    # Check requirements
    check_requirements()
    
    # Build the game
    if not build_game():
        print("Failed to build the game. Exiting.")
        return
    
    # Optimize images
    optimize_images()
    
    # Copy HTML and other files
    copy_html_files()
    
    print("\n===== Build completed successfully! =====")
    print(f"Web files are in: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'web')}")
    
    # Ask if user wants to start a local server
    response = input("\nDo you want to start a local server to test the game? (y/n): ")
    if response.lower() == 'y':
        start_local_server()
    else:
        print("\nTo test the game later, run:")
        print("python -m http.server 8000")
        print("And open http://localhost:8000 in your browser")
    
    print("\n===== Deployment Options =====")
    print("1. GitHub Pages: Push the repository to GitHub and enable GitHub Pages")
    print("2. Netlify: Upload the build/web folder or connect to your GitHub repository")
    print("3. Vercel: Upload the build/web folder or connect to your GitHub repository")
    
    print("\nFor step-by-step deployment instructions, see README_DEPLOYMENT.md")

if __name__ == "__main__":
    main()