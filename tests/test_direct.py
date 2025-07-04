#!/usr/bin/env python3
"""
Direct test of the new email and rating filter features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_email_rating_features():
    """Test the new email and rating filter features directly"""
    
    console.print(Panel.fit(
        "🧪 TESTING EMAIL & RATING FILTER FEATURES\n"
        "Direct test of the enhanced business search capabilities",
        style="bold blue"
    ))
    
    try:
        # Test import of updated modules
        console.print("\n[yellow]Testing module imports...[/yellow]")
        
        from src.business_search import search_businesses_all_sources, enhance_business_data
        console.print("✅ business_search module imported successfully")
        
        from src.google_maps_scraper import GoogleMapsScraper
        console.print("✅ google_maps_scraper module imported successfully")
        
        # Test business search with email fields
        console.print("\n[yellow]Testing business search with email fields...[/yellow]")
        
        businesses = search_businesses_all_sources(
            query="restaurants",
            location="Marrakesh, Morocco", 
            max_results=5
        )
        
        console.print(f"✅ Found {len(businesses)} businesses")
        
        # Display business data structure
        if businesses:
            business = businesses[0]
            
            table = Table(title="Sample Business Data Structure")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green") 
            table.add_column("Type", style="yellow")
            
            for key, value in business.items():
                table.add_row(key, str(value)[:50], str(type(value).__name__))
            
            console.print(table)
            
            # Check if email fields exist
            has_email_field = 'email' in business
            has_emails_field = 'emails' in business
            
            console.print(f"\n📧 Email field present: {'✅' if has_email_field else '❌'}")
            console.print(f"📧 Emails field present: {'✅' if has_emails_field else '❌'}")
            
            if has_emails_field:
                email_count = len(business.get('emails', []))
                console.print(f"📧 Email count: {email_count}")
        
        # Test Google Maps scraper
        console.print("\n[yellow]Testing Google Maps scraper with rating filter...[/yellow]")
        
        try:
            scraper = GoogleMapsScraper(headless=True)
            
            # Test rating filter method
            if hasattr(scraper, 'filter_businesses_by_website_potential'):
                console.print("✅ Rating filter method available")
            else:
                console.print("❌ Rating filter method missing")
                
            scraper.close()
            
        except Exception as e:
            console.print(f"⚠️ Google Maps scraper test failed: {e}")
        
        console.print("\n[bold green]🎉 Core functionality tests completed![/bold green]")
        
        # Show usage examples
        console.print("\n[bold cyan]💡 Usage Examples:[/bold cyan]")
        console.print("• Use sample data: [dim]python scripts/blf.py demo[/dim]")
        console.print("• Generate samples: [dim]python scripts/collect_real_data.py --generate-samples[/dim]")
        console.print("• Quick search: [dim]python quick_search/quick_all_cities_search.py --city marrakesh[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ Test failed: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")

if __name__ == "__main__":
    test_email_rating_features()
