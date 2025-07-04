"""
Configuration settings for Business Lead Finder.
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEYS = {
    'serpapi': os.getenv('SERPAPI_KEY'),
    'google_places': os.getenv('GOOGLE_PLACES_API_KEY'),
    'yelp': os.getenv('YELP_API_KEY'),
    'foursquare_client_id': os.getenv('FOURSQUARE_CLIENT_ID'),
    'foursquare_client_secret': os.getenv('FOURSQUARE_CLIENT_SECRET'),
}

# Search Configuration
SEARCH_CONFIG = {
    'default_location': os.getenv('DEFAULT_LOCATION', 'Marrakesh, Morocco'),
    'max_results_per_search': int(os.getenv('MAX_RESULTS_PER_SEARCH', '50')),
    'delay_between_requests': int(os.getenv('DELAY_BETWEEN_REQUESTS', '1')),
    'request_timeout': 30,
    'max_retries': 3,
}

# Business Categories
BUSINESS_CATEGORIES = {
    'high_priority': [
        'restaurants', 'hotels', 'riads', 'cafes', 'spas',
        'tour_operators', 'retail_shops', 'professional_services'
    ],
    'medium_priority': [
        'bars', 'nightclubs', 'gyms', 'beauty_salons',
        'car_rentals', 'pharmacies', 'banks'
    ],
    'all_categories': [
        'restaurants', 'hotels', 'riads', 'cafes', 'spas', 'tour_operators',
        'retail_shops', 'professional_services', 'bars', 'nightclubs',
        'gyms', 'beauty_salons', 'car_rentals', 'pharmacies', 'banks',
        'grocery_stores', 'gas_stations', 'hospitals', 'schools'
    ]
}

# File Paths
PATHS = {
    'results_dir': os.getenv('OUTPUT_DIRECTORY', 'results'),
    'data_dir': 'data',
    'reports_dir': 'results/reports',
    'exports_dir': 'results/exports',
    'logs_dir': 'logs',
    'templates_dir': 'data/templates',
}

# Output Configuration
OUTPUT_CONFIG = {
    'export_formats': os.getenv('EXPORT_FORMAT', 'csv,json').split(','),
    'report_formats': os.getenv('REPORT_FORMAT', 'html,pdf').split(','),
    'default_export_format': 'csv',
    'default_report_format': 'html',
}

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'smtp_username': os.getenv('SMTP_USERNAME'),
    'smtp_password': os.getenv('SMTP_PASSWORD'),
    'from_email': os.getenv('FROM_EMAIL'),
}

# Lead Scoring Weights
SCORING_WEIGHTS = {
    'rating': int(os.getenv('RATING_WEIGHT', '30')),
    'review_count': int(os.getenv('REVIEW_COUNT_WEIGHT', '20')),
    'category': int(os.getenv('CATEGORY_WEIGHT', '15')),
    'website_absence': int(os.getenv('WEBSITE_ABSENCE_WEIGHT', '25')),
    'social_media': int(os.getenv('SOCIAL_MEDIA_WEIGHT', '10')),
}

# Free API URLs
FREE_API_URLS = {
    'openstreetmap_nominatim': 'https://nominatim.openstreetmap.org',
    'foursquare_places': 'https://api.foursquare.com/v2',
    'serpapi': 'https://serpapi.com/search',
}

# User Agents for Web Scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

# Default Settings
DEFAULT_SETTINGS = {
    'api_keys': API_KEYS,
    'search': SEARCH_CONFIG,
    'categories': BUSINESS_CATEGORIES,
    'paths': PATHS,
    'output': OUTPUT_CONFIG,
    'email': EMAIL_CONFIG,
    'scoring': SCORING_WEIGHTS,
    'free_apis': FREE_API_URLS,
    'user_agents': USER_AGENTS,
}

# Validation Rules
VALIDATION_RULES = {
    'min_business_name_length': 2,
    'min_location_length': 2,
    'max_results_limit': 1000,
    'min_lead_score': 0,
    'max_lead_score': 100,
}

def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary."""
    return DEFAULT_SETTINGS

def validate_config() -> bool:
    """Validate configuration settings."""
    # Check if at least one free API is available
    has_free_api = (
        os.getenv('OPENSTREETMAP_ENABLED', 'true').lower() == 'true' or
        bool(API_KEYS['foursquare_client_id']) or
        bool(API_KEYS['serpapi'])
    )
    
    if not has_free_api:
        print("Warning: No free APIs configured. Please set up at least one free API.")
        return False
    
    return True

def get_api_status() -> Dict[str, bool]:
    """Get status of available APIs."""
    return {
        'openstreetmap': os.getenv('OPENSTREETMAP_ENABLED', 'true').lower() == 'true',
        'foursquare': bool(API_KEYS['foursquare_client_id'] and API_KEYS['foursquare_client_secret']),
        'serpapi': bool(API_KEYS['serpapi']),
        'google_places': bool(API_KEYS['google_places']),
        'yelp': bool(API_KEYS['yelp']),
    }
