#!/usr/bin/env python3
"""
Sample image downloader for testing pothole detection
This script creates sample pothole images for testing if you don't have your own images
"""

import cv2
import numpy as np
from pathlib import Path

def create_sample_pothole_image(filename, width=800, height=600):
    """Create a synthetic road image with potholes for testing"""
    
    # Create a road-like background
    image = np.ones((height, width, 3), dtype=np.uint8) * 120  # Gray road
    
    # Add some texture to make it look more like asphalt
    noise = np.random.randint(-20, 20, (height, width, 3))
    image = np.clip(image + noise, 0, 255).astype(np.uint8)
    
    # Add some road markings (yellow line)
    cv2.line(image, (width//2, 0), (width//2, height), (0, 255, 255), 8)
    
    # Create potholes (dark irregular circles)
    potholes = [
        (200, 300, 40),   # (x, y, radius)
        (500, 150, 30),
        (600, 400, 35),
        (150, 450, 25),
    ]
    
    for x, y, radius in potholes:
        # Create an irregular pothole shape
        for i in range(20):
            angle = i * 18  # 360/20 degrees
            r = radius + np.random.randint(-10, 10)
            px = int(x + r * np.cos(np.radians(angle)))
            py = int(y + r * np.sin(np.radians(angle)))
            cv2.circle(image, (px, py), 8, (40, 40, 40), -1)
        
        # Make the center darker
        cv2.circle(image, (x, y), radius//2, (20, 20, 20), -1)
        
        # Add some water effect (reflection)
        cv2.ellipse(image, (x, y), (radius//3, radius//4), 0, 0, 180, (100, 150, 200), -1)
    
    return image

def main():
    print("Creating sample pothole images for testing...")
    
    input_folder = Path("input_images")
    input_folder.mkdir(exist_ok=True)
    
    # Create a few sample images
    sample_images = [
        ("sample_road_1.jpg", 800, 600),
        ("sample_road_2.jpg", 1000, 700),
        ("sample_road_3.jpg", 900, 650),
    ]
    
    for filename, width, height in sample_images:
        image = create_sample_pothole_image(filename, width, height)
        image_path = input_folder / filename
        cv2.imwrite(str(image_path), image)
        print(f"Created: {image_path}")
    
    print(f"\n✅ Sample images created in '{input_folder}' folder")
    print("You can now run the pothole detection on these sample images!")
    print("Or replace them with your own road images.")

if __name__ == "__main__":
    main()
