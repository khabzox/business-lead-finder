# Business Lead Finder - Coding Rules & Guidelines

## 🎯 Project Philosophy

Build a scalable, maintainable, and efficient business lead finder with clean architecture and simple patterns.

## 📋 Core Architecture Rules

### 1. **NO CLASSES - Functions Only**

```python
# ❌ DON'T USE
class BusinessFinder:
    def __init__(self):
        pass

# ✅ DO USE
def find_businesses(location: str, categories: List[str]) -> List[Dict]:
    """Find businesses using functional approach."""
    pass
```

### 2. **Module Organization**

```text
src/
├── main.py              # Entry point only
├── cli_interface.py     # CLI commands and parsing
├── business_search.py   # Core search logic
├── website_checker.py   # Website detection
├── data_processor.py    # Data processing and export
├── report_generator.py  # Report generation
├── utils.py            # Utility functions
└── config/
    └── settings.py     # Configuration management
```

### 3. **Function Naming Convention**

```python
# ✅ Use descriptive, action-oriented names
def search_google_places(query: str, location: str) -> List[Dict]:
def check_website_exists(business_name: str) -> Optional[str]:
def generate_lead_report(business_data: List[Dict]) -> str:
def export_to_csv(data: List[Dict], filepath: str) -> bool:
```

### 4. **Type Hints Required**

```python
from typing import List, Dict, Optional, Union, Any

def process_business_data(
    location: str, 
    categories: List[str], 
    max_results: int = 20
) -> Dict[str, List[Dict]]:
    """Process business data with proper type hints."""
    pass
```

### 5. **Error Handling Pattern**

```python
# ✅ Consistent error handling
def api_call_wrapper(url: str, params: Dict) -> Optional[Dict]:
    """Standard API call pattern."""
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### 6. **Configuration Management**

```python
# ✅ Environment-based configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Constants in UPPER_CASE
GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', 'Marrakesh, Morocco')
MAX_RESULTS = int(os.getenv('MAX_RESULTS', '50'))
```

### 7. **Logging Instead of Print**

```python
import logging

# ✅ Structured logging
logger = logging.getLogger(__name__)

def search_businesses(query: str) -> List[Dict]:
    logger.info(f"Starting search for: {query}")
    # ... search logic
    logger.info(f"Found {len(results)} businesses")
    return results
```

### 8. **Data Validation**

```python
# ✅ Input validation for all functions
def validate_location(location: str) -> str:
    """Validate and clean location input."""
    if not location or not isinstance(location, str):
        raise ValueError("Location must be a non-empty string")
    return location.strip()

def validate_categories(categories: List[str]) -> List[str]:
    """Validate business categories."""
    if not categories:
        raise ValueError("At least one category required")
    return [cat.strip().lower() for cat in categories]
```

## 🔧 Code Quality Rules

### 1. **Import Organization**

```python
# ✅ Standard library first
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

# ✅ Third-party libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ✅ Local imports last
from utils import clean_phone_number, validate_email
from config.settings import API_KEYS, DEFAULT_SETTINGS
```

### 2. **Function Size Limits**

- Maximum 50 lines per function
- Single responsibility principle
- If longer, break into smaller functions

### 3. **Variable Naming**

```python
# ✅ Descriptive names
business_name = "Restaurant Atlas"
phone_number = "+212 5 24 44 33 22"
lead_score = 85
search_results = []

# ❌ Avoid abbreviations
bus_name = "Restaurant Atlas"
ph_num = "+212 5 24 44 33 22"
scr = 85
```

### 4. **Constants and Magic Numbers**

```python
# ✅ Named constants
MAX_RETRY_ATTEMPTS = 3
REQUEST_TIMEOUT_SECONDS = 30
MIN_BUSINESS_RATING = 4.0
HIGH_LEAD_SCORE_THRESHOLD = 70

# ✅ Use in code
def is_high_quality_lead(business: Dict) -> bool:
    return business.get('lead_score', 0) >= HIGH_LEAD_SCORE_THRESHOLD
```

## 🚀 Performance Rules

### 1. **Efficient Data Processing**

```python
# ✅ Use list comprehensions for simple operations
high_rated_businesses = [
    business for business in all_businesses 
    if business.get('rating', 0) >= MIN_BUSINESS_RATING
]

# ✅ Use generators for large datasets
def process_businesses_batch(business_list: List[Dict]) -> Iterator[Dict]:
    for business in business_list:
        if validate_business_data(business):
            yield process_single_business(business)
```

### 2. **Rate Limiting**

```python
import time
from functools import wraps

def rate_limit(seconds: int = 1):
    """Decorator to rate limit function calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(seconds=1)
def api_call(url: str, params: Dict) -> Optional[Dict]:
    return requests.get(url, params=params).json()
```

## 🔐 Security Rules

### 1. **API Key Management**

```python
# ✅ Environment variables only
def get_api_key(service_name: str) -> str:
    """Safely retrieve API key."""
    key = os.getenv(f'{service_name.upper()}_API_KEY')
    if not key:
        raise ValueError(f"Missing API key for {service_name}")
    return key
```

### 2. **Input Sanitization**

```python
import re

def sanitize_phone_number(phone: str) -> str:
    """Clean and validate phone number."""
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Validate format
    if not re.match(r'^\+?[\d\s\-\(\)]+$', phone):
        raise ValueError(f"Invalid phone format: {phone}")
    
    return cleaned
```

## 📊 Data Structure Rules

### 1. **Standard Business Data Format**

```python
# ✅ Consistent data structure
BUSINESS_SCHEMA = {
    'name': str,           # Required
    'category': str,       # Required
    'address': str,        # Required
    'phone': Optional[str],
    'email': Optional[str],
    'website': Optional[str],
    'rating': Optional[float],
    'review_count': Optional[int],
    'social_media': Dict[str, str],  # platform: url
    'lead_score': int,
    'last_updated': str,   # ISO format
    'source': str          # Data source identifier
}
```

## 🔄 Git Workflow Rules

### 1. **Commit Messages**

```bash
# ✅ Conventional commits format
git commit -m "feat: add OpenStreetMap API integration"
git commit -m "fix: handle empty search results gracefully"
git commit -m "docs: update CLI usage examples"
git commit -m "refactor: split website checker into separate functions"
```

### 2. **Branch Naming**

```bash
# ✅ Descriptive branch names
feature/google-places-integration
fix/phone-number-validation
docs/api-documentation
refactor/cli-interface-cleanup
```

## 📈 Testing Rules

### 1. **Test Structure**

```python
# ✅ Comprehensive test coverage
def test_search_businesses_success():
    """Test successful business search."""
    result = search_businesses("Marrakesh", ["restaurants"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'name' in result[0]

def test_search_businesses_invalid_location():
    """Test business search with invalid location."""
    with pytest.raises(ValueError):
        search_businesses("", ["restaurants"])
```

## 📝 CLI Interface Rules

### 1. **Command Structure**

```bash
# ✅ Clear, intuitive commands
python main.py search --location "Marrakesh" --categories restaurants hotels
python main.py check --business-name "Restaurant Atlas"
python main.py report --input leads.json --output report.html
python main.py export --format csv --output leads.csv
python main.py interactive
```

## 🎯 Free Implementation Priority

### 1. **API Priority Order**

1. **OpenStreetMap Nominatim** (100% free)
2. **Foursquare Places** (1000 requests/day free)
3. **SerpAPI** (100 searches/month free)
4. **Google Places** (premium, optional)

### 2. **Fallback Strategy**

```python
def search_with_fallbacks(query: str, location: str) -> List[Dict]:
    """Search with multiple API fallbacks."""
    # Try free APIs first
    results = search_openstreetmap(query, location)
    if not results:
        results = search_foursquare(query, location)
    if not results:
        results = search_serpapi(query, location)
    
    return results or []
```

## 📋 Code Review Checklist

- [ ] Functions are < 50 lines
- [ ] Type hints on all functions
- [ ] Proper error handling
- [ ] Logging instead of print statements
- [ ] Input validation
- [ ] Consistent naming conventions
- [ ] No hardcoded values
- [ ] Documentation strings
- [ ] Test coverage > 80%
- [ ] No classes (functional approach)

These rules ensure clean, maintainable, and scalable code for the Business Lead Finder project!
