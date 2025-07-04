#!/usr/bin/env python3
"""
Business Lead Finder - Professional CLI Application
Find local businesses without websites for lead generation in Morocco.

Usage:
    blf                              # Interactive mode
    blf restaurants marrakech        # Quick search
    blf cafes casablanca 20          # Find 20 cafes
    blf hotels fez                   # Find hotels
    blf demo                         # Run demo
    blf --help                       # Show help
"""

import argparse
import sys
import os
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
import time
import json

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

console = Console()

try:
    from src.services.lead_service import BusinessLeadService
    from src.core.config import config, SEARCH_CONFIG
    from src.data.real_sources import BusinessData
    # Always import these utility functions
    from src.business_search import search_businesses_all_sources, calculate_lead_score
    from src.website_checker import enhanced_website_detection
    from src.utils import setup_logging, load_config
    SERVICES_AVAILABLE = True
    FULL_CLI_AVAILABLE = True
except ImportError as e:
    console.print(f"[red]Error importing services: {e}[/red]")
    console.print("[yellow]Falling back to basic functionality...[/yellow]")
    try:
        from src.business_search import search_businesses_all_sources, calculate_lead_score
        from src.website_checker import enhanced_website_detection
        from src.utils import setup_logging, load_config
        SERVICES_AVAILABLE = False
        FULL_CLI_AVAILABLE = True
    except ImportError as e2:
        console.print(f"[red]Critical error: {e2}[/red]")
        SERVICES_AVAILABLE = False
        FULL_CLI_AVAILABLE = False

def display_banner():
    """Display application banner."""
    banner = Panel.fit(
        "[bold cyan]BUSINESS LEAD FINDER[/bold cyan]\n"
        "[dim]Find businesses without websites in Morocco[/dim]\n\n"
        "[green]🎯 Smart lead scoring[/green]  [yellow]🔍 Enhanced detection[/yellow]\n"
        "[green]📊 French language support[/green]  [yellow]📈 Morocco patterns[/yellow]",
        border_style="blue"
    )
    console.print(banner)
    console.print()

async def run_interactive_mode():
    """Interactive mode with guided prompts."""
    display_banner()
    
    console.print("[bold blue]Welcome to Interactive Mode![/bold blue]")
    console.print("I'll help you find businesses without websites in Morocco.\n")
    
    # Get search parameters
    categories = ["restaurants", "cafes", "hotels", "shops", "services", "spas"]
    cities = ["Marrakech", "Casablanca", "Fez", "Rabat", "Tangier"]
    
    category = Prompt.ask(
        "What type of business are you looking for?", 
        choices=categories,
        default="restaurants"
    )
    
    city = Prompt.ask(
        "Which city?", 
        choices=cities,
        default="Marrakech"
    )
    
    max_results = IntPrompt.ask(
        "How many results?",
        default=10,
        show_default=True
    )
    
    console.print(f"\n[green]🔍 Searching for {category} in {city}...[/green]")
    
    # Run search
    if SERVICES_AVAILABLE:
        lead_service = BusinessLeadService()
        result = await lead_service.search_leads(category, city, max_results)
        display_results(result)
    else:
        # Fallback to old method
        await run_basic_search(category, city, max_results)
    
    # Ask if user wants to search again
    if Confirm.ask("\nSearch for another category?", default=True):
        await run_interactive_mode()
    else:
        console.print("\n[bold green]Thank you for using Business Lead Finder![/bold green]")

async def run_quick_search(category: str, location: str = "Marrakech", max_results: int = 10):
    """Quick search with parameters."""
    display_banner()
    
    console.print(f"[green]🔍 Searching for {category} in {location}...[/green]")
    
    if SERVICES_AVAILABLE:
        lead_service = BusinessLeadService()
        result = await lead_service.search_leads(category, location, max_results)
        display_results(result)
    else:
        await run_basic_search(category, location, max_results)

async def run_demo():
    """Run comprehensive demo showing all features."""
    display_banner()
    
    console.print("[bold blue]🚀 Running Business Lead Finder Demo[/bold blue]")
    console.print("This demo will showcase key features using real Moroccan businesses.\n")
    
    demo_searches = [
        ("restaurants", "Marrakech", 5),
        ("cafes", "Casablanca", 5),
        ("hotels", "Fez", 5)
    ]
    
    for category, city, max_results in demo_searches:
        console.print(f"[bold]--- Demo: {category.title()} in {city} ---[/bold]")
        
        if SERVICES_AVAILABLE:
            lead_service = BusinessLeadService()
            result = await lead_service.search_leads(category, city, max_results)
            display_results(result, demo_mode=True)
        else:
            await run_basic_search(category, city, max_results)
        
        if not Confirm.ask(f"\nContinue with next demo?", default=True):
            break
        console.print()
    
    console.print("[bold green]🎉 Demo completed![/bold green]")

def display_results(result, demo_mode: bool = False):
    """Display search results in a formatted table."""
    if not result or not result.businesses:
        console.print("[yellow]No businesses found. Try a different search term or location.[/yellow]")
        return
    
    # Summary panel
    summary = Panel(
        f"[bold]Found {result.total_found} businesses[/bold]\n"
        f"High priority leads: [red]{result.high_priority_count}[/red]\n"
        f"Without websites: [yellow]{result.no_website_count}[/yellow]\n"
        f"Average rating: [green]{result.avg_rating:.1f}⭐[/green]\n"
        f"Sources: {', '.join(result.sources_used)}",
        title="📊 Search Summary",
        border_style="green"
    )
    console.print(summary)
    console.print()
    
    # Results table
    table = Table(title="🎯 Business Leads")
    table.add_column("Business", style="cyan", no_wrap=True)
    table.add_column("Category", justify="center")
    table.add_column("Rating", justify="center")
    table.add_column("Website", justify="center")
    table.add_column("Score", justify="center", style="bold")
    table.add_column("Priority", justify="center")
    
    # Sort by lead score
    sorted_businesses = sorted(result.businesses, key=lambda x: getattr(x, 'lead_score', 0), reverse=True)
    
    # Show top results (limit for demo mode)
    display_count = min(10, len(sorted_businesses)) if demo_mode else len(sorted_businesses)
    
    for business in sorted_businesses[:display_count]:
        rating = f"{business.rating:.1f}⭐" if business.rating > 0 else "No rating"
        website = "✅" if business.website else "❌"
        
        lead_score = getattr(business, 'lead_score', 0)
        if lead_score >= 80:
            priority = "[bold red]HIGH[/bold red]"
        elif lead_score >= 60:
            priority = "[bold yellow]MEDIUM[/bold yellow]"
        else:
            priority = "[dim]LOW[/dim]"
        
        table.add_row(
            business.name[:30] + "..." if len(business.name) > 30 else business.name,
            business.category[:15],
            rating,
            website,
            f"{lead_score}/100",
            priority
        )
    
    console.print(table)
    
    # Save results
    save_results(result)

def save_results(result, filename: str = None):
    """Save results to JSON file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/business_leads_{timestamp}.json"
    
    # Create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)
    
    # Convert to serializable format
    data = {
        "timestamp": result.timestamp.isoformat(),
        "summary": {
            "total_found": result.total_found,
            "high_priority_count": result.high_priority_count,
            "no_website_count": result.no_website_count,
            "avg_rating": result.avg_rating,
            "sources_used": result.sources_used
        },
        "businesses": [
            {
                "name": b.name,
                "category": b.category,
                "address": b.address,
                "phone": b.phone,
                "website": b.website,
                "rating": b.rating,
                "review_count": b.review_count,
                "lead_score": getattr(b, 'lead_score', 0),
                "source": b.source
            }
            for b in result.businesses
        ]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    console.print(f"[dim]Results saved to: {filename}[/dim]")

async def run_basic_search(category: str, location: str, max_results: int):
    """Fallback basic search when services are not available."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Finding businesses...", total=None)
        
        # Use old method
        result = search_businesses_all_sources(category, location, max_results)
        
        # Handle both old list format and new LeadAnalysisResult format
        if hasattr(result, 'businesses'):
            # New format - LeadAnalysisResult object
            businesses = result.businesses
        else:
            # Old format - list of businesses
            businesses = result
        
        if businesses:
            # Calculate lead scores if not already present
            for business in businesses:
                if 'lead_score' not in business:
                    business['lead_score'] = calculate_lead_score(business)
            
            # Sort by score
            businesses.sort(key=lambda x: x['lead_score'], reverse=True)
            
            # Display basic table
            table = Table(title="Business Leads")
            table.add_column("Business", style="cyan")
            table.add_column("Rating", justify="center") 
            table.add_column("Website", justify="center")
            table.add_column("Score", justify="center")
            
            for business in businesses[:10]:  # Show top 10
                rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else "No rating"
                website = "✅" if business.get('website') else "❌"
                
                table.add_row(
                    business['name'][:30],
                    rating,
                    website,
                    f"{business['lead_score']}/100"
                )
            
            console.print(table)
        else:
            console.print("[yellow]No businesses found. Try a different search term or location.[/yellow]")

def show_help():
    """Show help information."""
    display_banner()
    
    help_text = """[bold blue]Business Lead Finder - Usage Guide[/bold blue]

[bold green]Quick Commands:[/bold green]
  [cyan]blf[/cyan]                              → Interactive mode
  [cyan]blf restaurants marrakech[/cyan]        → Search restaurants in Marrakech
  [cyan]blf cafes casablanca 20[/cyan]          → Find 20 cafes in Casablanca    
  [cyan]blf hotels fez[/cyan]                   → Search hotels in Fez
  [cyan]blf demo[/cyan]                         → Run comprehensive demo

[bold green]Supported Categories:[/bold green]
  restaurants, cafes, hotels, shops, services, spas

[bold green]Supported Cities:[/bold green]
  Marrakech, Casablanca, Fez, Rabat, Tangier

[bold green]Examples:[/bold green]
  [cyan]blf restaurants[/cyan]              → Restaurants in Marrakech (default)
  [cyan]blf cafes casablanca[/cyan]         → Cafes in Casablanca
  [cyan]blf hotels fez 15[/cyan]            → 15 hotels in Fez
  [cyan]blf demo[/cyan]                     → Full demo with all features

[bold green]Features:[/bold green]
  🎯 Smart lead scoring (2-3 star businesses = high opportunity)
  � Enhanced website detection with French patterns
  📊 Morocco-specific domain patterns (.ma, .co.ma)
  📈 Real-time business analysis and scoring
  📁 Export results to JSON files
"""
    console.print(help_text)

async def main():
    """Main entry point."""
    # Set up logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/blf.log'),
            logging.StreamHandler()
        ]
    )
    
    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments - interactive mode
        await run_interactive_mode()
    elif len(sys.argv) >= 2:
        if sys.argv[1] in ['--help', '-h', 'help']:
            show_help()
        elif sys.argv[1] == 'demo':
            await run_demo()
        else:
            # Quick search: blf category [location] [max_results]
            category = sys.argv[1]
            location = sys.argv[2] if len(sys.argv) > 2 else "Marrakech"
            max_results = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 10
            
            await run_quick_search(category, location, max_results)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Search cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logging.exception("Unhandled exception in main")

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
        
        try:
            if SERVICES_AVAILABLE:
                # Use the new service
                lead_service = BusinessLeadService()
                result = asyncio.run(lead_service.search_leads(category, location, max_results))
                
                # Extract businesses from LeadAnalysisResult
                if hasattr(result, 'businesses'):
                    businesses = result.businesses
                else:
                    businesses = result
            else:
                # Use the legacy search function
                businesses = search_businesses_all_sources(category, location, max_results)
        except NameError as e:
            console.print(f"[red]Error: {e}[/red]")
            console.print("[yellow]Some modules may not be properly imported.[/yellow]")
            return
        
        progress.update(search_task, advance=50)
        
        # Scoring task
        progress.update(search_task, description="Analyzing websites and scoring leads...")
        scored_businesses = []
        for business in businesses:
            # Handle both BusinessData objects and dictionaries
            if hasattr(business, '__dict__'):
                # Convert BusinessData to dictionary for scoring
                business_dict = {
                    'name': business.name,
                    'category': business.category,
                    'address': business.address,
                    'phone': business.phone,
                    'website': business.website,
                    'rating': business.rating,
                    'review_count': business.review_count,
                    'latitude': business.latitude,
                    'longitude': business.longitude,
                    'source': business.source
                }
                business_dict['lead_score'] = calculate_lead_score(business_dict)
                scored_businesses.append(business_dict)
            else:
                # Dictionary format
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
    table.add_column("City", style="dim", justify="center")
    table.add_column("Rating", justify="center")
    table.add_column("Website", justify="center")
    table.add_column("Phone", justify="center")
    table.add_column("Lead Score", justify="center", style="bold")
    table.add_column("Priority", justify="center")
    
    for business in scored_businesses[:20]:  # Show top 20
        rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else "No rating"
        website = "✅" if business.get('website') else "❌"
        phone = "✅" if business.get('phone') else "❌"
        
        # Extract city from address or use the search location
        city = location
        if business.get('address'):
            # Try to extract city from address
            address_parts = business['address'].split(',')
            if len(address_parts) > 1:
                # Usually city is in the last parts of address
                potential_city = address_parts[-2].strip() if len(address_parts) > 2 else address_parts[-1].strip()
                if potential_city and len(potential_city) < 30:  # Reasonable city name length
                    city = potential_city
        
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
            city[:15],  # Limit city display length
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
    
    console.print(f"\n[bold]📊 Lead Analysis ({len(scored_businesses)} businesses found):[/bold]")
    console.print(f"• High priority leads: [bold red]{len(high_leads)}[/bold red]")
    console.print(f"• Businesses without websites: [bold yellow]{len(no_website)}[/bold yellow]")
    console.print(f"• Low-rated businesses (2-3.5⭐): [bold yellow]{len(low_rated)}[/bold yellow]")
    
    if len(scored_businesses) > 20:
        console.print(f"[dim]Showing top 20 results out of {len(scored_businesses)} total businesses.[/dim]")
    
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
    
    if not SERVICES_AVAILABLE:
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
