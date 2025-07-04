# Business Lead Finder - Coding Rules

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
├── main.py              # Entry point
├── business_search.py   # Core search functions
├── website_checker.py   # Website detection functions
├── data_processor.py    # Data processing functions
├── report_generator.py  # Report generation functions
├── simple_cli.py        # Basic CLI fallback
└── utils.py            # Utility functions
```

#### 4. **Import Guidelines**
```python
# ✅ Standard library first
import os
import time
import json
from datetime import datetime

# ✅ Third-party libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ✅ Local imports last
from utils import clean_phone_number, validate_email
from config import API_KEYS, DEFAULT_SETTINGS
```

#### 5. **Error Handling**
```python
# ✅ Always use try-except for API calls
def search_business_api(query):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

#### 6. **Configuration Management**
```python
# ✅ Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration constants
GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', 'Default City')
MAX_RESULTS = int(os.getenv('MAX_RESULTS', '50'))
DELAY_SECONDS = int(os.getenv('DELAY_SECONDS', '1'))
```

#### 7. **Data Validation**
```python
# ✅ Always validate inputs
def validate_business_data(business):
    required_fields = ['name', 'address', 'phone']
    for field in required_fields:
        if not business.get(field):
            return False
    return True
```

#### 8. **Logging Instead of Print**
```python
import logging

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

# ✅ Use logger instead of print
def search_businesses(query):
    logger.info(f"Starting search for: {query}")
    # ... search logic
    logger.info(f"Found {len(results)} businesses")
```

#### 9. **Type Hints**
```python
from typing import List, Dict, Optional, Union

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
```

#### 10. **Documentation Standards**
```python
def find_business_leads(
    location: str, 
    categories: List[str], 
    filters: Dict[str, str] = None
) -> Dict[str, List[Dict]]:
    """
    Find business leads without websites.
    
    Args:
        location: Target location (e.g., "City, Country")
        categories: List of business categories to search
        filters: Optional filters (rating, review_count, etc.)
    
    Returns:
        Dict containing 'with_websites' and 'without_websites' lists
    
    Example:
        >>> results = find_business_leads(
        ...     "Sample City", 
        ...     ["restaurants", "hotels"]
        ... )
        >>> print(f"Found {len(results['without_websites'])} leads")
    """
    pass
```

### 🔧 File Organization Rules

#### 1. **main.py Structure**
```python
#!/usr/bin/env python3
"""
Business Lead Finder - Main Entry Point
Finds local businesses without websites for lead generation.
"""

import argparse
from business_search import search_all_categories
from report_generator import generate_comprehensive_report
from utils import setup_logging, load_config

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Find business leads')
    parser.add_argument('--location', default='Default Location')
    parser.add_argument('--categories', nargs='+', default=['restaurants', 'hotels'])
    parser.add_argument('--max-results', type=int, default=50)
    
    args = parser.parse_args()
    
    # Run the search
    results = search_all_categories(
        location=args.location,
        categories=args.categories,
        max_results=args.max_results
    )
    
    # Generate report
    generate_comprehensive_report(results)

if __name__ == "__main__":
    main()
```

#### 2. **Configuration File (config.py)**
```python
"""Configuration settings for Business Lead Finder."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (free options prioritized)
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
YELP_API_KEY = os.getenv('YELP_API_KEY')

# Search Settings
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', 'Sample City')
MAX_RESULTS_PER_SEARCH = int(os.getenv('MAX_RESULTS_PER_SEARCH', '20'))
DELAY_BETWEEN_REQUESTS = int(os.getenv('DELAY_BETWEEN_REQUESTS', '1'))

# Business Categories
PRIORITY_CATEGORIES = [
    'restaurants', 'hotels', 'cafes', 'spas',
    'shops', 'services'
]

# File Paths
RESULTS_DIR = 'results'
REPORTS_DIR = 'reports'
DATA_DIR = 'data'
```

### 🎨 Code Style Rules

#### 1. **Variable Naming**
```python
# ✅ Use descriptive names
business_name = "Sample Business"
phone_number = "+1234567890"
website_url = "https://example.com"
search_results = []
total_businesses_found = 0

# ❌ Avoid abbreviations
bus_name = "Sample Business"  # Don't do this
ph_num = "+1234567890"        # Don't do this
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
```

#### 3. **Constants**
```python
# ✅ Use constants for magic numbers
MAX_RETRY_ATTEMPTS = 3
REQUEST_TIMEOUT = 30
MIN_BUSINESS_RATING = 4.0
DEFAULT_SEARCH_RADIUS = 5000  # meters

# ✅ Use in code
def search_nearby_businesses(location, radius=DEFAULT_SEARCH_RADIUS):
    pass
```

#### 4. **File Handling**
```python
# ✅ Always use context managers
def save_business_data(business_data, filename):
    """Save business data to file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(business_data, f, indent=2, ensure_ascii=False)
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

#### 2. **Memory Management**
```python
# ✅ Process data in chunks
def process_large_dataset(data, chunk_size=100):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        yield process_chunk(chunk)
```

#### 3. **Rate Limiting**
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
    return requests.get(url, params=params)
```

### 🔍 Testing Rules

#### 1. **Test Structure**
```python
# tests/test_business_search.py
import pytest
from unittest.mock import patch, MagicMock
from business_search import search_sample_places

def test_search_sample_places_success():
    """Test successful sample search."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [{'name': 'Test Business'}]
        }
        mock_get.return_value = mock_response
        
        results = search_sample_places('businesses', 'Sample City')
        assert len(results) == 1
        assert results[0]['name'] == 'Test Business'
```

#### 2. **Test Coverage**
```python
# ✅ Test edge cases
def test_search_empty_results():
    """Test handling of empty search results."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response
        
        results = search_sample_places('businesses', 'Sample City')
        assert results == []
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
    'last_updated': str
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
        'last_updated': datetime.now().isoformat()
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
        raise ValueError(f"Missing API key for {service_name}")
    return key

# ✅ Use in code
sample_api_key = get_api_key('sample_service')
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
```

### 📝 Documentation Rules

#### 1. **README Structure**
```markdown
# Business Lead Finder

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python main.py --location "Sample City"
```

## Features
- Find businesses without websites
- Generate lead reports
- Export to multiple formats
```

#### 2. **Function Documentation**
```python
def search_businesses(location, categories, max_results=20):
    """
    Search for businesses in specified location and categories.
    
    This function searches multiple data sources to find businesses
    and identifies which ones don't have websites.
    
    Args:
        location (str): Target location (e.g., "Sample City")
        categories (list): List of business categories to search
        max_results (int): Maximum number of results per category
    
    Returns:
        dict: Dictionary with 'with_websites' and 'without_websites' keys
    
    Raises:
        ValueError: If location is empty or invalid
        APIError: If API requests fail
    
    Example:
        >>> results = search_businesses(
        ...     "Sample City", 
        ...     ["restaurants", "hotels"],
        ...     max_results=10
        ... )
        >>> print(f"Found {len(results['without_websites'])} leads")
    """
```

### 🎯 Git Rules

#### 1. **Commit Messages**
```bash
# ✅ Good commit messages
git commit -m "feat: add sample API integration"
git commit -m "fix: handle empty search results gracefully"
git commit -m "docs: update README with setup instructions"
git commit -m "refactor: split website checker into separate function"
```

#### 2. **Branch Naming**
```bash
# ✅ Descriptive branch names
git checkout -b feature/add-sample-api
git checkout -b fix/phone-number-validation
git checkout -b docs/api-documentation
```

### 🚀 Deployment Rules

#### 1. **Environment Configuration**
```python
# ✅ Environment-specific settings
def get_config():
    """Get configuration based on environment."""
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        return {
            'debug': False,
            'log_level': 'INFO',
            'max_requests_per_minute': 30
        }
    else:
        return {
            'debug': True,
            'log_level': 'DEBUG',
            'max_requests_per_minute': 60
        }
```

### 📈 Monitoring Rules

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

These rules ensure consistent, maintainable, and professional code for the business lead finder project!
