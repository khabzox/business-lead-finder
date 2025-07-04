"""
Business Search Module - Enhanced Implementation
Searches for businesses using free APIs and web scraping with improved error handling.
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional, Union
from bs4 import BeautifulSoup
import json
import random
import re
from urllib.parse import urlencode, quote
from datetime import datetime
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import aiohttp

from config.settings import SEARCH_CONFIG, API_KEYS
from utils import clean_phone_number, validate_business_data, rate_limit

logger = logging.getLogger(__name__)

# Search result cache
_search_cache = {}

def handle_search_error(error: Exception, context: str = "search") -> None:
    """Handle search-related errors with proper logging."""
    logger.error(f"{context} error: {error}")

def handle_rate_limit_error(error: Exception, context: str = "API") -> None:
    """Handle rate limit errors with proper logging."""
    logger.warning(f"{context} rate limit exceeded: {error}")
    time.sleep(2)  # Wait before retrying

def async_rate_limit(calls_per_second: float = 1.0):
    """
    Async rate limiting decorator.
    
    Args:
        calls_per_second: Maximum calls per second allowed
    """
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                await asyncio.sleep(left_to_wait)
            ret = await func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

def cache_search_results(ttl_seconds: int = 3600):
    """
    Cache search results to avoid redundant API calls.
    
    Args:
        ttl_seconds: Time to live for cached results
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check if we have cached result
            if cache_key in _search_cache:
                cached_data, timestamp = _search_cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Using cached result for {func.__name__}")
                    return cached_data
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            _search_cache[cache_key] = (result, time.time())
            
            # Clean old cache entries
            current_time = time.time()
            keys_to_remove = [
                key for key, (_, timestamp) in _search_cache.items()
                if current_time - timestamp > ttl_seconds
            ]
            for key in keys_to_remove:
                del _search_cache[key]
            
            return result
        return wrapper
    return decorator

# Free API URLs
FREE_API_URLS = {
    'nominatim': 'https://nominatim.openstreetmap.org/search',
    'foursquare': 'https://api.foursquare.com/v3/places/search',
    'serpapi': 'https://serpapi.com/search'
}

# User agents for web scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def search_businesses_all_sources(
    query: str,
    location: str,
    max_results: int = 50,
    config: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Search businesses using all available free sources.
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
        config: Configuration dictionary
    
    Returns:
        List of business dictionaries
    """
    all_businesses = []
    config = config or {}
    
    logger.info(f"Starting business search for '{query}' in '{location}'")
    
    # Source 1: OpenStreetMap Nominatim (Always free)
    try:
        osm_businesses = search_openstreetmap(query, location, max_results // 3)
        all_businesses.extend(osm_businesses)
        logger.info(f"Found {len(osm_businesses)} businesses from OpenStreetMap")
    except Exception as e:
        logger.error(f"OpenStreetMap search failed: {e}")
    
    # Source 2: Foursquare API (Free tier - 950 requests/day)
    if config and config.get('api_keys', {}).get('foursquare'):
        try:
            foursquare_businesses = search_foursquare(query, location, max_results // 3, config)
            all_businesses.extend(foursquare_businesses)
            logger.info(f"Found {len(foursquare_businesses)} businesses from Foursquare")
        except Exception as e:
            logger.error(f"Foursquare search failed: {e}")
    
    # Source 3: SerpAPI (Free tier - 100 searches/month)
    if config and config.get('api_keys', {}).get('serpapi'):
        try:
            serpapi_businesses = search_serpapi(query, location, max_results // 3, config)
            all_businesses.extend(serpapi_businesses)
            logger.info(f"Found {len(serpapi_businesses)} businesses from SerpAPI")
        except Exception as e:
            logger.error(f"SerpAPI search failed: {e}")
    
    # Source 4: Web scraping Morocco directories
    try:
        scraped_businesses = scrape_morocco_directories(query, location, max_results // 4)
        all_businesses.extend(scraped_businesses)
        logger.info(f"Found {len(scraped_businesses)} businesses from web scraping")
    except Exception as e:
        logger.error(f"Web scraping failed: {e}")
    
    # Remove duplicates and enhance data
    unique_businesses = remove_duplicates(all_businesses)
    enhanced_businesses = enhance_business_data(unique_businesses)
    
    logger.info(f"Total unique businesses found: {len(enhanced_businesses)}")
    
    # Show helpful message if no businesses found
    if len(enhanced_businesses) == 0:
        logger.warning("No businesses found from any source")
        print("\n" + "="*60)
        print("🚨 NO BUSINESS DATA FOUND")
        print("="*60)
        print("💡 SUGGESTIONS:")
        print("1. 📊 Generate sample data first to test the system:")
        print("   python scripts/collect_real_data.py --generate-samples")
        print("   python main.py search --location 'Marrakesh' --categories restaurants --demo")
        print("")
        print("2. 🔑 Add API keys for better results:")
        print("   • Copy .env.example to .env")
        print("   • Add your API keys (Foursquare, SerpAPI)")
        print("   • Free tiers available for testing")
        print("")
        print("3. 🌐 Check internet connection and try again")
        print("4. 📍 Try different location or business categories")
        print("="*60)
    
    return enhanced_businesses[:max_results]

@rate_limit(seconds=1)
def search_openstreetmap(query: str, location: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Search businesses using OpenStreetMap Nominatim API (completely free).
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
    
    Returns:
        List of business dictionaries
    """
    businesses = []
    
    try:
        # Format search query
        search_term = f"{query} in {location}"
        
        params = {
            'q': search_term,
            'format': 'json',
            'limit': max_results,
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        }
        
        headers = {
            'User-Agent': 'BusinessLeadFinder/1.0 (https://example.com/contact; contact@example.com)',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.openstreetmap.org/',
            'DNT': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        # Add more substantial rate limiting delay for OpenStreetMap
        time.sleep(random.uniform(2, 4))
        
        response = requests.get(
            FREE_API_URLS['nominatim'],
            params=params,
            headers=headers,
            timeout=SEARCH_CONFIG['request_timeout']
        )
        response.raise_for_status()
        
        results = response.json()
        
        for place in results:
            business = extract_business_from_osm(place)
            if business:
                businesses.append(business)
                
    except Exception as e:
        logger.error(f"OpenStreetMap API error: {e}")
        
    return businesses

def extract_business_from_osm(place: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from OpenStreetMap place data."""
    try:
        # Only process commercial amenities
        if place.get('type') not in ['amenity', 'shop', 'tourism']:
            return None
            
        business = {
            'name': place.get('display_name', '').split(',')[0],
            'address': place.get('display_name', ''),
            'phone': place.get('extratags', {}).get('phone', ''),
            'website': place.get('extratags', {}).get('website', ''),
            'category': place.get('class', ''),
            'subcategory': place.get('type', ''),
            'latitude': float(place.get('lat', 0)),
            'longitude': float(place.get('lon', 0)),
            'source': 'openstreetmap',
            'rating': 0.0,
            'review_count': 0
        }
        
        # Clean phone number
        if business['phone']:
            business['phone'] = clean_phone_number(business['phone'])
            
        return business
        
    except Exception as e:
        logger.error(f"Error extracting OSM business data: {e}")
        return None

@rate_limit(seconds=1)
def search_foursquare(query: str, location: str, max_results: int = 20, config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Search businesses using Foursquare Places API (free tier).
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
        config: Configuration dictionary with API keys
    
    Returns:
        List of business dictionaries
    """
    businesses = []
    
    try:
        # Get API key from config or environment
        client_id = None
        if config and config.get('api_keys', {}).get('foursquare'):
            client_id = config['api_keys']['foursquare']
        elif API_KEYS.get('foursquare_client_id'):
            client_id = API_KEYS['foursquare_client_id']
        
        if not client_id:
            logger.warning("Foursquare client ID not configured")
            return businesses
        
        headers = {
            'Authorization': client_id,
            'Accept': 'application/json'
        }
        
        params = {
            'query': query,
            'near': location,
            'limit': min(max_results, 50),  # Foursquare max is 50
            'fields': 'name,location,contact,rating,stats,categories'
        }
        
        response = requests.get(
            FREE_API_URLS['foursquare'],
            headers=headers,
            params=params,
            timeout=SEARCH_CONFIG['request_timeout']
        )
        response.raise_for_status()
        
        data = response.json()
        
        for place in data.get('results', []):
            business = extract_business_from_foursquare(place)
            if business:
                businesses.append(business)
                
    except Exception as e:
        logger.error(f"Foursquare API error: {e}")
        
    return businesses

def extract_business_from_foursquare(place: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from Foursquare place data."""
    try:
        location_data = place.get('location', {})
        contact_data = place.get('contact', {})
        
        business = {
            'name': place.get('name', ''),
            'address': location_data.get('formatted_address', ''),
            'phone': contact_data.get('phone', ''),
            'website': contact_data.get('website', ''),
            'category': place.get('categories', [{}])[0].get('name', '') if place.get('categories') else '',
            'latitude': location_data.get('lat', 0),
            'longitude': location_data.get('lng', 0),
            'rating': place.get('rating', 0.0),
            'review_count': place.get('stats', {}).get('total_ratings', 0),
            'source': 'foursquare'
        }
        
        # Clean phone number
        if business['phone']:
            business['phone'] = clean_phone_number(business['phone'])
            
        return business
        
    except Exception as e:
        logger.error(f"Error extracting Foursquare business data: {e}")
        return None

@rate_limit(seconds=2)
def search_serpapi(query: str, location: str, max_results: int = 20, config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Search businesses using SerpAPI (free tier - 100 searches/month).
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
        config: Configuration dictionary with API keys
    
    Returns:
        List of business dictionaries
    """
    businesses = []
    
    try:
        # Get API key from config or environment
        api_key = None
        if config and config.get('api_keys', {}).get('serpapi'):
            api_key = config['api_keys']['serpapi']
        elif API_KEYS.get('serpapi'):
            api_key = API_KEYS['serpapi']
        
        if not api_key:
            logger.warning("SerpAPI key not configured")
            return businesses
        
        params = {
            'engine': 'google_maps',
            'q': f"{query} {location}",
            'api_key': api_key,
            'num': min(max_results, 20)  # SerpAPI limit
        }
        
        response = requests.get(
            FREE_API_URLS['serpapi'],
            params=params,
            timeout=SEARCH_CONFIG['request_timeout']
        )
        response.raise_for_status()
        
        data = response.json()
        
        for place in data.get('local_results', []):
            business = extract_business_from_serpapi(place)
            if business:
                businesses.append(business)
                
    except Exception as e:
        logger.error(f"SerpAPI error: {e}")
        
    return businesses

def extract_business_from_serpapi(place: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from SerpAPI place data."""
    try:
        business = {
            'name': place.get('title', ''),
            'address': place.get('address', ''),
            'phone': place.get('phone', ''),
            'website': place.get('website', ''),
            'category': place.get('type', ''),
            'rating': float(place.get('rating', 0)),
            'review_count': int(place.get('reviews', 0)),
            'latitude': place.get('gps_coordinates', {}).get('latitude', 0),
            'longitude': place.get('gps_coordinates', {}).get('longitude', 0),
            'source': 'serpapi'
        }
        
        # Clean phone number
        if business['phone']:
            business['phone'] = clean_phone_number(business['phone'])
            
        return business
        
    except Exception as e:
        logger.error(f"Error extracting SerpAPI business data: {e}")
        return None

def scrape_business_directories(query: str, location: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Scrape business information from public directories.
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
    
    Returns:
        List of business dictionaries
    """
    businesses = []
    
    try:
        # Simple web scraping for public directories
        # This is a basic implementation - in production, you'd want more sophisticated scraping
        search_url = f"https://www.google.com/search?q={quote(f'{query} {location} contact phone')}"
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic business information from search results
        for result in soup.find_all('div', class_='g')[:max_results]:
            business = extract_business_from_search_result(result)
            if business:
                businesses.append(business)
                
    except Exception as e:
        logger.error(f"Web scraping error: {e}")
        
    return businesses

def extract_business_from_search_result(result) -> Optional[Dict[str, Any]]:
    """Extract business information from search result."""
    try:
        # Basic extraction - this is simplified
        title_elem = result.find('h3')
        if not title_elem:
            return None
            
        business = {
            'name': title_elem.get_text(),
            'address': '',
            'phone': '',
            'website': '',
            'category': '',
            'rating': 0.0,
            'review_count': 0,
            'source': 'web_scraping'
        }
        
        # Look for phone numbers in the text
        text = result.get_text()
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            business['phone'] = clean_phone_number(phone_match.group(1))
            
        return business
        
    except Exception as e:
        logger.error(f"Error extracting search result: {e}")
        return None

def remove_duplicate_businesses(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate businesses based on name and phone number.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        List of unique business dictionaries
    """
    seen = set()
    unique_businesses = []
    
    for business in businesses:
        # Create a unique key based on name and phone
        name = business.get('name', '').lower().strip()
        phone = business.get('phone', '').strip()
        
        # Create identifier
        identifier = f"{name}|{phone}"
        
        if identifier not in seen and name:
            seen.add(identifier)
            unique_businesses.append(business)
            
    return unique_businesses

def search_specific_business(business_name: str, location: str, phone: str = None) -> Optional[Dict[str, Any]]:
    """
    Search for a specific business by name and location.
    
    Args:
        business_name: Name of the business
        location: Location of the business
        phone: Optional phone number for verification
    
    Returns:
        Business dictionary if found, None otherwise
    """
    try:
        # Try all sources for specific business
        all_results = []
        
        # Search with specific business name
        query = business_name
        
        # OpenStreetMap search
        osm_results = search_openstreetmap(query, location, 5)
        all_results.extend(osm_results)
        
        # Foursquare search
        if API_KEYS.get('foursquare_client_id'):
            foursquare_results = search_foursquare(query, location, 5)
            all_results.extend(foursquare_results)
        
        # Find best match
        for business in all_results:
            if business_name.lower() in business.get('name', '').lower():
                # If phone is provided, verify it matches
                if phone and business.get('phone'):
                    if clean_phone_number(phone) == clean_phone_number(business.get('phone', '')):
                        return business
                elif not phone:
                    return business
                    
        return None
        
    except Exception as e:
        logger.error(f"Error searching specific business: {e}")
        return None

def calculate_lead_score(business: Dict[str, Any]) -> int:
    """
    Calculate lead score for a business based on various factors.
    Updated to prioritize low-rated businesses (more likely to lack websites).
    
    Key insight: Businesses with 2-3 stars are most likely to not have websites
    and represent the highest opportunity for web design services.
    
    Args:
        business: Business dictionary
    
    Returns:
        Lead score from 0-100 (higher = better opportunity)
    """
    score = 0
    
    try:
        # Base score
        score = 20
        
        # No website = HIGH opportunity (30 points)
        if not business.get('website'):
            score += 30
            logger.debug(f"High opportunity: {business.get('name')} has no website")
        else:
            # Has website = lower priority
            score -= 10
        
        # Rating factor - LOW RATINGS ARE HIGH OPPORTUNITY!
        # Businesses with 2-3 stars are most likely to lack websites
        rating = business.get('rating', 0)
        if rating == 0:
            # No rating = unknown, medium opportunity
            score += 10
        elif 2.0 <= rating <= 3.5:
            # LOW RATING = HIGH OPPORTUNITY (businesses likely need help)
            score += 25
            logger.debug(f"High opportunity: {business.get('name')} has low rating {rating}")
        elif 3.5 < rating <= 4.0:
            # Medium rating = medium opportunity
            score += 15
        elif rating > 4.0:
            # High rating = lower opportunity (probably already successful)
            score += 8
        
        # Review count factor (15 points max)
        review_count = business.get('review_count', 0)
        if 0 < review_count <= 20:
            # Few reviews = higher opportunity (less established online)
            score += 15
        elif 20 < review_count <= 50:
            score += 12
        elif 50 < review_count <= 100:
            score += 8
        elif review_count > 100:
            # Many reviews = lower opportunity (already established)
            score += 5
        
        # Has phone number (10 points)
        if business.get('phone'):
            score += 10
        
        # Category factor (15 points max)
        category = business.get('category', '').lower()
        high_opportunity_categories = ['restaurant', 'hotel', 'spa', 'cafe', 'shop', 'service']
        if any(cat in category for cat in high_opportunity_categories):
            score += 15
        else:
            score += 5
        
        # Location factor - businesses in tourist areas have higher potential
        address = business.get('address', '').lower()
        if any(area in address for area in ['medina', 'gueliz', 'hivernage', 'majorelle']):
            score += 5
            
    except Exception as e:
        logger.error(f"Error calculating lead score: {e}")
        score = 0
    
    return min(score, 100)

def scrape_morocco_directories(query: str, location: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Scrape Morocco business directories for additional leads.
    
    Args:
        query: Business category or type
        location: Location to search
        max_results: Maximum number of results
    
    Returns:
        List of business dictionaries
    """
    businesses = []
    
    try:
        # This is a placeholder for web scraping functionality
        # In a real implementation, you would scrape various Morocco business directories
        # For now, return empty list to avoid errors
        logger.info("Web scraping functionality placeholder - returning empty results")
        return businesses
    
    except Exception as e:
        logger.error(f"Error in web scraping: {e}")
        return businesses

def remove_duplicates(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate businesses based on name and location.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        List of unique business dictionaries
    """
    seen = set()
    unique_businesses = []
    
    for business in businesses:
        # Create a key for duplicate detection
        name = business.get('name', '').lower().strip()
        address = business.get('address', '').lower().strip()
        phone = business.get('phone', '').strip()
        
        # Create composite key
        key = f"{name}:{address}:{phone}"
        
        if key not in seen:
            seen.add(key)
            unique_businesses.append(business)
    
    logger.info(f"Removed {len(businesses) - len(unique_businesses)} duplicates")
    return unique_businesses

def enhance_business_data(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enhance business data with additional information and scoring.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        List of enhanced business dictionaries
    """
    enhanced_businesses = []
    
    for business in businesses:
        try:
            # Add lead score
            business['lead_score'] = calculate_lead_score(business)
            
            # Add timestamp
            business['last_updated'] = datetime.now().isoformat()
            
            # Ensure all required fields exist
            business.setdefault('name', 'Unknown Business')
            business.setdefault('category', 'Unknown')
            business.setdefault('address', '')
            business.setdefault('phone', '')
            business.setdefault('email', '')
            business.setdefault('emails', [])  # List of emails for enhanced contact info
            business.setdefault('website', '')
            business.setdefault('rating', 0)
            business.setdefault('review_count', 0)
            business.setdefault('source', 'unknown')
            
            # If email field exists but emails list is empty, add to emails list
            if business.get('email') and not business.get('emails'):
                business['emails'] = [business['email']]
            elif business.get('emails') and not business.get('email'):
                business['email'] = business['emails'][0] if business['emails'] else ''
            
            # Quality filtering: Skip businesses with websites but low ratings (under 4.5)
            has_website = business.get('website', '').strip()
            rating = business.get('rating', 0)
            
            # If business has website but rating is under 4.5, skip it (not a good lead)
            if has_website and rating > 0 and rating < 4.5:
                continue  # Skip this business
            
            enhanced_businesses.append(business)
            
        except Exception as e:
            logger.error(f"Error enhancing business data: {e}")
            # Add business anyway with minimal data
            enhanced_businesses.append(business)
    
    return enhanced_businesses

def update_business_with_enhanced_website_check(business: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update business data with enhanced website detection.
    
    Args:
        business: Business data dictionary
        
    Returns:
        Updated business data with website information
    """
    from website_checker import enhanced_website_detection
    
    # Run enhanced website detection
    detection_result = enhanced_website_detection(
        business_name=business.get('name', ''),
        category=business.get('category', '')
    )
    
    # Update business data based on results
    if detection_result['website_found']:
        business['website'] = detection_result['website_url']
        business['website_detection_method'] = 'enhanced_domain_check'
        # Reduce lead score since they have a website
        business['lead_score'] = max(30, business.get('lead_score', 50) - 20)
    else:
        business['website'] = ''
        # Increase lead score since no website found
        business['lead_score'] = min(100, business.get('lead_score', 50) + 15)
    
    # Add detection metadata
    business['website_domains_checked'] = detection_result['domains_checked']
    business['website_domains_found'] = detection_result['domains_found']
    
    return business
