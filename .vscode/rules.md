# Business Lead Finder - VSCode Rules and Guidelines

## 🎯 Project: Business Lead Finder

### 📋 Core Coding Rules

#### 1. **NO CLASSES - Use Functions Only**
```python
# ❌ DON'T USE
class BusinessFinder:
    def __init__(self):
        pass

# ✅ DO USE
def find_businesses(location, categories):
    pass
```

#### 2. **Function Naming Convention**
```python
# ✅ Use descriptive function names
def search_google_places(query, location, max_results=20):
    pass

def check_website_exists(business_name, phone_number):
    pass

def generate_lead_report(business_data):
    pass
```

#### 3. **File Structure Rules**
```
src/
├── main.py              # Entry point with CLI
├── business_search.py   # Core search functions
├── website_checker.py   # Website detection functions
├── data_processor.py    # Data processing functions
├── report_generator.py  # Report generation functions
├── cli_interface.py     # CLI commands and interface
└── utils.py            # Utility functions
```

#### 4. **CLI Interface Guidelines**
```python
# ✅ Use argparse for CLI commands
import argparse

def create_cli_parser():
    """Create command line interface parser."""
    parser = argparse.ArgumentParser(
        description='Business Lead Finder - Find businesses without websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels
  python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
  python main.py report --input data/leads.json --output results/report.html
  python main.py export --format csv --output results/leads.csv
        '''
    )
    return parser

# ✅ CLI Commands Structure
def cli_search_command(args):
    """Handle search command from CLI."""
    pass

def cli_check_command(args):
    """Handle website check command from CLI."""
    pass

def cli_report_command(args):
    """Handle report generation command from CLI."""
    pass
```

#### 5. **Import Guidelines**
```python
# ✅ Standard library first
import os
import sys
import time
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path

# ✅ Third-party libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# ✅ Local imports last
from utils import clean_phone_number, validate_email
from config import API_KEYS, DEFAULT_SETTINGS
```

#### 6. **Error Handling**
```python
# ✅ Always use try-except for API calls
def search_business_api(query):
    try:
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
```

#### 7. **Configuration Management**
```python
# ✅ Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration constants
GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', 'Marrakesh, Morocco')
MAX_RESULTS = int(os.getenv('MAX_RESULTS', '50'))
DELAY_SECONDS = int(os.getenv('DELAY_SECONDS', '1'))
```

#### 8. **Data Validation**
```python
# ✅ Always validate inputs
def validate_business_data(business):
    required_fields = ['name', 'address', 'phone']
    for field in required_fields:
        if not business.get(field):
            return False
    return True

def validate_cli_args(args):
    """Validate CLI arguments."""
    if args.location and len(args.location.strip()) < 2:
        raise ValueError("Location must be at least 2 characters")
    return True
```

#### 9. **Logging Instead of Print**
```python
import logging
from rich.console import Console

# ✅ Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('business_finder.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
console = Console()

# ✅ Use logger and rich console
def search_businesses(query):
    logger.info(f"Starting search for: {query}")
    console.print(f"[blue]Searching for businesses: {query}[/blue]")
    # ... search logic
    logger.info(f"Found {len(results)} businesses")
    console.print(f"[green]Found {len(results)} businesses[/green]")
```

#### 10. **Type Hints**
```python
from typing import List, Dict, Optional, Union, Tuple

def search_businesses(
    location: str, 
    categories: List[str], 
    max_results: int = 20
) -> List[Dict[str, str]]:
    """Search for businesses in specified location."""
    pass

def check_website_exists(business_name: str) -> Optional[str]:
    """Check if business has a website."""
    pass

def process_cli_command(args: argparse.Namespace) -> bool:
    """Process CLI command and return success status."""
    pass
```

### 🔧 CLI Design Rules

#### 1. **Command Structure**
```bash
# ✅ Main commands
python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels
python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
python main.py report --input data/leads.json --output results/report.html
python main.py export --format csv --output results/leads.csv
python main.py analyze --input data/leads.json
python main.py interactive  # Interactive mode

# ✅ Global options
python main.py --verbose search --location "Marrakesh, Morocco"
python main.py --config custom.env search --location "Marrakesh, Morocco"
python main.py --help
```

#### 2. **Interactive Mode**
```python
# ✅ Interactive CLI session
def interactive_mode():
    """Run interactive CLI session."""
    console.print("[bold blue]Business Lead Finder - Interactive Mode[/bold blue]")
    console.print("Type 'help' for available commands or 'exit' to quit")
    
    while True:
        try:
            command = console.input("\n[bold green]business-finder>[/bold green] ")
            if command.lower() in ['exit', 'quit']:
                break
            elif command.lower() == 'help':
                show_interactive_help()
            else:
                process_interactive_command(command)
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
```

#### 3. **Progress Indicators**
```python
# ✅ Use rich progress bars
from rich.progress import Progress, SpinnerColumn, TextColumn

def search_with_progress(queries, location):
    """Search businesses with progress indicator."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Searching businesses...", total=len(queries))
        
        results = []
        for query in queries:
            progress.update(task, description=f"Searching {query}...")
            result = search_single_category(query, location)
            results.extend(result)
            progress.advance(task)
        
        return results
```

#### 4. **Output Formatting**
```python
# ✅ Use rich tables for output
from rich.table import Table

def display_business_results(businesses):
    """Display business results in formatted table."""
    table = Table(title="Business Search Results")
    
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Phone", style="green")
    table.add_column("Website", style="red")
    table.add_column("Lead Score", justify="right", style="blue")
    
    for business in businesses:
        website_status = "✅ Yes" if business.get('website') else "❌ No"
        table.add_row(
            business.get('name', 'N/A'),
            business.get('category', 'N/A'),
            business.get('phone', 'N/A'),
            website_status,
            str(business.get('lead_score', 0))
        )
    
    console.print(table)
```

### 🎨 Code Style Rules

#### 1. **Variable Naming**
```python
# ✅ Use descriptive names
business_name = "Restaurant Atlas"
phone_number = "+212 5 24 44 33 22"
website_url = "https://example.com"
search_results = []
total_businesses_found = 0
cli_args = None
user_input = ""

# ❌ Avoid abbreviations
bus_name = "Restaurant Atlas"  # Don't do this
ph_num = "+212 5 24 44 33 22"  # Don't do this
```

#### 2. **Function Size**
```python
# ✅ Keep functions small and focused
def extract_phone_number(business_data):
    """Extract and clean phone number from business data."""
    phone = business_data.get('phone', '')
    if phone:
        return clean_phone_number(phone)
    return None

def clean_phone_number(phone):
    """Remove non-numeric characters from phone number."""
    import re
    return re.sub(r'[^\d+]', '', phone)

def handle_cli_search(args):
    """Handle search command from CLI."""
    results = search_businesses(args.location, args.categories)
    display_business_results(results)
    return len(results)
```

#### 3. **Constants**
```python
# ✅ Use constants for configuration
MAX_RETRY_ATTEMPTS = 3
REQUEST_TIMEOUT = 30
MIN_BUSINESS_RATING = 4.0
DEFAULT_SEARCH_RADIUS = 5000  # meters
CLI_COMMANDS = ['search', 'check', 'report', 'export', 'analyze', 'interactive']
OUTPUT_FORMATS = ['csv', 'json', 'html', 'pdf']
```

#### 4. **File Handling**
```python
# ✅ Always use context managers
def save_business_data(business_data, filename):
    """Save business data to file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(business_data, f, indent=2, ensure_ascii=False)

def load_business_data(filename):
    """Load business data from file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filename}")
        return []
```

### 🚀 Performance Rules

#### 1. **Efficient Data Processing**
```python
# ✅ Use list comprehensions for simple operations
valid_businesses = [
    business for business in all_businesses 
    if business.get('rating', 0) >= MIN_BUSINESS_RATING
]

# ✅ Use generators for large datasets
def process_businesses(business_list):
    for business in business_list:
        if validate_business_data(business):
            yield process_single_business(business)
```

#### 2. **Rate Limiting**
```python
import time
from functools import wraps

def rate_limit(seconds=1):
    """Decorator to rate limit function calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(seconds=1)
def api_call(url, params):
    return requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
```

### 🔍 Testing Rules

#### 1. **Test Structure**
```python
# tests/test_business_search.py
import pytest
from unittest.mock import patch, MagicMock
from business_search import search_google_places

def test_search_google_places_success():
    """Test successful Google Places search."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [{'name': 'Test Restaurant'}]
        }
        mock_get.return_value = mock_response
        
        results = search_google_places('restaurants', 'Marrakesh')
        assert len(results) == 1
        assert results[0]['name'] == 'Test Restaurant'

def test_cli_search_command():
    """Test CLI search command."""
    from unittest.mock import Namespace
    args = Namespace(location='Marrakesh', categories=['restaurants'])
    
    with patch('business_search.search_businesses') as mock_search:
        mock_search.return_value = [{'name': 'Test Restaurant'}]
        result = cli_search_command(args)
        assert result == 1
```

### 📊 Data Structure Rules

#### 1. **Consistent Data Format**
```python
# ✅ Standard business data structure
BUSINESS_DATA_TEMPLATE = {
    'name': str,
    'category': str,
    'address': str,
    'phone': str,
    'email': str,
    'website': str,
    'rating': float,
    'review_count': int,
    'social_media': dict,
    'lead_score': int,
    'last_updated': str,
    'source': str
}

def create_business_record(name, category, address, phone=None):
    """Create a standardized business record."""
    return {
        'name': name,
        'category': category,
        'address': address,
        'phone': phone or '',
        'email': '',
        'website': '',
        'rating': 0.0,
        'review_count': 0,
        'social_media': {},
        'lead_score': 0,
        'last_updated': datetime.now().isoformat(),
        'source': 'unknown'
    }
```

### 🔐 Security Rules

#### 1. **API Key Management**
```python
# ✅ Never hardcode API keys
import os

def get_api_key(service_name):
    """Safely get API key from environment."""
    key = os.getenv(f'{service_name.upper()}_API_KEY')
    if not key:
        logger.warning(f"Missing API key for {service_name}")
        return None
    return key
```

#### 2. **Input Validation**
```python
def validate_location(location):
    """Validate location input."""
    if not location or not isinstance(location, str):
        raise ValueError("Location must be a non-empty string")
    
    if len(location) < 2:
        raise ValueError("Location must be at least 2 characters")
    
    return location.strip()

def validate_categories(categories):
    """Validate categories input."""
    if not categories or not isinstance(categories, list):
        raise ValueError("Categories must be a non-empty list")
    
    valid_categories = ['restaurants', 'hotels', 'cafes', 'shops', 'services']
    for category in categories:
        if category not in valid_categories:
            logger.warning(f"Unknown category: {category}")
    
    return categories
```

### 📝 Documentation Rules

#### 1. **Function Documentation**
```python
def search_businesses(location, categories, max_results=20):
    """
    Search for businesses in specified location and categories.
    
    This function searches multiple data sources to find businesses
    and identifies which ones don't have websites.
    
    Args:
        location (str): Target location (e.g., "Marrakesh, Morocco")
        categories (list): List of business categories to search
        max_results (int): Maximum number of results per category
    
    Returns:
        list: List of business dictionaries with lead information
    
    Raises:
        ValueError: If location is empty or invalid
        APIError: If API requests fail
    
    Example:
        >>> results = search_businesses(
        ...     "Marrakesh, Morocco", 
        ...     ["restaurants", "hotels"],
        ...     max_results=10
        ... )
        >>> print(f"Found {len(results)} businesses")
    """
    pass
```

#### 2. **CLI Help Documentation**
```python
def create_help_text():
    """Create comprehensive help text for CLI."""
    return """
Business Lead Finder - Find businesses without websites

USAGE:
    python main.py <command> [options]

COMMANDS:
    search      Search for businesses in a location
    check       Check if a business has a website
    report      Generate comprehensive report
    export      Export data to various formats
    analyze     Analyze existing lead data
    interactive Start interactive mode

EXAMPLES:
    python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels
    python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
    python main.py report --input data/leads.json --output results/report.html
    python main.py export --format csv --output results/leads.csv
    python main.py interactive

For more help on a specific command:
    python main.py <command> --help
    """
```

### 🎯 Git Rules

#### 1. **Commit Messages**
```bash
# ✅ Good commit messages
git commit -m "feat: add CLI interface with argparse"
git commit -m "fix: handle empty search results gracefully"
git commit -m "docs: update README with CLI usage examples"
git commit -m "refactor: split CLI commands into separate functions"
```

#### 2. **Branch Naming**
```bash
# ✅ Descriptive branch names
git checkout -b feature/cli-interface
git checkout -b fix/phone-number-validation
git checkout -b docs/cli-documentation
```

### 🚀 Performance Monitoring

#### 1. **Performance Tracking**
```python
import time
from functools import wraps

def track_performance(func):
    """Decorator to track function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@track_performance
def search_businesses(location, categories):
    # Function implementation
    pass
```

These rules ensure consistent, maintainable, and professional code for your business lead finder project with excellent CLI functionality!
