#!/usr/bin/env python3
"""
City Results Organization System
Organizes business search results by cities with proper folder structure.

Folder Structure:
results/
├── cities/
│   ├── marrakesh/
│   ├── casablanca/
│   ├── rabat/
│   ├── fez/
│   ├── tangier/
│   ├── agadir/
│   └── other/
├── analytics/
├── reports/
└── exports/
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CityResultsOrganizer:
    """Organizes business search results by cities with proper folder structure."""
    
    def __init__(self):
        self.base_results_dir = Path("results")
        self.cities_dir = self.base_results_dir / "cities"
        self.analytics_dir = self.base_results_dir / "analytics"
        self.reports_dir = self.base_results_dir / "reports"
        self.exports_dir = self.base_results_dir / "exports"
        
        # Supported Moroccan cities
        self.supported_cities = {
            'marrakesh': {
                'name': 'Marrakesh',
                'aliases': ['marrakech', 'marrakesh', 'marrakech-safi'],
                'description': 'Tourist capital - Red City',
                'priority': 1
            },
            'casablanca': {
                'name': 'Casablanca',
                'aliases': ['casa', 'casablanca', 'dar-el-beida'],
                'description': 'Economic capital - Business hub',
                'priority': 2
            },
            'rabat': {
                'name': 'Rabat',
                'aliases': ['rabat', 'rabat-sale', 'capital'],
                'description': 'Political capital - Government seat',
                'priority': 3
            },
            'fez': {
                'name': 'Fez',
                'aliases': ['fes', 'fez', 'fes-meknes'],
                'description': 'Cultural capital - Imperial city',
                'priority': 4
            },
            'tangier': {
                'name': 'Tangier',
                'aliases': ['tanger', 'tangier', 'tangier-tetouan'],
                'description': 'Northern gateway - Port city',
                'priority': 5
            },
            'agadir': {
                'name': 'Agadir',
                'aliases': ['agadir', 'agadir-ida-outanane'],
                'description': 'Atlantic coast - Beach resort',
                'priority': 6
            },
            'meknes': {
                'name': 'Meknes',
                'aliases': ['meknes', 'meknes-tafilalet'],
                'description': 'Imperial city - Historical center',
                'priority': 7
            },
            'oujda': {
                'name': 'Oujda',
                'aliases': ['oujda', 'oujda-angad'],
                'description': 'Eastern gateway - Border city',
                'priority': 8
            },
            'tetouan': {
                'name': 'Tetouan',
                'aliases': ['tetouan', 'tetuan'],
                'description': 'Northern cultural center',
                'priority': 9
            },
            'essaouira': {
                'name': 'Essaouira',
                'aliases': ['essaouira', 'mogador'],
                'description': 'Coastal gem - Windsurfing capital',
                'priority': 10
            }
        }
        
        self.setup_folder_structure()
    
    def setup_folder_structure(self):
        """Create organized folder structure for all supported cities."""
        console.print("[blue]🏗️ Setting up organized folder structure...[/blue]")
        
        # Create main directories
        directories = [
            self.cities_dir,
            self.analytics_dir,
            self.reports_dir,
            self.exports_dir
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
        
        # Create city-specific directories
        for city_key, city_info in self.supported_cities.items():
            city_dir = self.cities_dir / city_key
            city_dir.mkdir(exist_ok=True)
            
            # Create subdirectories for each city
            subdirs = ['searches', 'analytics', 'reports', 'exports']
            for subdir in subdirs:
                (city_dir / subdir).mkdir(exist_ok=True)
        
        # Create 'other' directory for unsupported cities
        other_dir = self.cities_dir / "other"
        other_dir.mkdir(exist_ok=True)
        
        console.print("[green]✅ Folder structure created successfully![/green]")
    
    def detect_city_from_filename(self, filename: str) -> str:
        """Detect city from filename or content."""
        filename_lower = filename.lower()
        
        for city_key, city_info in self.supported_cities.items():
            for alias in city_info['aliases']:
                if alias.lower() in filename_lower:
                    return city_key
        
        return 'other'
    
    def detect_city_from_content(self, file_path: Path) -> str:
        """Detect city from file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check metadata location
            metadata = data.get('metadata', {})
            location = metadata.get('location', '').lower()
            
            for city_key, city_info in self.supported_cities.items():
                for alias in city_info['aliases']:
                    if alias.lower() in location:
                        return city_key
            
            # Check business locations
            businesses = data.get('businesses', [])
            if businesses:
                first_business = businesses[0]
                address = first_business.get('address', '').lower()
                search_area = first_business.get('search_area', '').lower()
                
                for city_key, city_info in self.supported_cities.items():
                    for alias in city_info['aliases']:
                        if alias.lower() in address or alias.lower() in search_area:
                            return city_key
        
        except Exception as e:
            console.print(f"[yellow]Warning: Could not read {file_path}: {e}[/yellow]")
        
        return 'other'
    
    def organize_existing_files(self):
        """Organize existing result files into city-specific folders."""
        console.print("[blue]📁 Organizing existing result files by city...[/blue]")
        
        organized_count = 0
        city_counts = {}
        
        # Process all JSON files in the results directory
        for file_path in self.base_results_dir.glob("*.json"):
            if file_path.name.startswith('.'):
                continue
                
            # Detect city from filename first, then content
            city = self.detect_city_from_filename(file_path.name)
            if city == 'other':
                city = self.detect_city_from_content(file_path)
            
            # Move file to appropriate city folder
            target_dir = self.cities_dir / city / "searches"
            target_path = target_dir / file_path.name
            
            try:
                shutil.move(str(file_path), str(target_path))
                organized_count += 1
                city_counts[city] = city_counts.get(city, 0) + 1
                
            except Exception as e:
                console.print(f"[red]Error moving {file_path.name}: {e}[/red]")
        
        # Display organization results
        if organized_count > 0:
            console.print(f"[green]✅ Organized {organized_count} files by city:[/green]")
            for city, count in city_counts.items():
                city_name = self.supported_cities.get(city, {}).get('name', city.title())
                console.print(f"   📍 {city_name}: {count} files")
        else:
            console.print("[yellow]No files found to organize[/yellow]")
    
    def get_city_folder_path(self, city_name: str) -> Path:
        """Get the folder path for a specific city."""
        city_key = self.normalize_city_name(city_name)
        return self.cities_dir / city_key / "searches"
    
    def normalize_city_name(self, city_name: str) -> str:
        """Normalize city name to match folder structure."""
        city_lower = city_name.lower().strip()
        
        for city_key, city_info in self.supported_cities.items():
            for alias in city_info['aliases']:
                if alias.lower() == city_lower:
                    return city_key
        
        return 'other'
    
    def create_city_readme(self, city_key: str):
        """Create README file for city folder."""
        city_info = self.supported_cities.get(city_key)
        if not city_info:
            return
        
        city_dir = self.cities_dir / city_key
        readme_path = city_dir / "README.md"
        
        readme_content = f"""# {city_info['name']} Business Search Results

## About {city_info['name']}
{city_info['description']}

## Folder Structure
```
{city_key}/
├── searches/     # Raw search results (JSON files)
├── analytics/    # Analysis and statistics
├── reports/      # Generated reports (HTML, PDF)
└── exports/      # Exported data (CSV, Excel)
```

## Search Coverage
This folder contains business search results for {city_info['name']} and surrounding areas.

### Aliases Recognized
{', '.join(city_info['aliases'])}

### Priority Level
Priority {city_info['priority']} - {'High' if city_info['priority'] <= 3 else 'Medium' if city_info['priority'] <= 6 else 'Standard'} priority city

## File Naming Convention
- Search results: `{city_key}_massive_search_YYYYMMDD_HHMMSS_batch_XXX.json`
- Summaries: `{city_key}_massive_search_YYYYMMDD_HHMMSS_SUMMARY.json`
- Analytics: `{city_key}_analytics_YYYYMM.json`
- Reports: `{city_key}_report_YYYYMMDD.html`

## Quick Stats
- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Total search files: {len(list((city_dir / 'searches').glob('*.json')))}
- Total businesses: (Run analytics to calculate)

## Usage
```bash
# Search {city_info['name']} specifically
python city_search.py --city {city_key}

# Generate {city_info['name']} analytics
python generate_analytics.py --city {city_key}

# Create {city_info['name']} report
python generate_report.py --city {city_key}
```
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_all_city_readmes(self):
        """Create README files for all supported cities."""
        for city_key in self.supported_cities.keys():
            self.create_city_readme(city_key)
        
        console.print("[green]✅ Created README files for all cities[/green]")
    
    def display_folder_structure(self):
        """Display the current folder organization."""
        table = Table(title="🏙️ City Results Organization")
        
        table.add_column("City", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Files", style="magenta", justify="right")
        
        for city_key, city_info in sorted(self.supported_cities.items(), key=lambda x: x[1]['priority']):
            city_dir = self.cities_dir / city_key / "searches"
            file_count = len(list(city_dir.glob('*.json'))) if city_dir.exists() else 0
            
            priority_text = f"P{city_info['priority']}"
            if city_info['priority'] <= 3:
                priority_text += " (High)"
            elif city_info['priority'] <= 6:
                priority_text += " (Medium)"
            
            table.add_row(
                city_info['name'],
                city_info['description'],
                priority_text,
                str(file_count)
            )
        
        console.print(table)
        
        # Display folder structure
        panel = Panel(
            f"📁 Organized folder structure:\n"
            f"results/cities/\n"
            f"├── marrakesh/  (searches, analytics, reports, exports)\n"
            f"├── casablanca/ (searches, analytics, reports, exports)\n"
            f"├── rabat/      (searches, analytics, reports, exports)\n"
            f"├── fez/        (searches, analytics, reports, exports)\n"
            f"├── tangier/    (searches, analytics, reports, exports)\n"
            f"├── agadir/     (searches, analytics, reports, exports)\n"
            f"└── other/      (unsupported cities)",
            title="Folder Structure",
            border_style="blue"
        )
        console.print(panel)

def organize_city_results():
    """Main function to organize city results."""
    organizer = CityResultsOrganizer()
    
    console.print(Panel(
        "🏙️ CITY RESULTS ORGANIZATION SYSTEM\n"
        "Organizing business search results by cities\n"
        "Creating proper folder structure for better management",
        title="City Organization",
        border_style="blue"
    ))
    
    # Organize existing files
    organizer.organize_existing_files()
    
    # Create README files
    organizer.create_all_city_readmes()
    
    # Display structure
    organizer.display_folder_structure()
    
    console.print("[green]✅ City organization complete![/green]")
    console.print("[blue]📁 All results are now organized by city in results/cities/[/blue]")

if __name__ == "__main__":
    organize_city_results()
