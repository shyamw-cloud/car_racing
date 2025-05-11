import os
import sys
import subprocess
import json
import shutil
import webbrowser
import time

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check for Node.js
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True).strip()
        print(f"✓ Node.js {node_version} is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("✗ Node.js is not installed. Please install Node.js from https://nodejs.org/")
        return False
    
    # Check for Vercel CLI
    try:
        vercel_version = subprocess.check_output(["vercel", "--version"], text=True).strip()
        print(f"✓ Vercel CLI {vercel_version} is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("✗ Vercel CLI is not installed. Installing now...")
        try:
            subprocess.check_call(["npm", "install", "-g", "vercel"])
            print("✓ Vercel CLI installed successfully")
        except subprocess.SubprocessError:
            print("✗ Failed to install Vercel CLI. Please install manually with: npm install -g vercel")
            return False
    
    # Check for pygbag
    try:
        import pygbag
        print("✓ pygbag is installed")
    except ImportError:
        print("✗ pygbag is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
            print("✓ pygbag installed successfully")
        except subprocess.SubprocessError:
            print("✗ Failed to install pygbag. Please install manually with: pip install pygbag")
            return False
    
    return True

def build_game():
    """Build the game for web deployment"""
    print("\nBuilding game for web deployment...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run the build script
    try:
        subprocess.check_call([sys.executable, os.path.join(current_dir, "build_and_run.py")])
        return True
    except subprocess.SubprocessError:
        print("✗ Failed to build the game")
        return False

def create_vercel_config():
    """Create vercel.json configuration file"""
    print("\nCreating Vercel configuration...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Create vercel.json
    vercel_config = {
        "version": 2,
        "builds": [
            {"src": "**/*", "use": "@vercel/static"}
        ],
        "routes": [
            {"src": "/(.*)", "dest": "/"}
        ]
    }
    
    # Write the configuration file
    with open(os.path.join(build_dir, "vercel.json"), "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✓ Created vercel.json configuration file")
    return True

def deploy_to_vercel():
    """Deploy the game to Vercel"""
    print("\nDeploying to Vercel...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Check if build directory exists
    if not os.path.exists(build_dir):
        print("✗ Build directory not found. Please build the game first.")
        return False
    
    # Change to the build directory
    os.chdir(build_dir)
    
    # Deploy to Vercel
    try:
        # Run vercel command
        print("\nStarting Vercel deployment...")
        print("Follow the prompts to complete deployment.")
        print("If this is your first time, you'll need to log in and configure your project.")
        print("\nRecommended settings:")
        print("- Set up and deploy: Yes")
        print("- Link to existing project: No (unless you've deployed this before)")
        print("- Project name: car-racing-game (or any name you prefer)")
        print("- Directory: . (current directory)")
        print("\nPress Enter to continue...")
        input()
        
        # Run the vercel command
        result = subprocess.run(["vercel"], text=True, capture_output=True)
        
        # Check for deployment URL in the output
        output_lines = result.stdout.split('\n')
        deployment_url = None
        
        for line in output_lines:
            if "https://" in line and "vercel.app" in line:
                deployment_url = line.strip()
                break
        
        if deployment_url:
            print(f"\n✓ Deployment successful! Your game is now available at:")
            print(f"  {deployment_url}")
            
            # Ask if user wants to open the URL
            response = input("\nDo you want to open the game in your browser? (y/n): ")
            if response.lower() == 'y':
                webbrowser.open(deployment_url)
        else:
            print("\nDeployment completed, but couldn't find the URL in the output.")
            print("Please check your Vercel dashboard for the deployment URL.")
        
        return True
    except subprocess.SubprocessError as e:
        print(f"✗ Deployment failed: {e}")
        return False

def main():
    print("===== Vercel Deployment Tool for Kids Car Racing Adventure =====")
    
    # Check requirements
    if not check_requirements():
        print("\nPlease install the required tools and try again.")
        return
    
    # Ask if user wants to build the game
    response = input("\nDo you want to build the game before deployment? (y/n): ")
    if response.lower() == 'y':
        if not build_game():
            print("\nGame build failed. Please fix the issues and try again.")
            return
    
    # Create Vercel configuration
    create_vercel_config()
    
    # Deploy to Vercel
    deploy_to_vercel()
    
    print("\n===== Next Steps =====")
    print("1. Test your game thoroughly on different devices")
    print("2. Share your game URL with friends and family")
    print("3. To make updates, rebuild the game and deploy again")
    
    print("\nFor more information on managing your Vercel deployment, visit:")
    print("https://vercel.com/dashboard")

if __name__ == "__main__":
    main()