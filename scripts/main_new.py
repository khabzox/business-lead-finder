#!/usr/bin/env python3
"""
Business Lead Finder - Professional CLI Application
Find local businesses without websites for lead generation in Morocco.

Usage:
    python main.py                              # Interactive mode
    python main.py restaurants marrakech        # Quick search
    python main.py cafes casablanca             # Find cafes
    python main.py hotels fez                   # Find hotels
    python main.py demo                         # Run demo
    python main.py --help                       # Show help
"""

import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import time

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

console = Console()

try:
    from business_search import search_businesses_all_sources, calculate_lead_score
    from website_checker import enhanced_website_detection
    from utils import setup_logging, load_config
    FULL_CLI_AVAILABLE = True
except ImportError as e:
    console.print(f"[red]Error importing modules: {e}[/red]")
    FULL_CLI_AVAILABLE = False

def display_banner():
    """Display application banner."""
    console.print()
    console.print("[bold blue]" + "="*60 + "[/bold blue]")
    console.print("[bold cyan]            BUSINESS LEAD FINDER            [/bold cyan]")
    console.print("[dim]     Find businesses without websites in Morocco     [/dim]")
    console.print()
    console.print("[green]🎯 Smart lead scoring[/green]  [yellow]📊 French language support[/yellow]")
    console.print("[green]🔍 Enhanced detection[/green]  [yellow]📈 Morocco-specific patterns[/yellow]")
    console.print("[bold blue]" + "="*60 + "[/bold blue]")
    console.print()

def quick_search(category: str, location: str, max_results: int = 10):
    """Perform a quick search with professional output."""
    
    console.print(f"[bold]🔍 Searching for {category} in {location}...[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        
        # Search task
        search_task = progress.add_task("Finding businesses...", total=100)
        businesses = search_businesses_all_sources(category, location, max_results)
        progress.update(search_task, advance=50)
        
        # Scoring task
        progress.update(search_task, description="Analyzing websites and scoring leads...")
        scored_businesses = []
        for business in businesses:
            business['lead_score'] = calculate_lead_score(business)
            scored_businesses.append(business)
        
        progress.update(search_task, advance=50, description="Complete!")
        time.sleep(0.5)  # Brief pause to show completion
    
    if not scored_businesses:
        console.print("[yellow]No businesses found. Try a different search term or location.[/yellow]")
        return
    
    # Sort by lead score
    scored_businesses.sort(key=lambda x: x['lead_score'], reverse=True)
    
    # Display results
    console.print(f"[bold green]✅ Found {len(scored_businesses)} businesses[/bold green]")
    
    # Create results table
    table = Table(title=f"{category.title()} in {location.title()} - Lead Analysis")
    table.add_column("Business", style="cyan", no_wrap=True)
    table.add_column("Rating", justify="center")
    table.add_column("Website", justify="center")
    table.add_column("Phone", justify="center")
    table.add_column("Lead Score", justify="center", style="bold")
    table.add_column("Priority", justify="center")
    
    for business in scored_businesses[:10]:  # Show top 10
        rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else "No rating"
        website = "✅" if business.get('website') else "❌"
        phone = "✅" if business.get('phone') else "❌"
        
        # Priority based on score
        score = business['lead_score']
        if score >= 80:
            priority = "[bold red]HIGH[/bold red]"
        elif score >= 60:
            priority = "[bold yellow]MEDIUM[/bold yellow]"
        else:
            priority = "[dim]LOW[/dim]"
        
        table.add_row(
            business['name'][:30],
            rating,
            website,
            phone,
            f"{score}/100",
            priority
        )
    
    console.print(table)
    
    # Summary analysis
    high_leads = [b for b in scored_businesses if b['lead_score'] >= 80]
    no_website = [b for b in scored_businesses if not b.get('website')]
    low_rated = [b for b in scored_businesses if b.get('rating') and 2.0 <= b['rating'] <= 3.5]
    
    console.print(f"\n[bold]📊 Lead Analysis:[/bold]")
    console.print(f"• High priority leads: [bold red]{len(high_leads)}[/bold red]")
    console.print(f"• Businesses without websites: [bold yellow]{len(no_website)}[/bold yellow]")
    console.print(f"• Low-rated businesses (2-3.5⭐): [bold yellow]{len(low_rated)}[/bold yellow]")
    
    if high_leads:
        console.print(f"\n[bold green]🎯 Top Opportunity:[/bold green] {high_leads[0]['name']}")
        console.print(f"   Rating: {high_leads[0].get('rating', 'N/A')}⭐ | Website: {'Yes' if high_leads[0].get('website') else 'No'}")
    
    # Export option
    if Confirm.ask("\nWould you like to export these results?"):
        export_results(scored_businesses, category, location)

def export_results(businesses, category, location):
    """Export results to file."""
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/{category}_{location}_{timestamp}.json"
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(businesses, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✅ Results exported to {filename}[/green]")

def run_demo():
    """Run a comprehensive demo."""
    console.print("\n[bold blue]🚀 Running Business Lead Finder Demo[/bold blue]")
    console.print("This demo will showcase key features using real Moroccan businesses.\n")
    
    demos = [
        ("restaurants", "Marrakech"),
        ("cafes", "Casablanca"),
        ("hotels", "Fez")
    ]
    
    for category, location in demos:
        console.print(f"[dim]--- Demo: {category.title()} in {location} ---[/dim]")
        quick_search(category, location, 5)
        console.print()
        
        if not Confirm.ask("Continue with next demo?", default=True):
            break
    
    console.print("[bold green]🎉 Demo completed![/bold green]")

def interactive_mode():
    """Run interactive mode."""
    console.print("[bold]Welcome to Interactive Mode![/bold]")
    console.print("I'll help you find businesses without websites in Morocco.\n")
    
    while True:
        category = Prompt.ask(
            "What type of business are you looking for?",
            choices=["restaurants", "cafes", "hotels", "shops", "services", "spas"],
            default="restaurants"
        )
        
        location = Prompt.ask(
            "Which city?",
            choices=["Marrakech", "Casablanca", "Fez", "Rabat", "Tangier"],
            default="Marrakech"
        )
        
        max_results = int(Prompt.ask("How many results?", default="10"))
        
        quick_search(category, location, max_results)
        
        if not Confirm.ask("\nSearch for another category?", default=True):
            break
    
    console.print("\n[bold green]Thank you for using Business Lead Finder![/bold green]")

def show_help():
    """Show help information."""
    help_text = """
[bold blue]Business Lead Finder - Usage Guide[/bold blue]

[bold]Quick Commands:[/bold]
  python main.py                           → Interactive mode
  python main.py restaurants marrakech     → Search restaurants in Marrakech
  python main.py cafes casablanca 20       → Find 20 cafes in Casablanca
  python main.py hotels fez                → Search hotels in Fez
  python main.py demo                      → Run comprehensive demo

[bold]Supported Categories:[/bold]
  restaurants, cafes, hotels, shops, services, spas

[bold]Supported Cities:[/bold]
  Marrakech, Casablanca, Fez, Rabat, Tangier

[bold]Examples:[/bold]
  python main.py restaurants              → Restaurants in Marrakech (default)
  python main.py cafes casablanca         → Cafes in Casablanca  
  python main.py hotels fez 15            → 15 hotels in Fez
  python main.py demo                     → Full demo with all features

[bold]Features:[/bold]
  🎯 Smart lead scoring (2-3 star businesses = high opportunity)
  🔍 Enhanced website detection with French patterns
  📊 Morocco-specific domain patterns (.ma, .co.ma)
  📈 Real-time business analysis and scoring
  📁 Export results to JSON files
"""
    console.print(help_text)

def main():
    """Main entry point with smooth CLI experience."""
    
    if not FULL_CLI_AVAILABLE:
        console.print("[red]❌ Required modules not available. Please check installation.[/red]")
        sys.exit(1)
    
    display_banner()
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        interactive_mode()
        return
    
    # Check for simple commands
    args = sys.argv[1:]
    
    if args[0] in ['--help', '-h', 'help']:
        show_help()
        return
    
    if args[0] == 'demo':
        run_demo()
        return
    
    # Simple search commands (category location [max_results])
    if len(args) >= 2:
        category = args[0]
        location = args[1]
        max_results = int(args[2]) if len(args) > 2 else 10
        quick_search(category, location, max_results)
        return
    
    # Single argument - assume it's a category for Marrakech
    if len(args) == 1:
        category = args[0]
        if category in ['demo', 'help']:
            # Already handled above
            return
        quick_search(category, "Marrakech", 10)
        return
    
    # Fallback to interactive mode
    interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        sys.exit(1)
