#!/usr/bin/env python3
"""
Massive Marrakesh Business Search - Thousands of Opportunities
This script searches for ALL business opportunities in Marrakesh and saves massive datasets.

Features:
- Search ALL business categories in Marrakesh
- Generate thousands/millions of leads
- Save to timestamped JSON files in results folder
- Automated weekly/monthly scheduling
- Progress tracking for massive datasets
- Memory-efficient streaming for large datasets
"""

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Iterator
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
import schedule

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

console = Console()

# Marrakesh-specific business categories for massive search
MARRAKESH_CATEGORIES = [
    # Food & Beverage (High Opportunity)
    "restaurants", "cafes", "bars", "fast_food", "bakery", "food_delivery",
    "tea_house", "juice_bar", "ice_cream", "pastry", "traditional_food",
    
    # Hospitality (Very High Opportunity) 
    "hotels", "riads", "guesthouses", "hostels", "bed_breakfast",
    "vacation_rentals", "boutique_hotels", "traditional_houses",
    
    # Wellness & Beauty (High Opportunity)
    "spas", "hammams", "beauty_salons", "massage", "wellness_centers",
    "hair_salons", "nail_salons", "fitness_centers", "yoga_studios",
    
    # Shopping & Retail (Medium-High Opportunity)
    "clothing_stores", "souvenir_shops", "handicrafts", "jewelry_stores",
    "leather_goods", "carpet_shops", "antique_shops", "art_galleries",
    "bookstores", "electronics", "home_goods", "gift_shops",
    
    # Services (Medium Opportunity)
    "tour_operators", "travel_agencies", "car_rental", "taxi_services",
    "photography", "event_planning", "catering", "cleaning_services",
    "repair_services", "consulting", "real_estate", "insurance",
    
    # Professional Services (Medium Opportunity)
    "lawyers", "accountants", "doctors", "dentists", "veterinarians",
    "architects", "engineers", "designers", "translators", "tutoring",
    
    # Entertainment (Medium Opportunity)
    "nightlife", "entertainment", "music_venues", "cultural_centers",
    "museums", "theaters", "gaming", "sports_facilities",
]

# Marrakesh neighborhoods and areas for comprehensive coverage
MARRAKESH_AREAS = [
    # Tourist Areas (High Priority)
    "Medina", "Jemaa el-Fnaa", "Majorelle", "Hivernage", "Gueliz",
    
    # Residential Areas
    "Sidi Ghanem", "Targa", "Hay Riad", "Agdal", "Semlalia",
    "Daoudiate", "M'hamid", "Annakhil", "Menara", "Tameslouht",
    
    # Outer Areas
    "Marrakech Centre", "Marrakech Sud", "Marrakech Nord",
    "Route de Fes", "Route de Casablanca", "Route d'Essaouira",
    
    # Specific Locations
    "Atlas Mountains", "Palmeraie", "Route de l'Ourika",
    "Amizmiz", "Ait Ourir", "Chichaoua", "Essaouira Road",
]

class MassiveMarrakeshSearch:
    """Massive business search system for Marrakesh with thousands of results."""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.cities_dir = self.results_dir / "cities" / "marrakesh" / "searches"
        self.results_dir.mkdir(exist_ok=True)
        self.cities_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        self.total_businesses_found = 0
        self.categories_processed = 0
        self.areas_processed = 0
        
    def setup_logging(self):
        """Setup logging for massive search operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "massive_search.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def generate_search_queries(self) -> List[Dict]:
        """Generate massive list of search queries for comprehensive coverage."""
        queries = []
        
        for category in MARRAKESH_CATEGORIES:
            for area in MARRAKESH_AREAS:
                # Primary location format
                queries.append({
                    'query': category,
                    'location': f"{area}, Marrakesh, Morocco",
                    'category': category,
                    'area': area,
                    'priority': self.get_category_priority(category)
                })
                
                # Alternative location formats for better coverage
                queries.append({
                    'query': f"{category} {area}",
                    'location': "Marrakesh, Morocco", 
                    'category': category,
                    'area': area,
                    'priority': self.get_category_priority(category)
                })
                
        # Add general searches without specific areas
        for category in MARRAKESH_CATEGORIES:
            queries.append({
                'query': category,
                'location': "Marrakesh, Morocco",
                'category': category,
                'area': "General",
                'priority': self.get_category_priority(category)
            })
            
        console.print(f"[green]Generated {len(queries)} search queries for massive data collection![/green]")
        return queries
        
    def get_category_priority(self, category: str) -> int:
        """Get priority score for business category (1=highest, 3=lowest)."""
        high_priority = ["restaurants", "cafes", "hotels", "riads", "spas", "tour_operators"]
        medium_priority = ["bars", "shops", "services", "beauty_salons", "guesthouses"]
        
        if category in high_priority:
            return 1
        elif category in medium_priority:
            return 2
        else:
            return 3
    
    async def search_massive_businesses(self, max_results_per_query: int = 100) -> Iterator[Dict]:
        """
        Search for massive amounts of businesses with streaming results.
        Yields results one by one to handle millions of businesses efficiently.
        """
        queries = self.generate_search_queries()
        
        # Sort by priority (high priority categories first)
        queries.sort(key=lambda x: x['priority'])
        
        console.print(f"[blue]Starting massive search with {len(queries)} queries...[/blue]")
        console.print(f"[yellow]Expected results: {len(queries) * max_results_per_query:,} businesses[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=False,
        ) as progress:
            
            main_task = progress.add_task(
                "Massive Marrakesh Search", 
                total=len(queries)
            )
            
            for i, query in enumerate(queries):
                progress.update(
                    main_task, 
                    description=f"Searching {query['category']} in {query['area']} - Found: {self.total_businesses_found:,}",
                    advance=1
                )
                
                try:
                    # Search businesses for this query
                    businesses = await self.search_single_query(
                        query, 
                        max_results_per_query
                    )
                    
                    for business in businesses:
                        # Add search metadata
                        business['search_query'] = query['query']
                        business['search_area'] = query['area'] 
                        business['search_category'] = query['category']
                        business['search_timestamp'] = datetime.now().isoformat()
                        business['search_priority'] = query['priority']
                        
                        self.total_businesses_found += 1
                        yield business
                        
                    # Rate limiting to be respectful to APIs
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error searching {query}: {e}")
                    continue
                    
                self.categories_processed += 1
                
                # Log progress every 50 queries
                if i % 50 == 0:
                    self.logger.info(f"Processed {i}/{len(queries)} queries, found {self.total_businesses_found:,} businesses")
    
    async def search_single_query(self, query: Dict, max_results: int) -> List[Dict]:
        """Search businesses for a single query with multiple sources."""
        businesses = []
        
        try:
            # Import search functions
            from src.business_search import search_businesses_all_sources
            from src.website_checker import enhanced_website_detection
            
            # Search businesses
            results = await search_businesses_all_sources(
                query=query['query'],
                location=query['location'],
                max_results=max_results
            )
            
            for business in results:
                # Enhanced website detection
                website = await enhanced_website_detection(
                    business.get('name', ''),
                    business.get('phone', ''),
                    business.get('address', '')
                )
                
                # Calculate lead score
                business['website'] = website
                business['lead_score'] = self.calculate_enhanced_lead_score(business)
                business['opportunity_level'] = self.get_opportunity_level(business['lead_score'])
                
                businesses.append(business)
                
        except ImportError:
            # Fallback to mock data for testing
            businesses = self.generate_mock_businesses(query, max_results)
            
        return businesses
    
    def generate_mock_businesses(self, query: Dict, max_results: int) -> List[Dict]:
        """Generate mock business data for testing massive search."""
        businesses = []
        
        for i in range(min(max_results, 50)):  # Limit mock data
            business = {
                'name': f"{query['category'].title()} {query['area']} {i+1}",
                'category': query['category'],
                'address': f"{i+1} Street, {query['area']}, Marrakesh",
                'phone': f"+212 524 {100000 + i}",
                'rating': round(2.0 + (i % 3) * 0.5, 1),  # 2.0-3.5 ratings
                'review_count': (i % 50) + 1,
                'website': None if i % 3 == 0 else f"https://{query['category']}{i}.com",
                'source': 'mock_data'
            }
            
            business['lead_score'] = self.calculate_enhanced_lead_score(business)
            business['opportunity_level'] = self.get_opportunity_level(business['lead_score'])
            businesses.append(business)
            
        return businesses
    
    def calculate_enhanced_lead_score(self, business: Dict) -> int:
        """Calculate enhanced lead score for massive dataset."""
        score = 0
        
        # Website absence factor (30 points max)
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
    
    def get_opportunity_level(self, score: int) -> str:
        """Get opportunity level based on lead score."""
        if score >= 80:
            return "EXCELLENT"
        elif score >= 70:
            return "HIGH"
        elif score >= 60:
            return "MEDIUM"
        else:
            return "LOW"
    
    def save_massive_results(self, businesses: Iterator[Dict], batch_size: int = 1000):
        """Save massive results to JSON files with memory efficiency."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"marrakesh_massive_search_{timestamp}"
        
        # Stats tracking
        total_saved = 0
        excellent_leads = 0
        high_leads = 0
        batch_number = 1
        current_batch = []
        
        console.print(f"[blue]Saving massive results to results folder...[/blue]")
        
        for business in businesses:
            current_batch.append(business)
            
            # Track opportunity levels
            if business.get('opportunity_level') == 'EXCELLENT':
                excellent_leads += 1
            elif business.get('opportunity_level') == 'HIGH':
                high_leads += 1
                
            # Save batch when it reaches batch_size
            if len(current_batch) >= batch_size:
                batch_filename = f"{base_filename}_batch_{batch_number:03d}.json"
                batch_path = self.cities_dir / batch_filename
                
                with open(batch_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'metadata': {
                            'search_date': datetime.now().isoformat(),
                            'location': 'Marrakesh, Morocco',
                            'batch_number': batch_number,
                            'batch_size': len(current_batch),
                            'total_businesses': total_saved + len(current_batch)
                        },
                        'businesses': current_batch
                    }, f, indent=2, ensure_ascii=False)
                
                total_saved += len(current_batch)
                console.print(f"[green]Saved batch {batch_number}: {len(current_batch):,} businesses to {batch_filename}[/green]")
                
                current_batch = []
                batch_number += 1
        
        # Save remaining businesses in final batch
        if current_batch:
            batch_filename = f"{base_filename}_batch_{batch_number:03d}.json"
            batch_path = self.cities_dir / batch_filename
            
            with open(batch_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'search_date': datetime.now().isoformat(),
                        'location': 'Marrakesh, Morocco',
                        'batch_number': batch_number,
                        'batch_size': len(current_batch),
                        'total_businesses': total_saved + len(current_batch)
                    },
                    'businesses': current_batch
                }, f, indent=2, ensure_ascii=False)
            
            total_saved += len(current_batch)
            console.print(f"[green]Saved final batch {batch_number}: {len(current_batch):,} businesses[/green]")
        
        # Save summary file
        summary_path = self.cities_dir / f"{base_filename}_SUMMARY.json"
        summary = {
            'search_summary': {
                'search_date': datetime.now().isoformat(),
                'location': 'Marrakesh, Morocco',
                'total_businesses_found': total_saved,
                'total_batches': batch_number,
                'excellent_leads': excellent_leads,
                'high_leads': high_leads,
                'categories_searched': len(MARRAKESH_CATEGORIES),
                'areas_searched': len(MARRAKESH_AREAS),
                'total_queries': self.categories_processed
            }
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Display final results
        self.display_massive_results_summary(total_saved, excellent_leads, high_leads, batch_number)
        
        return total_saved
    
    def display_massive_results_summary(self, total: int, excellent: int, high: int, batches: int):
        """Display summary of massive search results."""
        table = Table(title="🚀 Massive Marrakesh Search Results")
        
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Count", style="magenta", justify="right")
        table.add_column("Details", style="green")
        
        table.add_row("Total Businesses", f"{total:,}", "All businesses found in Marrakesh")
        table.add_row("Excellent Leads", f"{excellent:,}", "Score 80+ (No website, 2-3 stars)")
        table.add_row("High Leads", f"{high:,}", "Score 70-79 (Good opportunity)")
        table.add_row("Data Batches", f"{batches}", "JSON files created")
        table.add_row("Categories", f"{len(MARRAKESH_CATEGORIES)}", "Business types searched")
        table.add_row("Areas", f"{len(MARRAKESH_AREAS)}", "Marrakesh neighborhoods")
        
        console.print(table)
        
        panel = Panel(
            f"✅ Massive search complete! Found {total:,} businesses in Marrakesh\n"
            f"🎯 {excellent:,} excellent leads ready for outreach\n"
            f"📁 Results saved in {batches} JSON batch files\n"
            f"📊 Summary saved to results folder",
            title="Search Complete",
            border_style="green"
        )
        console.print(panel)

async def run_massive_search(max_per_query: int = 100):
    """Run the massive Marrakesh business search."""
    searcher = MassiveMarrakeshSearch()
    
    console.print(Panel(
        f"🚀 Starting MASSIVE Marrakesh Business Search\n"
        f"📍 Location: Marrakesh, Morocco (ALL areas)\n"
        f"🏢 Categories: {len(MARRAKESH_CATEGORIES)} business types\n"
        f"📊 Expected Results: {len(MARRAKESH_CATEGORIES) * len(MARRAKESH_AREAS) * max_per_query:,}+ businesses\n"
        f"💾 Will save to: results/ folder in JSON batches",
        title="Massive Search Configuration",
        border_style="blue"
    ))
    
    if not console.input("[yellow]Press Enter to start massive search (or Ctrl+C to cancel)...[/yellow]"):
        pass
    
    # Run the massive search
    business_stream = searcher.search_massive_businesses(max_per_query)
    total_saved = searcher.save_massive_results(business_stream)
    
    return total_saved

def setup_scheduled_searches():
    """Setup automated weekly/monthly searches."""
    def weekly_search():
        console.print("[blue]🔄 Running scheduled weekly search...[/blue]")
        asyncio.run(run_massive_search(max_per_query=50))
        
    def monthly_search():
        console.print("[blue]🔄 Running scheduled monthly MEGA search...[/blue]")
        asyncio.run(run_massive_search(max_per_query=200))
    
    # Schedule searches
    schedule.every().monday.at("09:00").do(weekly_search)
    schedule.every().month.do(monthly_search)
    
    console.print("[green]✅ Scheduled searches configured:[/green]")
    console.print("   📅 Weekly: Every Monday at 9:00 AM")
    console.print("   📅 Monthly: First day of each month")
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Massive Marrakesh Business Search")
    parser.add_argument("--max-per-query", type=int, default=100, 
                       help="Maximum results per search query (default: 100)")
    parser.add_argument("--schedule", action="store_true",
                       help="Setup automated weekly/monthly searches")
    
    args = parser.parse_args()
    
    if args.schedule:
        console.print("[blue]Setting up scheduled searches...[/blue]")
        setup_scheduled_searches()
    else:
        # Run immediate massive search
        total = asyncio.run(run_massive_search(args.max_per_query))
        console.print(f"[green]✅ Massive search completed! Found {total:,} businesses![/green]")
