#!/usr/bin/env python3
"""
Setup script for Pothole Detection System
This will install required packages and set up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")
    
    # Create input and output directories
    Path("input_images").mkdir(exist_ok=True)
    Path("output_results").mkdir(exist_ok=True)
    
    print("✅ Directories created successfully!")

def main():
    print("POTHOLE DETECTION SYSTEM SETUP")
    print("=" * 40)
    
    # Setup directories
    setup_directories()
    
    # Install requirements
    if install_requirements():
        print("\n🚀 Setup complete!")
        print("\nNext steps:")
        print("1. Place your road images in the 'input_images' folder")
        print("2. Run: python run_detection.py")
        print("3. Check results in the 'output_results' folder")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
