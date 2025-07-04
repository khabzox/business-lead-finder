"""
Utility functions for Business Lead Finder.
"""

import os
import json
import logging
import re
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from functools import wraps

def setup_logging(log_level: str = 'INFO', log_file: str = 'business_finder.log') -> None:
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_path = log_dir / log_file
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_path}")

def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or environment variables."""
    from config.settings import SEARCH_CONFIG, API_KEYS, BUSINESS_CATEGORIES
    
    config = {
        'search_config': SEARCH_CONFIG,
        'api_keys': API_KEYS,
        'business_categories': BUSINESS_CATEGORIES
    }
    
    # Load custom config file if provided
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
            
            # Merge custom config with default config
            config.update(custom_config)
            logging.info(f"Custom configuration loaded from: {config_file}")
            
        except Exception as e:
            logging.error(f"Error loading custom config: {e}")
    
    return config

def clean_phone_number(phone: str) -> str:
    """
    Clean and format phone number.
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Cleaned phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Ensure it starts with + for international format
    if cleaned and not cleaned.startswith('+'):
        # Add Morocco country code if it looks like a Moroccan number
        if len(cleaned) == 9 and cleaned.startswith(('5', '6', '7')):
            cleaned = '+212' + cleaned
        elif len(cleaned) == 10 and cleaned.startswith('0'):
            cleaned = '+212' + cleaned[1:]
        else:
            cleaned = '+' + cleaned
    
    return cleaned

def validate_business_data(business: Dict[str, Any]) -> bool:
    """
    Validate business data structure and required fields.
    
    Args:
        business: Business data dictionary
    
    Returns:
        True if valid, False otherwise
    """
    try:
        # Required fields
        required_fields = ['name']
        
        for field in required_fields:
            if not business.get(field):
                return False
        
        # Name should be meaningful (not just a number or single character)
        name = business.get('name', '').strip()
        if len(name) < 2 or name.isdigit():
            return False
        
        # Phone validation if present
        phone = business.get('phone', '')
        if phone and len(clean_phone_number(phone)) < 8:
            return False
        
        return True
        
    except Exception:
        return False

def validate_location(location: str) -> bool:
    """
    Validate location string.
    
    Args:
        location: Location string
    
    Returns:
        True if valid, False otherwise
    """
    if not location or not isinstance(location, str):
        return False
    
    location = location.strip()
    if len(location) < 2:
        return False
    
    # Basic validation - no offensive patterns
    forbidden_patterns = ['<script', 'javascript:', 'http://', 'https://']
    if any(pattern in location.lower() for pattern in forbidden_patterns):
        return False
    
    return True

def validate_categories(categories: List[str]) -> bool:
    """
    Validate business categories list.
    
    Args:
        categories: List of category strings
    
    Returns:
        True if valid, False otherwise
    """
    if not categories or not isinstance(categories, list):
        return False
    
    if len(categories) == 0 or len(categories) > 10:  # Reasonable limits
        return False
    
    for category in categories:
        if not isinstance(category, str) or len(category.strip()) < 2:
            return False
    
    return True

def rate_limit(seconds: float = 1.0):
    """
    Decorator to add rate limiting to functions.
    
    Args:
        seconds: Number of seconds to wait between calls
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def extract_domain_from_url(url: str) -> Optional[str]:
    """
    Extract domain from URL.
    
    Args:
        url: URL string
    
    Returns:
        Domain name or None
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return None

def format_phone_for_display(phone: str) -> str:
    """
    Format phone number for display.
    
    Args:
        phone: Raw phone number
    
    Returns:
        Formatted phone number
    """
    cleaned = clean_phone_number(phone)
    
    if not cleaned:
        return ""
    
    # Format Morocco numbers nicely
    if cleaned.startswith('+212'):
        number = cleaned[4:]  # Remove +212
        if len(number) == 9:
            return f"+212 {number[0]} {number[1:3]} {number[3:5]} {number[5:7]} {number[7:]}"
    
    return cleaned

def create_directories(paths: List[str]) -> None:
    """
    Create directories if they don't exist.
    
    Args:
        paths: List of directory paths to create
    """
    for path in paths:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating directory {path}: {e}")

def save_json_file(data: Any, filepath: str) -> bool:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        filepath: File path
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        logging.error(f"Error saving JSON file {filepath}: {e}")
        return False

def load_json_file(filepath: str) -> Optional[Any]:
    """
    Load data from JSON file.
    
    Args:
        filepath: File path
    
    Returns:
        Loaded data or None
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file {filepath}: {e}")
        return None

def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().isoformat()

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for filesystem safety.
    
    Args:
        filename: Raw filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 200:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:200-len(ext)] + ext
    
    return sanitized

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points in kilometers.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
    
    Returns:
        Distance in kilometers
    """
    try:
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in km
        r = 6371
        
        return r * c
        
    except Exception:
        return 0.0

def filter_businesses_by_distance(
    businesses: List[Dict[str, Any]], 
    center_lat: float, 
    center_lon: float, 
    max_distance_km: float = 10.0
) -> List[Dict[str, Any]]:
    """
    Filter businesses by distance from center point.
    
    Args:
        businesses: List of business dictionaries
        center_lat: Center latitude
        center_lon: Center longitude
        max_distance_km: Maximum distance in kilometers
    
    Returns:
        Filtered list of businesses
    """
    filtered = []
    
    for business in businesses:
        try:
            lat = float(business.get('latitude', 0))
            lon = float(business.get('longitude', 0))
            
            if lat and lon:
                distance = calculate_distance(center_lat, center_lon, lat, lon)
                if distance <= max_distance_km:
                    business['distance_km'] = round(distance, 2)
                    filtered.append(business)
            else:
                # Include businesses without coordinates
                filtered.append(business)
                
        except Exception:
            # Include businesses with invalid coordinates
            filtered.append(business)
    
    return filtered

def deduplicate_businesses(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate businesses based on name and phone.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        Deduplicated list
    """
    seen = set()
    unique = []
    
    for business in businesses:
        # Create identifier
        name = business.get('name', '').lower().strip()
        phone = clean_phone_number(business.get('phone', ''))
        
        identifier = f"{name}|{phone}"
        
        if identifier not in seen and name:
            seen.add(identifier)
            unique.append(business)
    
    return unique

def format_currency(amount: float, currency: str = 'MAD') -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
    
    Returns:
        Formatted currency string
    """
    try:
        return f"{amount:,.2f} {currency}"
    except Exception:
        return f"{amount} {currency}"

def get_business_category_emoji(category: str) -> str:
    """
    Get emoji for business category.
    
    Args:
        category: Business category
    
    Returns:
        Appropriate emoji
    """
    category_emojis = {
        'restaurant': '🍽️',
        'hotel': '🏨',
        'cafe': '☕',
        'spa': '💆',
        'shop': '🛍️',
        'gym': '💪',
        'bar': '🍺',
        'pharmacy': '💊',
        'bank': '🏦',
        'gas_station': '⛽',
        'hospital': '🏥',
        'school': '🏫'
    }
    
    category_lower = category.lower()
    for key, emoji in category_emojis.items():
        if key in category_lower:
            return emoji
    
    return '🏢'  # Default business emoji

def generate_business_slug(business_name: str) -> str:
    """
    Generate URL-friendly slug from business name.
    
    Args:
        business_name: Business name
    
    Returns:
        URL slug
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = business_name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def estimate_website_cost(business_type: str, features: List[str] = None) -> Dict[str, float]:
    """
    Estimate website development cost.
    
    Args:
        business_type: Type of business
        features: List of desired features
    
    Returns:
        Cost estimate breakdown
    """
    base_costs = {
        'restaurant': 800,
        'hotel': 1500,
        'spa': 1000,
        'shop': 1200,
        'service': 600
    }
    
    feature_costs = {
        'online_booking': 300,
        'payment_processing': 200,
        'multilingual': 150,
        'mobile_app': 500,
        'seo_optimization': 100
    }
    
    base_cost = base_costs.get(business_type.lower(), 800)
    feature_cost = sum(feature_costs.get(feature, 0) for feature in (features or []))
    
    total_cost = base_cost + feature_cost
    
    return {
        'base_cost': base_cost,
        'feature_cost': feature_cost,
        'total_cost': total_cost,
        'currency': 'USD'
    }

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address
    
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_emails_from_text(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Text to search
    
    Returns:
        List of email addresses
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return [email for email in emails if validate_email(email)]

def performance_monitor(func):
    """
    Decorator to monitor function performance.
    
    Args:
        func: Function to monitor
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        logging.info(f"Function {func.__name__} took {duration:.2f} seconds")
        
        return result
    return wrapper

# ...existing code...
            logging.error(f"Error loading custom config: {e}")
    
    return config

def validate_location(location: str) -> str:
    """Validate and clean location input."""
    if not location or not isinstance(location, str):
        raise ValueError("Location must be a non-empty string")
    
    location = location.strip()
    
    if len(location) < 2:
        raise ValueError("Location must be at least 2 characters long")
    
    # Basic validation for common location formats
    if not re.match(r'^[a-zA-Z\s,.-]+$', location):
        raise ValueError("Location contains invalid characters")
    
    return location

def validate_categories(categories: List[str]) -> List[str]:
    """Validate and clean categories list."""
    if not categories or not isinstance(categories, list):
        raise ValueError("Categories must be a non-empty list")
    
    cleaned_categories = []
    valid_categories = [
        'restaurants', 'hotels', 'riads', 'cafes', 'spas', 'tour_operators',
        'retail_shops', 'professional_services', 'bars', 'nightclubs',
        'gyms', 'beauty_salons', 'car_rentals', 'pharmacies', 'banks',
        'grocery_stores', 'gas_stations', 'hospitals', 'schools', 'shops',
        'services', 'entertainment', 'automotive', 'health', 'education'
    ]
    
    for category in categories:
        if not isinstance(category, str):
            continue
        
        category = category.strip().lower()
        
        if category in valid_categories:
            cleaned_categories.append(category)
        else:
            # Try to find partial matches
            matches = [cat for cat in valid_categories if category in cat or cat in category]
            if matches:
                cleaned_categories.append(matches[0])
                logging.warning(f"Category '{category}' matched to '{matches[0]}'")
            else:
                cleaned_categories.append(category)  # Allow unknown categories
                logging.warning(f"Unknown category: '{category}'")
    
    if not cleaned_categories:
        raise ValueError("No valid categories found")
    
    return list(set(cleaned_categories))  # Remove duplicates

def validate_email(email: str) -> bool:
    """Validate email address format."""
    if not email:
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    if not phone:
        return False
    
    # Remove spaces and common separators
    clean_phone = re.sub(r'[\s\-\(\)\.]+', '', phone)
    
    # Check for valid phone patterns
    # International format or Morocco format
    patterns = [
        r'^\+\d{10,15}$',  # International format
        r'^\+212\d{9}$',   # Morocco international
        r'^0\d{9}$',       # Morocco national
        r'^\d{9,10}$'      # Simple format
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)

def clean_phone_number(phone: str) -> str:
    """Clean and standardize phone number."""
    if not phone:
        return ''
    
    # Remove all non-digit characters except +
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    # Handle Morocco phone numbers
    if clean_phone.startswith('0') and len(clean_phone) == 10:
        # Convert Morocco national to international
        clean_phone = '+212' + clean_phone[1:]
    elif clean_phone.startswith('212') and len(clean_phone) == 12:
        # Add + to Morocco international
        clean_phone = '+' + clean_phone
    elif not clean_phone.startswith('+') and len(clean_phone) == 9:
        # Add Morocco country code
        clean_phone = '+212' + clean_phone
    
    return clean_phone

def clean_business_name(name: str) -> str:
    """Clean and standardize business name."""
    if not name:
        return ''
    
    # Remove extra whitespace
    name = ' '.join(name.split())
    
    # Remove common prefixes/suffixes in multiple languages
    prefixes_suffixes = [
        'restaurant', 'hotel', 'cafe', 'spa', 'shop', 'store',
        'مطعم', 'فندق', 'مقهى', 'محل',  # Arabic
        'restaurant', 'hôtel', 'café', 'magasin'  # French
    ]
    
    # Don't remove if it's the main part of the name
    words = name.lower().split()
    if len(words) > 1:
        for prefix in prefixes_suffixes:
            if words[0] == prefix.lower():
                name = ' '.join(words[1:])
                break
            elif words[-1] == prefix.lower():
                name = ' '.join(words[:-1])
                break
    
    return name.strip()

def extract_domain_from_url(url: str) -> str:
    """Extract domain from URL."""
    if not url:
        return ''
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ''

def create_safe_filename(text: str) -> str:
    """Create a safe filename from text."""
    # Remove or replace unsafe characters
    safe_text = re.sub(r'[^\w\s-]', '', text)
    safe_text = re.sub(r'[-\s]+', '_', safe_text)
    return safe_text.strip('_').lower()

def save_json_data(data: Any, file_path: str) -> bool:
    """Save data to JSON file."""
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return True
    except Exception as e:
        logging.error(f"Error saving JSON data to {file_path}: {e}")
        return False

def load_json_data(file_path: str) -> Optional[Any]:
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in file {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading JSON data from {file_path}: {e}")
        return None

def save_csv_data(data: List[Dict[str, Any]], file_path: str) -> bool:
    """Save data to CSV file."""
    try:
        import csv
        
        if not data:
            logging.warning("No data to save to CSV")
            return False
        
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = data[0].keys()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return True
    except Exception as e:
        logging.error(f"Error saving CSV data to {file_path}: {e}")
        return False

def format_business_data_for_display(business: Dict[str, Any]) -> Dict[str, str]:
    """Format business data for display purposes."""
    formatted = {}
    
    # Basic info
    formatted['Name'] = business.get('name', 'N/A')
    formatted['Category'] = business.get('category', 'N/A')
    formatted['Address'] = business.get('address', 'N/A')
    formatted['Phone'] = business.get('phone', 'N/A')
    formatted['Email'] = business.get('email', 'N/A')
    
    # Website status
    website = business.get('website', '')
    formatted['Website'] = '✅ Yes' if website else '❌ No'
    if website:
        formatted['Website URL'] = website
    
    # Rating and reviews
    rating = business.get('rating', 0)
    review_count = business.get('review_count', 0)
    if rating > 0:
        formatted['Rating'] = f"{rating:.1f}/5 ({review_count} reviews)"
    else:
        formatted['Rating'] = 'No rating'
    
    # Lead score
    lead_score = business.get('lead_score', 0)
    formatted['Lead Score'] = f"{lead_score}/100"
    
    # Social media
    social_media = business.get('social_media', {})
    if social_media:
        platforms = list(social_media.keys())
        formatted['Social Media'] = ', '.join(platforms)
    else:
        formatted['Social Media'] = 'None found'
    
    # Source
    formatted['Data Source'] = business.get('source', 'Unknown')
    
    return formatted

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers."""
    try:
        import math
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r
    except:
        return 0.0

def get_current_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().isoformat()

def ensure_directory_exists(directory_path: str) -> bool:
    """Ensure directory exists, create if it doesn't."""
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Error creating directory {directory_path}: {e}")
        return False

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length with ellipsis."""
    if not text:
        return ''
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + '...'

def normalize_category(category: str) -> str:
    """Normalize business category."""
    if not category:
        return 'unknown'
    
    category = category.lower().strip()
    
    # Category mappings
    category_map = {
        'restaurant': 'restaurants',
        'food': 'restaurants',
        'dining': 'restaurants',
        'hotel': 'hotels',
        'accommodation': 'hotels',
        'lodging': 'hotels',
        'riad': 'riads',
        'cafe': 'cafes',
        'coffee': 'cafes',
        'spa': 'spas',
        'wellness': 'spas',
        'shop': 'shops',
        'store': 'shops',
        'retail': 'shops',
        'service': 'services',
        'professional': 'services',
        'tour': 'tours',
        'tourism': 'tours',
        'travel': 'tours'
    }
    
    # Check for exact matches first
    if category in category_map:
        return category_map[category]
    
    # Check for partial matches
    for key, value in category_map.items():
        if key in category or category in key:
            return value
    
    return category

def get_business_summary_stats(businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get summary statistics for a list of businesses."""
    if not businesses:
        return {}
    
    stats = {
        'total_businesses': len(businesses),
        'with_websites': 0,
        'without_websites': 0,
        'with_phone': 0,
        'with_email': 0,
        'with_social_media': 0,
        'average_rating': 0.0,
        'high_score_leads': 0,
        'categories': {},
        'sources': {}
    }
    
    total_rating = 0
    rated_businesses = 0
    
    for business in businesses:
        # Website stats
        if business.get('website'):
            stats['with_websites'] += 1
        else:
            stats['without_websites'] += 1
        
        # Contact info stats
        if business.get('phone'):
            stats['with_phone'] += 1
        
        if business.get('email'):
            stats['with_email'] += 1
        
        if business.get('social_media'):
            stats['with_social_media'] += 1
        
        # Rating stats
        rating = business.get('rating', 0)
        if rating > 0:
            total_rating += rating
            rated_businesses += 1
        
        # Lead score stats
        lead_score = business.get('lead_score', 0)
        if lead_score >= 70:
            stats['high_score_leads'] += 1
        
        # Category stats
        category = business.get('category', 'unknown')
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        # Source stats
        source = business.get('source', 'unknown')
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
    
    # Calculate average rating
    if rated_businesses > 0:
        stats['average_rating'] = total_rating / rated_businesses
    
    # Calculate percentages
    total = stats['total_businesses']
    stats['website_percentage'] = (stats['with_websites'] / total) * 100 if total > 0 else 0
    stats['lead_opportunity_percentage'] = (stats['without_websites'] / total) * 100 if total > 0 else 0
    stats['high_score_percentage'] = (stats['high_score_leads'] / total) * 100 if total > 0 else 0
    
    return stats
