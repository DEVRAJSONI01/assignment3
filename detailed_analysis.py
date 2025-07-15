#!/usr/bin/env python3
"""
Demonstration script showing step-by-step pothole detection
on an image similar to the uploaded one
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def demonstrate_detection():
    """Show step-by-step detection process"""
    
    image_path = "input_images/uploaded_pothole_road.jpg"
    
    if not Path(image_path).exists():
        print("Image not found. Please run save_uploaded_image.py first.")
        return
    
    print("🔍 STEP-BY-STEP POTHOLE DETECTION ANALYSIS")
    print("=" * 60)
    
    # Load image
    image = cv2.imread(image_path)
    print(f"📸 Loaded image: {Path(image_path).name}")
    print(f"   Dimensions: {image.shape[1]}x{image.shape[0]} pixels")
    
    # Step 1: Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blurred)
    
    print("\\n🔧 PREPROCESSING COMPLETE:")
    print("   ✅ Converted to grayscale")
    print("   ✅ Applied Gaussian blur (noise reduction)")
    print("   ✅ Enhanced contrast with CLAHE")
    
    # Step 2: Edge detection
    edges = cv2.Canny(enhanced, 50, 150)
    
    # Step 3: Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    print("\\n🎯 EDGE DETECTION:")
    print("   ✅ Canny edge detection applied")
    print("   ✅ Morphological closing to connect edges")
    
    # Step 4: Find and filter contours
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    height, width = image.shape[:2]
    potholes = []
    min_area = 200
    max_area = width * height * 0.3
    
    print(f"\\n📊 CONTOUR ANALYSIS:")
    print(f"   🔍 Found {len(contours)} total contours")
    print(f"   📏 Size filter: {min_area} - {max_area} pixels")
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if min_area < area < max_area:
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                
                if (0.1 < circularity < 1.2 and 
                    0.3 < aspect_ratio < 3.0 and
                    w > 20 and h > 20):
                    
                    potholes.append({
                        'contour': contour,
                        'area': area,
                        'bbox': (x, y, w, h),
                        'circularity': circularity,
                        'aspect_ratio': aspect_ratio
                    })
    
    print(f"   ✅ After filtering: {len(potholes)} potholes detected")
    
    # Step 5: Draw results
    result_image = image.copy()
    
    print("\\n🎨 MARKING DETECTED POTHOLES:")
    for i, pothole in enumerate(potholes):
        # Draw contour in green
        cv2.drawContours(result_image, [pothole['contour']], -1, (0, 255, 0), 3)
        
        # Draw bounding box in blue
        x, y, w, h = pothole['bbox']
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (255, 0, 0), 3)
        
        # Add label in yellow
        label = f"Pothole {i+1}"
        cv2.putText(result_image, label, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        # Print details
        area_sqm = pothole['area'] / 10000
        print(f"   🕳️  Pothole {i+1}:")
        print(f"      📐 Area: {pothole['area']:.0f} pixels (~{area_sqm:.2f} sq.m)")
        print(f"      🔵 Circularity: {pothole['circularity']:.2f}")
        print(f"      📊 Aspect Ratio: {pothole['aspect_ratio']:.2f}")
        print(f"      📍 Location: ({x}, {y})")
    
    # Add summary
    summary_text = f"Potholes detected: {len(potholes)}"
    cv2.putText(result_image, summary_text, (10, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    
    # Save detailed result
    output_path = "output_results/detailed_analysis.jpg"
    cv2.imwrite(output_path, result_image)
    
    print(f"\\n✅ DETECTION COMPLETE!")
    print(f"📁 Detailed result saved: {output_path}")
    print(f"🎯 Total potholes found: {len(potholes)}")
    
    return len(potholes), result_image

if __name__ == "__main__":
    demonstrate_detection()
