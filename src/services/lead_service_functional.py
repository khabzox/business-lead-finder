"""
Business Lead Service (Functional Approach)
High-level service for business lead generation and analysis
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime
from pathlib import Path

try:
    from ..data.real_sources import collect_business_data
    from ..config.config_manager import get_search_config, get_lead_scoring_config
    from ..website_checker import enhanced_website_detection
    from ..business_search import calculate_lead_score
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from data.real_sources import collect_business_data
    from config.config_manager import get_search_config, get_lead_scoring_config
    from website_checker import enhanced_website_detection
    from business_search import calculate_lead_score

logger = logging.getLogger(__name__)

def create_lead_analysis_result(
    businesses: List[Dict[str, Any]], 
    total_found: int,
    high_priority_count: int,
    no_website_count: int,
    avg_rating: float,
    sources_used: List[str]
) -> Dict[str, Any]:
    """Create lead analysis result dictionary."""
    return {
        'businesses': businesses,
        'total_found': total_found,
        'high_priority_count': high_priority_count,
        'no_website_count': no_website_count,
        'avg_rating': avg_rating,
        'sources_used': sources_used,
        'timestamp': datetime.now().isoformat()
    }

async def search_business_leads(
    category: str, 
    location: Optional[str] = None,
    max_results: Optional[int] = None,
    enhance_with_website_check: bool = True
) -> Dict[str, Any]:
    """
    Search for business leads with full analysis
    
    Args:
        category: Business category to search
        location: Location to search (uses default if None)
        max_results: Maximum results (uses default if None)
        enhance_with_website_check: Whether to check websites
        
    Returns:
        Lead analysis result dictionary
    """
    # Get configuration
    search_config = get_search_config()
    
    # Use defaults if not provided
    if location is None:
        location = search_config['default_location']
    if max_results is None:
        max_results = search_config['max_results_per_search']
    
    logger.info(f"Searching for {category} in {location} (max: {max_results})")
    
    # Collect raw business data
    businesses = await collect_business_data(
        query=category,
        location=location,
        max_results=max_results
    )
    
    if not businesses:
        logger.warning(f"No businesses found for {category} in {location}")
        return create_lead_analysis_result([], 0, 0, 0, 0.0, [])
    
    # Process and enhance business data
    processed_businesses = []
    sources_used = set()
    
    for business_data in businesses:
        # Convert to dictionary if needed
        if hasattr(business_data, 'to_dict'):
            business = business_data.to_dict()
        elif hasattr(business_data, '__dict__'):
            business = business_data.__dict__
        else:
            business = business_data
        
        # Track source
        if 'source' in business:
            sources_used.add(business['source'])
        
        # Enhance with website check if requested
        if enhance_with_website_check and not business.get('website'):
            website_result = await enhanced_website_detection(
                business_name=business.get('name', ''),
                phone_number=business.get('phone', ''),
                address=business.get('address', '')
            )
            if website_result:
                business['website'] = website_result.get('website', '')
                business['website_confidence'] = website_result.get('confidence', 0)
        
        # Calculate lead score
        business['lead_score'] = calculate_lead_score(business)
        
        processed_businesses.append(business)
    
    # Analyze results
    analysis = analyze_lead_results(processed_businesses)
    
    return create_lead_analysis_result(
        businesses=processed_businesses,
        total_found=len(processed_businesses),
        high_priority_count=analysis['high_priority_count'],
        no_website_count=analysis['no_website_count'],
        avg_rating=analysis['avg_rating'],
        sources_used=list(sources_used)
    )

def analyze_lead_results(businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze business lead results
    
    Args:
        businesses: List of business dictionaries
        
    Returns:
        Analysis results dictionary
    """
    if not businesses:
        return {
            'high_priority_count': 0,
            'no_website_count': 0,
            'avg_rating': 0.0,
            'total_with_phone': 0,
            'total_with_email': 0,
            'rating_distribution': {}
        }
    
    scoring_config = get_lead_scoring_config()
    high_score_threshold = scoring_config['high_score_threshold']
    
    # Count metrics
    high_priority_count = sum(1 for b in businesses if b.get('lead_score', 0) >= high_score_threshold)
    no_website_count = sum(1 for b in businesses if not b.get('website'))
    total_with_phone = sum(1 for b in businesses if b.get('phone'))
    total_with_email = sum(1 for b in businesses if b.get('email'))
    
    # Calculate average rating
    ratings = [b.get('rating', 0) for b in businesses if b.get('rating', 0) > 0]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
    
    # Rating distribution
    rating_distribution = {}
    for business in businesses:
        rating = business.get('rating', 0)
        if rating > 0:
            rating_range = f"{int(rating)}.0-{int(rating)}.9"
            rating_distribution[rating_range] = rating_distribution.get(rating_range, 0) + 1
    
    return {
        'high_priority_count': high_priority_count,
        'no_website_count': no_website_count,
        'avg_rating': round(avg_rating, 2),
        'total_with_phone': total_with_phone,
        'total_with_email': total_with_email,
        'rating_distribution': rating_distribution
    }

def filter_leads_by_criteria(
    businesses: List[Dict[str, Any]], 
    criteria: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filter business leads by specific criteria
    
    Args:
        businesses: List of business dictionaries
        criteria: Filter criteria dictionary
        
    Returns:
        Filtered list of businesses
    """
    filtered = []
    
    for business in businesses:
        # Check website criteria
        if 'no_website' in criteria and criteria['no_website']:
            if business.get('website'):
                continue
        
        # Check minimum rating
        if 'min_rating' in criteria:
            if business.get('rating', 0) < criteria['min_rating']:
                continue
        
        # Check maximum rating
        if 'max_rating' in criteria:
            if business.get('rating', 0) > criteria['max_rating']:
                continue
        
        # Check minimum lead score
        if 'min_lead_score' in criteria:
            if business.get('lead_score', 0) < criteria['min_lead_score']:
                continue
        
        # Check phone requirement
        if 'requires_phone' in criteria and criteria['requires_phone']:
            if not business.get('phone'):
                continue
        
        # Check email requirement
        if 'requires_email' in criteria and criteria['requires_email']:
            if not business.get('email'):
                continue
        
        # Check category filter
        if 'categories' in criteria:
            business_category = business.get('category', '').lower()
            if business_category not in [cat.lower() for cat in criteria['categories']]:
                continue
        
        filtered.append(business)
    
    return filtered

def sort_leads_by_priority(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort business leads by priority (lead score descending)
    
    Args:
        businesses: List of business dictionaries
        
    Returns:
        Sorted list of businesses
    """
    return sorted(businesses, key=lambda b: b.get('lead_score', 0), reverse=True)

def categorize_leads_by_quality(businesses: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize leads by quality levels
    
    Args:
        businesses: List of business dictionaries
        
    Returns:
        Dictionary with categorized businesses
    """
    scoring_config = get_lead_scoring_config()
    high_threshold = scoring_config['high_score_threshold']
    min_threshold = scoring_config['min_score_threshold']
    
    categorized = {
        'high_priority': [],
        'medium_priority': [],
        'low_priority': []
    }
    
    for business in businesses:
        score = business.get('lead_score', 0)
        
        if score >= high_threshold:
            categorized['high_priority'].append(business)
        elif score >= min_threshold:
            categorized['medium_priority'].append(business)
        else:
            categorized['low_priority'].append(business)
    
    return categorized

def export_leads_to_file(
    businesses: List[Dict[str, Any]], 
    filepath: str, 
    format_type: str = 'json'
) -> bool:
    """
    Export business leads to file
    
    Args:
        businesses: List of business dictionaries
        filepath: Output file path
        format_type: Export format ('json', 'csv')
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format_type.lower() == 'json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(businesses, f, indent=2, ensure_ascii=False, default=str)
        
        elif format_type.lower() == 'csv':
            import csv
            
            if not businesses:
                logger.warning("No businesses to export")
                return False
            
            # Get all possible fields
            all_fields = set()
            for business in businesses:
                all_fields.update(business.keys())
            
            fieldnames = sorted(list(all_fields))
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(businesses)
        
        else:
            logger.error(f"Unsupported export format: {format_type}")
            return False
        
        logger.info(f"Exported {len(businesses)} businesses to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to export leads to {filepath}: {e}")
        return False

def generate_lead_summary(analysis_result: Dict[str, Any]) -> str:
    """
    Generate a text summary of lead analysis results
    
    Args:
        analysis_result: Lead analysis result dictionary
        
    Returns:
        Formatted summary string
    """
    businesses = analysis_result.get('businesses', [])
    total_found = analysis_result.get('total_found', 0)
    high_priority = analysis_result.get('high_priority_count', 0)
    no_website = analysis_result.get('no_website_count', 0)
    avg_rating = analysis_result.get('avg_rating', 0.0)
    sources = analysis_result.get('sources_used', [])
    
    summary = f"""
🎯 Lead Analysis Summary
========================

📊 Total Businesses Found: {total_found}
🔥 High Priority Leads: {high_priority}
🌐 Businesses Without Websites: {no_website}
⭐ Average Rating: {avg_rating:.1f}
📡 Data Sources: {', '.join(sources) if sources else 'None'}

📈 Lead Quality Distribution:
"""
    
    if businesses:
        categorized = categorize_leads_by_quality(businesses)
        summary += f"""
  🚀 High Priority: {len(categorized['high_priority'])} businesses
  📈 Medium Priority: {len(categorized['medium_priority'])} businesses  
  📊 Low Priority: {len(categorized['low_priority'])} businesses
"""
    
    return summary

# Convenience functions for common operations
async def quick_lead_search(category: str, location: Optional[str] = None) -> Dict[str, Any]:
    """Quick lead search with default settings"""
    return await search_business_leads(category, location)

def get_top_leads(businesses: List[Dict[str, Any]], count: int = 10) -> List[Dict[str, Any]]:
    """Get top N leads by score"""
    sorted_businesses = sort_leads_by_priority(businesses)
    return sorted_businesses[:count]

def get_no_website_leads(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get only businesses without websites"""
    return filter_leads_by_criteria(businesses, {'no_website': True})
