"""
Enhanced Configuration Management for Business Lead Finder (Functional Approach)
Centralized configuration with validation and environment support.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_search_config() -> Dict[str, Any]:
    """Get search configuration parameters."""
    return {
        'default_location': os.getenv('DEFAULT_LOCATION', 'Marrakesh, Morocco'),
        'max_results_per_search': int(os.getenv('MAX_RESULTS_PER_SEARCH', '50')),
        'delay_between_requests': float(os.getenv('DELAY_BETWEEN_REQUESTS', '1.0')),
        'request_timeout': int(os.getenv('REQUEST_TIMEOUT', '30')),
        'max_retries': int(os.getenv('MAX_RETRIES', '3')),
        'enable_caching': os.getenv('ENABLE_CACHING', 'true').lower() == 'true',
        'cache_duration_hours': int(os.getenv('CACHE_DURATION_HOURS', '24'))
    }

def get_api_config() -> Dict[str, Any]:
    """Get API configuration and keys."""
    return {
        'serpapi_key': os.getenv('SERPAPI_API_KEY'),
        'google_places_key': os.getenv('GOOGLE_PLACES_API_KEY'),
        'yelp_api_key': os.getenv('YELP_API_KEY'),
        'foursquare_client_id': os.getenv('FOURSQUARE_CLIENT_ID'),
        'foursquare_client_secret': os.getenv('FOURSQUARE_CLIENT_SECRET'),
        'groq_api_key': os.getenv('GROQ_API_KEY'),
        
        # Rate limits
        'serpapi_daily_limit': int(os.getenv('SERPAPI_DAILY_LIMIT', '100')),
        'foursquare_daily_limit': int(os.getenv('FOURSQUARE_DAILY_LIMIT', '950')),
        'google_places_daily_limit': int(os.getenv('GOOGLE_PLACES_DAILY_LIMIT', '1000'))
    }

def get_output_config() -> Dict[str, Any]:
    """Get output and reporting configuration."""
    return {
        'results_dir': os.getenv('RESULTS_DIR', 'results'),
        'logs_dir': os.getenv('LOGS_DIR', 'logs'),
        'reports_dir': os.getenv('REPORTS_DIR', 'reports'),
        'default_format': os.getenv('DEFAULT_FORMAT', 'json'),
        'create_html_reports': os.getenv('CREATE_HTML_REPORTS', 'true').lower() == 'true',
        'create_csv_exports': os.getenv('CREATE_CSV_EXPORTS', 'true').lower() == 'true'
    }

def get_lead_scoring_config() -> Dict[str, Any]:
    """Get lead scoring configuration."""
    return {
        'no_website_score': int(os.getenv('NO_WEBSITE_SCORE', '40')),
        'phone_available_score': int(os.getenv('PHONE_AVAILABLE_SCORE', '25')),
        'email_available_score': int(os.getenv('EMAIL_AVAILABLE_SCORE', '20')),
        'high_rating_bonus': int(os.getenv('HIGH_RATING_BONUS', '10')),
        'low_rating_bonus': int(os.getenv('LOW_RATING_BONUS', '15')),
        'social_media_bonus': int(os.getenv('SOCIAL_MEDIA_BONUS', '5')),
        'min_score_threshold': int(os.getenv('MIN_SCORE_THRESHOLD', '30')),
        'high_score_threshold': int(os.getenv('HIGH_SCORE_THRESHOLD', '70'))
    }

def load_config_from_file(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        config_path = Path(config_file)
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_file}")
            return {}
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file {config_file}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading config file {config_file}: {e}")
        return {}

def save_config_to_file(config: Dict[str, Any], config_file: str) -> bool:
    """
    Save configuration to JSON file.
    
    Args:
        config: Configuration dictionary
        config_file: Path to save configuration
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Configuration saved to {config_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving config to {config_file}: {e}")
        return False

def get_full_config() -> Dict[str, Any]:
    """Get complete configuration combining all sections."""
    return {
        'search': get_search_config(),
        'api': get_api_config(),
        'output': get_output_config(),
        'lead_scoring': get_lead_scoring_config()
    }

def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate configuration and return list of issues.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of validation error messages
    """
    issues = []
    
    # Validate search config
    search_config = config.get('search', {})
    if search_config.get('max_results_per_search', 0) <= 0:
        issues.append("max_results_per_search must be positive")
    
    if search_config.get('delay_between_requests', 0) < 0:
        issues.append("delay_between_requests cannot be negative")
    
    if search_config.get('request_timeout', 0) <= 0:
        issues.append("request_timeout must be positive")
    
    # Validate API config
    api_config = config.get('api', {})
    if not any([
        api_config.get('serpapi_key'),
        api_config.get('google_places_key'),
        api_config.get('foursquare_client_id')
    ]):
        issues.append("At least one API key should be configured")
    
    # Validate output config
    output_config = config.get('output', {})
    for dir_key in ['results_dir', 'logs_dir', 'reports_dir']:
        if not output_config.get(dir_key):
            issues.append(f"{dir_key} cannot be empty")
    
    return issues

def setup_directories(config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Setup required directories based on configuration.
    
    Args:
        config: Configuration dictionary (uses default if None)
        
    Returns:
        True if successful, False otherwise
    """
    if config is None:
        config = get_full_config()
    
    try:
        output_config = config.get('output', {})
        
        # Create required directories
        directories = [
            output_config.get('results_dir', 'results'),
            output_config.get('logs_dir', 'logs'),
            output_config.get('reports_dir', 'reports')
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {directory}")
        
        # Create subdirectories for results
        results_dir = Path(output_config.get('results_dir', 'results'))
        (results_dir / 'cities').mkdir(exist_ok=True)
        (results_dir / 'sample_data').mkdir(exist_ok=True)
        (results_dir / 'tests').mkdir(exist_ok=True)
        
        return True
        
    except Exception as e:
        logger.error(f"Error setting up directories: {e}")
        return False

def get_api_key(service_name: str) -> Optional[str]:
    """
    Get API key for a specific service.
    
    Args:
        service_name: Name of the service (serpapi, google_places, etc.)
        
    Returns:
        API key if available, None otherwise
    """
    api_config = get_api_config()
    key_mapping = {
        'serpapi': 'serpapi_key',
        'google_places': 'google_places_key',
        'yelp': 'yelp_api_key',
        'foursquare': 'foursquare_client_id',
        'groq': 'groq_api_key'
    }
    
    key_name = key_mapping.get(service_name.lower())
    if key_name:
        return api_config.get(key_name)
    
    logger.warning(f"Unknown service name: {service_name}")
    return None

def is_api_available(service_name: str) -> bool:
    """
    Check if API key is available for a service.
    
    Args:
        service_name: Name of the service
        
    Returns:
        True if API key is available, False otherwise
    """
    return get_api_key(service_name) is not None

def get_rate_limit(service_name: str) -> int:
    """
    Get rate limit for a specific service.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Daily rate limit for the service
    """
    api_config = get_api_config()
    limit_mapping = {
        'serpapi': 'serpapi_daily_limit',
        'google_places': 'google_places_daily_limit',
        'foursquare': 'foursquare_daily_limit'
    }
    
    limit_name = limit_mapping.get(service_name.lower())
    if limit_name:
        return api_config.get(limit_name, 0)
    
    return 0

def log_config_status():
    """Log current configuration status."""
    config = get_full_config()
    api_config = config['api']
    
    logger.info("=== Configuration Status ===")
    logger.info(f"Default Location: {config['search']['default_location']}")
    logger.info(f"Max Results: {config['search']['max_results_per_search']}")
    logger.info(f"Results Directory: {config['output']['results_dir']}")
    
    # API availability
    apis = ['serpapi', 'google_places', 'foursquare', 'yelp', 'groq']
    available_apis = [api for api in apis if is_api_available(api)]
    logger.info(f"Available APIs: {', '.join(available_apis) if available_apis else 'None'}")
    
    # Validation
    issues = validate_config(config)
    if issues:
        logger.warning(f"Configuration issues: {', '.join(issues)}")
    else:
        logger.info("Configuration is valid")

# Initialize configuration on import
def init_config():
    """Initialize configuration and setup directories."""
    try:
        config = get_full_config()
        setup_directories(config)
        logger.debug("Configuration initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize configuration: {e}")
        return False

# Auto-initialize when module is imported
init_config()
