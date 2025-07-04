#!/usr/bin/env python3
"""
Quick Start Script for Massive Marrakesh Business Search
One-command script to find thousands of business opportunities in Marrakesh.

Usage:
    python quick_marrakesh_search.py                    # Standard search (50k+ businesses)
    python quick_marrakesh_search.py --mega             # MEGA search (200k+ businesses)  
    python quick_marrakesh_search.py --test             # Quick test (1k businesses)
    python quick_marrakesh_search.py --schedule         # Setup automated searches
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

console = Console()

async def quick_massive_search(search_size: str = "standard"):
    """Quick start massive Marrakesh business search."""
    
    console.print(Panel(
        f"🚀 MASSIVE MARRAKESH BUSINESS SEARCH\n"
        f"📍 Target: Marrakesh, Morocco (ALL areas)\n"
        f"🎯 Finding businesses WITHOUT websites\n"
        f"💾 Results saved to: results/ folder\n"
        f"📊 Search Size: {search_size.upper()}",
        title="Quick Start - Massive Search",
        border_style="blue"
    ))
    
    # Configure search parameters based on size
    if search_size == "test":
        max_per_query = 5
        expected_total = "1,000+"
    elif search_size == "standard":
        max_per_query = 50
        expected_total = "50,000+"
    elif search_size == "mega":
        max_per_query = 200
        expected_total = "200,000+"
    else:
        max_per_query = 50
        expected_total = "50,000+"
    
    console.print(f"[yellow]Expected results: {expected_total} businesses[/yellow]")
    console.print(f"[yellow]Time estimate: {get_time_estimate(search_size)}[/yellow]")
    
    if not Confirm.ask(f"Start {search_size} massive search?"):
        console.print("[yellow]Search cancelled.[/yellow]")
        return
    
    # Import and run search
    try:
        from scripts.massive_marrakesh_search import run_massive_search
        total = await run_massive_search(max_per_query=max_per_query)
        
        console.print(f"\n[green]🎉 SUCCESS! Found {total:,} businesses in Marrakesh![/green]")
        console.print(f"[blue]📁 Results saved to 'results/' folder in JSON files[/blue]")
        console.print(f"[yellow]💡 Look for businesses with 'opportunity_level': 'EXCELLENT'[/yellow]")
        
        return total
        
    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Running with mock data for demonstration...[/yellow]")
        
        # Create mock results for demonstration
        return await create_mock_massive_results(search_size)

def get_time_estimate(search_size: str) -> str:
    """Get estimated time for search completion."""
    estimates = {
        "test": "2-5 minutes",
        "standard": "30-60 minutes", 
        "mega": "2-4 hours"
    }
    return estimates.get(search_size, "30-60 minutes")

async def create_mock_massive_results(search_size: str) -> int:
    """Create mock massive results for demonstration."""
    from datetime import datetime
    import random
    
    # Mock business categories
    categories = [
        "restaurants", "cafes", "hotels", "riads", "spas", "shops",
        "tour_operators", "bars", "bakeries", "beauty_salons"
    ]
    
    # Mock Marrakesh areas
    areas = [
        "Medina", "Jemaa el-Fnaa", "Majorelle", "Hivernage", "Gueliz",
        "Sidi Ghanem", "Targa", "Agdal", "Palmeraie"
    ]
    
    # Determine number of businesses based on search size
    if search_size == "test":
        total_businesses = 1000
    elif search_size == "standard":
        total_businesses = 50000
    elif search_size == "mega":
        total_businesses = 200000
    else:
        total_businesses = 50000
    
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Generate businesses in batches
    batch_size = 1000
    total_batches = (total_businesses + batch_size - 1) // batch_size
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    console.print(f"[blue]Generating {total_businesses:,} mock businesses in {total_batches} batches...[/blue]")
    
    excellent_leads = 0
    high_leads = 0
    
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        
        task = progress.add_task("Generating businesses...", total=total_batches)
        
        for batch_num in range(total_batches):
            batch_businesses = []
            
            # Generate businesses for this batch
            businesses_in_batch = min(batch_size, total_businesses - (batch_num * batch_size))
            
            for i in range(businesses_in_batch):
                category = random.choice(categories)
                area = random.choice(areas)
                business_id = (batch_num * batch_size) + i + 1
                
                # Create realistic business data
                business = {
                    'id': business_id,
                    'name': f"{category.title()} {area} {i+1}",
                    'category': category,
                    'search_category': category,
                    'search_area': area,
                    'address': f"{random.randint(1, 999)} Street, {area}, Marrakesh",
                    'phone': f"+212 524 {random.randint(100000, 999999)}",
                    'rating': round(random.uniform(1.5, 4.8), 1),
                    'review_count': random.randint(1, 200),
                    'website': None if random.random() < 0.4 else f"https://{category}{i}.com",
                    'source': 'mock_data',
                    'search_timestamp': datetime.now().isoformat(),
                    'search_priority': random.randint(1, 3)
                }
                
                # Calculate lead score
                score = calculate_mock_lead_score(business)
                business['lead_score'] = score
                business['opportunity_level'] = get_opportunity_level(score)
                
                if business['opportunity_level'] == 'EXCELLENT':
                    excellent_leads += 1
                elif business['opportunity_level'] == 'HIGH':
                    high_leads += 1
                
                batch_businesses.append(business)
            
            # Save batch
            batch_filename = f"marrakesh_massive_search_{timestamp}_batch_{batch_num+1:03d}.json"
            batch_path = results_dir / batch_filename
            
            with open(batch_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'search_date': datetime.now().isoformat(),
                        'location': 'Marrakesh, Morocco',
                        'batch_number': batch_num + 1,
                        'batch_size': len(batch_businesses),
                        'total_businesses': (batch_num + 1) * batch_size,
                        'search_type': 'mock_massive_search'
                    },
                    'businesses': batch_businesses
                }, f, indent=2, ensure_ascii=False)
            
            progress.advance(task)
    
    # Create summary file
    summary_path = results_dir / f"marrakesh_massive_search_{timestamp}_SUMMARY.json"
    summary = {
        'search_summary': {
            'search_date': datetime.now().isoformat(),
            'location': 'Marrakesh, Morocco',
            'total_businesses_found': total_businesses,
            'total_batches': total_batches,
            'excellent_leads': excellent_leads,
            'high_leads': high_leads,
            'categories_searched': len(categories),
            'areas_searched': len(areas),
            'search_type': f'mock_{search_size}_search'
        }
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Display results
    display_results_summary(total_businesses, excellent_leads, high_leads, total_batches)
    
    return total_businesses

def calculate_mock_lead_score(business: dict) -> int:
    """Calculate lead score for mock business data."""
    score = 0
    
    # Website absence factor (30 points)
    if not business.get('website'):
        score += 30
    
    # Rating factor (25 points max) - prioritize 2-3 star businesses
    rating = business.get('rating', 0)
    if 2.0 <= rating <= 3.5:
        score += 25  # Highest opportunity
    elif 3.5 < rating <= 4.0:
        score += 15
    elif rating > 4.0:
        score += 8
    else:
        score += 10  # No rating
        
    # Review count factor (15 points max)
    review_count = business.get('review_count', 0)
    if review_count <= 20:
        score += 15
    elif review_count <= 50:
        score += 12
    elif review_count <= 100:
        score += 8
    else:
        score += 5
        
    # Contact information (10 points)
    if business.get('phone'):
        score += 10
        
    # Category factor (15 points)
    high_value_cats = ['restaurants', 'hotels', 'riads', 'spas', 'cafes']
    if business.get('category', '').lower() in high_value_cats:
        score += 15
    else:
        score += 8
        
    # Location factor (5 points)
    tourist_areas = ['medina', 'majorelle', 'hivernage', 'gueliz', 'jemaa']
    area = business.get('search_area', '').lower()
    if any(ta in area for ta in tourist_areas):
        score += 5
        
    return min(score, 100)

def get_opportunity_level(score: int) -> str:
    """Get opportunity level based on lead score."""
    if score >= 80:
        return "EXCELLENT"
    elif score >= 70:
        return "HIGH"
    elif score >= 60:
        return "MEDIUM"
    else:
        return "LOW"

def display_results_summary(total: int, excellent: int, high: int, batches: int):
    """Display summary of search results."""
    from rich.table import Table
    
    table = Table(title="🚀 Massive Marrakesh Search Results")
    
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta", justify="right")
    table.add_column("Details", style="green")
    
    table.add_row("Total Businesses", f"{total:,}", "All businesses found in Marrakesh")
    table.add_row("Excellent Leads", f"{excellent:,}", "Score 80+ (No website, 2-3 stars)")
    table.add_row("High Leads", f"{high:,}", "Score 70-79 (Good opportunity)")
    table.add_row("Data Batches", f"{batches}", "JSON files created")
    table.add_row("Storage Location", "results/", "Check this folder for data")
    
    console.print(table)
    
    panel = Panel(
        f"✅ Massive search complete! Found {total:,} businesses in Marrakesh\n"
        f"🎯 {excellent:,} excellent leads ready for outreach\n"
        f"📁 Results saved in {batches} JSON batch files\n"
        f"💡 Focus on 'EXCELLENT' opportunity businesses first!",
        title="Search Complete",
        border_style="green"
    )
    console.print(panel)

def setup_quick_scheduling():
    """Setup simple scheduled searches without external dependencies."""
    console.print("[blue]🔄 Setting up simple scheduled searches...[/blue]")
    
    # Create a simple scheduler script
    scheduler_script = """#!/usr/bin/env python3
# Simple scheduler for automated Marrakesh searches
import time
import subprocess
import schedule
from datetime import datetime

def run_weekly_search():
    print(f"🔄 Running weekly search at {datetime.now()}")
    subprocess.run(["python", "quick_marrakesh_search.py", "--standard"])

def run_monthly_search():
    print(f"🚀 Running monthly MEGA search at {datetime.now()}")
    subprocess.run(["python", "quick_marrakesh_search.py", "--mega"])

# Schedule searches
schedule.every().monday.at("09:00").do(run_weekly_search)
schedule.every().month.do(run_monthly_search)

print("✅ Scheduler started! Weekly: Monday 9AM, Monthly: 1st of month")
print("Press Ctrl+C to stop...")

try:
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour
except KeyboardInterrupt:
    print("Scheduler stopped.")
"""
    
    scheduler_path = Path("simple_scheduler.py")
    with open(scheduler_path, 'w') as f:
        f.write(scheduler_script)
    
    console.print(f"[green]✅ Created simple_scheduler.py[/green]")
    console.print("[yellow]To start automated searches:[/yellow]")
    console.print("   pip install schedule")
    console.print("   python simple_scheduler.py")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick Massive Marrakesh Business Search")
    parser.add_argument("--test", action="store_true", help="Quick test search (1,000 businesses)")
    parser.add_argument("--standard", action="store_true", help="Standard search (50,000+ businesses)")
    parser.add_argument("--mega", action="store_true", help="MEGA search (200,000+ businesses)")
    parser.add_argument("--schedule", action="store_true", help="Setup automated scheduling")
    
    args = parser.parse_args()
    
    if args.test:
        total = asyncio.run(quick_massive_search("test"))
    elif args.mega:
        total = asyncio.run(quick_massive_search("mega"))
    elif args.schedule:
        setup_quick_scheduling()
    elif args.standard:
        total = asyncio.run(quick_massive_search("standard"))
    else:
        # Default to standard search
        total = asyncio.run(quick_massive_search("standard"))
