#!/usr/bin/env python3
"""
Business Lead Finder - Quick Launcher
Just run: python blf.py
"""
import sys
import os
from pathlib import Path

# Change to script directory
os.chdir(Path(__file__).parent)

# Import and run main
from main import main

if __name__ == "__main__":
    main()
