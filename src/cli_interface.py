"""
CLI Interface Module for Business Lead Finder
Handles command-line interface commands and user interactions.
"""

import argparse
import sys
import logging
import requests  # Add missing import
from typing import Dict, Any, Optional, List
from pathlib import Path

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import rich components with fallback
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    logger.warning("Rich library not available, falling back to basic output")
    RICH_AVAILABLE = False

# Import local modules with proper error handling
try:
    from .business_search import search_businesses_all_sources, remove_duplicates
    from .website_checker import check_website_status
    from .report_generator import generate_report
    from .data_processor import export_data, analyze_leads
    from .utils import validate_location, validate_categories
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

# Google Maps scraping (optional)
try:
    from .google_maps_scraper import search_google_maps_business
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    logger.info("Google Maps scraper not available - install selenium for enhanced features")
    GOOGLE_MAPS_AVAILABLE = False

# Initialize console with fallback
if RICH_AVAILABLE:
    console = Console()
else:
    # Fallback console functions
    def console_print(*args, **kwargs):
        print(*args)
    
    # Create a simple namespace for console functions
    console = type('Console', (), {'print': console_print})()

def search_google_maps_businesses(query: str, location: str, max_results: int = 50, headless: bool = True, rating_filter: str = "low") -> List[Dict[str, Any]]:
    """
    Wrapper function for Google Maps business search with intelligent filtering.
    
    Args:
        query: Business type
        location: Location to search
        max_results: Maximum results
        headless: Run browser headless
        rating_filter: "low" (0-4.0 ratings - likely no website), "high" (4.5+), "all"
    """
    if not GOOGLE_MAPS_AVAILABLE:
        console.print("[yellow]⚠️ Google Maps scraping not available. Install selenium and chrome driver.[/yellow]")
        return []
    
    try:
        from .google_maps_scraper import search_google_maps_business
        businesses = search_google_maps_business(query, location, max_results, rating_filter)
        return businesses
            
    except Exception as e:
        console.print(f"[red]❌ Google Maps scraping failed: {e}[/red]")
        return []

def create_cli_parser() -> argparse.ArgumentParser:
    """Create command line interface parser."""
    parser = argparse.ArgumentParser(
        description='Business Lead Finder - Find businesses without websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py search --location "Marrakesh, Morocco" --categories restaurants --filter no-website
  python main.py search --location "Casablanca, Morocco" --categories hotels spas --ai-analysis
  python main.py search --location "Rabat, Morocco" --categories cafes --filter bad-website --sort-by rating
  python main.py search --location "Fez, Morocco" --categories restaurants --use-google-maps
  python main.py search --location "Tangier, Morocco" --categories spas --google-maps-only --max-results 30
  python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
  python main.py report --input data/leads.json --output results/report.html
  python main.py export --format csv --output results/leads.csv --filter "no_website=true"
  python main.py analyze --input data/leads.json
  python main.py interactive
        '''
    )
    
    # Global options
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output except errors')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for businesses')
    search_parser.add_argument('--location', '-l', required=True, help='Location to search (e.g., "Marrakesh, Morocco")')
    search_parser.add_argument('--categories', '-c', nargs='+', required=True, help='Business categories to search')
    search_parser.add_argument('--max-results', '-m', type=int, default=50, help='Maximum results per category')
    search_parser.add_argument('--output', '-o', help='Output file path')
    search_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    search_parser.add_argument('--filter', choices=['no-website', 'bad-website', 'all'], default='all', 
                             help='Filter results: no-website (no website), bad-website (poor website), all (no filter)')
    search_parser.add_argument('--ai-analysis', action='store_true', help='Enable AI-powered analysis with Groq')
    search_parser.add_argument('--sort-by', choices=['lead-score', 'rating', 'name'], default='lead-score',
                             help='Sort results by specified field')
    search_parser.add_argument('--use-google-maps', action='store_true', 
                             help='Use Google Maps scraping for enhanced business discovery with emails (FREE method)')
    search_parser.add_argument('--google-maps-only', action='store_true',
                             help='Use ONLY Google Maps scraping (no other sources)')
    search_parser.add_argument('--headless', action='store_true', default=True,
                             help='Run Google Maps scraper in headless mode (default: True)')
    search_parser.add_argument('--demo', action='store_true',
                             help='Use demo/sample data for testing the system')
    search_parser.add_argument('--rating-filter', choices=['low', 'high', 'all'], default='low',
                             help='Google Maps rating filter: low (0-4.0), high (4.5+), all (no filter)')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if a business has a website')
    check_parser.add_argument('--business-name', '-n', required=True, help='Business name')
    check_parser.add_argument('--phone', '-p', help='Business phone number')
    check_parser.add_argument('--address', '-a', help='Business address')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate comprehensive report')
    report_parser.add_argument('--input', '-i', required=True, help='Input data file path')
    report_parser.add_argument('--output', '-o', help='Output report file path')
    report_parser.add_argument('--format', choices=['html', 'pdf', 'json'], default='html', help='Report format')
    report_parser.add_argument('--template', help='Report template to use')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to various formats')
    export_parser.add_argument('--input', '-i', required=True, help='Input data file path')
    export_parser.add_argument('--output', '-o', required=True, help='Output file path')
    export_parser.add_argument('--format', choices=['csv', 'json', 'xlsx', 'vcf'], required=True, help='Export format')
    export_parser.add_argument('--filter', help='Filter criteria (e.g., "no_website=true")')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze existing lead data')
    analyze_parser.add_argument('--input', '-i', required=True, help='Input data file path')
    analyze_parser.add_argument('--output', '-o', help='Output analysis file path')
    analyze_parser.add_argument('--metrics', nargs='+', help='Specific metrics to analyze')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    
    return parser

def handle_cli_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle CLI command execution."""
    try:
        if args.command == 'search':
            return handle_search_command(args, config)
        elif args.command == 'check':
            return handle_check_command(args, config)
        elif args.command == 'report':
            return handle_report_command(args, config)
        elif args.command == 'export':
            return handle_export_command(args, config)
        elif args.command == 'analyze':
            return handle_analyze_command(args, config)
        elif args.command == 'interactive':
            return handle_interactive_command(args, config)
        else:
            console.print("[red]Unknown command. Use --help for available commands.[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error executing command: {e}[/red]")
        return False

def handle_search_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle search command with enhanced filtering, AI analysis, and Google Maps scraping."""
    console.print(f"[blue]🔍 Searching for businesses in: {args.location}[/blue]")
    console.print(f"[blue]📊 Categories: {', '.join(args.categories)}[/blue]")
    console.print(f"[blue]🎯 Filter: {args.filter}[/blue]")
    
    # Check if demo mode is enabled
    if args.demo:
        console.print("[yellow]🎪 Demo Mode: Using sample data for testing[/yellow]")
        return handle_demo_search(args, config)
    
    # Display search method info
    if args.google_maps_only:
        console.print("[blue]🗺️ Search Method: Google Maps ONLY (with email discovery)[/blue]")
        console.print(f"[blue]⭐ Rating Filter: {args.rating_filter} ratings ({'0-4.0' if args.rating_filter == 'low' else '4.5+' if args.rating_filter == 'high' else 'all'})[/blue]")
    elif args.use_google_maps:
        console.print("[blue]🔄 Search Method: Combined (Standard + Google Maps)[/blue]")
        console.print(f"[blue]⭐ Google Maps Rating Filter: {args.rating_filter} ratings[/blue]")
    else:
        console.print("[blue]🔍 Search Method: Standard sources[/blue]")
    
    if args.ai_analysis:
        console.print("[blue]🤖 AI Analysis: Enabled[/blue]")
    
    # Validate inputs
    location = validate_location(args.location)
    categories = validate_categories(args.categories)
    
    # Search businesses with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        all_results = []
        
        if args.google_maps_only:
            # Use ONLY Google Maps scraping
            total_tasks = len(categories)
            task = progress.add_task("Searching with Google Maps...", total=total_tasks)
            
            for category in categories:
                progress.update(task, description=f"Google Maps: {category}...")
                gmaps_results = search_google_maps_businesses(
                    query=category,
                    location=location,
                    max_results=args.max_results,
                    headless=args.headless,
                    rating_filter=args.rating_filter
                )
                all_results.extend(gmaps_results)
                progress.advance(task)
                
        elif args.use_google_maps:
            # Combined search: Standard + Google Maps
            total_tasks = len(categories) * 2  # Both standard and Google Maps
            task = progress.add_task("Combined search...", total=total_tasks)
            
            for category in categories:
                # Standard search
                progress.update(task, description=f"Standard search: {category}...")
                standard_results = search_businesses_all_sources(
                    query=category,
                    location=location,
                    max_results=args.max_results,
                    config=config
                )
                all_results.extend(standard_results)
                progress.advance(task)
                
                # Google Maps search
                progress.update(task, description=f"Google Maps: {category}...")
                gmaps_results = search_google_maps_businesses(
                    query=category,
                    location=location,
                    max_results=args.max_results // 2,  # Split results between methods
                    headless=args.headless,
                    rating_filter=args.rating_filter
                )
                all_results.extend(gmaps_results)
                progress.advance(task)
                
        else:
            # Standard search only
            task = progress.add_task("Searching businesses...", total=len(categories))
            
            for category in categories:
                progress.update(task, description=f"Searching {category}...")
                results = search_businesses_all_sources(
                    query=category,
                    location=location,
                    max_results=args.max_results,
                    config=config
                )
                all_results.extend(results)
                progress.advance(task)
    
    # Remove duplicates
    unique_results = remove_duplicates(all_results)
    
    # Apply filters
    filtered_results = apply_search_filters(unique_results, args.filter)
    
    # Sort results
    sorted_results = sort_results(filtered_results, args.sort_by)
    
    # AI Analysis if requested
    if args.ai_analysis:
        console.print("[blue]🤖 Starting AI analysis...[/blue]")
        try:
            from ai_assistant import batch_analyze_businesses
            sorted_results = batch_analyze_businesses(sorted_results)
            console.print("[green]✅ AI analysis completed[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️ AI analysis failed: {e}[/yellow]")
    
    # Display results
    display_search_results(sorted_results, args.filter, use_google_maps=args.use_google_maps or args.google_maps_only)
    
    # Save results if output specified
    if args.output:
        save_search_results(sorted_results, args.output, args.format)
        console.print(f"[green]✅ Results saved to: {args.output}[/green]")
    
    return True

def handle_check_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle website check command."""
    console.print(f"[blue]🔍 Checking website for: {args.business_name}[/blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Checking website...", total=1)
        
        website_status = check_website_status(
            business_name=args.business_name,
            phone=args.phone,
            address=args.address,
            config=config
        )
        
        progress.advance(task)
    
    # Display results
    display_website_check_results(args.business_name, website_status)
    
    return True

def handle_report_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle report generation command."""
    console.print(f"[blue]📊 Generating report from: {args.input}[/blue]")
    
    try:
        # Load data from input file
        from utils import load_json_data
        leads_data = load_json_data(args.input)
        
        if not leads_data:
            console.print(f"[red]❌ No data found in {args.input}[/red]")
            return False
        
        # Generate report
        report_path = generate_report(
            leads_data=leads_data,
            output_path=args.output,
            format_type=args.format
        )
        
        console.print(f"[green]✅ Report generated: {report_path}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        return False

def handle_export_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle data export command."""
    console.print(f"[blue]📤 Exporting data to: {args.output}[/blue]")
    
    try:
        export_data(
            input_file=args.input,
            output_file=args.output,
            format=args.format,
            filter_criteria=args.filter,
            config=config
        )
        
        console.print(f"[green]✅ Data exported: {args.output}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]Error exporting data: {e}[/red]")
        return False

def handle_analyze_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle data analysis command."""
    console.print(f"[blue]📈 Analyzing data from: {args.input}[/blue]")
    
    try:
        analysis_results = analyze_leads(
            input_file=args.input,
            output_file=args.output,
            metrics=args.metrics,
            config=config
        )
        
        display_analysis_results(analysis_results)
        
        if args.output:
            console.print(f"[green]✅ Analysis saved to: {args.output}[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error analyzing data: {e}[/red]")
        return False

def handle_interactive_command(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle interactive mode."""
    console.print("[bold blue]🎯 Welcome to Business Lead Finder Interactive Mode![/bold blue]")
    console.print("Type 'help' for available commands or 'exit' to quit\n")
    
    while True:
        try:
            command = Prompt.ask("\n[bold green]business-finder>[/bold green]", default="help")
            
            if command.lower() in ['exit', 'quit']:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            elif command.lower() == 'help':
                show_interactive_help()
            elif command.lower() == 'search':
                interactive_search(config)
            elif command.lower() == 'check':
                interactive_check(config)
            elif command.lower() == 'report':
                interactive_report(config)
            elif command.lower() == 'status':
                show_status(config)
            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    return True

def apply_search_filters(results: List[Dict[str, Any]], filter_type: str) -> List[Dict[str, Any]]:
    """Apply search filters to results."""
    if filter_type == 'no-website':
        return [r for r in results if not r.get('website')]
    elif filter_type == 'bad-website':
        return [r for r in results if r.get('website') and r.get('website_quality_score', 100) < 50]
    else:  # 'all'
        return results

def sort_results(results: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    """Sort results by specified field."""
    if sort_by == 'lead-score':
        return sorted(results, key=lambda x: x.get('lead_score', 0), reverse=True)
    elif sort_by == 'rating':
        return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == 'name':
        return sorted(results, key=lambda x: x.get('name', '').lower())
    else:
        return results

def display_search_results(results: List[Dict[str, Any]], filter_type: str = 'all', use_google_maps: bool = False) -> None:
    """Display search results in organized format."""
    if not results:
        console.print("[red]❌ No businesses found matching your criteria.[/red]")
        console.print("\n[yellow]💡 Try these suggestions:[/yellow]")
        console.print("• Generate sample data: [cyan]python scripts/collect_real_data.py --generate-samples[/cyan]")
        console.print("• Add API keys in .env file for better results")
        console.print("• Try different locations or business categories")
        console.print("• Use Google Maps option: [cyan]--use-google-maps[/cyan] or [cyan]--google-maps-only[/cyan]")
        return
    
    # Summary stats
    total_results = len(results)
    no_website_count = len([r for r in results if not r.get('website')])
    with_emails_count = len([r for r in results if r.get('emails')])
    avg_lead_score = sum(r.get('lead_score', 0) for r in results) / total_results if total_results > 0 else 0
    
    # Display summary
    console.print(f"\n[bold green]📊 SEARCH RESULTS SUMMARY[/bold green]")
    console.print(f"[green]Total Businesses Found: {total_results}[/green]")
    console.print(f"[yellow]Without Website: {no_website_count} ({no_website_count/total_results*100:.1f}%)[/yellow]")
    console.print(f"[blue]Average Lead Score: {avg_lead_score:.1f}/100[/blue]")
    
    # Google Maps specific stats
    if use_google_maps:
        console.print(f"[magenta]📧 With Email Addresses: {with_emails_count} ({with_emails_count/total_results*100:.1f}%)[/magenta]")
        console.print(f"[cyan]🗺️ Google Maps Data Enhanced: {len([r for r in results if r.get('source') == 'google_maps_scraper'])} businesses[/cyan]")
    
    # Filter-specific messages
    if filter_type == 'no-website':
        console.print(f"[bold yellow]🎯 HIGH OPPORTUNITY: All {total_results} businesses have NO WEBSITE![/bold yellow]")
    elif filter_type == 'bad-website':
        console.print(f"[bold orange]🔧 IMPROVEMENT OPPORTUNITY: {total_results} businesses have poor websites![/bold orange]")
    
    # Display top results
    console.print(f"\n[bold blue]🏆 TOP OPPORTUNITIES[/bold blue]")
    
    # Create table for results - enhanced for Google Maps
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=6)
    table.add_column("Business Name", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Rating", style="yellow")
    table.add_column("Lead Score", style="green")
    table.add_column("Website Status", style="red")
    
    if use_google_maps:
        table.add_column("Email Count", style="magenta")
        table.add_column("Contact Level", style="bold cyan")
        table.add_column("Lead Priority", style="bold red")
    else:
        table.add_column("Opportunity", style="bold red")
    
    for i, business in enumerate(results[:20], 1):  # Show top 20
        name = business.get('name', 'Unknown')[:30]
        category = business.get('category', 'Unknown')[:15]
        rating = f"{business.get('rating', 0):.1f}⭐" if business.get('rating') else 'N/A'
        lead_score = f"{business.get('lead_score', 0)}/100"
        
        # Website status
        if business.get('website'):
            website_status = "✅ Has Website"
            opportunity = "Website Upgrade"
        else:
            website_status = "❌ NO WEBSITE"
            opportunity = "🔥 HIGH PRIORITY"
        
        if use_google_maps:
            email_count = len(business.get('emails', []))
            email_display = f"📧 {email_count}" if email_count > 0 else "No emails"
            
            # Contact level based on available information
            contact_level = "🔥 COMPLETE"
            if business.get('phone') and business.get('emails') and business.get('address'):
                contact_level = "🔥 COMPLETE"
            elif business.get('phone') or business.get('emails'):
                contact_level = "⚡ GOOD"
            else:
                contact_level = "📍 BASIC"
            
            # Lead priority from Google Maps filtering
            lead_priority = business.get('lead_priority', 'MEDIUM')
            priority_display = {
                'HIGH': '🔥 HIGH',
                'MEDIUM': '⚡ MEDIUM', 
                'UPGRADE': '📈 UPGRADE'
            }.get(lead_priority, '⚡ MEDIUM')
            
            table.add_row(str(i), name, category, rating, lead_score, website_status, email_display, contact_level, priority_display)
        else:
            table.add_row(str(i), name, category, rating, lead_score, website_status, opportunity)
    
    console.print(table)
    
    # Show AI insights if available
    ai_businesses = [b for b in results if b.get('ai_analysis')]
    if ai_businesses:
        console.print(f"\n[bold blue]🤖 AI INSIGHTS[/bold blue]")
        for business in ai_businesses[:3]:  # Show top 3 AI insights
            ai_data = business.get('ai_analysis', {})
            if 'ai_analysis' in ai_data:
                console.print(f"[bold cyan]{business.get('name', 'Unknown')}:[/bold cyan]")
                console.print(f"  {ai_data['ai_analysis'][:200]}...")
                console.print()
    
    # Contact information for top opportunities
    console.print(f"\n[bold green]📞 CONTACT INFORMATION (Top 5)[/bold green]")
    contact_table = Table(show_header=True, header_style="bold green")
    contact_table.add_column("Business", style="bold")
    contact_table.add_column("Phone", style="blue")
    
    if use_google_maps:
        contact_table.add_column("Emails", style="magenta")
        contact_table.add_column("Address", style="dim")
    else:
        contact_table.add_column("Address", style="dim")
        contact_table.add_column("Email Template", style="cyan")
    
    for business in results[:5]:
        name = business.get('name', 'Unknown')[:25]
        phone = business.get('phone', 'N/A')
        address = business.get('address', 'N/A')[:30]
        
        if use_google_maps:
            emails = business.get('emails', [])
            email_display = ', '.join(emails[:2]) if emails else 'N/A'  # Show first 2 emails
            if len(emails) > 2:
                email_display += f" (+{len(emails)-2} more)"
            
            contact_table.add_row(name, phone, email_display, address)
        else:
            # Check if AI generated email is available
            has_ai_email = business.get('personalized_email', False)
            email_status = "🤖 AI Generated" if has_ai_email else "📧 Standard"
            
            contact_table.add_row(name, phone, address, email_status)
    
    console.print(contact_table)
    
    # Google Maps specific tips
    if use_google_maps and with_emails_count > 0:
        console.print(f"\n[bold magenta]📧 EMAIL OUTREACH TIPS:[/bold magenta]")
        console.print("• Use professional email templates")
        console.print("• Personalize messages based on business type")
        console.print("• Mention specific website benefits for their industry")
        console.print("• Include your portfolio examples")
        console.print("• Follow up within 3-5 business days")
    
    if filter_type == 'no-website':
        console.print(f"\n[bold yellow]💡 NEXT STEPS:[/bold yellow]")
        console.print("1. Contact businesses with highest lead scores first")
        console.print("2. Use provided phone numbers for direct contact")
        if use_google_maps:
            console.print("3. Send personalized emails to discovered email addresses")
        console.print("4. Reference their excellent ratings in your pitch")
        console.print("5. Emphasize missed online opportunities")
    
    console.print(f"\n[green]✅ Search completed successfully![/green]")

def display_website_check_results(business_name: str, website_status: Dict[str, Any]):
    """Display website check results."""
    console.print(f"\n[bold]🔍 Website Check Results for: {business_name}[/bold]")
    
    if website_status.get('website'):
        console.print(f"[green]✅ Website found: {website_status['website']}[/green]")
        console.print(f"[blue]Confidence: {website_status.get('confidence', 'N/A')}%[/blue]")
    else:
        console.print("[red]❌ No website found[/red]")
    
    if website_status.get('social_media'):
        console.print(f"[yellow]📱 Social Media: {', '.join(website_status['social_media'].keys())}[/yellow]")
    
    if website_status.get('additional_info'):
        console.print(f"[blue]ℹ️ Additional Info: {website_status['additional_info']}[/blue]")

def display_analysis_results(analysis: Dict[str, Any]):
    """Display analysis results."""
    console.print("\n[bold]📈 Lead Analysis Results[/bold]")
    
    # Create metrics table
    table = Table(title="Key Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Description", style="white")
    
    for metric, data in analysis.items():
        if isinstance(data, dict) and 'value' in data:
            table.add_row(
                metric.replace('_', ' ').title(),
                str(data['value']),
                data.get('description', '')
            )
    
    console.print(table)

def show_interactive_help():
    """Show help for interactive mode."""
    help_text = f"""
[bold blue]Available Commands:[/bold blue]

• [green]search[/green] - Search for businesses interactively
• [green]check[/green] - Check if a business has a website
• [green]report[/green] - Generate a report from existing data
• [green]status[/green] - Show current system status
• [green]help[/green] - Show this help message
• [green]exit[/green] - Exit interactive mode

[bold blue]Google Maps Features:[/bold blue]
• [magenta]Enhanced Search[/magenta] - Discover business emails automatically
• [magenta]Contact Discovery[/magenta] - Find phone numbers and addresses
• [magenta]Website Detection[/magenta] - Identify businesses without websites
• [cyan]Status: {'✅ Available' if GOOGLE_MAPS_AVAILABLE else '❌ Not Available'}[/cyan]

[bold blue]Tips:[/bold blue]
• Use Tab completion for faster input
• All data is automatically saved
• Use Ctrl+C to cancel any operation
• Google Maps search provides email addresses for direct outreach
• Combine with AI analysis for best results
    """
    console.print(help_text)

def interactive_search(config: Dict[str, Any]):
    """Interactive search mode with Google Maps options."""
    console.print("[bold blue]🔍 Interactive Business Search[/bold blue]")
    
    location = Prompt.ask("Enter location", default="Marrakesh, Morocco")
    categories_input = Prompt.ask("Enter categories (comma-separated)", default="restaurants,hotels")
    max_results = Prompt.ask("Maximum results per category", default="20")
    
    # Google Maps options
    if GOOGLE_MAPS_AVAILABLE:
        console.print("\n[bold cyan]🗺️ Google Maps Enhanced Search Options:[/bold cyan]")
        console.print("1. Standard search only")
        console.print("2. Standard + Google Maps (recommended for emails)")
        console.print("3. Google Maps only")
        
        search_type = Prompt.ask("Choose search type", choices=["1", "2", "3"], default="2")
        
        use_google_maps = search_type in ["2", "3"]
        google_maps_only = search_type == "3"
        
        if use_google_maps:
            console.print("[green]✅ Google Maps enhanced search enabled - will discover email addresses![/green]")
    else:
        console.print("[yellow]⚠️ Google Maps scraping not available. Install selenium and chrome driver for enhanced features.[/yellow]")
        use_google_maps = False
        google_maps_only = False
    
    # Filter options
    console.print("\n[bold yellow]🎯 Filter Options:[/bold yellow]")
    console.print("1. All businesses")
    console.print("2. Businesses without websites")
    console.print("3. Businesses with poor websites")
    
    filter_choice = Prompt.ask("Choose filter", choices=["1", "2", "3"], default="2")
    filter_map = {"1": "all", "2": "no-website", "3": "bad-website"}
    filter_type = filter_map[filter_choice]
    
    # AI Analysis option
    ai_analysis = Confirm.ask("Enable AI analysis?", default=False)
    
    categories = [cat.strip() for cat in categories_input.split(',')]
    
    # Confirm search
    search_desc = f"{categories} in {location}"
    if use_google_maps:
        search_desc += " (with Google Maps email discovery)"
    
    if Confirm.ask(f"Search for {search_desc}?"):
        # Simulate search command
        from argparse import Namespace
        args = Namespace(
            location=location,
            categories=categories,
            max_results=int(max_results),
            output=None,
            format='json',
            filter=filter_type,
            ai_analysis=ai_analysis,
            use_google_maps=use_google_maps,
            google_maps_only=google_maps_only,
            headless=True,
            sort_by='lead-score'  # Add missing attribute
        )
        handle_search_command(args, config)

def interactive_check(config: Dict[str, Any]):
    """Interactive website check mode."""
    console.print("[bold blue]🔍 Interactive Website Check[/bold blue]")
    
    business_name = Prompt.ask("Enter business name")
    phone = Prompt.ask("Enter phone number (optional)", default="")
    address = Prompt.ask("Enter address (optional)", default="")
    
    # Simulate check command
    from argparse import Namespace
    args = Namespace(
        business_name=business_name,
        phone=phone if phone else None,
        address=address if address else None
    )
    handle_check_command(args, config)

def interactive_report(config: Dict[str, Any]):
    """Interactive report generation mode."""
    console.print("[bold blue]📊 Interactive Report Generation[/bold blue]")
    
    input_file = Prompt.ask("Enter input data file path")
    output_file = Prompt.ask("Enter output report file path", default="report.html")
    format_choice = Prompt.ask("Choose format", choices=['html', 'pdf', 'json'], default='html')
    
    # Simulate report command
    from argparse import Namespace
    args = Namespace(
        input=input_file,
        output=output_file,
        format=format_choice,
        template=None
    )
    handle_report_command(args, config)

def show_status(config: Dict[str, Any]):
    """Show system status including Google Maps scraping."""
    console.print("[bold blue]📊 System Status[/bold blue]")
    
    # Check API availability
    api_status = check_api_availability(config)
    
    table = Table(title="API Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Limit", style="yellow")
    table.add_column("Notes", style="dim")
    
    for service, status in api_status.items():
        status_icon = "✅" if status['available'] else "❌"
        table.add_row(
            service,
            f"{status_icon} {status['status']}",
            status.get('limit', 'N/A'),
            status.get('notes', '')
        )
    
    console.print(table)
    
    # Google Maps specific status
    console.print(f"\n[bold magenta]🗺️ Google Maps Scraping:[/bold magenta]")
    if GOOGLE_MAPS_AVAILABLE:
        console.print("[green]✅ Available - Enhanced email discovery enabled[/green]")
        console.print("[dim]Features: Business emails, phone numbers, ratings, contact info[/dim]")
    else:
        console.print("[red]❌ Not Available[/red]")
        console.print("[dim]Install: pip install selenium[/dim]")
        console.print("[dim]Download: Chrome WebDriver[/dim]")
    
    console.print(f"\n[bold yellow]💡 Recommendations:[/bold yellow]")
    if not GOOGLE_MAPS_AVAILABLE:
        console.print("• Install Google Maps scraping for email discovery")
    console.print("• Use combined search for best results")
    console.print("• Enable AI analysis for lead scoring")
    console.print("• Save results with --output for tracking")

def check_api_availability(config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Check availability of various APIs and services."""
    return {
        'OpenStreetMap': {
            'available': True, 
            'status': 'Available', 
            'limit': 'Unlimited',
            'notes': 'Free mapping service'
        },
        'Foursquare': {
            'available': bool(config.get('foursquare_client_id')), 
            'status': 'Available' if config.get('foursquare_client_id') else 'No API Key', 
            'limit': '1000/day',
            'notes': 'Business directory'
        },
        'SerpAPI': {
            'available': bool(config.get('serpapi_key')), 
            'status': 'Available' if config.get('serpapi_key') else 'No API Key', 
            'limit': '100/month',
            'notes': 'Google search results'
        },
        'Google Places': {
            'available': bool(config.get('google_places_key')), 
            'status': 'Optional', 
            'limit': 'Varies',
            'notes': 'Enhanced business data'
        },
        'Google Maps Scraper': {
            'available': GOOGLE_MAPS_AVAILABLE,
            'status': 'Available' if GOOGLE_MAPS_AVAILABLE else 'Missing Dependencies',
            'limit': 'FREE',
            'notes': 'Email discovery, contact info'
        }
    }

def save_search_results(results: list, output_path: str, format: str):
    """Save search results to file."""
    import json
    import csv
    from pathlib import Path
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    elif format == 'csv':
        if results:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)

def handle_demo_search(args: argparse.Namespace, config: Dict[str, Any]) -> bool:
    """Handle demo search with sample data generation."""
    import json
    import random
    from datetime import datetime
    
    console.print("[yellow]🎪 Generating sample demo data...[/yellow]")
    
    # Generate sample data for each category
    all_results = []
    
    for category in args.categories:
        # Generate 15-25 businesses per category
        count = random.randint(15, 25)
        demo_businesses = generate_demo_data(args.location, category, count)
        all_results.extend(demo_businesses)
    
    # Apply filters
    if args.filter == 'no-website':
        filtered_results = [b for b in all_results if not b.get('website')]
    elif args.filter == 'bad-website':
        filtered_results = [b for b in all_results if b.get('website_status') == 'poor']
    else:
        filtered_results = all_results
    
    # Sort results
    if args.sort_by == 'lead-score':
        filtered_results.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
    elif args.sort_by == 'rating':
        filtered_results.sort(key=lambda x: x.get('rating', 0), reverse=True)
    elif args.sort_by == 'name':
        filtered_results.sort(key=lambda x: x.get('name', ''))
    
    # Limit results
    final_results = filtered_results[:args.max_results]
    
    # Display results
    display_search_results(final_results, args.filter, use_google_maps=False)
    
    # Save results if requested
    if args.output:
        export_data(final_results, args.output, args.format)
        console.print(f"[green]✅ Results saved to: {args.output}[/green]")
    
    console.print("[yellow]💡 This was demo data. For real data, remove --demo flag and add API keys.[/yellow]")
    return True

def generate_demo_data(location: str, category: str, count: int = 20) -> List[Dict[str, Any]]:
    """Generate realistic demo business data."""
    import random
    from datetime import datetime
    
    # Moroccan business name components
    prefixes = ["Riad", "Maison", "Dar", "Restaurant", "Café", "Hotel", "Spa", "Boutique", "Atlas", "Medina"]
    suffixes = ["Al Baraka", "Majorelle", "Bahia", "Saadian", "Koutoubia", "Agafay", "Atlas", "Berbère", "Royal"]
    
    businesses = []
    
    for i in range(count):
        name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        
        # 70% have no website (realistic for Morocco small businesses)
        has_website = random.random() < 0.3
        has_email = random.random() < 0.4
        has_phone = random.random() < 0.85
        
        business = {
            'name': name,
            'address': f"{random.randint(1, 200)} {random.choice(['Rue Mohammed V', 'Rue Hassan II', 'Avenue de la Liberté'])}, {location.split(',')[0]}",
            'phone': f"+212 {random.randint(500, 699)}-{random.randint(100000, 999999)}" if has_phone else "",
            'website': f"www.{name.lower().replace(' ', '').replace('ç', 'c')}.ma" if has_website else "",
            'emails': [f"contact@{name.lower().replace(' ', '').replace('ç', 'c')}.ma"] if has_email else [],
            'category': category,
            'rating': round(random.uniform(3.2, 4.9), 1),
            'review_count': random.randint(8, 180),
            'lead_score': random.randint(65, 98) if not has_website else random.randint(40, 75),
            'source': 'demo_data',
            'search_timestamp': datetime.now().isoformat(),
            'location': location,
            'verified': False,
            'website_status': 'none' if not has_website else random.choice(['good', 'poor', 'outdated'])
        }
        
        businesses.append(business)
    
    return businesses

def validate_search_parameters(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Validate and sanitize search parameters.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Dict with validated parameters
        
    Raises:
        ValueError: If validation fails
    """
    errors = []
    
    # Validate location
    if not args.location or len(args.location.strip()) < 3:
        errors.append("Location must be at least 3 characters long")
    
    # Validate categories
    if not args.categories or len(args.categories) == 0:
        errors.append("At least one category must be specified")
    
    # Validate max_results
    if hasattr(args, 'max_results'):
        if args.max_results < 1 or args.max_results > 1000:
            errors.append("Max results must be between 1 and 1000")
    
    # Validate output path
    if hasattr(args, 'output') and args.output:
        output_path = Path(args.output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            errors.append(f"Cannot create output directory: {e}")
    
    if errors:
        raise ValueError("Validation failed:\n" + "\n".join(f"- {error}" for error in errors))
    
    return {
        'location': args.location.strip(),
        'categories': [cat.strip().lower() for cat in args.categories],
        'max_results': getattr(args, 'max_results', 50),
        'output': getattr(args, 'output', None)
    }

def handle_api_errors(func):
    """
    Decorator for handling API errors gracefully.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            logger.error("Network connection error - check your internet connection")
            if RICH_AVAILABLE:
                console.print("[red]❌ Network error: Check your internet connection[/red]")
            return []
        except requests.exceptions.Timeout:
            logger.error("Request timeout - API server may be slow")
            if RICH_AVAILABLE:
                console.print("[yellow]⏰ Request timeout - trying alternative sources[/yellow]")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            if RICH_AVAILABLE:
                console.print(f"[red]❌ Error: {e}[/red]")
            return []
    return wrapper
