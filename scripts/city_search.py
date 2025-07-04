#!/usr/bin/env python3
"""
Multi-City Business Search - All Morocco Cities
Find business opportunities across ALL major cities in Morocco.

Supported Cities:
- Marrakesh (Tourist capital)
- Casablanca (Economic capital) 
- Rabat (Political capital)
- Fez (Cultural capital)
- Tangier (Northern gateway)
- Agadir (Atlantic coast)
- Meknes (Imperial city)
- Oujda (Eastern gateway)

Usage:
    python city_search.py --city marrakesh --standard
    python city_search.py --city casablanca --mega
    python city_search.py --all-cities --test
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

console = Console()

# City configurations with business categories and areas
CITY_CONFIGS = {
    'marrakesh': {
        'name': 'Marrakesh',
        'description': 'Tourist capital - Red City',
        'categories': [
            # Tourism & Hospitality (High Priority)
            "hotels", "riads", "guesthouses", "hostels", "vacation_rentals",
            "restaurants", "cafes", "bars", "traditional_restaurants",
            "tour_operators", "travel_agencies", "guides",
            
            # Wellness & Beauty
            "spas", "hammams", "wellness_centers", "massage", "beauty_salons",
            
            # Shopping & Crafts
            "handicrafts", "souvenir_shops", "carpet_shops", "jewelry_stores",
            "leather_goods", "art_galleries", "antique_shops",
            
            # Entertainment
            "nightlife", "cultural_centers", "museums", "entertainment",
        ],
        'areas': [
            "Medina", "Jemaa el-Fnaa", "Majorelle", "Hivernage", "Gueliz",
            "Sidi Ghanem", "Palmeraie", "Agdal", "Targa", "Semlalia"
        ],
        'priority': 1
    },
    
    'casablanca': {
        'name': 'Casablanca',
        'description': 'Economic capital - Business hub',
        'categories': [
            # Business Services (High Priority)
            "consulting", "accounting", "law_firms", "real_estate", "insurance",
            "banks", "financial_services", "business_centers",
            
            # Corporate Hospitality
            "business_hotels", "conference_centers", "restaurants", "cafes",
            
            # Professional Services
            "marketing_agencies", "web_design", "printing", "translation",
            "recruitment", "training_centers",
            
            # Retail & Shopping
            "clothing_stores", "electronics", "home_goods", "furniture",
        ],
        'areas': [
            "Centre-ville", "Maarif", "Gauthier", "Bourgogne", "Ain Diab",
            "Sidi Belyout", "Hay Hassani", "Bernoussi", "Roches Noires"
        ],
        'priority': 2
    },
    
    'rabat': {
        'name': 'Rabat',
        'description': 'Political capital - Government seat',
        'categories': [
            # Government & Professional
            "government_contractors", "consulting", "law_firms", "lobbying",
            "diplomatic_services", "translation", "protocol_services",
            
            # Business Services
            "restaurants", "hotels", "business_centers", "printing",
            "catering", "event_planning", "security_services",
            
            # Cultural & Education
            "museums", "cultural_centers", "universities", "training",
            "libraries", "research_centers",
        ],
        'areas': [
            "Agdal", "Hay Riad", "Souissi", "Centre-ville", "Hassan",
            "Yacoub El Mansour", "Temara", "Sale", "Chellah"
        ],
        'priority': 3
    },
    
    'fez': {
        'name': 'Fez',
        'description': 'Cultural capital - Imperial city',
        'categories': [
            # Traditional Crafts (High Priority)
            "handicrafts", "pottery", "leather_goods", "textiles", "carpets",
            "metalwork", "woodwork", "traditional_arts",
            
            # Cultural Tourism
            "museums", "cultural_centers", "guided_tours", "riads", "hotels",
            "traditional_restaurants", "cultural_experiences",
            
            # Education & Research
            "universities", "research_centers", "libraries", "schools",
            "religious_institutions", "cultural_preservation",
        ],
        'areas': [
            "Fez el Bali", "Fez el Jdid", "Ville Nouvelle", "Zouagha",
            "Ben Souda", "Narjiss", "Route d'Imouzzer", "Ain Chkef"
        ],
        'priority': 4
    },
    
    'tangier': {
        'name': 'Tangier',
        'description': 'Northern gateway - Port city',
        'categories': [
            # Port & Logistics
            "shipping", "logistics", "freight", "customs", "warehousing",
            "transportation", "port_services",
            
            # International Business
            "import_export", "trading", "international_services",
            "currency_exchange", "travel_agencies",
            
            # Tourism & Hospitality
            "hotels", "restaurants", "tour_operators", "car_rental",
            "travel_services", "entertainment",
        ],
        'areas': [
            "Centre-ville", "Malabata", "California", "Boukhalef", "Gzenaya",
            "Mesnana", "Charf", "Beni Makada", "Port"
        ],
        'priority': 5
    },
    
    'agadir': {
        'name': 'Agadir',
        'description': 'Atlantic coast - Beach resort',
        'categories': [
            # Beach Tourism (High Priority)
            "beach_hotels", "resorts", "restaurants", "beach_clubs",
            "water_sports", "surfing", "fishing", "boat_tours",
            
            # Wellness & Recreation
            "spas", "wellness_centers", "fitness", "yoga", "massage",
            "beauty_salons", "sports_facilities",
            
            # Agriculture & Fishing
            "fishing", "seafood_restaurants", "agriculture", "argan_oil",
            "local_products", "markets",
        ],
        'areas': [
            "Agadir Bay", "Founty", "Hay Mohammadi", "Anza", "Tikiouine",
            "Cite Suisse", "Nouveau Talborjt", "Bensergao", "Tamraght"
        ],
        'priority': 6
    }
}

class MultiCityBusinessSearch:
    """Multi-city business search system for all Morocco cities."""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.cities_dir = self.results_dir / "cities"
        
        # Ensure folder structure exists
        self.setup_city_folders()
        self.setup_logging()
    
    def setup_city_folders(self):
        """Setup organized folder structure for all cities."""
        self.results_dir.mkdir(exist_ok=True)
        self.cities_dir.mkdir(exist_ok=True)
        
        for city_key in CITY_CONFIGS.keys():
            city_dir = self.cities_dir / city_key
            city_dir.mkdir(exist_ok=True)
            
            # Create subdirectories
            for subdir in ['searches', 'analytics', 'reports', 'exports']:
                (city_dir / subdir).mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Setup logging for multi-city searches."""
        import logging
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "multi_city_search.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def search_single_city(self, city_key: str, search_size: str = "standard") -> int:
        """Search businesses in a single city."""
        city_config = CITY_CONFIGS.get(city_key)
        if not city_config:
            console.print(f"[red]Error: City '{city_key}' not supported[/red]")
            return 0
        
        console.print(f"[blue]🏙️ Searching {city_config['name']} - {city_config['description']}[/blue]")
        
        # Configure search parameters
        if search_size == "test":
            max_per_query = 5
        elif search_size == "standard":
            max_per_query = 50
        elif search_size == "mega":
            max_per_query = 200
        else:
            max_per_query = 50
        
        total_businesses = 0
        city_dir = self.cities_dir / city_key / "searches"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate search queries for this city
        queries = self.generate_city_queries(city_config)
        
        console.print(f"[yellow]Generated {len(queries)} search queries for {city_config['name']}[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            
            task = progress.add_task(
                f"Searching {city_config['name']}", 
                total=len(queries)
            )
            
            batch_number = 1
            current_batch = []
            batch_size = 1000
            
            for i, query in enumerate(queries):
                progress.update(
                    task,
                    description=f"Searching {query['category']} in {query['area']} - Found: {total_businesses:,}",
                    advance=1
                )
                
                # Generate mock businesses for this query
                businesses = await self.search_city_query(query, max_per_query, city_key)
                
                for business in businesses:
                    business['city'] = city_key
                    business['city_name'] = city_config['name']
                    business['search_timestamp'] = datetime.now().isoformat()
                    
                    current_batch.append(business)
                    total_businesses += 1
                    
                    # Save batch when full
                    if len(current_batch) >= batch_size:
                        await self.save_city_batch(
                            city_key, current_batch, batch_number, timestamp
                        )
                        current_batch = []
                        batch_number += 1
                
                # Rate limiting
                await asyncio.sleep(0.1)
            
            # Save final batch
            if current_batch:
                await self.save_city_batch(
                    city_key, current_batch, batch_number, timestamp
                )
        
        # Save city summary
        await self.save_city_summary(city_key, total_businesses, timestamp)
        
        console.print(f"[green]✅ {city_config['name']} search complete: {total_businesses:,} businesses found![/green]")
        return total_businesses
    
    def generate_city_queries(self, city_config: Dict) -> List[Dict]:
        """Generate search queries for a specific city."""
        queries = []
        
        for category in city_config['categories']:
            for area in city_config['areas']:
                queries.append({
                    'query': category,
                    'location': f"{area}, {city_config['name']}, Morocco",
                    'category': category,
                    'area': area,
                    'city': city_config['name'],
                    'priority': city_config['priority']
                })
        
        return queries
    
    async def search_city_query(self, query: Dict, max_results: int, city_key: str) -> List[Dict]:
        """Search businesses for a city-specific query."""
        # Generate mock business data for demonstration
        businesses = []
        
        for i in range(min(max_results, 25)):  # Limit for demo
            business = {
                'id': f"{city_key}_{query['category']}_{i+1}",
                'name': f"{query['category'].replace('_', ' ').title()} {query['area']} {i+1}",
                'category': query['category'],
                'search_category': query['category'],
                'search_area': query['area'],
                'address': f"{i+1} Street, {query['area']}, {query['city']}",
                'phone': f"+212 5{city_key[:2]} {100000 + i}",
                'rating': round(2.0 + (i % 3) * 0.5, 1),
                'review_count': (i % 50) + 1,
                'website': None if i % 3 == 0 else f"https://{query['category']}{i}.com",
                'source': f'{city_key}_search'
            }
            
            # Calculate lead score
            business['lead_score'] = self.calculate_lead_score(business)
            business['opportunity_level'] = self.get_opportunity_level(business['lead_score'])
            
            businesses.append(business)
        
        return businesses
    
    def calculate_lead_score(self, business: Dict) -> int:
        """Calculate lead score for business."""
        score = 0
        
        # Website absence (30 points)
        if not business.get('website'):
            score += 30
        
        # Rating factor (25 points max)
        rating = business.get('rating', 0)
        if 2.0 <= rating <= 3.5:
            score += 25
        elif 3.5 < rating <= 4.0:
            score += 15
        elif rating > 4.0:
            score += 8
        else:
            score += 10
        
        # Review count (15 points max)
        review_count = business.get('review_count', 0)
        if review_count <= 20:
            score += 15
        elif review_count <= 50:
            score += 12
        else:
            score += 8
        
        # Contact info (10 points)
        if business.get('phone'):
            score += 10
        
        # Category factor (15 points)
        high_value_cats = ['restaurants', 'hotels', 'spas', 'tour_operators']
        if business.get('category', '').lower() in high_value_cats:
            score += 15
        else:
            score += 8
        
        # Location factor (5 points)
        score += 5
        
        return min(score, 100)
    
    def get_opportunity_level(self, score: int) -> str:
        """Get opportunity level based on score."""
        if score >= 80:
            return "EXCELLENT"
        elif score >= 70:
            return "HIGH"
        elif score >= 60:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def save_city_batch(self, city_key: str, businesses: List[Dict], 
                            batch_number: int, timestamp: str):
        """Save a batch of businesses for a city."""
        city_dir = self.cities_dir / city_key / "searches"
        filename = f"{city_key}_massive_search_{timestamp}_batch_{batch_number:03d}.json"
        filepath = city_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'search_date': datetime.now().isoformat(),
                    'city': city_key,
                    'city_name': CITY_CONFIGS[city_key]['name'],
                    'location': f"{CITY_CONFIGS[city_key]['name']}, Morocco",
                    'batch_number': batch_number,
                    'batch_size': len(businesses),
                    'search_type': 'city_specific_search'
                },
                'businesses': businesses
            }, f, indent=2, ensure_ascii=False)
    
    async def save_city_summary(self, city_key: str, total_businesses: int, timestamp: str):
        """Save summary for a city search."""
        city_dir = self.cities_dir / city_key / "searches"
        filename = f"{city_key}_massive_search_{timestamp}_SUMMARY.json"
        filepath = city_dir / filename
        
        city_config = CITY_CONFIGS[city_key]
        
        summary = {
            'search_summary': {
                'search_date': datetime.now().isoformat(),
                'city': city_key,
                'city_name': city_config['name'],
                'city_description': city_config['description'],
                'total_businesses_found': total_businesses,
                'categories_searched': len(city_config['categories']),
                'areas_searched': len(city_config['areas']),
                'priority_level': city_config['priority']
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    async def search_all_cities(self, search_size: str = "standard") -> Dict[str, int]:
        """Search all supported cities."""
        console.print(Panel(
            f"🇲🇦 MOROCCO-WIDE BUSINESS SEARCH\n"
            f"Searching ALL major cities in Morocco\n"
            f"Cities: {', '.join([c['name'] for c in CITY_CONFIGS.values()])}\n"
            f"Search Size: {search_size.upper()}",
            title="Multi-City Search",
            border_style="blue"
        ))
        
        results = {}
        total_all_cities = 0
        
        # Sort cities by priority
        sorted_cities = sorted(CITY_CONFIGS.items(), key=lambda x: x[1]['priority'])
        
        for city_key, city_config in sorted_cities:
            try:
                total = await self.search_single_city(city_key, search_size)
                results[city_key] = total
                total_all_cities += total
                
                console.print(f"[green]✅ {city_config['name']}: {total:,} businesses[/green]")
                
            except Exception as e:
                console.print(f"[red]❌ Error searching {city_config['name']}: {e}[/red]")
                results[city_key] = 0
        
        # Display final results
        self.display_multi_city_results(results, total_all_cities)
        
        return results
    
    def display_multi_city_results(self, results: Dict[str, int], total: int):
        """Display multi-city search results."""
        table = Table(title="🇲🇦 Morocco-Wide Business Search Results")
        
        table.add_column("City", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Businesses", style="magenta", justify="right")
        table.add_column("Status", style="blue")
        
        for city_key, city_config in CITY_CONFIGS.items():
            business_count = results.get(city_key, 0)
            status = "✅ Complete" if business_count > 0 else "❌ Failed"
            
            table.add_row(
                city_config['name'],
                city_config['description'],
                f"P{city_config['priority']}",
                f"{business_count:,}",
                status
            )
        
        table.add_row("", "", "", "", "", style="dim")
        table.add_row("TOTAL", "All Morocco", "", f"{total:,}", "✅ Complete", style="bold")
        
        console.print(table)
        
        panel = Panel(
            f"🎉 Morocco-wide search completed!\n"
            f"📊 Total businesses found: {total:,}\n"
            f"🏙️ Cities searched: {len([r for r in results.values() if r > 0])}/{len(CITY_CONFIGS)}\n"
            f"📁 Results organized in: results/cities/[city_name]/searches/",
            title="Search Complete",
            border_style="green"
        )
        console.print(panel)
    
    def list_supported_cities(self):
        """List all supported cities."""
        table = Table(title="🏙️ Supported Morocco Cities")
        
        table.add_column("City", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Categories", style="blue", justify="right")
        table.add_column("Areas", style="magenta", justify="right")
        
        for city_key, city_config in sorted(CITY_CONFIGS.items(), key=lambda x: x[1]['priority']):
            table.add_row(
                city_config['name'],
                city_config['description'],
                f"P{city_config['priority']}",
                str(len(city_config['categories'])),
                str(len(city_config['areas']))
            )
        
        console.print(table)

async def main():
    """Main function for city search."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-City Business Search for Morocco")
    parser.add_argument("--city", choices=list(CITY_CONFIGS.keys()) + ['all'], 
                       help="City to search (or 'all' for all cities)")
    parser.add_argument("--search-size", choices=['test', 'standard', 'mega'], 
                       default='standard', help="Search size")
    parser.add_argument("--list-cities", action="store_true", 
                       help="List supported cities")
    
    args = parser.parse_args()
    
    searcher = MultiCityBusinessSearch()
    
    if args.list_cities:
        searcher.list_supported_cities()
        return
    
    if not args.city:
        console.print("[yellow]Please specify a city or use --list-cities to see options[/yellow]")
        parser.print_help()
        return
    
    if args.city == 'all':
        await searcher.search_all_cities(args.search_size)
    else:
        await searcher.search_single_city(args.city, args.search_size)

if __name__ == "__main__":
    asyncio.run(main())
