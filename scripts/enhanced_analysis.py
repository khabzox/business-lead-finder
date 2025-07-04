#!/usr/bin/env python3
"""
Re-analyze collected businesses with enhanced website detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
from business_search import update_business_with_enhanced_website_check
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

def analyze_businesses_with_enhanced_detection():
    """Re-analyze businesses with enhanced website detection."""
    
    # Load the businesses we collected
    input_file = 'results/morocco_businesses.json'
    
    if not os.path.exists(input_file):
        console.print(f"[red]❌ File not found: {input_file}[/red]")
        console.print("Please run the business collection first.")
        return
    
    with open(input_file, 'r') as f:
        businesses = json.load(f)
    
    console.print(f"[blue]🔍 Re-analyzing {len(businesses)} businesses with enhanced website detection[/blue]")
    console.print(f"[yellow]⚠️ This will take some time as we check multiple domain variations for each business[/yellow]")
    
    updated_businesses = []
    websites_found = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        
        task = progress.add_task("Analyzing businesses...", total=len(businesses))
        
        for i, business in enumerate(businesses):
            progress.update(task, description=f"Analyzing {business.get('name', 'Unknown')}...")
            
            # Update with enhanced website detection
            updated_business = update_business_with_enhanced_website_check(business)
            updated_businesses.append(updated_business)
            
            if updated_business.get('website'):
                websites_found += 1
                console.print(f"  [green]✅ Found website for {updated_business['name']}: {updated_business['website']}[/green]")
            
            progress.advance(task)
            
            # Rate limiting
            import time
            time.sleep(1)  # 1 second between checks to be respectful
    
    # Save updated results
    output_file = 'results/morocco_businesses_enhanced.json'
    with open(output_file, 'w') as f:
        json.dump(updated_businesses, f, indent=2)
    
    # Generate summary
    console.print(f"\n[bold green]📊 ENHANCED ANALYSIS COMPLETE[/bold green]")
    console.print(f"[green]Total Businesses: {len(updated_businesses)}[/green]")
    console.print(f"[green]Websites Found: {websites_found}[/green]")
    console.print(f"[yellow]Still No Website: {len(updated_businesses) - websites_found}[/yellow]")
    console.print(f"[blue]Improvement: Found {websites_found} additional websites![/blue]")
    
    # Show examples of found websites
    businesses_with_websites = [b for b in updated_businesses if b.get('website')]
    if businesses_with_websites:
        console.print(f"\n[bold blue]🌐 WEBSITES FOUND[/bold blue]")
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Business", style="bold")
        table.add_column("Website", style="green")
        table.add_column("Quality", style="yellow")
        table.add_column("Method", style="cyan")
        
        for business in businesses_with_websites[:10]:  # Show first 10
            table.add_row(
                business['name'][:30],
                business['website'][:40],
                f"{business.get('website_quality_score', 0)}/100",
                business.get('website_detection_method', 'unknown')
            )
        
        console.print(table)
    
    # Show high priority leads (still no website)
    no_website_businesses = [b for b in updated_businesses if not b.get('website')]
    console.print(f"\n[bold red]🎯 HIGH PRIORITY LEADS (No Website Found)[/bold red]")
    
    # Sort by lead score
    no_website_businesses.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
    
    table = Table(show_header=True, header_style="bold red")
    table.add_column("Business", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Lead Score", style="green")
    table.add_column("Phone", style="blue")
    table.add_column("Domains Checked", style="dim")
    
    for business in no_website_businesses[:15]:  # Show top 15
        domains_checked = len(business.get('website_domains_checked', []))
        table.add_row(
            business['name'][:25],
            business.get('category', 'Unknown')[:15],
            f"{business.get('lead_score', 0)}/100",
            business.get('phone', 'N/A')[:15],
            str(domains_checked)
        )
    
    console.print(table)
    
    # Export high priority leads
    high_priority_file = 'results/high_priority_no_website.json'
    with open(high_priority_file, 'w') as f:
        json.dump(no_website_businesses[:50], f, indent=2)  # Top 50 leads
    
    console.print(f"\n[green]✅ Results saved to:[/green]")
    console.print(f"  📁 {output_file}")
    console.print(f"  🎯 {high_priority_file}")

if __name__ == "__main__":
    analyze_businesses_with_enhanced_detection()
