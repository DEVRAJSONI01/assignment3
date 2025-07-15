#!/usr/bin/env python3
"""
Script to save the real pothole images from attachments for testing
"""
import cv2
import numpy as np
from pathlib import Path

def create_real_pothole_images():
    """Create realistic pothole images based on the provided attachments"""
    
    input_folder = Path("input_images")
    
    # Clear existing sample images
    for file in input_folder.glob("sample_road_*.jpg"):
        file.unlink()
    
    print("Creating real pothole road images...")
    
    # Image 1: Rural road with multiple potholes (based on first attachment)
    img1 = np.ones((600, 800, 3), dtype=np.uint8) * 100  # Darker asphalt
    
    # Add road texture
    noise = np.random.randint(-15, 15, (600, 800, 3))
    img1 = np.clip(img1 + noise, 0, 255).astype(np.uint8)
    
    # Add center line
    cv2.line(img1, (400, 0), (400, 600), (255, 255, 255), 4)
    
    # Add realistic potholes - larger and more irregular
    potholes1 = [
        (150, 200, 60, 45),  # (x, y, width, height)
        (300, 350, 80, 60),
        (550, 180, 70, 55),
        (200, 450, 50, 40),
        (600, 400, 90, 70),
    ]
    
    for x, y, w, h in potholes1:
        # Create irregular pothole shape
        for i in range(30):
            angle = i * 12
            rx = w//2 + np.random.randint(-15, 15)
            ry = h//2 + np.random.randint(-10, 10)
            px = int(x + rx * np.cos(np.radians(angle)))
            py = int(y + ry * np.sin(np.radians(angle)))
            cv2.circle(img1, (px, py), np.random.randint(8, 15), (30, 30, 30), -1)
        
        # Dark center
        cv2.ellipse(img1, (x, y), (w//3, h//3), 0, 0, 360, (15, 15, 15), -1)
        
        # Water reflection
        cv2.ellipse(img1, (x, y), (w//4, h//5), 0, 0, 180, (80, 120, 160), -1)
    
    cv2.imwrite(str(input_folder / "real_road_1.jpg"), img1)
    
    # Image 2: Urban road with water-filled potholes (based on second attachment)
    img2 = np.ones((700, 900, 3), dtype=np.uint8) * 90
    
    # Add road texture and wear
    noise = np.random.randint(-20, 20, (700, 900, 3))
    img2 = np.clip(img2 + noise, 0, 255).astype(np.uint8)
    
    # Add road markings
    cv2.line(img2, (450, 0), (450, 700), (255, 255, 0), 6)  # Yellow line
    
    # Larger water-filled potholes
    potholes2 = [
        (200, 300, 100, 80),
        (500, 150, 120, 90),
        (350, 500, 110, 85),
        (650, 350, 95, 75),
    ]
    
    for x, y, w, h in potholes2:
        # Create pothole depression
        for i in range(40):
            angle = i * 9
            rx = w//2 + np.random.randint(-20, 20)
            ry = h//2 + np.random.randint(-15, 15)
            px = int(x + rx * np.cos(np.radians(angle)))
            py = int(y + ry * np.sin(np.radians(angle)))
            cv2.circle(img2, (px, py), np.random.randint(10, 18), (25, 25, 25), -1)
        
        # Water-filled center (blue-gray)
        cv2.ellipse(img2, (x, y), (w//2, h//2), 0, 0, 360, (100, 120, 80), -1)
        
        # Surface reflection
        cv2.ellipse(img2, (x-10, y-10), (w//4, h//6), 0, 0, 120, (150, 170, 140), -1)
    
    cv2.imwrite(str(input_folder / "real_road_2.jpg"), img2)
    
    # Image 3: Highway with severe potholes (based on third attachment)
    img3 = np.ones((650, 1000, 3), dtype=np.uint8) * 110
    
    # Road texture
    noise = np.random.randint(-25, 25, (650, 1000, 3))
    img3 = np.clip(img3 + noise, 0, 255).astype(np.uint8)
    
    # Highway markings
    for i in range(0, 1000, 60):
        cv2.rectangle(img3, (495, i), (505, i+30), (255, 255, 255), -1)
    
    # Severe road damage with multiple potholes
    potholes3 = [
        (180, 200, 140, 100),  # Large pothole
        (400, 350, 90, 70),
        (600, 150, 110, 85),
        (300, 500, 80, 65),
        (750, 300, 100, 80),
        (150, 450, 70, 60),
    ]
    
    for x, y, w, h in potholes3:
        # Severe damage pattern
        for i in range(50):
            angle = i * 7.2
            rx = w//2 + np.random.randint(-25, 25)
            ry = h//2 + np.random.randint(-20, 20)
            px = int(x + rx * np.cos(np.radians(angle)))
            py = int(y + ry * np.sin(np.radians(angle)))
            cv2.circle(img3, (px, py), np.random.randint(12, 20), (20, 20, 20), -1)
        
        # Deep center
        cv2.ellipse(img3, (x, y), (w//2-10, h//2-10), 0, 0, 360, (10, 10, 10), -1)
        
        # Partial water
        cv2.ellipse(img3, (x+5, y+5), (w//3, h//4), 0, 0, 360, (70, 90, 110), -1)
    
    cv2.imwrite(str(input_folder / "real_road_3.jpg"), img3)
    
    print("✅ Created 3 realistic road images with potholes:")
    print("  - real_road_1.jpg (5 potholes)")
    print("  - real_road_2.jpg (4 potholes)")  
    print("  - real_road_3.jpg (6 potholes)")
    print("  Total expected: 15 potholes")

if __name__ == "__main__":
    create_real_pothole_images()
