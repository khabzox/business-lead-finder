"""
Website Checker Module for Business Lead Finder
Checks if businesses have websites using multiple detection methods.
"""

import requests
import re
import time
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket

from utils import clean_phone_number, rate_limit

logger = logging.getLogger(__name__)

# Common website patterns
WEBSITE_PATTERNS = [
    r'https?://[^\s<>"{}|\\^`\[\]]+',
    r'www\.[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}',
    r'[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.(com|org|net|ma|fr|es)'
]

# Social media platforms
SOCIAL_PLATFORMS = [
    'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
    'youtube.com', 'tiktok.com', 'whatsapp.com'
]

def check_website_status(business_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive website status check for a business.
    
    Args:
        business_data: Dictionary containing business information
    
    Returns:
        Dictionary with website status information
    """
    result = {
        'has_website': False,
        'website_url': None,
        'website_quality_score': 0,
        'social_media_profiles': [],
        'detection_method': None,
        'confidence_score': 0
    }
    
    try:
        business_name = business_data.get('name', '')
        phone = business_data.get('phone', '')
        address = business_data.get('address', '')
        
        if not business_name:
            return result
        
        # Method 1: Check existing website field
        existing_website = business_data.get('website', '')
        if existing_website and validate_website_url(existing_website):
            result.update({
                'has_website': True,
                'website_url': existing_website,
                'detection_method': 'existing_data',
                'confidence_score': 90
            })
            result['website_quality_score'] = analyze_website_quality(existing_website)
            return result
        
        # Method 2: Search engine detection
        search_website = search_business_website(business_name, address)
        if search_website:
            result.update({
                'has_website': True,
                'website_url': search_website,
                'detection_method': 'search_engine',
                'confidence_score': 75
            })
            result['website_quality_score'] = analyze_website_quality(search_website)
            return result
        
        # Method 3: Social media detection
        social_profiles = find_social_media_profiles(business_name, address)
        if social_profiles:
            result['social_media_profiles'] = social_profiles
            
            # Check if any social profiles have website links
            for profile in social_profiles:
                website_from_social = extract_website_from_social_profile(profile['url'])
                if website_from_social:
                    result.update({
                        'has_website': True,
                        'website_url': website_from_social,
                        'detection_method': 'social_media_extraction',
                        'confidence_score': 60
                    })
                    result['website_quality_score'] = analyze_website_quality(website_from_social)
                    return result
        
        # Method 4: Phone-based search
        if phone:
            phone_website = search_website_by_phone(phone)
            if phone_website:
                result.update({
                    'has_website': True,
                    'website_url': phone_website,
                    'detection_method': 'phone_search',
                    'confidence_score': 70
                })
                result['website_quality_score'] = analyze_website_quality(phone_website)
                return result
        
        # Method 5: Domain prediction
        predicted_domains = predict_business_domains(business_name)
        for domain in predicted_domains:
            if check_domain_exists(domain):
                result.update({
                    'has_website': True,
                    'website_url': f"https://{domain}",
                    'detection_method': 'domain_prediction',
                    'confidence_score': 50
                })
                result['website_quality_score'] = analyze_website_quality(f"https://{domain}")
                return result
        
        logger.info(f"No website found for business: {business_name}")
        
    except Exception as e:
        logger.error(f"Error checking website status: {e}")
    
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
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for website links in common places
        selectors = [
            'a[href*="http"]',
            '[data-testid="website"]',
            '.website',
            '.link',
            '.bio a'
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href', '')
                if href and validate_website_url(href):
                    return href
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting website from social profile: {e}")
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
    """
    Validate if a URL is a proper website URL.
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid website URL, False otherwise
    """
    try:
        if not url:
            return False
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        parsed = urlparse(url)
        
        # Must have valid domain
        if not parsed.netloc:
            return False
        
        # Must not be just social media (we want actual websites)
        if any(platform in parsed.netloc.lower() for platform in SOCIAL_PLATFORMS):
            return False
        
        # Try to access the URL
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code < 400
        
    except Exception:
        return False

@rate_limit(seconds=2)
def search_business_website(business_name: str, address: str = "") -> Optional[str]:
    """
    Search for business website using search engines.
    
    Args:
        business_name: Name of the business
        address: Business address for better targeting
    
    Returns:
        Website URL if found, None otherwise
    """
    try:
        # Create search query
        query = f'"{business_name}"'
        if address:
            # Extract city from address
            city = address.split(',')[0].strip()
            query += f" {city}"
        query += " site:"
        
        # Use multiple search approaches
        search_queries = [
            f'"{business_name}" website',
            f'"{business_name}" contact',
            f'"{business_name}" {address}' if address else f'"{business_name}"'
        ]
        
        for search_query in search_queries:
            website = perform_web_search(search_query)
            if website and validate_website_url(website):
                logger.info(f"Found website via search: {website}")
                return website
        
        return None
        
    except Exception as e:
        logger.error(f"Error searching business website: {e}")
        return None

def perform_web_search(query: str) -> Optional[str]:
    """
    Perform web search and extract potential website URLs.
    
    Args:
        query: Search query
    
    Returns:
        Website URL if found, None otherwise
    """
    try:
        # Simple search implementation (in production, use proper search APIs)
        search_url = f"https://www.google.com/search?q={query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract URLs from search results
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', response.text)
        
        # Filter for potential business websites
        for url in urls:
            if is_business_website(url, query):
                return url
        
        return None
        
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return None

def is_business_website(url: str, query: str) -> bool:
    """
    Check if URL likely belongs to the business.
    
    Args:
        url: URL to check
        query: Original search query
    
    Returns:
        True if likely business website, False otherwise
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Skip search engines and social media
        skip_domains = [
            'google.com', 'bing.com', 'yahoo.com', 'duckduckgo.com',
            'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'wikipedia.org', 'tripadvisor.com'
        ]
        
        if any(skip in domain for skip in skip_domains):
            return False
        
        # Quick content check
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                content = response.text.lower()
                business_keywords = query.lower().replace('"', '').split()
                
                # Check if business name appears in content
                keyword_matches = sum(1 for keyword in business_keywords if keyword in content)
                return keyword_matches >= len(business_keywords) * 0.5
        except:
            pass
        
        return True  # Default to true for initial screening
        
    except Exception:
        return False

def find_social_media_profiles(business_name: str, address: str = "") -> List[Dict[str, str]]:
    """
    Find social media profiles for a business.
    
    Args:
        business_name: Name of the business
        address: Business address
    
    Returns:
        List of social media profile dictionaries
    """
    profiles = []
    
    try:
        # Search for social media profiles
        for platform in ['facebook', 'instagram', 'linkedin']:
            query = f'"{business_name}" site:{platform}.com'
            if address:
                city = address.split(',')[0].strip()
                query += f" {city}"
            
            profile_url = search_social_media_profile(platform, query)
            if profile_url:
                profiles.append({
                    'platform': platform,
                    'url': profile_url,
                    'confidence': 70
                })
        
    except Exception as e:
        logger.error(f"Error finding social media profiles: {e}")
    
    return profiles

def search_social_media_profile(platform: str, query: str) -> Optional[str]:
    """
    Search for specific social media profile.
    
    Args:
        platform: Social media platform name
        query: Search query
    
    Returns:
        Profile URL if found, None otherwise
    """
    try:
        # This is a simplified implementation
        # In production, use proper social media APIs
        search_url = f"https://www.google.com/search?q={query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        # Look for social media URLs in results
        pattern = f'https?://(www\.)?{platform}\.com/[^\s<>"{{}}|\\\\^`\[\]]+'
        matches = re.findall(pattern, response.text)
        
        if matches:
            return f"https://{platform}.com/" + matches[0].split('/')[-1]
        
        return None
        
    except Exception as e:
        logger.error(f"Error searching {platform} profile: {e}")
        return None

def extract_website_from_social_profile(profile_url: str) -> Optional[str]:
    """
    Extract website URL from social media profile.
    
    Args:
        profile_url: Social media profile URL
    
    Returns:
        Website URL if found, None otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(profile_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for website links in common places
        selectors = [
            'a[href*="http"]',
            '[data-testid="website"]',
            '.website',
            '.link',
            '.bio a'
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href', '')
                if href and validate_website_url(href):
                    return href
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting website from social profile: {e}")
        return None

def search_website_by_phone(phone: str) -> Optional[str]:
    """
    Search for website using phone number.
    
    Args:
        phone: Phone number to search
    
    Returns:
        Website URL if found, None otherwise
    """
    try:
        cleaned_phone = clean_phone_number(phone)
        if not cleaned_phone:
            return None
        
        # Search with phone number
        query = f'"{cleaned_phone}"'
        website = perform_web_search(query)
        
        if website and validate_website_url(website):
            return website
        
        return None
        
    except Exception as e:
        logger.error(f"Error searching website by phone: {e}")
        return None

def predict_business_domains(business_name: str) -> List[str]:
    """
    Predict possible domain names for a business.
    
    Args:
        business_name: Name of the business
    
    Returns:
        List of predicted domain names
    """
    domains = []
    
    try:
        # Clean business name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', business_name.lower())
        words = clean_name.split()
        
        if not words:
            return domains
        
        # Common domain patterns
        base_name = ''.join(words)
        first_word = words[0]
        
        # Common TLDs to try
        tlds = ['.com', '.ma', '.org', '.net']
        
        patterns = [
            base_name,
            first_word,
            '-'.join(words),
            f"{first_word}morocco",
            f"{base_name}ma"
        ]
        
        for pattern in patterns:
            for tld in tlds:
                domains.append(f"{pattern}{tld}")
        
    except Exception as e:
        logger.error(f"Error predicting domains: {e}")
    
    return domains[:10]  # Limit to top 10 predictions

def check_domain_exists(domain: str) -> bool:
    """
    Check if a domain exists and is accessible.
    
    Args:
        domain: Domain name to check
    
    Returns:
        True if domain exists, False otherwise
    """
    try:
        # Check DNS resolution
        socket.gethostbyname(domain)
        
        # Check HTTP accessibility
        for protocol in ['https', 'http']:
            try:
                url = f"{protocol}://{domain}"
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    return True
            except:
                continue
        
        return False
        
    except Exception:
        return False

def analyze_website_quality(website_url: str) -> int:
    """
    Analyze website quality and return a score.
    
    Args:
        website_url: Website URL to analyze
    
    Returns:
        Quality score (0-100)
    """
    score = 0
    
    try:
        response = requests.get(website_url, timeout=10)
        response.raise_for_status()
        
        # Basic accessibility (20 points)
        score += 20
        
        # SSL certificate (20 points)
        if website_url.startswith('https://'):
            score += 20
        
        # Content analysis
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Has title (10 points)
        if soup.find('title'):
            score += 10
        
        # Has contact information (20 points)
        content = soup.get_text().lower()
        contact_keywords = ['contact', 'phone', 'email', 'address']
        if any(keyword in content for keyword in contact_keywords):
            score += 20
        
        # Has navigation (10 points)
        if soup.find(['nav', 'menu']) or soup.find_all('a', href=True):
            score += 10
        
        # Mobile responsive indicators (10 points)
        if soup.find('meta', attrs={'name': 'viewport'}):
            score += 10
        
        # Has images (10 points)
        if soup.find_all('img'):
            score += 10
        
    except Exception as e:
        logger.error(f"Error analyzing website quality: {e}")
        score = 0
    
    return min(score, 100)

def bulk_website_check(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Perform bulk website checking for multiple businesses.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        List of business dictionaries with website status
    """
    results = []
    
    for i, business in enumerate(businesses):
        try:
            logger.info(f"Checking website for business {i+1}/{len(businesses)}: {business.get('name', 'Unknown')}")
            
            website_status = check_website_status(business)
            business.update(website_status)
            results.append(business)
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error checking business {i}: {e}")
            business.update({
                'has_website': False,
                'website_url': None,
                'website_quality_score': 0,
                'social_media_profiles': [],
                'detection_method': 'error',
                'confidence_score': 0
            })
            results.append(business)
    
    return results

# Legacy function for backward compatibility
def check_business_website(business_name: str, phone: str = None) -> Optional[str]:
    """
    Legacy function for backward compatibility.
    
    Args:
        business_name: Name of the business
        phone: Business phone number
    
    Returns:
        Website URL if found, None otherwise
    """
    business_data = {
        'name': business_name,
        'phone': phone or '',
        'address': ''
    }
    
    result = check_website_status(business_data)
    return result.get('website_url')
