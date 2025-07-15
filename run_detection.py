#!/usr/bin/env python3
"""
Simple script to run pothole detection
Just run this file and it will do everything automatically!
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pothole_detector import main

if __name__ == "__main__":
    main()
