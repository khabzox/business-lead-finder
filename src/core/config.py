"""
Application Configuration
Central configuration management for Business Lead Finder
"""

import os
from pathlib import Path
from typing import Dict, Any
import json
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

@dataclass
class APIConfig:
    """API configuration settings"""
    foursquare_api_key: str = ""
    serp_api_key: str = ""
    groq_api_key: str = ""
    
    def is_valid(self) -> bool:
        """Check if API configuration is valid"""
        return bool(self.foursquare_api_key and self.serp_api_key)

@dataclass
class SearchConfig:
    """Search configuration settings"""
    default_location: str = "Marrakech, Morocco"
    max_results_per_source: int = 50
    timeout_seconds: int = 30
    rate_limit_delay: float = 1.0
    categories: list = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = [
                "restaurants", "cafes", "hotels", "riads", 
                "shops", "spas", "services", "boutiques"
            ]

@dataclass
class LeadScoringConfig:
    """Lead scoring configuration"""
    no_website_bonus: int = 30
    low_rating_bonus: int = 25  # For 2-3 star businesses
    few_reviews_bonus: int = 15  # For < 20 reviews
    phone_bonus: int = 10
    category_bonus: int = 15
    location_bonus: int = 5
    
    # Rating thresholds
    low_rating_min: float = 2.0
    low_rating_max: float = 3.5
    high_rating_threshold: float = 4.0
    
    # Review count thresholds
    few_reviews_threshold: int = 20
    many_reviews_threshold: int = 100

@dataclass
class AppConfig:
    """Main application configuration"""
    # Directories
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = None
    results_dir: Path = None
    logs_dir: Path = None
    cache_dir: Path = None
    
    # Sub-configurations
    api: APIConfig = None
    search: SearchConfig = None
    scoring: LeadScoringConfig = None
    
    def __post_init__(self):
        # Set up directories
        self.data_dir = self.project_root / "data"
        self.results_dir = self.project_root / "results"
        self.logs_dir = self.project_root / "logs"
        self.cache_dir = self.project_root / ".cache"
        
        # Create directories if they don't exist
        for directory in [self.data_dir, self.results_dir, self.logs_dir, self.cache_dir]:
            directory.mkdir(exist_ok=True)
        
        # Initialize sub-configurations
        if self.api is None:
            self.api = APIConfig(
                foursquare_api_key=os.getenv('FOURSQUARE_API_KEY', ''),
                serp_api_key=os.getenv('SERP_API_KEY', ''),
                groq_api_key=os.getenv('GROQ_API_KEY', '')
            )
        
        if self.search is None:
            self.search = SearchConfig()
        
        if self.scoring is None:
            self.scoring = LeadScoringConfig()

class ConfigManager:
    """Configuration manager for the application"""
    
    def __init__(self):
        self._config = AppConfig()
    
    @property
    def config(self) -> AppConfig:
        """Get the current configuration"""
        return self._config
    
    def validate_apis(self) -> Dict[str, bool]:
        """Validate API configurations"""
        return {
            'foursquare': bool(self._config.api.foursquare_api_key),
            'serp': bool(self._config.api.serp_api_key),
            'groq': bool(self._config.api.groq_api_key),
            'any_valid': self._config.api.is_valid()
        }
    
    def get_search_params(self, **overrides) -> Dict[str, Any]:
        """Get search parameters with optional overrides"""
        params = {
            'location': self._config.search.default_location,
            'max_results': self._config.search.max_results_per_source,
            'timeout': self._config.search.timeout_seconds,
            'categories': self._config.search.categories.copy()
        }
        params.update(overrides)
        return params
    
    def save_config(self, filepath: str = None):
        """Save current configuration to file"""
        if filepath is None:
            filepath = self._config.project_root / "config.json"
        
        config_dict = {
            'search': {
                'default_location': self._config.search.default_location,
                'max_results_per_source': self._config.search.max_results_per_source,
                'timeout_seconds': self._config.search.timeout_seconds,
                'rate_limit_delay': self._config.search.rate_limit_delay,
                'categories': self._config.search.categories
            },
            'scoring': {
                'no_website_bonus': self._config.scoring.no_website_bonus,
                'low_rating_bonus': self._config.scoring.low_rating_bonus,
                'few_reviews_bonus': self._config.scoring.few_reviews_bonus,
                'phone_bonus': self._config.scoring.phone_bonus,
                'category_bonus': self._config.scoring.category_bonus,
                'location_bonus': self._config.scoring.location_bonus,
                'low_rating_min': self._config.scoring.low_rating_min,
                'low_rating_max': self._config.scoring.low_rating_max,
                'high_rating_threshold': self._config.scoring.high_rating_threshold,
                'few_reviews_threshold': self._config.scoring.few_reviews_threshold,
                'many_reviews_threshold': self._config.scoring.many_reviews_threshold
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    def load_config(self, filepath: str = None):
        """Load configuration from file"""
        if filepath is None:
            filepath = self._config.project_root / "config.json"
        
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            # Update search config
            if 'search' in config_dict:
                search_data = config_dict['search']
                for key, value in search_data.items():
                    if hasattr(self._config.search, key):
                        setattr(self._config.search, key, value)
            
            # Update scoring config
            if 'scoring' in config_dict:
                scoring_data = config_dict['scoring']
                for key, value in scoring_data.items():
                    if hasattr(self._config.scoring, key):
                        setattr(self._config.scoring, key, value)
                        
        except Exception as e:
            print(f"Warning: Could not load config from {filepath}: {e}")

# Global configuration instance
config_manager = ConfigManager()
config = config_manager.config

# Convenience exports
API_CONFIG = config.api
SEARCH_CONFIG = config.search
SCORING_CONFIG = config.scoring
