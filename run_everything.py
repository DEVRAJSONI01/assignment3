#!/usr/bin/env python3
"""
One-click pothole detection runner
This script does everything automatically - just run it!
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_images():
    """Check if there are images to process"""
    input_folder = Path("input_images")
    extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    image_files = []
    for ext in extensions:
        image_files.extend(input_folder.glob(f'*{ext}'))
        image_files.extend(input_folder.glob(f'*{ext.upper()}'))
    
    return len(image_files) > 0, len(image_files)

def main():
    print("🎯 ONE-CLICK POTHOLE DETECTION SYSTEM")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing required packages"):
        return
    
    # Step 2: Check for images
    has_images, num_images = check_images()
    
    if not has_images:
        print("\\n📷 No images found in 'input_images' folder.")
        print("Creating sample images for demonstration...")
        
        if run_command(f"{sys.executable} create_sample_images.py", "Creating sample images"):
            has_images, num_images = check_images()
    
    if has_images:
        print(f"\\n📸 Found {num_images} image(s) to process")
        
        # Step 3: Run detection
        if run_command(f"{sys.executable} run_detection.py", "Running pothole detection"):
            print("\\n🎉 DETECTION COMPLETE!")
            print("\\n📁 Check these folders for results:")
            print("   • output_results/ - Contains detected images and reports")
            print("   • input_images/ - Contains your input images")
            
            # Show what was generated
            output_folder = Path("output_results")
            if output_folder.exists():
                files = list(output_folder.glob("*"))
                print(f"\\n📄 Generated {len(files)} output files:")
                for file in files:
                    print(f"   • {file.name}")
        else:
            print("\\n❌ Detection failed. Check error messages above.")
    else:
        print("\\n❌ No images found. Please add some road images to 'input_images' folder and run again.")

if __name__ == "__main__":
    main()
