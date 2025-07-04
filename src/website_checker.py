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
        'confidence_score': 0,
        'potential_domains': []
    }
    
    business_name = business_data.get('name', '')
    phone = business_data.get('phone', '')
    address = business_data.get('address', '')
    existing_website = business_data.get('website', '')
    
    # Method 1: Check existing website URL if provided
    if existing_website:
        website_info = validate_website_url(existing_website)
        if website_info['is_valid']:
            result['has_website'] = True
            result['website_url'] = existing_website
            result['website_quality_score'] = website_info['quality_score']
            result['detection_method'] = 'provided_url'
            result['confidence_score'] = 95
            return result
    
    # Method 2: Generate and test potential domain names
    potential_domains = generate_potential_domains(business_name)
    result['potential_domains'] = potential_domains
    
    for domain in potential_domains:
        logger.info(f"Testing domain: {domain}")
        website_info = test_domain_availability(domain)
        if website_info['exists']:
            result['has_website'] = True
            result['website_url'] = website_info['url']
            result['website_quality_score'] = website_info['quality_score']
            result['detection_method'] = 'domain_guessing'
            result['confidence_score'] = website_info['confidence']
            break
    
    # Method 3: Google search for business website
    if not result['has_website']:
        google_result = search_business_website(business_name, address)
        if google_result['found']:
            result['has_website'] = True
            result['website_url'] = google_result['url']
            result['website_quality_score'] = google_result['quality_score']
            result['detection_method'] = 'google_search'
            result['confidence_score'] = google_result['confidence']
    
    # Method 4: Check for social media presence
    social_profiles = find_social_media_profiles(business_name)
    result['social_media_profiles'] = social_profiles
    
    # If no website but has social media, adjust confidence
    if not result['has_website'] and social_profiles:
        result['confidence_score'] = 90  # High confidence they don't have website
    elif not result['has_website']:
        result['confidence_score'] = 85  # Medium-high confidence
    
    return result
    
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

def generate_potential_domains(business_name: str) -> List[str]:
    """
    Generate potential domain names for a business.
    
    Args:
        business_name: Name of the business
        
    Returns:
        List of potential domain names
    """
    if not business_name:
        return []
    
    # Clean business name
    clean_name = clean_business_name_for_domain(business_name)
    
    # Generate variations
    domains = []
    
    # Common TLDs for Morocco
    tlds = ['.com', '.ma', '.org', '.net', '.fr', '.es']
    
    # Generate different name variations
    name_variations = [
        clean_name,
        clean_name.replace(' ', ''),
        clean_name.replace(' ', '-'),
        clean_name.replace(' ', '_'),
        clean_name.split()[0] if ' ' in clean_name else clean_name,  # First word only
    ]
    
    # Add common business prefixes/suffixes
    business_prefixes = ['', 'restaurant', 'cafe', 'hotel', 'spa', 'shop']
    business_suffixes = ['', 'marrakesh', 'morocco', 'marrakech']
    
    for variation in name_variations:
        if len(variation) < 3:  # Skip very short names
            continue
            
        for tld in tlds:
            # Basic domain
            domains.append(f"{variation}{tld}")
            
            # With common prefixes
            for prefix in business_prefixes:
                if prefix and prefix.lower() not in variation.lower():
                    domains.append(f"{prefix}{variation}{tld}")
                    domains.append(f"{prefix}-{variation}{tld}")
            
            # With common suffixes
            for suffix in business_suffixes:
                if suffix and suffix.lower() not in variation.lower():
                    domains.append(f"{variation}{suffix}{tld}")
                    domains.append(f"{variation}-{suffix}{tld}")
    
    # Remove duplicates and sort by likelihood
    unique_domains = list(set(domains))
    
    # Prioritize .com and .ma domains
    prioritized_domains = []
    for domain in unique_domains:
        if domain.endswith('.com'):
            prioritized_domains.insert(0, domain)
        elif domain.endswith('.ma'):
            prioritized_domains.insert(1 if prioritized_domains and prioritized_domains[0].endswith('.com') else 0, domain)
        else:
            prioritized_domains.append(domain)
    
    return prioritized_domains[:20]  # Return top 20 most likely domains

def clean_business_name_for_domain(name: str) -> str:
    """Clean business name for domain generation."""
    # Convert to lowercase
    clean = name.lower()
    
    # Remove common business words
    business_words = [
        'restaurant', 'cafe', 'hotel', 'spa', 'shop', 'store', 'boutique',
        'riad', 'dar', 'chez', 'le', 'la', 'les', 'du', 'de', 'des',
        'et', 'and', '&', 'ltd', 'sarl', 'sas'
    ]
    
    for word in business_words:
        clean = re.sub(r'\b' + re.escape(word) + r'\b', '', clean)
    
    # Remove special characters except spaces and hyphens
    clean = re.sub(r'[^\w\s-]', '', clean)
    
    # Remove extra whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean

def test_domain_availability(domain: str) -> Dict[str, Any]:
    """
    Test if a domain exists and has a website.
    
    Args:
        domain: Domain name to test
        
    Returns:
        Dictionary with domain test results
    """
    result = {
        'exists': False,
        'url': None,
        'quality_score': 0,
        'confidence': 0,
        'response_time': 0,
        'status_code': None
    }
    
    # Test both HTTP and HTTPS
    protocols = ['https://', 'http://']
    
    for protocol in protocols:
        test_url = f"{protocol}{domain}"
        
        try:
            start_time = time.time()
            response = requests.get(
                test_url,
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                allow_redirects=True
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result['exists'] = True
                result['url'] = test_url
                result['status_code'] = response.status_code
                result['response_time'] = response_time
                
                # Analyze website quality
                quality_info = analyze_website_quality(response.text, test_url)
                result['quality_score'] = quality_info['score']
                result['confidence'] = quality_info['confidence']
                
                logger.info(f"Found website: {test_url} (Quality: {quality_info['score']}/100)")
                return result
            
        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to connect to {test_url}: {e}")
            continue
        
        # Add delay between requests
        time.sleep(0.5)
    
    return result

def search_business_website(business_name: str, address: str = '') -> Dict[str, Any]:
    """
    Search for business website using various methods.
    
    Args:
        business_name: Name of the business
        address: Business address for context
        
    Returns:
        Dictionary with search results
    """
    result = {
        'found': False,
        'url': None,
        'quality_score': 0,
        'confidence': 0,
        'method': None
    }
    
    # This is a placeholder for more advanced search methods
    # In a real implementation, you could use:
    # - Google Custom Search API
    # - Bing Search API
    # - DuckDuckGo search
    # - Social media APIs
    
    logger.info(f"Searching web for: {business_name}")
    
    # For now, return not found
    return result

def find_social_media_profiles(business_name: str) -> List[Dict[str, str]]:
    """
    Find social media profiles for a business.
    
    Args:
        business_name: Name of the business
        
    Returns:
        List of social media profiles found
    """
    profiles = []
    
    # This is a placeholder for social media detection
    # In a real implementation, you could check:
    # - Facebook API
    # - Instagram API
    # - Google My Business
    # - LinkedIn API
    
    logger.info(f"Searching social media for: {business_name}")
    
    return profiles

def analyze_website_quality(html_content: str, url: str) -> Dict[str, Any]:
    """
    Analyze website quality and determine if it's a legitimate business website.
    
    Args:
        html_content: HTML content of the website
        url: Website URL
        
    Returns:
        Quality analysis results
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        score = 0
        confidence = 0
        
        # Check for basic website structure
        if soup.find('title'):
            score += 20
        
        # Check for business-relevant content
        business_indicators = [
            'menu', 'contact', 'about', 'reservation', 'booking',
            'location', 'hours', 'services', 'gallery', 'restaurant',
            'hotel', 'cafe', 'spa'
        ]
        
        text_content = soup.get_text().lower()
        
        for indicator in business_indicators:
            if indicator in text_content:
                score += 5
        
        # Check for contact information
        if re.search(r'\+212\d{9}', text_content):  # Moroccan phone number
            score += 15
        
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_content):  # Email
            score += 10
        
        # Check for address/location
        morocco_locations = ['marrakesh', 'marrakech', 'rabat', 'casablanca', 'fez', 'morocco', 'maroc']
        if any(location in text_content for location in morocco_locations):
            score += 10
        
        # Check for images
        if soup.find_all('img'):
            score += 5
        
        # Penalize if it looks like a parking/placeholder page
        if any(word in text_content for word in ['domain', 'parking', 'for sale', 'coming soon']):
            score -= 30
        
        # Set confidence based on score
        if score >= 70:
            confidence = 95
        elif score >= 50:
            confidence = 85
        elif score >= 30:
            confidence = 70
        else:
            confidence = 50
        
        return {
            'score': max(0, min(100, score)),
            'confidence': confidence,
            'has_contact_info': score >= 25,
            'appears_legitimate': score >= 40
        }
        
    except Exception as e:
        logger.error(f"Error analyzing website quality: {e}")
        return {
            'score': 0,
            'confidence': 0,
            'has_contact_info': False,
            'appears_legitimate': False
        }

def validate_website_url(url: str) -> Dict[str, Any]:
    """
    Validate a website URL and check its quality.
    
    Args:
        url: URL to validate
        
    Returns:
        Validation results
    """
    result = {
        'is_valid': False,
        'quality_score': 0,
        'final_url': url,
        'status_code': None
    }
    
    try:
        # Clean and format URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(
            url,
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            allow_redirects=True
        )
        
        if response.status_code == 200:
            result['is_valid'] = True
            result['status_code'] = response.status_code
            result['final_url'] = response.url
            
            # Analyze quality
            quality_info = analyze_website_quality(response.text, response.url)
            result['quality_score'] = quality_info['score']
        
    except Exception as e:
        logger.debug(f"URL validation failed for {url}: {e}")
    
    return result

def is_valid_website_url(url: str) -> bool:
    """Check if URL is a valid website URL."""
    if not url:
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def ai_generate_domain_variations(business_name: str, category: str = '', client: Optional[Any] = None) -> List[str]:
    """
    Use AI to generate realistic domain variations for a business.
    
    Args:
        business_name: Business name
        category: Business category (restaurant, cafe, etc.)
        client: Groq AI client
    
    Returns:
        List of possible domain variations
    """
    try:
        if not client:
            try:
                from ai_assistant import initialize_groq_client
                client = initialize_groq_client()
            except ImportError:
                logger.warning("AI assistant module not available, using fallback")
                return generate_fallback_domains(business_name, category)
        
        if not client:
            logger.warning("AI client not available, using fallback domain generation")
            return generate_fallback_domains(business_name, category)
        
        # Create prompt for AI domain generation
        prompt = f"""
        Generate 5 realistic domain variations for this business:
        Business Name: "{business_name}"
        Category: "{category}"
        
        Rules for domain generation:
        1. Remove spaces, accents, and special characters
        2. Use only letters and numbers
        3. Keep it short and memorable
        4. Common patterns: businessname.com, businessnamecategory.com, categorybusinessname.com
        5. No underscores, spaces, or special characters in domain
        6. Convert accented characters (é→e, à→a, etc.)
        
        Examples:
        - "Café Argana" → "cafeargana.com", "argana.com", "restaurantargana.com"
        - "Restaurant Atlas" → "restaurantatlas.com", "atlas.com", "atlasrestaurant.com"
        
        Return ONLY the domain names (without http/https), one per line, no explanations.
        """
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        # Parse AI response
        ai_domains = []
        for line in response.choices[0].message.content.strip().split('\n'):
            domain = line.strip()
            if domain and '.' in domain and len(domain) < 50:
                # Clean domain further
                domain = clean_domain_name(domain)
                if domain:
                    ai_domains.append(domain)
        
        # Add some manual variations as backup
        fallback_domains = generate_fallback_domains(business_name, category)
        
        # Combine and deduplicate
        all_domains = list(set(ai_domains + fallback_domains))
        
        logger.info(f"Generated {len(all_domains)} domain variations for '{business_name}'")
        return all_domains[:8]  # Return max 8 domains to check
    
    except Exception as e:
        logger.error(f"AI domain generation failed: {e}")
        return generate_fallback_domains(business_name, category)

def clean_domain_name(domain: str) -> str:
    """Clean and validate domain name."""
    import re
    import unicodedata
    
    try:
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
        
        # Normalize unicode characters (é → e, à → a, etc.)
        domain = unicodedata.normalize('NFD', domain)
        domain = domain.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase
        domain = domain.lower()
        
        # Remove all non-alphanumeric except dots
        domain = re.sub(r'[^a-z0-9.]', '', domain)
        
        # Ensure it has a valid TLD
        if '.' not in domain:
            domain += '.com'
        elif domain.endswith('.'):
            domain += 'com'
        
        # Validate domain format
        if re.match(r'^[a-z0-9]+\.[a-z]{2,}$', domain) and len(domain) > 4:
            return domain
        
        return None
    
    except Exception as e:
        logger.error(f"Error cleaning domain '{domain}': {e}")
        return None

def generate_fallback_domains(business_name: str, category: str = '') -> List[str]:
    """Generate fallback domain variations when AI is not available."""
    import re
    import unicodedata
    
    # Normalize and clean business name
    clean_name = unicodedata.normalize('NFD', business_name.lower())
    clean_name = clean_name.encode('ascii', 'ignore').decode('ascii')
    clean_name = re.sub(r'[^a-z0-9]', '', clean_name)
    
    # Clean category
    clean_category = re.sub(r'[^a-z0-9]', '', category.lower()) if category else ''
    
    domains = []
    
    if clean_name:
        # Basic variations
        domains.extend([
            f"{clean_name}.com",
            f"{clean_name}.ma",  # Morocco TLD
            f"{clean_name}marrakech.com",
            f"{clean_name}morocco.com"
        ])
        
        # Category combinations
        if clean_category:
            domains.extend([
                f"{clean_category}{clean_name}.com",
                f"{clean_name}{clean_category}.com",
                f"{clean_category}{clean_name}.ma"
            ])
        
        # Common prefixes for Morocco
        domains.extend([
            f"restaurant{clean_name}.com",
            f"cafe{clean_name}.com",
            f"hotel{clean_name}.com",
            f"{clean_name}restaurant.com"
        ])
    
    return list(set(domains))

def enhanced_website_search(business_name: str, category: str = '', config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Enhanced website search using AI-generated domain variations.
    
    Args:
        business_name: Business name
        category: Business category
        config: Configuration dictionary
    
    Returns:
        Website search results with detailed information
    """
    logger.info(f"Starting enhanced website search for: {business_name}")
    
    result = {
        'business_name': business_name,
        'website_found': False,
        'website_url': '',
        'domains_checked': [],
        'working_domains': [],
        'quality_score': 0,
        'search_method': 'ai_enhanced',
        'details': {}
    }
    
    try:
        # Generate domain variations using AI
        try:
            from ai_assistant import initialize_groq_client
            client = initialize_groq_client()
        except ImportError:
            logger.warning("AI assistant not available, using fallback domain generation")
            client = None
        
        domain_variations = ai_generate_domain_variations(business_name, category, client)
        
        logger.info(f"Checking {len(domain_variations)} domain variations")
        
        working_domains = []
        
        # Check each domain variation
        for domain in domain_variations:
            result['domains_checked'].append(domain)
            
            # Check both HTTP and HTTPS
            for protocol in ['https://', 'http://']:
                full_url = f"{protocol}{domain}"
                
                try:
                    logger.debug(f"Checking: {full_url}")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    response = requests.get(full_url, headers=headers, timeout=10, allow_redirects=True)
                    
                    if response.status_code == 200:
                        # Check if it's a real website (not a parking page)
                        content = response.text.lower()
                        
                        # Look for signs it's a real business website
                        business_indicators = [
                            business_name.lower().replace(' ', ''),
                            'contact', 'menu', 'about', 'services',
                            'reservation', 'book', 'order'
                        ]
                        
                        parking_indicators = [
                            'domain for sale', 'parked domain', 'buy this domain',
                            'domain parking', 'coming soon', 'under construction'
                        ]
                        
                        business_score = sum(1 for indicator in business_indicators if indicator in content)
                        parking_score = sum(1 for indicator in parking_indicators if indicator in content)
                        
                        if business_score > parking_score and business_score > 0:
                            working_domains.append({
                                'url': full_url,
                                'status_code': response.status_code,
                                'business_score': business_score,
                                'content_length': len(content),
                                'title': extract_title_from_content(content)
                            })
                            
                            logger.info(f"✅ Found working website: {full_url}")
                
                except requests.exceptions.RequestException as e:
                    logger.debug(f"❌ Failed to connect to {full_url}: {e}")
                    continue
            
            # Rate limiting
            import time
            time.sleep(0.5)
        
        # Process results
        if working_domains:
            # Sort by business score (most relevant first)
            working_domains.sort(key=lambda x: x['business_score'], reverse=True)
            best_site = working_domains[0]
            
            result['website_found'] = True
            result['website_url'] = best_site['url']
            result['working_domains'] = working_domains
            result['quality_score'] = min(best_site['business_score'] * 20, 100)  # Score out of 100
            result['details'] = {
                'title': best_site.get('title', ''),
                'content_length': best_site['content_length'],
                'total_domains_found': len(working_domains)
            }
    
    except Exception as e:
        logger.error(f"Enhanced website search failed: {e}")
        result['details']['error'] = str(e)
    
    return result

def extract_title_from_content(content: str) -> str:
    """Extract title from HTML content."""
    try:
        import re
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
    except:
        pass
    return ''
