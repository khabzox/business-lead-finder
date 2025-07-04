#!/usr/bin/env python3
"""
Test Enhanced Website Detection
Demonstrates the AI-powered domain generation and enhanced website checking.
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
    # Note: Morocco is French-speaking, so businesses often use French patterns
    test_businesses = [
        {
            "name": "La Mamounia",
            "category": "hotel",
            "address": "Avenue Bab Jdid, Marrakech",
            "phone": "+212524388600"
        },
        {
            "name": "Café Argana", 
            "category": "cafe",
            "address": "Jemaa el-Fnaa, Marrakech",
            "phone": "+212524000000",
            "expected_domain": "restaurantargana.com"  # Real domain: they added "restaurant"
        },
        {
            "name": "Riad Yasmine",
            "category": "hotel", 
            "address": "Derb Sidi Bouloukat, Marrakech",
            "phone": "+212524387654"
        },
        {
            "name": "Le Jardin",
            "category": "restaurant",
            "address": "32 Souk el Jeld, Marrakech", 
            "phone": "+212524000001"
        }
    ]
    
    table = Table(title="Website Detection Results")
    table.add_column("Business", style="cyan")
    table.add_column("Category", justify="center")
    table.add_column("Website Found", justify="center")
    table.add_column("Status", justify="center")
    
    for business in test_businesses:
        console.print(f"\n[yellow]🔍 Checking: {business['name']}[/yellow]")
        
        # Show expected domain if available
        if business.get('expected_domain'):
            console.print(f"  Expected domain: {business['expected_domain']}")
        
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
        
        # Check if we found the expected domain
        if business.get('expected_domain') and result['website_found']:
            if business['expected_domain'] in result['website_url']:
                console.print(f"  ✅ Found expected domain!")
            else:
                console.print(f"  ⚠️  Found different domain than expected")
    
    console.print(table)
    
    console.print("\n[bold green]📈 Enhanced Detection Features:[/bold green]")
    console.print("• AI-powered domain generation using business context")
    console.print("• French language patterns (Morocco is French-speaking)")
    console.print("• Hyphenated and concatenated name patterns")
    console.print("• Category and location-based domain patterns")
    console.print("• Common French business prefixes: restaurant, cafe, hotel, riad, le, la")
    console.print("• Fallback patterns for common Moroccan business domains")
    console.print("• Example: 'Café Argana' → 'restaurantargana.com' (adds 'restaurant')")

if __name__ == "__main__":
    test_website_detection()
