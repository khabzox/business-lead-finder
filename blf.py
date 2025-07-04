#!/usr/bin/env python3
"""
Business Lead Finder (BLF) - Python Launcher
============================================

Cross-platform Python launcher for the Business Lead Finder CLI tool.
This provides an alternative way to run BLF without batch files or PowerShell scripts.

Usage:
    python blf.py [mode] [options]
    python blf.py --help
    python blf.py interactive
    python blf.py quick
    python blf.py demo

Examples:
    python blf.py                    # Interactive mode (default)
    python blf.py interactive        # Interactive mode with prompts
    python blf.py quick              # Quick mode with defaults
    python blf.py demo               # Demo mode with sample data
    python blf.py --help             # Show help
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function that delegates to main.py"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Add the project root to Python path
    sys.path.insert(0, str(script_dir))
    
    try:
        # Import and run the main CLI
        from main import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"Error: Could not import main module: {e}")
        print("Please ensure you're running this from the Business Lead Finder root directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
