"""
Google Maps Scraper - FREE Implementation (Functional Approach)
No credit card required, scrapes public business data from Google Maps
"""

import time
import random
import logging
import requests
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Global driver instance (to be managed functionally)
_current_driver = None

def setup_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """Setup Chrome driver with improved stability options"""
    global _current_driver
    
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        
    # Enhanced stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-css")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Memory optimization
    chrome_options.add_argument("--max_old_space_size=4096")
    chrome_options.add_argument("--memory-pressure-off")
    
    # Disable logging
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add prefs to disable images and other resources
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        # Try with ChromeDriverManager first
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
        except ImportError:
            # Fallback to system chromedriver
            logger.info("ChromeDriverManager not available, trying system chromedriver...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
        _current_driver = driver
        return driver
        
    except Exception as e:
        logger.error(f"Failed to setup Chrome driver: {e}")
        logger.info("Make sure Chrome and ChromeDriver are installed and in PATH")
        raise

def close_driver():
    """Close the current driver"""
    global _current_driver
    if _current_driver:
        try:
            _current_driver.quit()
        except:
            pass
        _current_driver = None

def random_delay(delay_range: tuple = (2, 4)) -> None:
    """Random delay between requests"""
    delay = random.uniform(delay_range[0], delay_range[1])
    time.sleep(delay)

def search_google_maps_business(query: str, location: str, max_results: int = 50, rating_filter: str = "low") -> List[Dict[str, Any]]:
    """
    Search for businesses on Google Maps
    
    Args:
        query: Business type (e.g., "restaurants", "hotels")
        location: Location to search (e.g., "Marrakesh, Morocco")
        max_results: Maximum number of results
        rating_filter: "low" (0-4.0 ratings), "high" (4.5+), "all"
    
    Returns:
        List of business dictionaries
    """
    driver = setup_chrome_driver(headless=True)
    businesses = []
    
    try:
        # Construct search URL
        search_query = f"{query} {location}"
        maps_url = f"https://www.google.com/maps/search/{quote(search_query)}"
        
        logger.info(f"Searching Google Maps for: {search_query}")
        driver.get(maps_url)
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-result-index]"))
        )
        
        # Scroll to load more results
        businesses = _scroll_and_extract_businesses(driver, max_results, rating_filter)
        
        logger.info(f"Found {len(businesses)} businesses after filtering")
        return businesses
        
    except Exception as e:
        logger.error(f"Google Maps search failed: {e}")
        return []
    finally:
        close_driver()

def _scroll_and_extract_businesses(driver, max_results: int, rating_filter: str) -> List[Dict[str, Any]]:
    """Scroll through results and extract business data"""
    businesses = []
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "[role='main']")
    
    # Scroll and collect results
    for scroll_attempt in range(10):  # Max 10 scrolls
        if len(businesses) >= max_results:
            break
            
        # Extract current businesses
        new_businesses = _extract_business_elements(driver, rating_filter)
        
        # Add new businesses (avoid duplicates)
        existing_names = {b['name'] for b in businesses}
        for business in new_businesses:
            if business['name'] not in existing_names and len(businesses) < max_results:
                businesses.append(business)
                
        # Scroll down
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)
        
        # Check if we can scroll more
        try:
            driver.find_element(By.CSS_SELECTOR, "[data-result-index]")
        except:
            break
            
    return businesses

def _extract_business_elements(driver, rating_filter: str) -> List[Dict[str, Any]]:
    """Extract business data from current page elements"""
    businesses = []
    
    try:
        # Find all business elements
        business_elements = driver.find_elements(By.CSS_SELECTOR, "[data-result-index]")
        
        for element in business_elements:
            try:
                business_data = _extract_single_business_data(element)
                if business_data and _passes_rating_filter(business_data, rating_filter):
                    businesses.append(business_data)
            except Exception as e:
                logger.debug(f"Failed to extract business data: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Failed to extract business elements: {e}")
        
    return businesses

def _extract_single_business_data(element) -> Optional[Dict[str, Any]]:
    """Extract data from a single business element"""
    try:
        # Extract business name
        name_element = element.find_element(By.CSS_SELECTOR, "[data-value='Name']")
        name = name_element.text.strip() if name_element else "N/A"
        
        # Extract rating
        rating = 0.0
        try:
            rating_element = element.find_element(By.CSS_SELECTOR, "[data-value='Rating']")
            rating_text = rating_element.text.strip()
            rating = float(rating_text.split()[0]) if rating_text else 0.0
        except:
            pass
            
        # Extract address
        address = "N/A"
        try:
            address_element = element.find_element(By.CSS_SELECTOR, "[data-value='Address']")
            address = address_element.text.strip() if address_element else "N/A"
        except:
            pass
            
        # Extract phone
        phone = ""
        try:
            phone_element = element.find_element(By.CSS_SELECTOR, "[data-value='Phone']")
            phone = phone_element.text.strip() if phone_element else ""
        except:
            pass
            
        # Extract website
        website = ""
        try:
            website_element = element.find_element(By.CSS_SELECTOR, "[data-value='Website']")
            website = website_element.get_attribute("href") if website_element else ""
        except:
            pass
            
        # Extract category
        category = "N/A"
        try:
            category_element = element.find_element(By.CSS_SELECTOR, "[data-value='Category']")
            category = category_element.text.strip() if category_element else "N/A"
        except:
            pass
            
        # Calculate lead score
        lead_score = calculate_lead_score(name, phone, website, rating)
        
        return {
            'name': name,
            'category': category,
            'address': address,
            'phone': phone,
            'email': generate_potential_email(name, phone, website),
            'emails': [generate_potential_email(name, phone, website)] if generate_potential_email(name, phone, website) else [],
            'website': website,
            'rating': rating,
            'review_count': 0,  # Would need additional scraping
            'social_media': {},
            'lead_score': lead_score,
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'google_maps'
        }
        
    except Exception as e:
        logger.debug(f"Failed to extract business data: {e}")
        return None

def _passes_rating_filter(business: Dict[str, Any], rating_filter: str) -> bool:
    """Check if business passes rating filter"""
    if rating_filter == "all":
        return True
    
    rating = business.get('rating', 0.0)
    has_website = bool(business.get('website'))
    
    if rating_filter == "low":
        # Show businesses with low ratings (likely no website) OR businesses without websites
        return rating <= 4.0 or not has_website
    elif rating_filter == "high":
        return rating >= 4.5
    
    return True

def calculate_lead_score(name: str, phone: str, website: str, rating: float) -> int:
    """Calculate lead score based on available data"""
    score = 0
    
    # Base score
    score += 20
    
    # Phone number available
    if phone:
        score += 25
    
    # No website (main criteria)
    if not website:
        score += 40
    
    # Rating considerations
    if rating > 0:
        if rating >= 4.5:
            score += 10
        elif rating >= 4.0:
            score += 5
        else:
            score += 15  # Lower ratings might indicate less web presence
    
    return min(score, 100)

def generate_potential_email(name: str, phone: str, website: str) -> str:
    """Generate potential email based on business data"""
    if website:
        # Extract domain from website
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', website)
        if domain_match:
            domain = domain_match.group(1)
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '', clean_name)
            return f"contact@{domain}"
    
    # Fallback: generate from name
    clean_name = re.sub(r'[^\w\s]', '', name.lower())
    clean_name = re.sub(r'\s+', '', clean_name)
    if clean_name:
        return f"{clean_name}@gmail.com"
    
    return ""

def scrape_google_maps_businesses(query: str, location: str, max_results: int = 50, headless: bool = True, rating_filter: str = "low") -> List[Dict[str, Any]]:
    """
    Main function to scrape Google Maps businesses
    
    Args:
        query: Business type
        location: Location to search
        max_results: Maximum results
        headless: Run browser headless
        rating_filter: Rating filter type
    
    Returns:
        List of business dictionaries
    """
    return search_google_maps_business(query, location, max_results, rating_filter)

# Test functions
def test_google_maps_search():
    """Test Google Maps search functionality"""
    try:
        print("Testing Google Maps search...")
        results = search_google_maps_business("restaurants", "Marrakesh, Morocco", max_results=5)
        
        print(f"Found {len(results)} businesses:")
        for i, business in enumerate(results, 1):
            print(f"{i}. {business['name']}")
            print(f"   Rating: {business['rating']}")
            print(f"   Phone: {business['phone']}")
            print(f"   Website: {business['website']}")
            print(f"   Lead Score: {business['lead_score']}")
            print(f"   Address: {business['address']}")
            print()
            
    except Exception as e:
        print(f"Test failed: {e}")

def test_rating_filter():
    """Test rating filter functionality"""
    try:
        print("Testing rating filter...")
        
        # Test low rating filter
        low_results = search_google_maps_business("restaurants", "Marrakesh, Morocco", max_results=3, rating_filter="low")
        print(f"Low rating filter: {len(low_results)} results")
        
        # Test high rating filter
        high_results = search_google_maps_business("restaurants", "Marrakesh, Morocco", max_results=3, rating_filter="high")
        print(f"High rating filter: {len(high_results)} results")
        
        # Test all filter
        all_results = search_google_maps_business("restaurants", "Marrakesh, Morocco", max_results=3, rating_filter="all")
        print(f"All filter: {len(all_results)} results")
        
    except Exception as e:
        print(f"Test failed: {e}")

def test_multiple_categories():
    """Test multiple business categories"""
    categories = ["restaurants", "hotels", "cafes"]
    
    for category in categories:
        try:
            print(f"Testing {category}...")
            results = search_google_maps_business(category, "Marrakesh, Morocco", max_results=2)
            print(f"Found {len(results)} {category}")
            
            for business in results:
                print(f"  - {business['name']} (Rating: {business['rating']})")
                
        except Exception as e:
            print(f"Test failed for {category}: {e}")

if __name__ == "__main__":
    test_google_maps_search()
