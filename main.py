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

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Import our modules
from cli_interface import create_cli_parser, handle_cli_command
from utils import setup_logging, load_config
from config.settings import DEFAULT_SETTINGS

console = Console()

def display_banner():
    """Display application banner."""
    banner_text = Text("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  BUSINESS LEAD FINDER                        ║
    ║          Find businesses without websites in Morocco         ║
    ║                                                              ║
    ║  🎯 Search local businesses  📊 Generate reports            ║
    ║  🔍 Check website presence   📧 Create email templates      ║
    ║  💼 Score potential leads    📈 Track ROI                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """, style="bold blue")
    
    console.print(Panel(banner_text, border_style="bright_blue"))

def main():
    """Main entry point for the application."""
    try:
        # Setup logging
        setup_logging()
        
        # Display banner
        display_banner()
        
        # Create CLI parser
        parser = create_cli_parser()
        
        # Parse arguments
        if len(sys.argv) == 1:
            # No arguments provided, show help
            parser.print_help()
            console.print("\n[yellow]Tip: Try 'python main.py interactive' for guided mode[/yellow]")
            return
        
        args = parser.parse_args()
        
        # Load configuration
        config = load_config(args.config if hasattr(args, 'config') else None)
        
        # Handle the command
        success = handle_cli_command(args, config)
        
        if success:
            console.print("\n[green]✅ Command completed successfully![/green]")
        else:
            console.print("\n[red]❌ Command failed. Check logs for details.[/red]")
            sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
