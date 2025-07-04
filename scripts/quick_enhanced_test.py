#!/usr/bin/env python3
"""
Quick test of enhanced website detection on a few sample businesses
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
from business_search import update_business_with_enhanced_website_check
from rich.console import Console
from rich.table import Table

console = Console()

def quick_enhanced_test():
    """Quick test of enhanced website detection."""
    
    console.print("[blue]🚀 Quick Enhanced Website Detection Test[/blue]")
    console.print("=" * 60)
    
    # Sample businesses (including real examples with known websites)
    test_businesses = [
        {
            "name": "Riad Yasmine",
            "category": "hotel",
            "address": "Derb Asmakh, Medina, Marrakesh",
            "phone": "+212524387654",
            "rating": 4.3,
            "lead_score": 80
        },
        {
            "name": "Café Argana", 
            "category": "restaurant",
            "address": "Place Jemaa el-Fna, Marrakesh",
            "phone": "+212524443322",
            "rating": 4.2,
            "lead_score": 85
        },
        {
            "name": "Restaurant Atlas",
            "category": "restaurant", 
            "address": "Rue Moulay Ismail, Medina, Marrakesh",
            "phone": "+212524556677",
            "rating": 4.5,
            "lead_score": 90
        }
    ]
    
    results = []
    
    for business in test_businesses:
        console.print(f"\n🔍 Testing: [bold]{business['name']}[/bold]")
        console.print(f"   Category: {business['category']}")
        console.print(f"   Original Lead Score: {business['lead_score']}")
        
        # Run enhanced detection
        updated_business = update_business_with_enhanced_website_check(business.copy())
        results.append(updated_business)
        
        # Show results
        if updated_business.get('website'):
            console.print(f"   [green]✅ Website Found: {updated_business['website']}[/green]")
            console.print(f"   [blue]Quality Score: {updated_business.get('website_quality_score', 0)}/100[/blue]")
            console.print(f"   [yellow]New Lead Score: {updated_business['lead_score']} (reduced due to existing website)[/yellow]")
        else:
            console.print(f"   [red]❌ No Website Found[/red]")
            console.print(f"   [green]New Lead Score: {updated_business['lead_score']} (boosted - high opportunity!)[/green]")
        
        domains_checked = updated_business.get('website_domains_checked', [])
        console.print(f"   [dim]Domains Checked ({len(domains_checked)}): {', '.join(domains_checked[:3])}{'...' if len(domains_checked) > 3 else ''}[/dim]")
    
    # Summary table
    console.print(f"\n[bold blue]📊 SUMMARY TABLE[/bold blue]")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Business", style="bold")
    table.add_column("Website Status", style="green")
    table.add_column("Website URL", style="cyan")
    table.add_column("Lead Score", style="yellow")
    table.add_column("Opportunity", style="red")
    
    for business in results:
        website_status = "✅ Found" if business.get('website') else "❌ Not Found"
        website_url = business.get('website', 'N/A')[:30]
        lead_score = f"{business.get('lead_score', 0)}/100"
        
        if business.get('website'):
            opportunity = "Website Upgrade"
        else:
            opportunity = "🔥 HIGH PRIORITY"
        
        table.add_row(
            business['name'],
            website_status,
            website_url,
            lead_score,
            opportunity
        )
    
    console.print(table)
    
    # Key insights
    websites_found = len([b for b in results if b.get('website')])
    
    console.print(f"\n[bold green]🎯 KEY INSIGHTS[/bold green]")
    console.print(f"• Tested {len(results)} businesses")
    console.print(f"• Found {websites_found} websites using enhanced detection")
    console.print(f"• {len(results) - websites_found} businesses remain high-priority leads")
    console.print(f"• Enhanced detection prevents false negatives!")
    
    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/quick_enhanced_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    console.print(f"\n[green]📁 Results saved to: results/quick_enhanced_test.json[/green]")

if __name__ == "__main__":
    quick_enhanced_test()
