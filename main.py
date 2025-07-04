#!/usr/bin/env python3
"""
Business Lead Finder - Main CLI Application
Finds local businesses without websites for lead generation.

Usage:
    python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels
    python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
    python main.py report --input data/leads.json --output results/report.html
    python main.py export --format csv --output results/leads.csv
    python main.py interactive
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import our modules
try:
    from cli_interface import create_cli_parser, handle_cli_command
    from utils import setup_logging, load_config
    from config.settings import DEFAULT_SETTINGS
    FULL_CLI_AVAILABLE = True
except ImportError as e:
    print(f"Full CLI not available: {e}")
    print("Using basic CLI interface...")
    from simple_cli import create_basic_cli_parser, handle_basic_cli_command
    FULL_CLI_AVAILABLE = False
    
    # Create basic versions of missing functions
    def setup_logging():
        import logging
        logging.basicConfig(level=logging.INFO)
    
    def load_config(config_file=None):
        return {
            'default_location': 'Marrakesh, Morocco',
            'max_results': 50,
            'categories': ['restaurants', 'hotels', 'cafes', 'spas']
        }

def display_banner():
    """Display application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  BUSINESS LEAD FINDER                        ║
║          Find businesses without websites in Morocco         ║
║                                                              ║
║  🎯 Search local businesses  📊 Generate reports             ║
║  🔍 Check website presence   📧 Create email templates       ║
║  💼 Score potential leads    📈 Track ROI                    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point for the application."""
    try:
        # Setup logging
        setup_logging()
        
        # Display banner
        display_banner()
        
        # Create CLI parser
        if FULL_CLI_AVAILABLE:
            parser = create_cli_parser()
        else:
            parser = create_basic_cli_parser()
        
        # Parse arguments
        if len(sys.argv) == 1:
            # No arguments provided, show help
            parser.print_help()
            print("\nTip: Try 'python main.py interactive' for guided mode")
            return
        
        args = parser.parse_args()
        
        # Load configuration
        config = load_config(args.config if hasattr(args, 'config') else None)
        
        # Handle the command
        if FULL_CLI_AVAILABLE:
            success = handle_cli_command(args, config)
        else:
            success = handle_basic_cli_command(args, config)
        
        if success:
            print("\n✅ Command completed successfully!")
        else:
            print("\n❌ Command failed. Check logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
