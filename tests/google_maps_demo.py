#!/usr/bin/env python3
"""
Simple working example of Google Maps CLI integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console

console = Console()

def main():
    """Simple demo of Google Maps integration"""
    
    console.print("[bold blue]🎯 Google Maps CLI Integration - Simple Demo[/bold blue]")
    console.print()
    
    # Show available commands
    commands = [
        ("Standard search", "python main.py search --location 'Marrakesh, Morocco' --categories restaurants --filter no-website"),
        ("Enhanced search", "python main.py search --location 'Casablanca, Morocco' --categories hotels --use-google-maps"),
        ("Google Maps only", "python main.py search --location 'Fez, Morocco' --categories spas --google-maps-only --max-results 5"),
        ("Interactive mode", "python main.py interactive"),
        ("Check status", "python main.py status")
    ]
    
    console.print("[bold green]✅ Available Commands:[/bold green]")
    for i, (name, command) in enumerate(commands, 1):
        console.print(f"[cyan]{i}. {name}:[/cyan]")
        console.print(f"   {command}")
        console.print()
    
    console.print("[bold yellow]💡 Recommendations:[/bold yellow]")
    console.print("• Start with interactive mode: python main.py interactive")
    console.print("• Check system status first: python main.py status")
    console.print("• Use --max-results 5 for quick tests")
    console.print("• Save results with --output filename.json")
    console.print()
    
    console.print("[bold magenta]🗺️ Google Maps Features:[/bold magenta]")
    console.print("• Automatic email discovery")
    console.print("• Enhanced contact information") 
    console.print("• Business ratings and reviews")
    console.print("• No API keys required (FREE)")
    console.print()
    
    console.print("[bold blue]🚀 Ready to use! Choose a command above to get started.[/bold blue]")

if __name__ == "__main__":
    main()
