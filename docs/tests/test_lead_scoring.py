#!/usr/bin/env python3
"""
Test Lead Scoring Logic
Demonstrates that businesses with 2-3 star ratings are prioritized as high opportunity leads.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from business_search import calculate_lead_score
from rich.console import Console
from rich.table import Table

console = Console()

def test_lead_scoring():
    """Test the lead scoring logic with various business scenarios."""
    
    console.print("[blue]🎯 Lead Scoring Test - Low Ratings = High Opportunity[/blue]")
    console.print("=" * 70)
    
    # Test businesses with different characteristics
    test_businesses = [
        {
            "name": "High-End Restaurant (4.8 stars, has website)",
            "rating": 4.8,
            "review_count": 150,
            "website": "https://example.com",
            "phone": "+212123456789",
            "category": "restaurant",
            "address": "Gueliz, Marrakech"
        },
        {
            "name": "Struggling Cafe (2.3 stars, no website)",
            "rating": 2.3,
            "review_count": 12,
            "website": None,
            "phone": "+212123456789",
            "category": "cafe",
            "address": "Medina, Marrakech"
        },
        {
            "name": "Average Hotel (3.2 stars, no website)",
            "rating": 3.2,
            "review_count": 34,
            "website": None,
            "phone": "+212123456789",
            "category": "hotel",
            "address": "Hivernage, Marrakech"
        },
        {
            "name": "New Business (no ratings, no website)",
            "rating": 0,
            "review_count": 0,
            "website": None,
            "phone": "+212123456789",
            "category": "shop",
            "address": "Majorelle, Marrakech"
        },
        {
            "name": "Popular Shop (4.5 stars, has website)",
            "rating": 4.5,
            "review_count": 89,
            "website": "https://shop.example.com",
            "phone": "+212123456789",
            "category": "shop",
            "address": "Gueliz, Marrakech"
        }
    ]
    
    # Calculate scores and show results
    table = Table(title="Lead Scoring Results")
    table.add_column("Business", style="cyan", no_wrap=True)
    table.add_column("Rating", justify="center")
    table.add_column("Website", justify="center")
    table.add_column("Reviews", justify="center")
    table.add_column("Lead Score", justify="center", style="bold")
    table.add_column("Priority", justify="center")
    
    scored_businesses = []
    for business in test_businesses:
        score = calculate_lead_score(business)
        scored_businesses.append((business, score))
    
    # Sort by score (highest first)
    scored_businesses.sort(key=lambda x: x[1], reverse=True)
    
    for business, score in scored_businesses:
        website_status = "✅" if business.get('website') else "❌"
        rating = f"{business['rating']:.1f}⭐" if business['rating'] > 0 else "No rating"
        
        # Determine priority based on score
        if score >= 80:
            priority = "[bold red]HIGH[/bold red]"
        elif score >= 60:
            priority = "[bold yellow]MEDIUM[/bold yellow]"
        else:
            priority = "[dim]LOW[/dim]"
        
        table.add_row(
            business['name'],
            rating,
            website_status,
            str(business['review_count']),
            f"{score}/100",
            priority
        )
    
    console.print(table)
    
    # Analysis
    console.print("\n[bold green]📊 Analysis:[/bold green]")
    console.print("• Businesses with 2-3 star ratings get +25 points (high opportunity)")
    console.print("• Businesses without websites get +30 points")
    console.print("• Businesses with few reviews (1-20) get +15 points")
    console.print("• High-rated businesses (4+ stars) get fewer points (already successful)")
    
    # Show the top lead
    top_business, top_score = scored_businesses[0]
    console.print(f"\n[bold]🎯 Top Lead:[/bold] {top_business['name']} (Score: {top_score}/100)")
    
    if top_business['rating'] >= 2.0 and top_business['rating'] <= 3.5:
        console.print("[green]✅ Confirms insight: Low-rated business is top priority![/green]")
    
    return scored_businesses

if __name__ == "__main__":
    test_lead_scoring()
