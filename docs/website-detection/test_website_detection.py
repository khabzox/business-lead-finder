#!/usr/bin/env python3
"""
Website Detection Test
Demonstrates the enhanced website detection with AI-powered domain generation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from website_checker import enhanced_website_detection
from rich.console import Console
from rich.table import Table

console = Console()

def test_website_detection():
    """Test enhanced website detection on real businesses."""
    
    console.print("[blue]🔍 Enhanced Website Detection Test[/blue]")
    console.print("=" * 60)
    
    # Test businesses with different scenarios
    test_businesses = [
        {
            "name": "La Mamounia",
            "category": "hotel",
            "address": "Avenue Bab Jdid, Marrakech",
            "phone": "+212524388600",
            "expected": "mamounia.com"
        },
        {
            "name": "Riad Yasmine",
            "category": "hotel",
            "address": "Derb Sidi Bouloukat, Marrakech", 
            "phone": "+212524387654",
            "expected": "riad-yasmine.com"
        },
        {
            "name": "Le Jardin",
            "category": "restaurant",
            "address": "32 Souk el Jeld, Marrakech",
            "phone": "+212524000001",
            "expected": "lejardin-marrakech.com"
        },
        {
            "name": "Café des Épices",
            "category": "cafe",
            "address": "75 Rahba Lakdima, Marrakech",
            "phone": "+212524000002",
            "expected": "cafedesepices.com"
        }
    ]
    
    table = Table(title="Website Detection Results")
    table.add_column("Business", style="cyan")
    table.add_column("Category", justify="center")
    table.add_column("Expected", justify="center", style="dim")
    table.add_column("Website Found", justify="center")
    table.add_column("Status", justify="center")
    
    for business in test_businesses:
        console.print(f"\n[yellow]🔍 Checking: {business['name']}[/yellow]")
        
        result = enhanced_website_detection(business['name'], business['category'])
        
        if result['website_found']:
            website_status = f"✅ {result['website_url'][:30]}..."
            status = "[green]Found[/green]"
        else:
            website_status = "❌ None"
            status = "[red]Not Found[/red]"
        
        table.add_row(
            business['name'],
            business['category'],
            business.get('expected', 'N/A'),
            website_status,
            status
        )
        
        # Show some details
        if result.get('domains_checked'):
            console.print(f"  Domains checked: {len(result['domains_checked'])}")
            if result['website_found']:
                console.print(f"  Found domains: {result['domains_found']}")
            else:
                console.print(f"  Sample domains tried: {result['domains_checked'][:3]}")
    
    console.print(table)
    
    console.print("\n[bold green]📈 Enhanced Detection Features:[/bold green]")
    console.print("• AI-powered domain generation using business context")
    console.print("• Multiple domain pattern strategies")
    console.print("• Real-time domain validation and accessibility checks")
    console.print("• Intelligent fallback patterns")

if __name__ == "__main__":
    test_website_detection()
