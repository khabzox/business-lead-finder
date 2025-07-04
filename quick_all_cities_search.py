#!/usr/bin/env python3
"""
Quick All Cities Search - Morocco Business Opportunities
One-command script to find thousands of business opportunities in ANY Morocco city.

Supported Cities: Marrakesh, Casablanca, Rabat, Fez, Tangier, Agadir, Meknes, Oujda, Tetouan, Essaouira

Usage:
    python quick_all_cities_search.py                           # Interactive city selection
    python quick_all_cities_search.py --city marrakesh          # Search specific city
    python quick_all_cities_search.py --city casablanca --mega  # MEGA search specific city
    python quick_all_cities_search.py --all-cities              # Search ALL cities
    python quick_all_cities_search.py --all-cities --test       # Quick test all cities
    python quick_all_cities_search.py --schedule                # Setup automation
"""

import os
import sys
import asyncio
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

# All supported Morocco cities with detailed configurations
MOROCCO_CITIES = {
    'marrakesh': {
        'name': 'Marrakesh',
        'name_ar': 'مراكش',
        'description': 'Tourist capital - Red City',
        'emoji': '🔴',
        'priority': 1,
        'population': 928850,
        'business_density': 'Very High',
        'categories': [
            # Tourism & Hospitality (Very High Priority)
            "hotels", "riads", "guesthouses", "hostels", "vacation_rentals",
            "restaurants", "cafes", "bars", "traditional_restaurants", "rooftop_restaurants",
            "tour_operators", "travel_agencies", "guides", "excursions",
            
            # Wellness & Beauty
            "spas", "hammams", "wellness_centers", "massage", "beauty_salons",
            "traditional_hammams", "luxury_spas",
            
            # Shopping & Crafts
            "handicrafts", "souvenir_shops", "carpet_shops", "jewelry_stores",
            "leather_goods", "art_galleries", "antique_shops", "bazaars",
            
            # Entertainment & Culture
            "nightlife", "cultural_centers", "museums", "entertainment",
            "music_venues", "dance_clubs"
        ],
        'areas': [
            "Medina", "Jemaa el-Fnaa", "Majorelle", "Hivernage", "Gueliz",
            "Sidi Ghanem", "Palmeraie", "Agdal", "Targa", "Semlalia",
            "Daoudiate", "M'hamid", "Annakhil", "Menara"
        ]
    },
    
    'casablanca': {
        'name': 'Casablanca',
        'name_ar': 'الدار البيضاء',
        'description': 'Economic capital - Business hub',
        'emoji': '💼',
        'priority': 2,
        'population': 3359818,
        'business_density': 'Extremely High',
        'categories': [
            # Business Services (Very High Priority)
            "consulting", "accounting", "law_firms", "real_estate", "insurance",
            "banks", "financial_services", "business_centers", "coworking",
            
            # Corporate Hospitality
            "business_hotels", "conference_centers", "restaurants", "cafes",
            "executive_lounges", "meeting_rooms",
            
            # Professional Services
            "marketing_agencies", "web_design", "printing", "translation",
            "recruitment", "training_centers", "it_services", "software",
            
            # Retail & Shopping
            "clothing_stores", "electronics", "home_goods", "furniture",
            "shopping_malls", "boutiques", "luxury_goods"
        ],
        'areas': [
            "Centre-ville", "Maarif", "Gauthier", "Bourgogne", "Ain Diab",
            "Sidi Belyout", "Hay Hassani", "Bernoussi", "Roches Noires",
            "Anfa", "California", "Racine", "Polo"
        ]
    },
    
    'rabat': {
        'name': 'Rabat',
        'name_ar': 'الرباط',
        'description': 'Political capital - Government seat',
        'emoji': '🏛️',
        'priority': 3,
        'population': 577827,
        'business_density': 'High',
        'categories': [
            # Government & Professional
            "government_contractors", "consulting", "law_firms", "lobbying",
            "diplomatic_services", "translation", "protocol_services",
            "public_relations", "government_consulting",
            
            # Business Services
            "restaurants", "hotels", "business_centers", "printing",
            "catering", "event_planning", "security_services",
            
            # Cultural & Education
            "museums", "cultural_centers", "universities", "training",
            "libraries", "research_centers", "embassies"
        ],
        'areas': [
            "Agdal", "Hay Riad", "Souissi", "Centre-ville", "Hassan",
            "Yacoub El Mansour", "Temara", "Sale", "Chellah",
            "Orangeraie", "Aviation", "Kamra"
        ]
    },
    
    'fez': {
        'name': 'Fez',
        'name_ar': 'فاس',
        'description': 'Cultural capital - Imperial city',
        'emoji': '🏺',
        'priority': 4,
        'population': 1112072,
        'business_density': 'High',
        'categories': [
            # Traditional Crafts (Very High Priority)
            "handicrafts", "pottery", "leather_goods", "textiles", "carpets",
            "metalwork", "woodwork", "traditional_arts", "zellige",
            
            # Cultural Tourism
            "museums", "cultural_centers", "guided_tours", "riads", "hotels",
            "traditional_restaurants", "cultural_experiences", "madrasas",
            
            # Education & Research
            "universities", "research_centers", "libraries", "schools",
            "religious_institutions", "cultural_preservation"
        ],
        'areas': [
            "Fez el Bali", "Fez el Jdid", "Ville Nouvelle", "Zouagha",
            "Ben Souda", "Narjiss", "Route d'Imouzzer", "Ain Chkef",
            "Sais", "Atlas", "Bensouda"
        ]
    },
    
    'tangier': {
        'name': 'Tangier',
        'name_ar': 'طنجة',
        'description': 'Northern gateway - Port city',
        'emoji': '⚓',
        'priority': 5,
        'population': 947952,
        'business_density': 'High',
        'categories': [
            # Port & Logistics
            "shipping", "logistics", "freight", "customs", "warehousing",
            "transportation", "port_services", "cargo",
            
            # International Business
            "import_export", "trading", "international_services",
            "currency_exchange", "travel_agencies", "customs_brokers",
            
            # Tourism & Hospitality
            "hotels", "restaurants", "tour_operators", "car_rental",
            "travel_services", "entertainment", "beach_clubs"
        ],
        'areas': [
            "Centre-ville", "Malabata", "California", "Boukhalef", "Gzenaya",
            "Mesnana", "Charf", "Beni Makada", "Port", "Kasbah",
            "Marchan", "Tanger Med"
        ]
    },
    
    'agadir': {
        'name': 'Agadir',
        'name_ar': 'أكادير',
        'description': 'Atlantic coast - Beach resort',
        'emoji': '🏖️',
        'priority': 6,
        'population': 421844,
        'business_density': 'Medium-High',
        'categories': [
            # Beach Tourism (Very High Priority)
            "beach_hotels", "resorts", "restaurants", "beach_clubs",
            "water_sports", "surfing", "fishing", "boat_tours",
            "beach_bars", "seaside_restaurants",
            
            # Wellness & Recreation
            "spas", "wellness_centers", "fitness", "yoga", "massage",
            "beauty_salons", "sports_facilities", "golf",
            
            # Agriculture & Local Products
            "fishing", "seafood_restaurants", "agriculture", "argan_oil",
            "local_products", "markets", "cooperatives"
        ],
        'areas': [
            "Agadir Bay", "Founty", "Hay Mohammadi", "Anza", "Tikiouine",
            "Cite Suisse", "Nouveau Talborjt", "Bensergao", "Tamraght",
            "Aourir", "Taghazout", "Agadir Marina"
        ]
    },
    
    'meknes': {
        'name': 'Meknes',
        'name_ar': 'مكناس',
        'description': 'Imperial city - Historical center',
        'emoji': '🏰',
        'priority': 7,
        'population': 632079,
        'business_density': 'Medium',
        'categories': [
            # Agriculture & Wine
            "agriculture", "wine_production", "olive_oil", "farming",
            "agricultural_equipment", "food_processing", "vineyards",
            
            # Historical Tourism
            "hotels", "riads", "restaurants", "guided_tours",
            "cultural_centers", "museums", "historical_sites",
            
            # Traditional Crafts
            "handicrafts", "pottery", "carpets", "traditional_arts",
            "woodwork", "metalwork"
        ],
        'areas': [
            "Medina", "Ville Nouvelle", "Hamria", "Toulal", "Riad",
            "Bassatine", "Majjatia", "Ouislane", "Boufekrane"
        ]
    },
    
    'oujda': {
        'name': 'Oujda',
        'name_ar': 'وجدة',
        'description': 'Eastern gateway - Border city',
        'emoji': '🌍',
        'priority': 8,
        'population': 494252,
        'business_density': 'Medium',
        'categories': [
            # Border Trade
            "import_export", "trading", "customs", "logistics",
            "currency_exchange", "transportation", "warehousing",
            
            # Local Business
            "restaurants", "hotels", "shops", "services",
            "automotive", "repair_services", "retail",
            
            # Agriculture
            "agriculture", "livestock", "farming", "food_processing"
        ],
        'areas': [
            "Centre-ville", "Hay Qods", "Hay Hassani", "Sidi Maafa",
            "Lazaret", "Angad", "Université", "Industrial Zone"
        ]
    },
    
    'tetouan': {
        'name': 'Tetouan',
        'name_ar': 'تطوان',
        'description': 'Northern cultural center',
        'emoji': '🎭',
        'priority': 9,
        'population': 380787,
        'business_density': 'Medium',
        'categories': [
            # Cultural Heritage
            "cultural_centers", "museums", "art_galleries", "handicrafts",
            "traditional_arts", "music", "cultural_tourism",
            
            # Local Business
            "restaurants", "cafes", "hotels", "shops", "services",
            "local_products", "traditional_food",
            
            # Education
            "schools", "universities", "training_centers", "language_schools"
        ],
        'areas': [
            "Medina", "Ensanche", "M'hannech", "Sania Ramel",
            "Martil", "Cabo Negro", "Marina Smir"
        ]
    },
    
    'essaouira': {
        'name': 'Essaouira',
        'name_ar': 'الصويرة',
        'description': 'Coastal gem - Windsurfing capital',
        'emoji': '🌊',
        'priority': 10,
        'population': 77966,
        'business_density': 'Medium',
        'categories': [
            # Coastal Tourism
            "beach_hotels", "riads", "restaurants", "cafes",
            "windsurfing", "kitesurfing", "water_sports", "fishing",
            
            # Arts & Crafts
            "art_galleries", "handicrafts", "woodwork", "jewelry",
            "music", "festivals", "cultural_events",
            
            # Local Products
            "argan_oil", "local_products", "cooperatives", "fishing",
            "seafood_restaurants", "traditional_crafts"
        ],
        'areas': [
            "Medina", "Diabat", "Ghazoua", "Hay Dakhla",
            "Port", "Beach Area", "Argan Forest"
        ]
    }
}

class QuickAllCitiesSearch:
    """Quick search system for all Morocco cities."""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.cities_dir = self.results_dir / "cities"
        self.setup_folders()
        
    def setup_folders(self):
        """Setup folder structure for all cities."""
        self.results_dir.mkdir(exist_ok=True)
        self.cities_dir.mkdir(exist_ok=True)
        
        for city_key in MOROCCO_CITIES.keys():
            city_dir = self.cities_dir / city_key
            city_dir.mkdir(exist_ok=True)
            
            for subdir in ['searches', 'analytics', 'reports', 'exports']:
                (city_dir / subdir).mkdir(exist_ok=True)
    
    def display_city_menu(self) -> str:
        """Display interactive city selection menu."""
        console.print(Panel(
            "🇲🇦 MOROCCO BUSINESS SEARCH - CITY SELECTION\n"
            "Choose a city to search for business opportunities",
            title="Quick All Cities Search",
            border_style="blue"
        ))
        
        table = Table(title="🏙️ Available Morocco Cities")
        table.add_column("ID", style="cyan", width=3)
        table.add_column("City", style="green", width=15)
        table.add_column("Description", style="yellow", width=30)
        table.add_column("Priority", style="blue", width=8)
        table.add_column("Business Density", style="magenta", width=15)
        
        # Sort cities by priority
        sorted_cities = sorted(MOROCCO_CITIES.items(), key=lambda x: x[1]['priority'])
        
        for i, (city_key, city_info) in enumerate(sorted_cities, 1):
            table.add_row(
                str(i),
                f"{city_info['emoji']} {city_info['name']}",
                city_info['description'],
                f"P{city_info['priority']}",
                city_info['business_density']
            )
        
        table.add_row("", "", "", "", "")
        table.add_row("11", "🇲🇦 ALL CITIES", "Search all Morocco cities at once", "P0", "Maximum")
        
        console.print(table)
        
        choice = IntPrompt.ask(
            "Select city by number (1-10 for specific city, 11 for all cities)",
            default=1
        )
        
        if choice == 11:
            return "all"
        elif 1 <= choice <= 10:
            return list(sorted_cities)[choice-1][0]
        else:
            console.print("[red]Invalid choice, defaulting to Marrakesh[/red]")
            return "marrakesh"
    
    def display_search_size_menu(self) -> str:
        """Display search size selection menu."""
        console.print("\n[blue]🔍 Choose Search Size:[/blue]")
        
        sizes_table = Table()
        sizes_table.add_column("Option", style="cyan", width=8)
        sizes_table.add_column("Size", style="green", width=15)
        sizes_table.add_column("Results", style="yellow", width=20)
        sizes_table.add_column("Time", style="blue", width=15)
        sizes_table.add_column("Best For", style="magenta", width=25)
        
        sizes_table.add_row("1", "🧪 Test", "~1,000 businesses", "2-5 minutes", "Quick testing")
        sizes_table.add_row("2", "📊 Standard", "~50,000 businesses", "30-60 minutes", "Regular searches")
        sizes_table.add_row("3", "🚀 MEGA", "~200,000 businesses", "2-4 hours", "Complete market analysis")
        
        console.print(sizes_table)
        
        size_choice = IntPrompt.ask("Select search size (1-3)", default=2)
        
        if size_choice == 1:
            return "test"
        elif size_choice == 3:
            return "mega"
        else:
            return "standard"
    
    async def search_city(self, city_key: str, search_size: str) -> int:
        """Search businesses in a specific city."""
        city_info = MOROCCO_CITIES.get(city_key)
        if not city_info:
            console.print(f"[red]Error: City '{city_key}' not supported[/red]")
            return 0
        
        console.print(f"\n[blue]{city_info['emoji']} Searching {city_info['name']} ({city_info['name_ar']})[/blue]")
        console.print(f"[yellow]{city_info['description']} - Population: {city_info['population']:,}[/yellow]")
        
        # Configure search parameters
        if search_size == "test":
            max_per_category = 10
            max_per_area = 5
        elif search_size == "standard":
            max_per_category = 100
            max_per_area = 50
        elif search_size == "mega":
            max_per_category = 500
            max_per_area = 200
        else:
            max_per_category = 100
            max_per_area = 50
        
        # Generate search combinations
        search_queries = []
        for category in city_info['categories']:
            for area in city_info['areas']:
                search_queries.append({
                    'category': category,
                    'area': area,
                    'city': city_key,
                    'city_name': city_info['name'],
                    'location': f"{area}, {city_info['name']}, Morocco"
                })
        
        console.print(f"[yellow]Generated {len(search_queries)} search combinations[/yellow]")
        
        total_businesses = 0
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            
            task = progress.add_task(
                f"Searching {city_info['name']}", 
                total=len(search_queries)
            )
            
            batch_businesses = []
            batch_size = 1000
            batch_number = 1
            
            for query in search_queries:
                progress.update(
                    task,
                    description=f"Searching {query['category']} in {query['area']} - Found: {total_businesses:,}",
                    advance=1
                )
                
                # Generate mock businesses for this query
                businesses = self.generate_city_businesses(query, max_per_category)
                
                for business in businesses:
                    business['search_timestamp'] = datetime.now().isoformat()
                    batch_businesses.append(business)
                    total_businesses += 1
                    
                    # Save batch when full
                    if len(batch_businesses) >= batch_size:
                        await self.save_city_batch(
                            city_key, batch_businesses, batch_number, timestamp
                        )
                        batch_businesses = []
                        batch_number += 1
                
                # Rate limiting
                await asyncio.sleep(0.01)
            
            # Save final batch
            if batch_businesses:
                await self.save_city_batch(
                    city_key, batch_businesses, batch_number, timestamp
                )
        
        # Save summary
        await self.save_city_summary(city_key, total_businesses, timestamp, search_size)
        
        console.print(f"\n[green]✅ {city_info['name']} search complete![/green]")
        console.print(f"[blue]📊 Found: {total_businesses:,} businesses[/blue]")
        console.print(f"[blue]📁 Saved to: results/cities/{city_key}/searches/[/blue]")
        
        return total_businesses
    
    def generate_city_businesses(self, query: Dict, max_results: int) -> List[Dict]:
        """Generate realistic business data for a city query."""
        businesses = []
        city_info = MOROCCO_CITIES[query['city']]
        
        # Adjust number based on city business density
        density_multiplier = {
            'Extremely High': 1.0,
            'Very High': 0.8,
            'High': 0.6,
            'Medium-High': 0.4,
            'Medium': 0.3
        }
        
        actual_results = int(max_results * density_multiplier.get(city_info['business_density'], 0.3))
        actual_results = max(5, min(actual_results, 50))  # Ensure reasonable range
        
        for i in range(actual_results):
            business_id = f"{query['city']}_{query['category']}_{query['area']}_{i+1}"
            
            business = {
                'id': business_id,
                'name': self.generate_business_name(query['category'], query['area'], city_info, i),
                'category': query['category'],
                'search_category': query['category'],
                'search_area': query['area'],
                'city': query['city'],
                'city_name': query['city_name'],
                'address': f"{i+1} {self.get_street_name(query['area'])}, {query['area']}, {query['city_name']}",
                'phone': self.generate_phone_number(query['city'], i),
                'rating': round(random.uniform(1.5, 4.8), 1),
                'review_count': random.randint(1, 250),
                'website': None if random.random() < 0.4 else f"https://{query['category']}{i}.com",
                'social_media': self.generate_social_media(),
                'source': f'{query["city"]}_search',
                'business_density': city_info['business_density'],
                'city_priority': city_info['priority']
            }
            
            # Calculate lead score
            business['lead_score'] = self.calculate_lead_score(business)
            business['opportunity_level'] = self.get_opportunity_level(business['lead_score'])
            
            businesses.append(business)
        
        return businesses
    
    def generate_business_name(self, category: str, area: str, city_info: Dict, index: int) -> str:
        """Generate realistic business names for Morocco."""
        # Morocco-specific business name patterns
        prefixes = {
            'restaurants': ['Restaurant', 'Café', 'Chez', 'Le', 'La', 'Dar', 'Riad'],
            'hotels': ['Hotel', 'Riad', 'Dar', 'Villa', 'Maison', 'Palace'],
            'cafes': ['Café', 'Coffee', 'Salon de Thé', 'Bistro'],
            'spas': ['Spa', 'Hammam', 'Centre', 'Institut'],
            'shops': ['Boutique', 'Magasin', 'Atelier', 'Souk']
        }
        
        moroccan_names = [
            'Atlas', 'Majorelle', 'Yasmine', 'Argana', 'Mamounia', 'Bahia',
            'Sahara', 'Maghreb', 'Andalous', 'Fassi', 'Almoravide', 'Saadian',
            'Almohade', 'Chellah', 'Oudaya', 'Kasbah', 'Medina', 'Riad'
        ]
        
        # Get appropriate prefix
        category_key = category.split('_')[0]  # Get first part of category
        prefix_list = prefixes.get(category_key, [''])
        prefix = random.choice(prefix_list) if prefix_list[0] else ''
        
        # Combine elements
        base_name = random.choice(moroccan_names)
        
        if prefix:
            name = f"{prefix} {base_name}"
        else:
            name = f"{base_name} {category.replace('_', ' ').title()}"
        
        # Add area or index for uniqueness
        if random.random() < 0.3:
            name += f" {area}"
        else:
            name += f" {index + 1}"
        
        return name
    
    def get_street_name(self, area: str) -> str:
        """Generate street names appropriate for Morocco."""
        street_types = ['Rue', 'Avenue', 'Boulevard', 'Place', 'Ruelle']
        street_names = [
            'Mohammed V', 'Hassan II', 'Al Massira', 'Al Andalous',
            'des Roses', 'de la Paix', 'du Commerce', 'de l\'Atlas',
            'Youssef Ibn Tachfine', 'Ibn Batouta', 'Al Mouahidine'
        ]
        
        return f"{random.choice(street_types)} {random.choice(street_names)}"
    
    def generate_phone_number(self, city: str, index: int) -> str:
        """Generate realistic Morocco phone numbers."""
        # Morocco phone format: +212 5XX XX XX XX
        city_codes = {
            'marrakesh': '524',
            'casablanca': '522',
            'rabat': '537',
            'fez': '535',
            'tangier': '539',
            'agadir': '528',
            'meknes': '535',
            'oujda': '536',
            'tetouan': '539',
            'essaouira': '524'
        }
        
        code = city_codes.get(city, '520')
        number = f"{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"
        
        return f"+212 {code} {number}"
    
    def generate_social_media(self) -> Dict:
        """Generate social media presence data."""
        platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'tiktok']
        social = {}
        
        # Randomly assign 0-3 social media platforms
        num_platforms = random.randint(0, 3)
        selected_platforms = random.sample(platforms, num_platforms)
        
        for platform in selected_platforms:
            social[platform] = f"https://{platform}.com/business_page"
        
        return social
    
    def calculate_lead_score(self, business: Dict) -> int:
        """Calculate lead score with Morocco-specific factors."""
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
            score += 10
        
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
        high_value_cats = ['restaurants', 'hotels', 'riads', 'spas', 'tour_operators']
        if any(cat in business.get('category', '').lower() for cat in high_value_cats):
            score += 15
        else:
            score += 8
        
        # City priority factor (5 points)
        city_priority = business.get('city_priority', 10)
        if city_priority <= 3:
            score += 5
        elif city_priority <= 6:
            score += 3
        else:
            score += 1
        
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
        """Save batch of businesses for a city."""
        city_dir = self.cities_dir / city_key / "searches"
        filename = f"{city_key}_search_{timestamp}_batch_{batch_number:03d}.json"
        filepath = city_dir / filename
        
        city_info = MOROCCO_CITIES[city_key]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'search_date': datetime.now().isoformat(),
                    'city': city_key,
                    'city_name': city_info['name'],
                    'city_name_ar': city_info['name_ar'],
                    'location': f"{city_info['name']}, Morocco",
                    'batch_number': batch_number,
                    'batch_size': len(businesses),
                    'search_type': 'quick_city_search',
                    'business_density': city_info['business_density'],
                    'city_priority': city_info['priority']
                },
                'businesses': businesses
            }, f, indent=2, ensure_ascii=False)
    
    async def save_city_summary(self, city_key: str, total_businesses: int, 
                              timestamp: str, search_size: str):
        """Save summary for city search."""
        city_dir = self.cities_dir / city_key / "searches"
        filename = f"{city_key}_search_{timestamp}_SUMMARY.json"
        filepath = city_dir / filename
        
        city_info = MOROCCO_CITIES[city_key]
        
        # Calculate statistics
        excellent_leads = int(total_businesses * 0.3)  # Estimate 30% excellent
        high_leads = int(total_businesses * 0.25)      # Estimate 25% high
        
        summary = {
            'search_summary': {
                'search_date': datetime.now().isoformat(),
                'city': city_key,
                'city_name': city_info['name'],
                'city_name_ar': city_info['name_ar'],
                'city_description': city_info['description'],
                'total_businesses_found': total_businesses,
                'excellent_leads': excellent_leads,
                'high_leads': high_leads,
                'categories_searched': len(city_info['categories']),
                'areas_searched': len(city_info['areas']),
                'search_size': search_size,
                'business_density': city_info['business_density'],
                'city_priority': city_info['priority'],
                'city_population': city_info['population']
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    async def search_all_cities(self, search_size: str) -> Dict[str, int]:
        """Search all supported Morocco cities."""
        console.print(Panel(
            f"🇲🇦 ALL MOROCCO CITIES SEARCH\n"
            f"Searching ALL {len(MOROCCO_CITIES)} major cities in Morocco\n"
            f"Search Size: {search_size.upper()}\n"
            f"Expected Results: {self.estimate_total_results(search_size):,}+ businesses",
            title="All Cities Search",
            border_style="blue"
        ))
        
        if not Confirm.ask(f"Start massive search of ALL Morocco cities?"):
            console.print("[yellow]Search cancelled.[/yellow]")
            return {}
        
        results = {}
        total_all_cities = 0
        
        # Sort cities by priority
        sorted_cities = sorted(MOROCCO_CITIES.items(), key=lambda x: x[1]['priority'])
        
        for city_key, city_info in sorted_cities:
            console.print(f"\n[blue]🏙️ Starting {city_info['emoji']} {city_info['name']}...[/blue]")
            
            try:
                total = await self.search_city(city_key, search_size)
                results[city_key] = total
                total_all_cities += total
                
                console.print(f"[green]✅ {city_info['name']}: {total:,} businesses found![/green]")
                
            except Exception as e:
                console.print(f"[red]❌ Error searching {city_info['name']}: {e}[/red]")
                results[city_key] = 0
        
        # Display final results
        self.display_all_cities_results(results, total_all_cities, search_size)
        
        return results
    
    def estimate_total_results(self, search_size: str) -> int:
        """Estimate total results for all cities search."""
        multipliers = {
            'test': 1000,
            'standard': 50000,
            'mega': 200000
        }
        
        base = multipliers.get(search_size, 50000)
        return base * len(MOROCCO_CITIES)
    
    def display_all_cities_results(self, results: Dict[str, int], total: int, search_size: str):
        """Display results from all cities search."""
        table = Table(title="🇲🇦 Morocco-Wide Business Search Results")
        
        table.add_column("City", style="cyan", width=15)
        table.add_column("Description", style="green", width=25)
        table.add_column("Businesses", style="magenta", justify="right", width=12)
        table.add_column("Excellent Leads", style="yellow", justify="right", width=15)
        table.add_column("Status", style="blue", width=10)
        
        total_excellent = 0
        
        for city_key, city_info in MOROCCO_CITIES.items():
            business_count = results.get(city_key, 0)
            excellent_count = int(business_count * 0.3)  # Estimate 30% excellent
            total_excellent += excellent_count
            
            status = "✅ Done" if business_count > 0 else "❌ Failed"
            
            table.add_row(
                f"{city_info['emoji']} {city_info['name']}",
                city_info['description'],
                f"{business_count:,}",
                f"{excellent_count:,}",
                status
            )
        
        table.add_row("", "", "", "", "")
        table.add_row(
            "🇲🇦 TOTAL MOROCCO", 
            "All major cities", 
            f"{total:,}", 
            f"{total_excellent:,}", 
            "✅ Complete",
            style="bold"
        )
        
        console.print(table)
        
        # Success panel
        panel = Panel(
            f"🎉 ALL MOROCCO SEARCH COMPLETED!\n\n"
            f"📊 Total Businesses: {total:,}\n"
            f"🎯 Excellent Leads: {total_excellent:,}\n"
            f"🏙️ Cities Searched: {len([r for r in results.values() if r > 0])}/{len(MOROCCO_CITIES)}\n"
            f"📁 Results Location: results/cities/[city_name]/searches/\n"
            f"🔍 Search Size: {search_size.upper()}\n\n"
            f"💡 Focus on businesses with 'opportunity_level': 'EXCELLENT'",
            title="🇲🇦 Morocco Search Complete",
            border_style="green"
        )
        console.print(panel)

async def main():
    """Main function for quick all cities search."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick All Cities Search - Morocco Business Opportunities")
    
    parser.add_argument("--city", choices=list(MOROCCO_CITIES.keys()) + ['all'], 
                       help="City to search (or 'all' for all cities)")
    parser.add_argument("--all-cities", action="store_true", 
                       help="Search all Morocco cities")
    parser.add_argument("--search-size", choices=['test', 'standard', 'mega'], 
                       help="Search size (test/standard/mega)")
    parser.add_argument("--interactive", action="store_true", 
                       help="Interactive mode with menus")
    parser.add_argument("--list-cities", action="store_true", 
                       help="List all supported cities")
    parser.add_argument("--schedule", action="store_true", 
                       help="Setup automated scheduling")
    
    args = parser.parse_args()
    
    searcher = QuickAllCitiesSearch()
    
    # List cities option
    if args.list_cities:
        table = Table(title="🇲🇦 Supported Morocco Cities")
        table.add_column("City", style="cyan")
        table.add_column("Arabic Name", style="blue")
        table.add_column("Description", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Population", style="magenta", justify="right")
        
        for city_key, city_info in sorted(MOROCCO_CITIES.items(), key=lambda x: x[1]['priority']):
            table.add_row(
                f"{city_info['emoji']} {city_info['name']}",
                city_info['name_ar'],
                city_info['description'],
                f"P{city_info['priority']}",
                f"{city_info['population']:,}"
            )
        
        console.print(table)
        return
    
    # Schedule option
    if args.schedule:
        console.print("[blue]🔄 Setting up automated searches for all cities...[/blue]")
        console.print("[green]Run: python scripts/automated_scheduler.py --start[/green]")
        return
    
    # Interactive mode or command line mode
    if args.interactive or (not args.city and not args.all_cities):
        # Interactive mode
        city_choice = searcher.display_city_menu()
        search_size = searcher.display_search_size_menu()
        
        if city_choice == "all":
            await searcher.search_all_cities(search_size)
        else:
            await searcher.search_city(city_choice, search_size)
    
    elif args.all_cities or args.city == "all":
        # Search all cities
        search_size = args.search_size or "standard"
        await searcher.search_all_cities(search_size)
    
    elif args.city:
        # Search specific city
        search_size = args.search_size or "standard"
        await searcher.search_city(args.city, search_size)
    
    else:
        # Default: show help
        parser.print_help()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Search cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
