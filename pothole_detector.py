import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path

class PotholeDetector:
    def __init__(self):
        self.results = []
    
    def preprocess_image(self, image):
        """Preprocess the image for better pothole detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        
        return enhanced
    
    def detect_potholes(self, image_path):
        """Main function to detect potholes in an image"""
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return None
        
        original = image.copy()
        height, width = image.shape[:2]
        
        # Preprocess the image
        processed = self.preprocess_image(image)
        
        # Edge detection using Canny
        edges = cv2.Canny(processed, 50, 150)
        
        # Morphological operations to close gaps in edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours based on area and shape
        potholes = []
        min_area = 200  # Minimum area for a pothole
        max_area = width * height * 0.3  # Maximum area (30% of image)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if min_area < area < max_area:
                # Calculate additional features
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h
                    
                    # Filter based on shape characteristics
                    if (0.1 < circularity < 1.2 and 
                        0.3 < aspect_ratio < 3.0 and
                        w > 20 and h > 20):
                        
                        potholes.append({
                            'contour': contour,
                            'area': area,
                            'bbox': (x, y, w, h),
                            'circularity': circularity
                        })
        
        # Draw detected potholes
        result_image = original.copy()
        
        for i, pothole in enumerate(potholes):
            # Draw contour
            cv2.drawContours(result_image, [pothole['contour']], -1, (0, 255, 0), 2)
            
            # Draw bounding box
            x, y, w, h = pothole['bbox']
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Add label
            label = f"Pothole {i+1}"
            cv2.putText(result_image, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Add summary text
        summary_text = f"Potholes detected: {len(potholes)}"
        cv2.putText(result_image, summary_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return {
            'original': original,
            'result': result_image,
            'pothole_count': len(potholes),
            'potholes': potholes,
            'filename': os.path.basename(image_path)
        }
    
    def process_images(self, input_folder, output_folder):
        """Process all images in the input folder"""
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        # Supported image extensions
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        # Find all image files
        image_files = []
        for ext in extensions:
            image_files.extend(Path(input_folder).glob(f'*{ext}'))
            image_files.extend(Path(input_folder).glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"No image files found in {input_folder}")
            return
        
        print(f"Found {len(image_files)} image(s) to process...")
        
        for image_path in image_files:
            print(f"\nProcessing: {image_path.name}")
            
            result = self.detect_potholes(str(image_path))
            
            if result:
                # Save the result image
                output_path = Path(output_folder) / f"detected_{result['filename']}"
                cv2.imwrite(str(output_path), result['result'])
                
                self.results.append(result)
                
                print(f"  - Potholes detected: {result['pothole_count']}")
                print(f"  - Output saved: {output_path}")
        
        self.generate_summary_report(output_folder)
    
    def generate_summary_report(self, output_folder):
        """Generate a summary report of all detections"""
        if not self.results:
            return
        
        # Create a figure with subplots
        n_images = len(self.results)
        fig, axes = plt.subplots(2, n_images, figsize=(5*n_images, 10))
        
        if n_images == 1:
            axes = axes.reshape(2, 1)
        
        for i, result in enumerate(self.results):
            # Original image
            axes[0, i].imshow(cv2.cvtColor(result['original'], cv2.COLOR_BGR2RGB))
            axes[0, i].set_title(f"Original: {result['filename']}")
            axes[0, i].axis('off')
            
            # Result image
            axes[1, i].imshow(cv2.cvtColor(result['result'], cv2.COLOR_BGR2RGB))
            axes[1, i].set_title(f"Detected: {result['pothole_count']} potholes")
            axes[1, i].axis('off')
        
        plt.tight_layout()
        plt.savefig(Path(output_folder) / "detection_summary.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        # Generate text report
        report_path = Path(output_folder) / "detection_report.txt"
        with open(report_path, 'w') as f:
            f.write("POTHOLE DETECTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            total_potholes = sum(r['pothole_count'] for r in self.results)
            f.write(f"Total images processed: {len(self.results)}\n")
            f.write(f"Total potholes detected: {total_potholes}\n\n")
            
            f.write("DETAILED RESULTS:\n")
            f.write("-" * 30 + "\n")
            
            for result in self.results:
                f.write(f"\nImage: {result['filename']}\n")
                f.write(f"Potholes detected: {result['pothole_count']}\n")
                
                for i, pothole in enumerate(result['potholes']):
                    area_sqm = pothole['area'] / 10000  # Rough conversion to square meters
                    f.write(f"  Pothole {i+1}: Area = {pothole['area']:.0f} pixels (~{area_sqm:.2f} sq.m)\n")
        
        print(f"\nSummary report generated: {report_path}")
        print(f"Visual summary saved: {Path(output_folder) / 'detection_summary.png'}")

def main():
    print("POTHOLE DETECTION SYSTEM")
    print("=" * 40)
    
    # Initialize detector
    detector = PotholeDetector()
    
    # Set up directories
    input_folder = "input_images"
    output_folder = "output_results"
    
    # Create input folder if it doesn't exist
    Path(input_folder).mkdir(exist_ok=True)
    
    print(f"\nPlease place your road images in the '{input_folder}' folder")
    print("Supported formats: JPG, JPEG, PNG, BMP, TIFF")
    print("\nStarting detection process...")
    
    # Process images
    detector.process_images(input_folder, output_folder)
    
    if detector.results:
        print(f"\n✅ Processing complete!")
        print(f"Results saved in '{output_folder}' folder")
        print(f"Total images processed: {len(detector.results)}")
        print(f"Total potholes detected: {sum(r['pothole_count'] for r in detector.results)}")
    else:
        print(f"\n❌ No images found in '{input_folder}' folder")
        print("Please add some road images and run again.")

if __name__ == "__main__":
    main()
