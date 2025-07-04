#!/usr/bin/env python3
"""
Test script for the new rating filtering feature
Demonstrates how to find businesses with low ratings that likely don't have websites
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_rating_filtering():
    """Test the new rating filtering functionality"""
    
    console.print(Panel.fit(
        "🎯 RATING FILTER TEST\n"
        "Testing the new Google Maps rating filtering to find businesses\n"
        "with low ratings (0-4.0) that likely don't have websites",
        style="bold blue"
    ))
    
    console.print("\n[bold green]📊 Rating Filter Options:[/bold green]")
    console.print("• [yellow]--rating-filter low[/yellow]   → Focus on 0-4.0 star businesses (likely no website)")
    console.print("• [yellow]--rating-filter high[/yellow]  → Focus on 4.5+ star businesses") 
    console.print("• [yellow]--rating-filter all[/yellow]   → No rating filter")
    
    console.print("\n[bold green]🎯 Why Low Ratings Work:[/bold green]")
    console.print("• Businesses with low ratings often lack online presence")
    console.print("• They're less likely to have professional websites")
    console.print("• Perfect targets for website/digital marketing services")
    console.print("• Higher chance of needing business improvement help")
    
    console.print("\n[bold green]📧 Enhanced Contact Discovery:[/bold green]")
    console.print("• Automatically extracts emails from Google Maps")
    console.print("• Finds social media links when available")
    console.print("• Prioritizes businesses based on contact completeness")
    console.print("• Shows lead priority: HIGH, MEDIUM, or UPGRADE")
    
    console.print("\n[bold cyan]🧪 Test Commands:[/bold cyan]")
    console.print("[dim]# Find low-rated restaurants (0-4.0 stars) in Marrakesh[/dim]")
    console.print("python main.py search --location 'Marrakesh, Morocco' --categories restaurants --google-maps-only --rating-filter low")
    
    console.print("\n[dim]# Find high-rated spas (4.5+ stars) for comparison[/dim]")
    console.print("python main.py search --location 'Casablanca, Morocco' --categories spas --google-maps-only --rating-filter high")
    
    console.print("\n[dim]# Combined search with low rating filter[/dim]")
    console.print("python main.py search --location 'Rabat, Morocco' --categories cafes hotels --use-google-maps --rating-filter low")
    
    console.print("\n[bold yellow]💡 Expected Results:[/bold yellow]")
    console.print("• Higher percentage of businesses without websites")
    console.print("• Better lead scores for low-rated businesses")
    console.print("• More actionable leads for digital marketing services")
    
if __name__ == "__main__":
    test_rating_filtering()
