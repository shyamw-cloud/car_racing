import os
import sys
import subprocess
import shutil
import webbrowser
import time

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check for Node.js
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True).strip()
        print(f"Node.js {node_version} is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Node.js is not installed. Please install Node.js from https://nodejs.org/")
        return False
    
    # Check for Vercel CLI
    try:
        vercel_version = subprocess.check_output(["vercel", "--version"], text=True).strip()
        print(f"Vercel CLI {vercel_version} is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Vercel CLI is not installed. Installing now...")
        try:
            subprocess.check_call(["npm", "install", "-g", "vercel"])
            print("Vercel CLI installed successfully")
        except subprocess.SubprocessError:
            print("Failed to install Vercel CLI. Please install manually with: npm install -g vercel")
            return False
    
    return True

def deploy_to_vercel():
    """Deploy the game to Vercel"""
    print("\nDeploying to Vercel...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Check if build directory exists
    if not os.path.exists(build_dir):
        print("Build directory not found. Running simple_web_game.py first...")
        try:
            subprocess.check_call([sys.executable, "simple_web_game.py"])
        except subprocess.SubprocessError:
            print("Failed to create build directory. Please run simple_web_game.py manually.")
            return False
    
    # Change to the build directory
    os.chdir(build_dir)
    
    # Deploy to Vercel
    try:
        # Run vercel command
        print("\nStarting Vercel deployment...")
        print("Follow the prompts to complete deployment.")
        print("\nRecommended settings:")
        print("- Set up and deploy: Yes")
        print("- Link to existing project: No (unless you've deployed this before)")
        print("- Project name: car-racing-game (or any name you prefer)")
        print("- Directory: . (current directory)")
        
        # Run the vercel command
        subprocess.run(["vercel"])
        
        print("\nDeployment completed!")
        print("Your game should now be available at the URL provided by Vercel.")
        return True
    except subprocess.SubprocessError as e:
        print(f"Deployment failed: {e}")
        return False

def main():
    print("===== Car Racing Game Vercel Deployment =====")
    
    # Check requirements
    if not check_requirements():
        print("\nPlease install the required tools and try again.")
        return
    
    # Deploy to Vercel
    deploy_to_vercel()

if __name__ == "__main__":
    main()