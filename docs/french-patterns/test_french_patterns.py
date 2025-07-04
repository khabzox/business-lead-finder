#!/usr/bin/env python3
"""
French Language Patterns Test
Demonstrates website detection for French business names in Morocco.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from website_checker import enhanced_website_detection
from rich.console import Console
from rich.table import Table

console = Console()

def test_french_patterns():
    """Test French language pattern detection for Moroccan businesses."""
    
    console.print("[blue]🇫🇷 French Language Patterns Test[/blue]")
    console.print("=" * 60)
    
    # French businesses in Morocco with known domain patterns
    french_businesses = [
        {
            "name": "Café Argana",
            "category": "cafe",
            "address": "Jemaa el-Fnaa, Marrakech",
            "known_domain": "restaurantargana.com",
            "pattern": "Adds 'restaurant' prefix"
        },
        {
            "name": "Le Jardin",
            "category": "restaurant", 
            "address": "32 Souk el Jeld, Marrakech",
            "known_domain": "lejardin-marrakech.com",
            "pattern": "Uses hyphen with location"
        },
        {
            "name": "La Mamounia",
            "category": "hotel",
            "address": "Avenue Bab Jdid, Marrakech",
            "known_domain": "mamounia.com",
            "pattern": "Removes French article 'La'"
        },
        {
            "name": "Café des Épices",
            "category": "cafe",
            "address": "75 Rahba Lakdima, Marrakech",
            "known_domain": "cafedesepices.com",
            "pattern": "Removes accents, joins words"
        },
        {
            "name": "Restaurant Al Fassia",
            "category": "restaurant",
            "address": "55 Boulevard Zerktouni, Marrakech",
            "known_domain": "alfassia.com",
            "pattern": "Removes category, simplifies name"
        }
    ]
    
    table = Table(title="French Pattern Detection Results")
    table.add_column("Business", style="cyan")
    table.add_column("Known Domain", style="green")
    table.add_column("Pattern Used", style="yellow")
    table.add_column("Detection", justify="center")
    table.add_column("Status", justify="center")
    
    successful_detections = 0
    total_businesses = len(french_businesses)
    
    for business in french_businesses:
        console.print(f"\n[yellow]🔍 Testing: {business['name']}[/yellow]")
        console.print(f"  Known domain: {business['known_domain']}")
        console.print(f"  Pattern: {business['pattern']}")
        
        result = enhanced_website_detection(business['name'], business['category'])
        
        # Check if we found the known domain
        found_correct_domain = False
        if result['website_found']:
            # Extract domain from URL
            found_domain = result['website_url'].replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
            if business['known_domain'] in found_domain or found_domain in business['known_domain']:
                found_correct_domain = True
                successful_detections += 1
        
        if found_correct_domain:
            detection_result = f"✅ Found: {result['website_url'][:25]}..."
            status = "[green]SUCCESS[/green]"
        elif result['website_found']:
            detection_result = f"⚠️ Different: {result['website_url'][:25]}..."
            status = "[yellow]PARTIAL[/yellow]"
        else:
            detection_result = "❌ Not found"
            status = "[red]FAILED[/red]"
        
        table.add_row(
            business['name'],
            business['known_domain'],
            business['pattern'],
            detection_result,
            status
        )
        
        # Show domains checked
        if result.get('domains_checked'):
            console.print(f"  Checked {len(result['domains_checked'])} domains")
            # Show if the known domain was in our attempts
            known_in_attempts = any(business['known_domain'].replace('.com', '') in domain for domain in result['domains_checked'])
            if known_in_attempts:
                console.print(f"  ✅ Known domain pattern was attempted")
            else:
                console.print(f"  ⚠️ Known domain pattern was NOT attempted")
    
    console.print(table)
    
    # Summary
    success_rate = (successful_detections / total_businesses) * 100
    console.print(f"\n[bold]📊 Success Rate: {successful_detections}/{total_businesses} ({success_rate:.1f}%)[/bold]")
    
    console.print("\n[bold green]🇫🇷 French Pattern Insights:[/bold green]")
    console.print("• Moroccan businesses often add French category words ('restaurant', 'cafe')")
    console.print("• French articles ('Le', 'La', 'Des') are usually removed from domains")
    console.print("• Accents and special characters (é, è, ç) are simplified or removed")
    console.print("• Multi-word names often joined without hyphens or with hyphens")
    console.print("• Location names sometimes added with hyphens")
    
    console.print("\n[bold yellow]🔧 Suggested Improvements:[/bold yellow]")
    if success_rate < 80:
        console.print("• Add more French prefix/suffix patterns")
        console.print("• Improve accent character handling")
        console.print("• Add location-based domain variations")
        console.print("• Include category word combinations")

if __name__ == "__main__":
    test_french_patterns()
