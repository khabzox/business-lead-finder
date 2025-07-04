"""
Real Data Sources
Implements robust data collection from multiple sources with fallbacks
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio
import aiohttp
from urllib.parse import urlencode, quote
import json
from datetime import datetime, timedelta

from ..core.config import config, API_CONFIG, SEARCH_CONFIG

logger = logging.getLogger(__name__)

@dataclass
class BusinessData:
    """Standardized business data structure"""
    name: str
    category: str = ""
    address: str = ""
    phone: str = ""
    website: str = ""
    rating: float = 0.0
    review_count: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    source: str = ""
    raw_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.raw_data is None:
            self.raw_data = {}

class DataSourceError(Exception):
    """Custom exception for data source errors"""
    pass

class RateLimiter:
    """Rate limiter for API calls"""
    def __init__(self, calls_per_second: float = 1.0):
        self.delay = 1.0 / calls_per_second
        self.last_call = 0.0
    
    async def wait(self):
        """Wait if necessary to respect rate limits"""
        now = time.time()
        time_since_last = now - self.last_call
        if time_since_last < self.delay:
            await asyncio.sleep(self.delay - time_since_last)
        self.last_call = time.time()

class FoursquareDataSource:
    """Foursquare Places API data source"""
    
    def __init__(self):
        self.api_key = API_CONFIG.foursquare_api_key
        self.base_url = "https://api.foursquare.com/v3/places"
        self.rate_limiter = RateLimiter(2.0)  # 2 calls per second
        
    def is_available(self) -> bool:
        """Check if this data source is available"""
        return bool(self.api_key)
    
    async def search_businesses(
        self, 
        query: str, 
        location: str, 
        limit: int = 50
    ) -> List[BusinessData]:
        """Search businesses using Foursquare API"""
        if not self.is_available():
            raise DataSourceError("Foursquare API key not configured")
        
        await self.rate_limiter.wait()
        
        params = {
            'query': query,
            'near': location,
            'limit': min(limit, 50),  # Foursquare limit
            'fields': 'name,categories,location,tel,website,rating,stats'
        }
        
        headers = {
            'Authorization': self.api_key,
            'Accept': 'application/json'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/search"
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_foursquare_response(data)
                    else:
                        error_text = await response.text()
                        logger.error(f"Foursquare API error {response.status}: {error_text}")
                        raise DataSourceError(f"Foursquare API error: {response.status}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"Foursquare connection error: {e}")
            raise DataSourceError(f"Foursquare connection error: {e}")
    
    def _parse_foursquare_response(self, data: Dict[str, Any]) -> List[BusinessData]:
        """Parse Foursquare API response into BusinessData objects"""
        businesses = []
        
        for place in data.get('results', []):
            try:
                # Extract location data
                location = place.get('location', {})
                address_parts = []
                if location.get('address'):
                    address_parts.append(location['address'])
                if location.get('locality'):
                    address_parts.append(location['locality'])
                if location.get('region'):
                    address_parts.append(location['region'])
                
                # Extract category
                categories = place.get('categories', [])
                category = categories[0].get('name', '') if categories else ''
                
                # Extract stats
                stats = place.get('stats', {})
                
                business = BusinessData(
                    name=place.get('name', ''),
                    category=category,
                    address=', '.join(address_parts),
                    phone=place.get('tel', ''),
                    website=place.get('website', ''),
                    rating=place.get('rating', 0.0),
                    review_count=stats.get('total_ratings', 0),
                    latitude=location.get('lat', 0.0),
                    longitude=location.get('lng', 0.0),
                    source='foursquare',
                    raw_data=place
                )
                
                businesses.append(business)
                
            except Exception as e:
                logger.warning(f"Error parsing Foursquare place data: {e}")
                continue
        
        logger.info(f"Parsed {len(businesses)} businesses from Foursquare")
        return businesses

class SerpApiDataSource:
    """Google Search results via SerpAPI"""
    
    def __init__(self):
        self.api_key = API_CONFIG.serp_api_key
        self.base_url = "https://serpapi.com/search"
        self.rate_limiter = RateLimiter(1.0)  # 1 call per second
    
    def is_available(self) -> bool:
        """Check if this data source is available"""
        return bool(self.api_key)
    
    async def search_businesses(
        self, 
        query: str, 
        location: str, 
        limit: int = 20
    ) -> List[BusinessData]:
        """Search businesses using Google Local results"""
        if not self.is_available():
            raise DataSourceError("SerpAPI key not configured")
        
        await self.rate_limiter.wait()
        
        params = {
            'engine': 'google_maps',
            'q': f"{query} {location}",
            'type': 'search',
            'api_key': self.api_key,
            'num': min(limit, 20)  # SerpAPI limit for maps
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_serpapi_response(data)
                    else:
                        error_text = await response.text()
                        logger.error(f"SerpAPI error {response.status}: {error_text}")
                        raise DataSourceError(f"SerpAPI error: {response.status}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"SerpAPI connection error: {e}")
            raise DataSourceError(f"SerpAPI connection error: {e}")
    
    def _parse_serpapi_response(self, data: Dict[str, Any]) -> List[BusinessData]:
        """Parse SerpAPI response into BusinessData objects"""
        businesses = []
        
        for place in data.get('local_results', []):
            try:
                business = BusinessData(
                    name=place.get('title', ''),
                    category=place.get('type', ''),
                    address=place.get('address', ''),
                    phone=place.get('phone', ''),
                    website=place.get('website', ''),
                    rating=float(place.get('rating', 0)),
                    review_count=int(place.get('reviews', 0)),
                    latitude=place.get('gps_coordinates', {}).get('latitude', 0.0),
                    longitude=place.get('gps_coordinates', {}).get('longitude', 0.0),
                    source='serpapi',
                    raw_data=place
                )
                
                businesses.append(business)
                
            except Exception as e:
                logger.warning(f"Error parsing SerpAPI place data: {e}")
                continue
        
        logger.info(f"Parsed {len(businesses)} businesses from SerpAPI")
        return businesses

class OpenStreetMapDataSource:
    """OpenStreetMap Nominatim API (free fallback)"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.rate_limiter = RateLimiter(0.5)  # 0.5 calls per second (conservative)
    
    def is_available(self) -> bool:
        """Always available (free service)"""
        return True
    
    async def search_businesses(
        self, 
        query: str, 
        location: str, 
        limit: int = 10
    ) -> List[BusinessData]:
        """Search businesses using Nominatim"""
        await self.rate_limiter.wait()
        
        params = {
            'q': f"{query} in {location}",
            'format': 'json',
            'limit': min(limit, 10),
            'addressdetails': 1,
            'extratags': 1,
            'namedetails': 1
        }
        
        headers = {
            'User-Agent': 'BusinessLeadFinder/1.0 (Educational Use)'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_nominatim_response(data)
                    else:
                        error_text = await response.text()
                        logger.error(f"Nominatim error {response.status}: {error_text}")
                        raise DataSourceError(f"Nominatim error: {response.status}")
                        
        except aiohttp.ClientError as e:
            logger.error(f"Nominatim connection error: {e}")
            raise DataSourceError(f"Nominatim connection error: {e}")
    
    def _parse_nominatim_response(self, data: List[Dict[str, Any]]) -> List[BusinessData]:
        """Parse Nominatim response into BusinessData objects"""
        businesses = []
        
        for place in data:
            try:
                # Extract name
                name = place.get('display_name', '').split(',')[0]
                if not name:
                    name = place.get('name', 'Unknown Business')
                
                # Extract address
                address_parts = []
                address = place.get('address', {})
                for key in ['house_number', 'road', 'neighbourhood', 'city']:
                    if address.get(key):
                        address_parts.append(address[key])
                
                business = BusinessData(
                    name=name,
                    category=place.get('type', ''),
                    address=', '.join(address_parts) if address_parts else place.get('display_name', ''),
                    phone=place.get('extratags', {}).get('phone', ''),
                    website=place.get('extratags', {}).get('website', ''),
                    rating=0.0,  # Not available in Nominatim
                    review_count=0,  # Not available in Nominatim
                    latitude=float(place.get('lat', 0)),
                    longitude=float(place.get('lon', 0)),
                    source='nominatim',
                    raw_data=place
                )
                
                businesses.append(business)
                
            except Exception as e:
                logger.warning(f"Error parsing Nominatim place data: {e}")
                continue
        
        logger.info(f"Parsed {len(businesses)} businesses from Nominatim")
        return businesses

class RealDataCollector:
    """Main data collector that manages multiple sources"""
    
    def __init__(self):
        self.sources = [
            FoursquareDataSource(),
            SerpApiDataSource(),
            OpenStreetMapDataSource()
        ]
        self.cache = {}
        self.cache_ttl = timedelta(hours=1)  # Cache for 1 hour
    
    def get_available_sources(self) -> List[str]:
        """Get list of available data sources"""
        return [
            source.__class__.__name__ 
            for source in self.sources 
            if source.is_available()
        ]
    
    async def collect_business_data(
        self, 
        query: str, 
        location: str, 
        max_results: int = 50
    ) -> List[BusinessData]:
        """Collect business data from all available sources"""
        
        # Check cache first
        cache_key = f"{query}_{location}_{max_results}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                logger.info(f"Using cached data for {cache_key}")
                return cached_data
        
        all_businesses = []
        results_per_source = max(max_results // len(self.sources), 10)
        
        for source in self.sources:
            if not source.is_available():
                logger.warning(f"Skipping {source.__class__.__name__} - not available")
                continue
            
            try:
                logger.info(f"Collecting data from {source.__class__.__name__}")
                businesses = await source.search_businesses(query, location, results_per_source)
                all_businesses.extend(businesses)
                
                # Add delay between sources
                await asyncio.sleep(1)
                
            except DataSourceError as e:
                logger.error(f"Error from {source.__class__.__name__}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error from {source.__class__.__name__}: {e}")
                continue
        
        # Remove duplicates
        unique_businesses = self._deduplicate_businesses(all_businesses)
        
        # Cache results
        self.cache[cache_key] = (unique_businesses, datetime.now())
        
        logger.info(f"Collected {len(unique_businesses)} unique businesses")
        return unique_businesses[:max_results]
    
    def _deduplicate_businesses(self, businesses: List[BusinessData]) -> List[BusinessData]:
        """Remove duplicate businesses based on name and location similarity"""
        unique_businesses = []
        seen_names = set()
        
        for business in businesses:
            # Create a normalized key for comparison
            name_key = business.name.lower().strip()
            name_key = ''.join(c for c in name_key if c.isalnum())
            
            if name_key not in seen_names and name_key:
                unique_businesses.append(business)
                seen_names.add(name_key)
        
        return unique_businesses

# Global instance
real_data_collector = RealDataCollector()
