"""
Website Checker Module
Advanced website detection using multiple methods.
"""

import requests
import logging
import time
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup

from utils import clean_phone_number, extract_domain_from_url

logger = logging.getLogger(__name__)

def check_website_status(
    business_name: str,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Check if a business has a website using multiple detection methods.
    
    Args:
        business_name: Name of the business
        phone: Business phone number (optional)
        address: Business address (optional)
        config: Configuration dictionary
    
    Returns:
        Dictionary with website status and additional information
    """
    logger.info(f"Checking website status for: {business_name}")
    
    result = {
        'business_name': business_name,
        'website': None,
        'confidence': 0,
        'social_media': {},
        'additional_info': {},
        'methods_used': [],
        'timestamp': time.time()
    }
    
    # Method 1: Direct search engine queries
    try:
        search_results = search_engine_website_detection(business_name, address)
        if search_results['website']:
            result['website'] = search_results['website']
            result['confidence'] = search_results['confidence']
            result['methods_used'].append('search_engine')
            logger.info(f"Website found via search engine: {result['website']}")
    except Exception as e:
        logger.error(f"Search engine detection failed: {e}")
    
    # Method 2: Social media profile analysis
    try:
        social_results = check_social_media_profiles(business_name, address)
        result['social_media'] = social_results['profiles']
        
        # Check if social media has website links
        if not result['website'] and social_results.get('website_from_social'):
            result['website'] = social_results['website_from_social']
            result['confidence'] = 60
            result['methods_used'].append('social_media')
            logger.info(f"Website found via social media: {result['website']}")
    except Exception as e:
        logger.error(f"Social media detection failed: {e}")
    
    # Method 3: Phone number reverse lookup
    if phone and not result['website']:
        try:
            phone_results = phone_reverse_lookup(phone, business_name)
            if phone_results['website']:
                result['website'] = phone_results['website']
                result['confidence'] = phone_results['confidence']
                result['methods_used'].append('phone_lookup')
                logger.info(f"Website found via phone lookup: {result['website']}")
        except Exception as e:
            logger.error(f"Phone lookup failed: {e}")
    
    # Method 4: Business directory checks
    try:
        directory_results = check_business_directories(business_name, address, phone)
        if not result['website'] and directory_results['website']:
            result['website'] = directory_results['website']
            result['confidence'] = directory_results['confidence']
            result['methods_used'].append('directory_search')
            logger.info(f"Website found via directory: {result['website']}")
        
        # Merge additional info
        result['additional_info'].update(directory_results.get('additional_info', {}))
    except Exception as e:
        logger.error(f"Directory search failed: {e}")
    
    # Method 5: Domain guessing
    if not result['website']:
        try:
            guessed_domains = guess_business_domains(business_name)
            for domain in guessed_domains:
                if verify_domain_belongs_to_business(domain, business_name):
                    result['website'] = domain
                    result['confidence'] = 40
                    result['methods_used'].append('domain_guessing')
                    logger.info(f"Website found via domain guessing: {result['website']}")
                    break
        except Exception as e:
            logger.error(f"Domain guessing failed: {e}")
    
    # Validate final website if found
    if result['website']:
        validation_result = validate_website_belongs_to_business(result['website'], business_name)
        if not validation_result['is_valid']:
            logger.warning(f"Website validation failed for {result['website']}")
            result['website'] = None
            result['confidence'] = 0
        else:
            result['confidence'] = min(result['confidence'] + validation_result['confidence_boost'], 100)
    
    logger.info(f"Website check completed. Found: {'Yes' if result['website'] else 'No'}")
    return result

def search_engine_website_detection(business_name: str, address: Optional[str] = None) -> Dict[str, Any]:
    """Search for business website using search engine queries."""
    result = {
        'website': None,
        'confidence': 0,
        'search_queries_used': []
    }
    
    # Create search queries
    queries = []
    base_name = business_name.strip()
    
    queries.append(f'"{base_name}" website')
    queries.append(f'"{base_name}" site:')
    queries.append(f'"{base_name}" official website')
    
    if address:
        queries.append(f'"{base_name}" "{address}" website')
        queries.append(f'"{base_name}" "{address}" site:')
    
    # Common business keywords
    business_keywords = ['menu', 'booking', 'reservation', 'contact', 'about']
    for keyword in business_keywords:
        queries.append(f'"{base_name}" {keyword} site:')
    
    # Try each query (this is a simplified version - real implementation would use search APIs)
    for query in queries[:3]:  # Limit to avoid rate limiting
        try:
            websites = simulate_search_query(query)
            if websites:
                # Take the first valid website
                for website in websites:
                    if is_valid_website_url(website):
                        result['website'] = website
                        result['confidence'] = 80
                        result['search_queries_used'].append(query)
                        break
                if result['website']:
                    break
        except Exception as e:
            logger.error(f"Error in search query '{query}': {e}")
            continue
    
    return result

def simulate_search_query(query: str) -> List[str]:
    """
    Simulate search query results.
    In a real implementation, this would use a search API like SerpAPI or custom search.
    """
    # This is a placeholder - real implementation would:
    # 1. Use SerpAPI or similar service
    # 2. Parse search results
    # 3. Extract website URLs
    # 4. Filter and validate results
    
    websites = []
    
    # For demonstration, we'll simulate some common patterns
    business_name_clean = re.sub(r'[^\w\s]', '', query.split('"')[1] if '"' in query else query)
    business_slug = business_name_clean.lower().replace(' ', '')
    
    # Common domain patterns
    common_domains = [
        f"{business_slug}.com",
        f"{business_slug}.ma",
        f"{business_slug}-marrakech.com",
        f"{business_slug}-morocco.com",
        f"www.{business_slug}.com"
    ]
    
    # In real implementation, these would come from actual search results
    return []

def check_social_media_profiles(business_name: str, address: Optional[str] = None) -> Dict[str, Any]:
    """Check social media profiles for website links."""
    result = {
        'profiles': {},
        'website_from_social': None
    }
    
    # Social media platforms to check
    platforms = {
        'facebook': 'https://www.facebook.com',
        'instagram': 'https://www.instagram.com',
        'linkedin': 'https://www.linkedin.com',
        'twitter': 'https://twitter.com'
    }
    
    business_slug = re.sub(r'[^\w]', '', business_name.lower().replace(' ', ''))
    
    for platform, base_url in platforms.items():
        try:
            # Common profile URL patterns
            profile_patterns = [
                f"{base_url}/{business_slug}",
                f"{base_url}/{business_slug}official",
                f"{base_url}/{business_slug}marrakech",
                f"{base_url}/{business_slug}morocco"
            ]
            
            for profile_url in profile_patterns:
                if check_social_profile_exists(profile_url, business_name):
                    result['profiles'][platform] = profile_url
                    
                    # Try to extract website from profile
                    website = extract_website_from_social_profile(profile_url)
                    if website and not result['website_from_social']:
                        result['website_from_social'] = website
                    break
        except Exception as e:
            logger.error(f"Error checking {platform} for {business_name}: {e}")
            continue
    
    return result

def check_social_profile_exists(profile_url: str, business_name: str) -> bool:
    """Check if a social media profile exists and belongs to the business."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(profile_url, headers=headers, timeout=10)
        
        # If page loads without 404, consider it exists
        if response.status_code == 200:
            # Simple content check
            content = response.text.lower()
            business_keywords = business_name.lower().split()
            
            # Check if business name appears in content
            keyword_matches = sum(1 for keyword in business_keywords if keyword in content)
            return keyword_matches >= len(business_keywords) * 0.5
        
        return False
    except:
        return False

def extract_website_from_social_profile(profile_url: str) -> Optional[str]:
    """Extract website URL from social media profile."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(profile_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for website links in common locations
        website_selectors = [
            'a[href*="http"]:not([href*="facebook"]):not([href*="instagram"]):not([href*="twitter"]):not([href*="linkedin"])',
            '[data-testid="website"]',
            '.website',
            '.external-link'
        ]
        
        for selector in website_selectors:
            link_elem = soup.select_one(selector)
            if link_elem:
                href = link_elem.get('href')
                if href and is_valid_website_url(href):
                    return href
        
        return None
    except:
        return None

def phone_reverse_lookup(phone: str, business_name: str) -> Dict[str, Any]:
    """Perform reverse lookup on phone number to find website."""
    result = {
        'website': None,
        'confidence': 0
    }
    
    clean_phone = clean_phone_number(phone)
    
    # This is a simplified version - real implementation would:
    # 1. Use phone directory APIs
    # 2. Search business directories by phone
    # 3. Check online directories
    
    # For now, we'll simulate by checking if phone appears in common business directories
    directories_to_check = [
        'https://www.pagesjaunes.ma',
        'https://www.yelo.ma'
    ]
    
    for directory in directories_to_check:
        try:
            website = search_directory_by_phone(directory, clean_phone, business_name)
            if website:
                result['website'] = website
                result['confidence'] = 70
                break
        except Exception as e:
            logger.error(f"Error in phone lookup from {directory}: {e}")
            continue
    
    return result

def search_directory_by_phone(directory_url: str, phone: str, business_name: str) -> Optional[str]:
    """Search a business directory by phone number."""
    # This is a placeholder for actual directory search implementation
    # Real implementation would:
    # 1. Navigate to directory search page
    # 2. Search by phone number
    # 3. Parse results for matching business
    # 4. Extract website if available
    
    return None

def check_business_directories(
    business_name: str,
    address: Optional[str] = None,
    phone: Optional[str] = None
) -> Dict[str, Any]:
    """Check business directories for website information."""
    result = {
        'website': None,
        'confidence': 0,
        'additional_info': {}
    }
    
    # Common business directories
    directories = [
        {
            'name': 'Google My Business',
            'search_method': 'google_business'
        },
        {
            'name': 'Yelp',
            'search_method': 'yelp'
        },
        {
            'name': 'TripAdvisor',
            'search_method': 'tripadvisor'
        }
    ]
    
    for directory in directories:
        try:
            dir_result = search_single_directory(
                directory['search_method'],
                business_name,
                address,
                phone
            )
            
            if dir_result['website'] and not result['website']:
                result['website'] = dir_result['website']
                result['confidence'] = dir_result['confidence']
            
            # Merge additional info
            result['additional_info'].update(dir_result.get('info', {}))
            
        except Exception as e:
            logger.error(f"Error searching {directory['name']}: {e}")
            continue
    
    return result

def search_single_directory(
    method: str,
    business_name: str,
    address: Optional[str] = None,
    phone: Optional[str] = None
) -> Dict[str, Any]:
    """Search a single directory for business information."""
    result = {
        'website': None,
        'confidence': 0,
        'info': {}
    }
    
    # This is a simplified version - real implementation would:
    # 1. Use directory-specific APIs or scraping
    # 2. Search for business by name/address/phone
    # 3. Extract website and other information
    # 4. Validate results
    
    if method == 'google_business':
        # Would use Google My Business API or Google Places API
        pass
    elif method == 'yelp':
        # Would use Yelp Fusion API
        pass
    elif method == 'tripadvisor':
        # Would use TripAdvisor API or scraping
        pass
    
    return result

def guess_business_domains(business_name: str) -> List[str]:
    """Generate potential domain names for a business."""
    domains = []
    
    # Clean business name
    clean_name = re.sub(r'[^\w\s]', '', business_name.lower())
    words = clean_name.split()
    
    # Remove common business words
    business_words = ['restaurant', 'hotel', 'cafe', 'spa', 'shop', 'store', 'bar']
    filtered_words = [word for word in words if word not in business_words]
    
    if not filtered_words:
        filtered_words = words  # Use all words if none left
    
    # Generate domain patterns
    base_name = ''.join(filtered_words)
    hyphen_name = '-'.join(filtered_words)
    
    # Common TLDs
    tlds = ['.com', '.ma', '.net', '.org']
    
    for tld in tlds:
        domains.extend([
            f"{base_name}{tld}",
            f"{hyphen_name}{tld}",
            f"www.{base_name}{tld}",
            f"{base_name}-marrakech{tld}",
            f"{base_name}-morocco{tld}"
        ])
    
    return domains

def verify_domain_belongs_to_business(domain: str, business_name: str) -> bool:
    """Verify if a domain belongs to the specified business."""
    try:
        # Add protocol if missing
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        response = requests.get(domain, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            return validate_website_content(response.text, business_name)
        
        return False
    except:
        return False

def validate_website_belongs_to_business(website_url: str, business_name: str) -> Dict[str, Any]:
    """Validate if website actually belongs to the business."""
    result = {
        'is_valid': False,
        'confidence_boost': 0,
        'validation_details': {}
    }
    
    try:
        # Add protocol if missing
        if not website_url.startswith(('http://', 'https://')):
            website_url = f"https://{website_url}"
        
        response = requests.get(website_url, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            content = response.text.lower()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for business name in various places
            business_keywords = business_name.lower().split()
            
            # Title check
            title = soup.find('title')
            title_matches = 0
            if title:
                title_text = title.get_text().lower()
                title_matches = sum(1 for keyword in business_keywords if keyword in title_text)
            
            # Content check
            content_matches = sum(1 for keyword in business_keywords if keyword in content)
            
            # Meta description check
            meta_desc = soup.find('meta', {'name': 'description'})
            meta_matches = 0
            if meta_desc:
                meta_text = meta_desc.get('content', '').lower()
                meta_matches = sum(1 for keyword in business_keywords if keyword in meta_text)
            
            # Calculate confidence
            total_keywords = len(business_keywords)
            if total_keywords > 0:
                title_score = (title_matches / total_keywords) * 30
                content_score = min((content_matches / total_keywords) * 50, 50)
                meta_score = (meta_matches / total_keywords) * 20
                
                total_score = title_score + content_score + meta_score
                
                result['validation_details'] = {
                    'title_matches': title_matches,
                    'content_matches': content_matches,
                    'meta_matches': meta_matches,
                    'total_keywords': total_keywords
                }
                
                if total_score >= 40:  # Threshold for validation
                    result['is_valid'] = True
                    result['confidence_boost'] = min(int(total_score), 30)
    
    except Exception as e:
        logger.error(f"Error validating website {website_url}: {e}")
    
    return result

def validate_website_content(content: str, business_name: str) -> bool:
    """Validate website content against business name."""
    content_lower = content.lower()
    business_keywords = business_name.lower().split()
    
    # Check if at least 50% of business name keywords appear in content
    keyword_matches = sum(1 for keyword in business_keywords if keyword in content_lower)
    return keyword_matches >= len(business_keywords) * 0.5

def is_valid_website_url(url: str) -> bool:
    """Check if URL is a valid website URL."""
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        
        # Must have domain
        if not parsed.netloc:
            return False
        
        # Exclude social media and directory sites
        excluded_domains = [
            'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'tiktok.com', 'snapchat.com',
            'tripadvisor.com', 'yelp.com', 'foursquare.com',
            'google.com', 'maps.google.com'
        ]
        
        domain = parsed.netloc.lower()
        for excluded in excluded_domains:
            if excluded in domain:
                return False
        
        return True
    except:
        return False

def extract_additional_contact_info(website_url: str) -> Dict[str, Any]:
    """Extract additional contact information from website."""
    contact_info = {
        'emails': [],
        'phones': [],
        'social_links': {},
        'contact_page': None
    }
    
    try:
        response = requests.get(website_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, response.text)
        contact_info['emails'] = list(set(emails))
        
        # Extract phone numbers
        phone_links = soup.find_all('a', href=re.compile(r'tel:'))
        for link in phone_links:
            phone = link.get('href').replace('tel:', '')
            contact_info['phones'].append(phone)
        
        # Extract social media links
        social_platforms = ['facebook', 'instagram', 'twitter', 'linkedin']
        for platform in social_platforms:
            links = soup.find_all('a', href=re.compile(f'{platform}.com'))
            if links:
                contact_info['social_links'][platform] = links[0].get('href')
        
        # Find contact page
        contact_links = soup.find_all('a', href=re.compile(r'contact|about|reach'))
        if contact_links:
            contact_info['contact_page'] = urljoin(website_url, contact_links[0].get('href'))
    
    except Exception as e:
        logger.error(f"Error extracting contact info from {website_url}: {e}")
    
    return contact_info
