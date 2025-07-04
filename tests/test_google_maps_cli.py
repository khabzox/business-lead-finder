#!/usr/bin/env python3
"""
Test script for Google Maps CLI integration
Demonstrates the new Google Maps scraping functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from argparse import Namespace

console = Console()

def test_google_maps_integration():
    """Test Google Maps integration with CLI"""
    console.print("[bold blue]🧪 Testing Google Maps CLI Integration[/bold blue]")
    
    try:
        # Import CLI functions
        from cli_interface import (
            handle_search_command, 
            GOOGLE_MAPS_AVAILABLE,
            show_status
        )
        
        # Test configuration
        config = {
            'debug': True,
            'output_dir': 'results/tests',
            'max_retries': 3
        }
        
        # Show system status
        console.print("\n[bold green]1. Checking System Status[/bold green]")
        show_status(config)
        
        if not GOOGLE_MAPS_AVAILABLE:
            console.print("\n[red]❌ Google Maps scraping not available.[/red]")
            console.print("[yellow]Install selenium: pip install selenium[/yellow]")
            console.print("[yellow]Download ChromeDriver: https://chromedriver.chromium.org/[/yellow]")
            return False
        
        # Test 1: Standard search
        console.print("\n[bold green]2. Testing Standard Search[/bold green]")
        args_standard = Namespace(
            location="Marrakesh, Morocco",
            categories=["restaurants"],
            max_results=5,
            output="results/tests/standard_search.json",
            format='json',
            filter='no-website',
            ai_analysis=False,
            use_google_maps=False,
            google_maps_only=False,
            headless=True,
            sort_by='lead-score'  # Added missing attribute
        )
        
        success = handle_search_command(args_standard, config)
        if success:
            console.print("[green]✅ Standard search completed[/green]")
        else:
            console.print("[red]❌ Standard search failed[/red]")
        
        # Test 2: Google Maps only search
        console.print("\n[bold green]3. Testing Google Maps Only Search[/bold green]")
        args_gmaps = Namespace(
            location="Marrakesh, Morocco",
            categories=["cafes"],
            max_results=3,
            output="results/tests/gmaps_search.json",
            format='json',
            filter='all',
            ai_analysis=False,
            use_google_maps=False,
            google_maps_only=True,
            headless=True,
            sort_by='lead-score'  # Added missing attribute
        )
        
        success = handle_search_command(args_gmaps, config)
        if success:
            console.print("[green]✅ Google Maps search completed[/green]")
        else:
            console.print("[red]❌ Google Maps search failed[/red]")
        
        # Test 3: Combined search
        console.print("\n[bold green]4. Testing Combined Search[/bold green]")
        args_combined = Namespace(
            location="Casablanca, Morocco",
            categories=["spas"],
            max_results=3,
            output="results/tests/combined_search.json",
            format='json',
            filter='no-website',
            ai_analysis=False,
            use_google_maps=True,
            google_maps_only=False,
            headless=True,
            sort_by='lead-score'  # Added missing attribute
        )
        
        success = handle_search_command(args_combined, config)
        if success:
            console.print("[green]✅ Combined search completed[/green]")
        else:
            console.print("[red]❌ Combined search failed[/red]")
        
        console.print("\n[bold blue]🎉 Google Maps CLI Integration Tests Completed![/bold blue]")
        console.print("\n[bold yellow]📊 Usage Examples:[/bold yellow]")
        console.print("• Standard: python main.py search --location 'Marrakesh, Morocco' --categories restaurants")
        console.print("• With Google Maps: python main.py search --location 'Fez, Morocco' --categories hotels --use-google-maps")
        console.print("• Google Maps Only: python main.py search --location 'Rabat, Morocco' --categories spas --google-maps-only")
        console.print("• Interactive: python main.py interactive")
        
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Import error: {e}[/red]")
        console.print("[yellow]Make sure all dependencies are installed[/yellow]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error during testing: {e}[/red]")
        return False

def show_google_maps_features():
    """Show Google Maps features"""
    console.print("\n[bold magenta]🗺️ Google Maps Scraping Features:[/bold magenta]")
    
    features = [
        "📧 Email Discovery - Find business email addresses",
        "📞 Phone Numbers - Extract contact phone numbers", 
        "📍 Addresses - Get complete business addresses",
        "⭐ Ratings & Reviews - Business rating information",
        "🌐 Website Detection - Identify businesses without websites",
        "🔍 Category Detection - Automatic business categorization",
        "🆓 FREE - No API keys or payments required",
        "🤖 AI Integration - Works with lead scoring",
        "📊 Enhanced Reporting - Detailed contact information",
        "🎯 Lead Filtering - Focus on high-opportunity businesses"
    ]
    
    for feature in features:
        console.print(f"  {feature}")
    
    console.print("\n[bold cyan]🚀 CLI Integration Benefits:[/bold cyan]")
    benefits = [
        "Choose between standard and Google Maps scraping",
        "Combine methods for maximum coverage",
        "Interactive mode with guided setup",
        "Automatic email extraction and validation",
        "Enhanced contact information for outreach",
        "Compatible with existing features and workflows"
    ]
    
    for benefit in benefits:
        console.print(f"  • {benefit}")

if __name__ == "__main__":
    console.print("[bold blue]🎯 Business Lead Finder - Google Maps CLI Test[/bold blue]")
    
    show_google_maps_features()
    
    # Run tests
    test_google_maps_integration()
