"""
Business Search Module - Free Implementation
Searches for businesses using free APIs and web scraping.
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import json
import random

from config.settings import FREE_API_URLS, USER_AGENTS, SEARCH_CONFIG

logger = logging.getLogger(__name__)

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
    
    logger.info(f"Starting business search for '{query}' in '{location}'")
    
    # Source 1: OpenStreetMap Nominatim (Always free)
    try:
        osm_businesses = search_openstreetmap(query, location, max_results // 3)
        all_businesses.extend(osm_businesses)
        logger.info(f"Found {len(osm_businesses)} businesses from OpenStreetMap")
    except Exception as e:
        logger.error(f"OpenStreetMap search failed: {e}")
    
    # Source 2: Foursquare (Free tier - 1000 requests/day)
    if config and config.get('api_keys', {}).get('foursquare_client_id'):
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
    
    return enhanced_businesses[:max_results]

def search_openstreetmap(query: str, location: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Search businesses using OpenStreetMap Nominatim API.
    Completely free, no API key required.
    """
    base_url = f"{FREE_API_URLS['openstreetmap_nominatim']}/search"
    
    params = {
        'q': f"{query} {location}",
        'format': 'json',
        'limit': max_results,
        'addressdetails': 1,
        'extratags': 1,
        'namedetails': 1
    }
    
    headers = {
        'User-Agent': 'BusinessLeadFinder/1.0 (business-finder@example.com)'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Respect rate limits
        time.sleep(1)
        
        data = response.json()
        businesses = []
        
        for place in data:
            if place.get('class') in ['amenity', 'shop', 'tourism', 'leisure']:
                business = extract_business_from_osm(place)
                if business:
                    businesses.append(business)
        
        return businesses
        
    except Exception as e:
        logger.error(f"OpenStreetMap API error: {e}")
        return []

def extract_business_from_osm(place: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from OpenStreetMap data."""
    try:
        display_name_parts = place.get('display_name', '').split(',')
        business_name = display_name_parts[0] if display_name_parts else ''
        
        if len(business_name) < 2:
            return None
        
        business = {
            'name': business_name.strip(),
            'address': place.get('display_name', ''),
            'category': place.get('class', ''),
            'subcategory': place.get('type', ''),
            'lat': place.get('lat', ''),
            'lon': place.get('lon', ''),
            'osm_id': place.get('osm_id', ''),
            'source': 'openstreetmap',
            'phone': '',
            'website': '',
            'email': '',
            'rating': 0.0,
            'review_count': 0,
            'social_media': {}
        }
        
        # Extract additional info from extratags
        extratags = place.get('extratags', {})
        if extratags:
            business['phone'] = extratags.get('phone', '')
            business['website'] = extratags.get('website', '')
            business['email'] = extratags.get('email', '')
            business['opening_hours'] = extratags.get('opening_hours', '')
        
        return business
        
    except Exception as e:
        logger.error(f"Error extracting OSM business data: {e}")
        return None

def search_foursquare(query: str, location: str, max_results: int = 20, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Search businesses using Foursquare Places API."""
    if not config or not config.get('api_keys', {}).get('foursquare_client_id'):
        return []
    
    base_url = f"{FREE_API_URLS['foursquare_places']}/venues/search"
    
    params = {
        'client_id': config['api_keys']['foursquare_client_id'],
        'client_secret': config['api_keys']['foursquare_client_secret'],
        'v': '20230101',  # API version
        'near': location,
        'query': query,
        'limit': min(max_results, 50),  # Foursquare limit
        'intent': 'browse'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Respect rate limits
        time.sleep(1)
        
        data = response.json()
        businesses = []
        
        for venue in data.get('response', {}).get('venues', []):
            business = extract_business_from_foursquare(venue)
            if business:
                businesses.append(business)
        
        return businesses
        
    except Exception as e:
        logger.error(f"Foursquare API error: {e}")
        return []

def extract_business_from_foursquare(venue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from Foursquare data."""
    try:
        location_data = venue.get('location', {})
        categories = venue.get('categories', [])
        
        business = {
            'name': venue.get('name', ''),
            'address': ', '.join(location_data.get('formattedAddress', [])),
            'category': categories[0].get('name', '') if categories else '',
            'subcategory': categories[0].get('shortName', '') if categories else '',
            'lat': location_data.get('lat', ''),
            'lon': location_data.get('lng', ''),
            'foursquare_id': venue.get('id', ''),
            'source': 'foursquare',
            'phone': venue.get('contact', {}).get('phone', ''),
            'website': venue.get('url', ''),
            'email': '',
            'rating': venue.get('rating', 0.0),
            'review_count': venue.get('ratingSignals', 0),
            'social_media': {}
        }
        
        # Extract social media if available
        contact = venue.get('contact', {})
        if contact.get('twitter'):
            business['social_media']['twitter'] = f"https://twitter.com/{contact['twitter']}"
        if contact.get('facebook'):
            business['social_media']['facebook'] = f"https://facebook.com/{contact['facebook']}"
        if contact.get('instagram'):
            business['social_media']['instagram'] = f"https://instagram.com/{contact['instagram']}"
        
        return business if business['name'] else None
        
    except Exception as e:
        logger.error(f"Error extracting Foursquare business data: {e}")
        return None

def search_serpapi(query: str, location: str, max_results: int = 20, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Search businesses using SerpAPI."""
    if not config or not config.get('api_keys', {}).get('serpapi'):
        return []
    
    base_url = FREE_API_URLS['serpapi']
    
    params = {
        'engine': 'google_maps',
        'q': f"{query} {location}",
        'api_key': config['api_keys']['serpapi'],
        'num': min(max_results, 20)  # SerpAPI limit for free tier
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        businesses = []
        
        for result in data.get('local_results', []):
            business = extract_business_from_serpapi(result)
            if business:
                businesses.append(business)
        
        return businesses
        
    except Exception as e:
        logger.error(f"SerpAPI error: {e}")
        return []

def extract_business_from_serpapi(result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract business information from SerpAPI data."""
    try:
        business = {
            'name': result.get('title', ''),
            'address': result.get('address', ''),
            'category': result.get('type', ''),
            'subcategory': '',
            'lat': result.get('gps_coordinates', {}).get('latitude', ''),
            'lon': result.get('gps_coordinates', {}).get('longitude', ''),
            'serpapi_id': result.get('place_id', ''),
            'source': 'serpapi',
            'phone': result.get('phone', ''),
            'website': result.get('website', ''),
            'email': '',
            'rating': result.get('rating', 0.0),
            'review_count': result.get('reviews', 0),
            'social_media': {}
        }
        
        # Extract hours
        if result.get('hours'):
            business['opening_hours'] = result['hours']
        
        return business if business['name'] else None
        
    except Exception as e:
        logger.error(f"Error extracting SerpAPI business data: {e}")
        return None

def scrape_morocco_directories(query: str, location: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Scrape business listings from Morocco business directories.
    Uses public data from business directory websites.
    """
    businesses = []
    
    # Morocco business directories (public data)
    directories = [
        {
            'name': 'Morocco Business Directory',
            'base_url': 'https://www.pagesjaunes.ma',
            'search_path': '/recherche'
        },
        {
            'name': 'Yelo Morocco',
            'base_url': 'https://www.yelo.ma',
            'search_path': '/search'
        }
    ]
    
    for directory in directories:
        try:
            dir_businesses = scrape_single_directory(directory, query, location, max_results // len(directories))
            businesses.extend(dir_businesses)
            
            # Be respectful with delays
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error scraping {directory['name']}: {e}")
            continue
    
    return businesses

def scrape_single_directory(directory: Dict[str, str], query: str, location: str, max_results: int) -> List[Dict[str, Any]]:
    """Scrape a single business directory."""
    businesses = []
    
    try:
        # Construct search URL (this is simplified - real implementation would be more complex)
        search_url = f"{directory['base_url']}{directory['search_path']}?q={query}&location={location}"
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This is a simplified example - real selectors would be specific to each site
        listings = soup.find_all('div', class_=['business-item', 'listing', 'result-item'])
        
        for listing in listings[:max_results]:
            business = extract_business_from_html(listing, directory['name'])
            if business:
                businesses.append(business)
        
    except Exception as e:
        logger.error(f"Error scraping directory {directory['name']}: {e}")
    
    return businesses

def extract_business_from_html(listing, source: str) -> Optional[Dict[str, Any]]:
    """Extract business information from HTML listing."""
    try:
        business = {
            'name': '',
            'address': '',
            'category': '',
            'subcategory': '',
            'lat': '',
            'lon': '',
            'source': f'scraping_{source.lower().replace(" ", "_")}',
            'phone': '',
            'website': '',
            'email': '',
            'rating': 0.0,
            'review_count': 0,
            'social_media': {}
        }
        
        # Extract name (adapt selectors for each site)
        name_selectors = ['h3', 'h2', '.business-name', '.title', '.name']
        for selector in name_selectors:
            name_elem = listing.select_one(selector)
            if name_elem:
                business['name'] = name_elem.get_text(strip=True)
                break
        
        # Extract address
        address_selectors = ['.address', '.location', '.addr']
        for selector in address_selectors:
            addr_elem = listing.select_one(selector)
            if addr_elem:
                business['address'] = addr_elem.get_text(strip=True)
                break
        
        # Extract phone
        phone_elem = listing.select_one('a[href*="tel:"]')
        if phone_elem:
            business['phone'] = phone_elem.get_text(strip=True)
        
        # Extract website
        website_elem = listing.select_one('a[href*="http"]')
        if website_elem and 'http' in website_elem.get('href', ''):
            business['website'] = website_elem.get('href')
        
        # Extract category
        category_selectors = ['.category', '.type', '.business-type']
        for selector in category_selectors:
            cat_elem = listing.select_one(selector)
            if cat_elem:
                business['category'] = cat_elem.get_text(strip=True)
                break
        
        return business if business['name'] and len(business['name']) > 1 else None
        
    except Exception as e:
        logger.error(f"Error extracting business from HTML: {e}")
        return None

def remove_duplicates(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate businesses based on name and address similarity."""
    unique_businesses = []
    seen_combinations = set()
    
    for business in businesses:
        # Create a normalized key for duplicate detection
        name_key = business.get('name', '').lower().strip()
        address_key = business.get('address', '').lower().strip()
        phone_key = business.get('phone', '').strip()
        
        # Use name + first part of address as key
        address_parts = address_key.split(',')
        address_key = address_parts[0] if address_parts else address_key
        
        duplicate_key = f"{name_key}|{address_key}"
        
        # Also check phone number if available
        if phone_key:
            phone_duplicate_key = f"{name_key}|{phone_key}"
            if phone_duplicate_key in seen_combinations:
                continue
            seen_combinations.add(phone_duplicate_key)
        
        if duplicate_key not in seen_combinations:
            seen_combinations.add(duplicate_key)
            unique_businesses.append(business)
    
    logger.info(f"Removed {len(businesses) - len(unique_businesses)} duplicates")
    return unique_businesses

def enhance_business_data(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enhance business data with additional information and lead scoring."""
    enhanced_businesses = []
    
    for business in businesses:
        try:
            # Calculate lead score
            business['lead_score'] = calculate_lead_score(business)
            
            # Standardize phone number
            if business.get('phone'):
                business['phone'] = standardize_phone_number(business['phone'])
            
            # Validate and clean data
            business = clean_business_data(business)
            
            enhanced_businesses.append(business)
            
        except Exception as e:
            logger.error(f"Error enhancing business data: {e}")
            continue
    
    # Sort by lead score
    enhanced_businesses.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
    
    return enhanced_businesses

def calculate_lead_score(business: Dict[str, Any]) -> int:
    """Calculate lead score for a business."""
    score = 0
    
    # Rating factor (30% weight)
    rating = business.get('rating', 0)
    if rating >= 4.5:
        score += 30
    elif rating >= 4.0:
        score += 25
    elif rating >= 3.5:
        score += 15
    elif rating > 0:
        score += 10
    
    # Review count factor (20% weight)
    review_count = business.get('review_count', 0)
    if review_count >= 100:
        score += 20
    elif review_count >= 50:
        score += 15
    elif review_count >= 20:
        score += 10
    elif review_count > 0:
        score += 5
    
    # Category factor (15% weight)
    category = business.get('category', '').lower()
    high_value_categories = ['restaurant', 'hotel', 'spa', 'tour', 'shop', 'retail']
    if any(cat in category for cat in high_value_categories):
        score += 15
    else:
        score += 8
    
    # Website absence factor (25% weight)
    if not business.get('website'):
        score += 25
    
    # Contact information factor (10% weight)
    if business.get('phone'):
        score += 5
    if business.get('email'):
        score += 3
    if business.get('social_media'):
        score += 2
    
    return min(score, 100)

def standardize_phone_number(phone: str) -> str:
    """Standardize phone number format."""
    if not phone:
        return ''
    
    # Remove common separators and spaces
    clean_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
    
    # Add Morocco country code if missing
    if clean_phone and not clean_phone.startswith('+'):
        if clean_phone.startswith('0'):
            clean_phone = '+212' + clean_phone[1:]
        elif len(clean_phone) == 9:
            clean_phone = '+212' + clean_phone
    
    return clean_phone

def clean_business_data(business: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate business data."""
    # Clean name
    if business.get('name'):
        business['name'] = business['name'].strip()
    
    # Clean address
    if business.get('address'):
        business['address'] = business['address'].strip()
    
    # Ensure numeric fields are proper types
    try:
        business['rating'] = float(business.get('rating', 0))
    except (ValueError, TypeError):
        business['rating'] = 0.0
    
    try:
        business['review_count'] = int(business.get('review_count', 0))
    except (ValueError, TypeError):
        business['review_count'] = 0
    
    try:
        business['lead_score'] = int(business.get('lead_score', 0))
    except (ValueError, TypeError):
        business['lead_score'] = 0
    
    # Ensure social_media is a dict
    if not isinstance(business.get('social_media'), dict):
        business['social_media'] = {}
    
    return business
