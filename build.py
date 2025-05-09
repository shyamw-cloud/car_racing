import os
import sys
import shutil
import subprocess
import zipfile
import glob
from PIL import Image
import io

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def optimize_image(input_path, output_path, quality=85):
    """Optimize an image file"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if RGBA (remove alpha channel)
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
                img = background
            
            # Save with optimization
            img.save(output_path, optimize=True, quality=quality)
        
        original_size = os.path.getsize(input_path)
        optimized_size = os.path.getsize(output_path)
        savings = original_size - optimized_size
        
        print(f"Optimized {input_path}: {original_size/1024:.1f}KB → {optimized_size/1024:.1f}KB (saved {savings/1024:.1f}KB)")
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")
        # If optimization fails, just copy the original
        shutil.copy2(input_path, output_path)

def optimize_images(source_dir, target_dir):
    """Optimize all images in a directory"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                source_path = os.path.join(root, file)
                # Create the same directory structure in target_dir
                rel_path = os.path.relpath(root, source_dir)
                target_subdir = os.path.join(target_dir, rel_path)
                create_directory(target_subdir)
                
                target_path = os.path.join(target_subdir, file)
                optimize_image(source_path, target_path)

def copy_non_image_files(source_dir, target_dir):
    """Copy all non-image files to target directory"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not any(file.lower().endswith(ext) for ext in image_extensions):
                source_path = os.path.join(root, file)
                # Create the same directory structure in target_dir
                rel_path = os.path.relpath(root, source_dir)
                target_subdir = os.path.join(target_dir, rel_path)
                create_directory(target_subdir)
                
                target_path = os.path.join(target_subdir, file)
                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} → {target_path}")

def create_netlify_config(build_dir):
    """Create netlify.toml configuration file"""
    config_content = """
[build]
  publish = "."
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    with open(os.path.join(build_dir, "netlify.toml"), "w") as f:
        f.write(config_content.strip())
    print("Created netlify.toml configuration file")

def create_vercel_config(build_dir):
    """Create vercel.json configuration file"""
    config_content = """
{
  "version": 2,
  "builds": [
    { "src": "**/*", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/" }
  ]
}
"""
    with open(os.path.join(build_dir, "vercel.json"), "w") as f:
        f.write(config_content.strip())
    print("Created vercel.json configuration file")

def create_github_workflow(repo_dir):
    """Create GitHub Actions workflow for GitHub Pages"""
    workflow_dir = os.path.join(repo_dir, ".github", "workflows")
    create_directory(workflow_dir)
    
    workflow_content = """
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@4.1.4
        with:
          branch: gh-pages
          folder: build/web
"""
    with open(os.path.join(workflow_dir, "deploy.yml"), "w") as f:
        f.write(workflow_content.strip())
    print("Created GitHub Actions workflow for GitHub Pages")

def main():
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(base_dir, "build", "web")
    assets_dir = os.path.join(base_dir, "assets")
    optimized_assets_dir = os.path.join(build_dir, "assets")
    
    # Create build directory
    create_directory(build_dir)
    create_directory(optimized_assets_dir)
    
    # Copy and optimize assets
    print("Optimizing and copying assets...")
    optimize_images(assets_dir, optimized_assets_dir)
    copy_non_image_files(assets_dir, optimized_assets_dir)
    
    # Copy main HTML and other files
    print("Copying main files...")
    shutil.copy2(os.path.join(base_dir, "index.html"), build_dir)
    
    # Create platform-specific configuration files
    create_netlify_config(build_dir)
    create_vercel_config(build_dir)
    create_github_workflow(base_dir)
    
    # Create a zip file for easy upload
    print("Creating deployment zip file...")
    with zipfile.ZipFile(os.path.join(base_dir, "car_racing_game_web.zip"), 'w') as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arcname)
    
    print("\nBuild completed successfully!")
    print(f"Web files are in: {build_dir}")
    print(f"Deployment zip: {os.path.join(base_dir, 'car_racing_game_web.zip')}")
    print("\nDeployment options:")
    print("1. GitHub Pages: Push the repository to GitHub and enable GitHub Pages")
    print("2. Netlify: Upload the zip file or connect to your GitHub repository")
    print("3. Vercel: Upload the zip file or connect to your GitHub repository")

if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        print("PIL/Pillow is required for image optimization.")
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image
    
    main()