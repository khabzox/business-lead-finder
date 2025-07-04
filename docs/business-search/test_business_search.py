#!/usr/bin/env python3
"""
Business Search Test
Demonstrates searching for businesses and analyzing their lead potential.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from business_search import search_businesses_all_sources, calculate_lead_score
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

def test_business_search():
    """Test business search functionality with lead scoring."""
    
    console.print("[blue]🔍 Business Search & Lead Scoring Test[/blue]")
    console.print("=" * 60)
    
    # Test different search scenarios
    test_searches = [
        {
            "query": "restaurant",
            "location": "Marrakech",
            "max_results": 10,
            "description": "Restaurants in Marrakech"
        },
        {
            "query": "cafe",
            "location": "Casablanca", 
            "max_results": 10,
            "description": "Cafes in Casablanca"
        },
        {
            "query": "hotel",
            "location": "Fez",
            "max_results": 10,
            "description": "Hotels in Fez"
        }
    ]
    
    all_results = []
    
    for search in test_searches:
        console.print(f"\n[yellow]🔍 Searching: {search['description']}[/yellow]")
        
        with Progress() as progress:
            task = progress.add_task(f"Searching {search['query']}...", total=100)
            
            # Perform search
            businesses = search_businesses_all_sources(
                query=search['query'],
                location=search['location'],
                max_results=search['max_results']
            )
            
            progress.update(task, advance=50)
            
            # Calculate lead scores
            scored_businesses = []
            for business in businesses:
                business['lead_score'] = calculate_lead_score(business)
                scored_businesses.append(business)
            
            progress.update(task, advance=50)
        
        # Sort by lead score
        scored_businesses.sort(key=lambda x: x['lead_score'], reverse=True)
        all_results.extend(scored_businesses)
        
        console.print(f"Found {len(businesses)} businesses")
        
        # Show top 3 leads
        if scored_businesses:
            console.print("Top 3 leads:")
            for i, business in enumerate(scored_businesses[:3]):
                rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else "No rating"
                website = "✅" if business.get('website') else "❌"
                console.print(f"  {i+1}. {business['name']} - Score: {business['lead_score']}/100 - {rating} - Website: {website}")
    
    # Overall analysis
    console.print(f"\n[bold green]📊 Overall Analysis[/bold green]")
    
    if all_results:
        # Lead score distribution
        high_leads = [b for b in all_results if b['lead_score'] >= 80]
        medium_leads = [b for b in all_results if 60 <= b['lead_score'] < 80]
        low_leads = [b for b in all_results if b['lead_score'] < 60]
        
        console.print(f"Total businesses found: {len(all_results)}")
        console.print(f"High priority leads (80+): {len(high_leads)}")
        console.print(f"Medium priority leads (60-79): {len(medium_leads)}")
        console.print(f"Low priority leads (<60): {len(low_leads)}")
        
        # Website analysis
        no_website = [b for b in all_results if not b.get('website')]
        has_website = [b for b in all_results if b.get('website')]
        
        console.print(f"\nWebsite presence:")
        console.print(f"No website: {len(no_website)} ({len(no_website)/len(all_results)*100:.1f}%)")
        console.print(f"Has website: {len(has_website)} ({len(has_website)/len(all_results)*100:.1f}%)")
        
        # Rating analysis
        low_rated = [b for b in all_results if b.get('rating') and 2.0 <= b['rating'] <= 3.5]
        high_rated = [b for b in all_results if b.get('rating') and b['rating'] > 4.0]
        
        console.print(f"\nRating analysis:")
        console.print(f"Low rated (2-3.5 stars): {len(low_rated)}")
        console.print(f"High rated (4+ stars): {len(high_rated)}")
        
        # Top leads table
        console.print(f"\n[bold]🎯 Top 10 Leads Overall[/bold]")
        all_results.sort(key=lambda x: x['lead_score'], reverse=True)
        
        table = Table(title="Top Leads")
        table.add_column("Business", style="cyan")
        table.add_column("Category", justify="center")
        table.add_column("Rating", justify="center")
        table.add_column("Website", justify="center")
        table.add_column("Score", justify="center", style="bold")
        
        for business in all_results[:10]:
            rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else "No rating"
            website = "✅" if business.get('website') else "❌"
            
            table.add_row(
                business['name'][:30],
                business.get('category', 'N/A')[:15],
                rating,
                website,
                f"{business['lead_score']}/100"
            )
        
        console.print(table)
    
    else:
        console.print("No businesses found. Check your search parameters.")

if __name__ == "__main__":
    test_business_search()
