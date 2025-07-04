"""
Data Processor Module
Handles data processing, export, and analysis functions.
"""

import json
import csv
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime

from utils import save_json_data, save_csv_data, get_business_summary_stats

logger = logging.getLogger(__name__)

def export_data(
    input_file: str,
    output_file: str,
    format: str,
    filter_criteria: Optional[str] = None,
    config: Dict[str, Any] = None
) -> bool:
    """
    Export business data to various formats.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output file
        format: Export format (csv, json, xlsx, vcf)
        filter_criteria: Optional filter string
        config: Configuration dictionary
    
    Returns:
        Success status
    """
    try:
        # Load data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            logger.warning("No data to export")
            return False
        
        # Apply filters if specified
        if filter_criteria:
            data = apply_filters(data, filter_criteria)
        
        # Create output directory
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Export based on format
        if format == 'csv':
            return export_to_csv(data, output_file)
        elif format == 'json':
            return export_to_json(data, output_file)
        elif format == 'xlsx':
            return export_to_excel(data, output_file)
        elif format == 'vcf':
            return export_to_vcf(data, output_file)
        else:
            logger.error(f"Unsupported export format: {format}")
            return False
    
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return False

def apply_filters(data: List[Dict[str, Any]], filter_criteria: str) -> List[Dict[str, Any]]:
    """Apply filter criteria to data."""
    filtered_data = []
    
    # Parse filter criteria (e.g., "no_website=true", "lead_score>=70")
    filters = {}
    for criterion in filter_criteria.split(','):
        if '=' in criterion:
            key, value = criterion.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle special cases
            if key == 'no_website' and value.lower() == 'true':
                filters['website_empty'] = True
            elif key == 'has_website' and value.lower() == 'true':
                filters['website_not_empty'] = True
            elif '>=' in criterion:
                key, value = criterion.split('>=', 1)
                filters[key.strip()] = ('>=', float(value.strip()))
            elif '<=' in criterion:
                key, value = criterion.split('<=', 1)
                filters[key.strip()] = ('<=', float(value.strip()))
            else:
                filters[key] = value
    
    # Apply filters
    for business in data:
        include = True
        
        for filter_key, filter_value in filters.items():
            if filter_key == 'website_empty':
                if business.get('website'):
                    include = False
                    break
            elif filter_key == 'website_not_empty':
                if not business.get('website'):
                    include = False
                    break
            elif isinstance(filter_value, tuple):
                operator, threshold = filter_value
                business_value = business.get(filter_key, 0)
                if operator == '>=' and business_value < threshold:
                    include = False
                    break
                elif operator == '<=' and business_value > threshold:
                    include = False
                    break
            else:
                if str(business.get(filter_key, '')).lower() != str(filter_value).lower():
                    include = False
                    break
        
        if include:
            filtered_data.append(business)
    
    logger.info(f"Filtered data: {len(filtered_data)} out of {len(data)} businesses")
    return filtered_data

def export_to_csv(data: List[Dict[str, Any]], output_file: str) -> bool:
    """Export data to CSV format."""
    try:
        if not data:
            return False
        
        # Flatten nested data for CSV
        flattened_data = []
        for business in data:
            flat_business = flatten_business_data(business)
            flattened_data.append(flat_business)
        
        return save_csv_data(flattened_data, output_file)
    
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        return False

def export_to_json(data: List[Dict[str, Any]], output_file: str) -> bool:
    """Export data to JSON format."""
    try:
        return save_json_data(data, output_file)
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}")
        return False

def export_to_excel(data: List[Dict[str, Any]], output_file: str) -> bool:
    """Export data to Excel format."""
    try:
        if not data:
            return False
        
        # Flatten data for Excel
        flattened_data = []
        for business in data:
            flat_business = flatten_business_data(business)
            flattened_data.append(flat_business)
        
        # Create DataFrame
        df = pd.DataFrame(flattened_data)
        
        # Export to Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        return True
    
    except Exception as e:
        logger.error(f"Error exporting to Excel: {e}")
        return False

def export_to_vcf(data: List[Dict[str, Any]], output_file: str) -> bool:
    """Export data to VCF (vCard) format for contacts."""
    try:
        vcf_content = []
        
        for business in data:
            vcf_entry = create_vcf_entry(business)
            if vcf_entry:
                vcf_content.append(vcf_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(vcf_content))
        
        return True
    
    except Exception as e:
        logger.error(f"Error exporting to VCF: {e}")
        return False

def flatten_business_data(business: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten nested business data for CSV/Excel export."""
    flat_data = {}
    
    # Basic fields
    flat_data['name'] = business.get('name', '')
    flat_data['category'] = business.get('category', '')
    flat_data['address'] = business.get('address', '')
    flat_data['phone'] = business.get('phone', '')
    flat_data['email'] = business.get('email', '')
    flat_data['website'] = business.get('website', '')
    flat_data['rating'] = business.get('rating', 0)
    flat_data['review_count'] = business.get('review_count', 0)
    flat_data['lead_score'] = business.get('lead_score', 0)
    flat_data['source'] = business.get('source', '')
    
    # Location data
    flat_data['latitude'] = business.get('lat', '')
    flat_data['longitude'] = business.get('lon', '')
    
    # Social media (flatten)
    social_media = business.get('social_media', {})
    flat_data['facebook'] = social_media.get('facebook', '')
    flat_data['instagram'] = social_media.get('instagram', '')
    flat_data['twitter'] = social_media.get('twitter', '')
    flat_data['linkedin'] = social_media.get('linkedin', '')
    
    # Additional fields
    flat_data['has_website'] = 'Yes' if business.get('website') else 'No'
    flat_data['opportunity_level'] = get_opportunity_level(business.get('lead_score', 0))
    flat_data['last_updated'] = business.get('last_updated', '')
    
    return flat_data

def create_vcf_entry(business: Dict[str, Any]) -> str:
    """Create VCF entry for a business."""
    try:
        name = business.get('name', '').replace(',', ' ')
        phone = business.get('phone', '')
        email = business.get('email', '')
        website = business.get('website', '')
        address = business.get('address', '').replace(',', ' ')
        
        vcf_lines = [
            'BEGIN:VCARD',
            'VERSION:3.0',
            f'FN:{name}',
            f'ORG:{name}',
        ]
        
        if phone:
            vcf_lines.append(f'TEL:{phone}')
        
        if email:
            vcf_lines.append(f'EMAIL:{email}')
        
        if website:
            vcf_lines.append(f'URL:{website}')
        
        if address:
            vcf_lines.append(f'ADR:;;{address}')
        
        # Add note with lead information
        lead_score = business.get('lead_score', 0)
        note = f"Lead Score: {lead_score}/100. Category: {business.get('category', 'Unknown')}"
        if not business.get('website'):
            note += ". NO WEBSITE - Opportunity!"
        vcf_lines.append(f'NOTE:{note}')
        
        vcf_lines.append('END:VCARD')
        
        return '\n'.join(vcf_lines)
    
    except Exception as e:
        logger.error(f"Error creating VCF entry for {business.get('name', 'unknown')}: {e}")
        return ''

def get_opportunity_level(lead_score: int) -> str:
    """Get opportunity level based on lead score."""
    if lead_score >= 80:
        return 'High'
    elif lead_score >= 60:
        return 'Medium'
    elif lead_score >= 40:
        return 'Low'
    else:
        return 'Very Low'

def analyze_leads(
    input_file: str,
    output_file: Optional[str] = None,
    metrics: Optional[List[str]] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze lead data and generate insights.
    
    Args:
        input_file: Path to input JSON file
        output_file: Optional path to save analysis
        metrics: Specific metrics to analyze
        config: Configuration dictionary
    
    Returns:
        Analysis results dictionary
    """
    try:
        # Load data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            logger.warning("No data to analyze")
            return {}
        
        # Perform analysis
        analysis = {
            'summary_stats': get_business_summary_stats(data),
            'category_analysis': analyze_by_category(data),
            'location_analysis': analyze_by_location(data),
            'lead_score_analysis': analyze_lead_scores(data),
            'opportunity_analysis': analyze_opportunities(data),
            'competitive_analysis': analyze_competition(data),
            'recommendations': generate_recommendations(data)
        }
        
        # Filter by requested metrics if specified
        if metrics:
            filtered_analysis = {}
            for metric in metrics:
                if metric in analysis:
                    filtered_analysis[metric] = analysis[metric]
            analysis = filtered_analysis
        
        # Save analysis if output file specified
        if output_file:
            save_json_data(analysis, output_file)
        
        return analysis
    
    except Exception as e:
        logger.error(f"Error analyzing leads: {e}")
        return {}

def analyze_by_category(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze businesses by category."""
    category_stats = {}
    
    for business in data:
        category = business.get('category', 'unknown')
        if category not in category_stats:
            category_stats[category] = {
                'total': 0,
                'with_website': 0,
                'without_website': 0,
                'avg_lead_score': 0,
                'avg_rating': 0,
                'total_rating': 0,
                'rated_count': 0
            }
        
        stats = category_stats[category]
        stats['total'] += 1
        
        if business.get('website'):
            stats['with_website'] += 1
        else:
            stats['without_website'] += 1
        
        stats['avg_lead_score'] += business.get('lead_score', 0)
        
        rating = business.get('rating', 0)
        if rating > 0:
            stats['total_rating'] += rating
            stats['rated_count'] += 1
    
    # Calculate averages
    for category, stats in category_stats.items():
        if stats['total'] > 0:
            stats['avg_lead_score'] = stats['avg_lead_score'] / stats['total']
            stats['website_percentage'] = (stats['with_website'] / stats['total']) * 100
            stats['opportunity_percentage'] = (stats['without_website'] / stats['total']) * 100
        
        if stats['rated_count'] > 0:
            stats['avg_rating'] = stats['total_rating'] / stats['rated_count']
    
    return category_stats

def analyze_by_location(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze businesses by location patterns."""
    location_stats = {}
    
    for business in data:
        address = business.get('address', '')
        if not address:
            continue
        
        # Extract location keywords
        location_keywords = ['medina', 'gueliz', 'hivernage', 'majorelle', 'atlas', 'centre']
        location = 'other'
        
        for keyword in location_keywords:
            if keyword.lower() in address.lower():
                location = keyword.lower()
                break
        
        if location not in location_stats:
            location_stats[location] = {
                'total': 0,
                'without_website': 0,
                'avg_lead_score': 0,
                'high_score_leads': 0
            }
        
        stats = location_stats[location]
        stats['total'] += 1
        
        if not business.get('website'):
            stats['without_website'] += 1
        
        lead_score = business.get('lead_score', 0)
        stats['avg_lead_score'] += lead_score
        
        if lead_score >= 70:
            stats['high_score_leads'] += 1
    
    # Calculate averages and percentages
    for location, stats in location_stats.items():
        if stats['total'] > 0:
            stats['avg_lead_score'] = stats['avg_lead_score'] / stats['total']
            stats['opportunity_percentage'] = (stats['without_website'] / stats['total']) * 100
            stats['high_score_percentage'] = (stats['high_score_leads'] / stats['total']) * 100
    
    return location_stats

def analyze_lead_scores(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze lead score distribution."""
    scores = [business.get('lead_score', 0) for business in data]
    
    if not scores:
        return {}
    
    score_ranges = {
        'very_high': [80, 100],
        'high': [60, 79],
        'medium': [40, 59],
        'low': [0, 39]
    }
    
    distribution = {}
    for range_name, (min_score, max_score) in score_ranges.items():
        count = sum(1 for score in scores if min_score <= score <= max_score)
        distribution[range_name] = {
            'count': count,
            'percentage': (count / len(scores)) * 100,
            'range': f"{min_score}-{max_score}"
        }
    
    analysis = {
        'distribution': distribution,
        'average_score': sum(scores) / len(scores),
        'median_score': sorted(scores)[len(scores) // 2],
        'max_score': max(scores),
        'min_score': min(scores),
        'total_businesses': len(scores)
    }
    
    return analysis

def analyze_opportunities(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze business opportunities."""
    opportunities = []
    
    for business in data:
        if not business.get('website'):  # No website = opportunity
            opportunity = {
                'name': business.get('name', ''),
                'category': business.get('category', ''),
                'lead_score': business.get('lead_score', 0),
                'rating': business.get('rating', 0),
                'review_count': business.get('review_count', 0),
                'phone': business.get('phone', ''),
                'address': business.get('address', ''),
                'opportunity_reasons': []
            }
            
            # Identify opportunity reasons
            if business.get('rating', 0) >= 4.0:
                opportunity['opportunity_reasons'].append('High rating')
            
            if business.get('review_count', 0) >= 20:
                opportunity['opportunity_reasons'].append('Many reviews')
            
            if business.get('social_media'):
                opportunity['opportunity_reasons'].append('Active on social media')
            
            if business.get('phone'):
                opportunity['opportunity_reasons'].append('Contact information available')
            
            opportunities.append(opportunity)
    
    # Sort by lead score
    opportunities.sort(key=lambda x: x['lead_score'], reverse=True)
    
    analysis = {
        'total_opportunities': len(opportunities),
        'top_opportunities': opportunities[:20],  # Top 20
        'by_category': {},
        'avg_opportunity_score': 0
    }
    
    # Analyze by category
    for opp in opportunities:
        category = opp['category']
        if category not in analysis['by_category']:
            analysis['by_category'][category] = {
                'count': 0,
                'avg_score': 0,
                'total_score': 0
            }
        
        analysis['by_category'][category]['count'] += 1
        analysis['by_category'][category]['total_score'] += opp['lead_score']
    
    # Calculate averages
    for category, stats in analysis['by_category'].items():
        if stats['count'] > 0:
            stats['avg_score'] = stats['total_score'] / stats['count']
    
    if opportunities:
        analysis['avg_opportunity_score'] = sum(opp['lead_score'] for opp in opportunities) / len(opportunities)
    
    return analysis

def analyze_competition(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze competitive landscape."""
    total_businesses = len(data)
    businesses_with_websites = len([b for b in data if b.get('website')])
    
    analysis = {
        'total_businesses': total_businesses,
        'with_websites': businesses_with_websites,
        'without_websites': total_businesses - businesses_with_websites,
        'website_penetration': (businesses_with_websites / total_businesses * 100) if total_businesses > 0 else 0,
        'market_opportunity': (total_businesses - businesses_with_websites) / total_businesses * 100 if total_businesses > 0 else 0,
        'by_category': {}
    }
    
    # Analyze by category
    categories = {}
    for business in data:
        category = business.get('category', 'unknown')
        if category not in categories:
            categories[category] = {'total': 0, 'with_website': 0}
        
        categories[category]['total'] += 1
        if business.get('website'):
            categories[category]['with_website'] += 1
    
    for category, stats in categories.items():
        penetration = (stats['with_website'] / stats['total'] * 100) if stats['total'] > 0 else 0
        analysis['by_category'][category] = {
            'total': stats['total'],
            'with_website': stats['with_website'],
            'without_website': stats['total'] - stats['with_website'],
            'penetration': penetration,
            'opportunity': 100 - penetration
        }
    
    return analysis

def generate_recommendations(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate actionable recommendations based on analysis."""
    opportunities = [b for b in data if not b.get('website')]
    high_score_opportunities = [b for b in opportunities if b.get('lead_score', 0) >= 70]
    
    recommendations = {
        'immediate_actions': [],
        'strategy_recommendations': [],
        'target_categories': [],
        'priority_leads': []
    }
    
    # Immediate actions
    if high_score_opportunities:
        recommendations['immediate_actions'].append(
            f"Contact top {min(10, len(high_score_opportunities))} high-score leads immediately"
        )
    
    if len(opportunities) > 50:
        recommendations['immediate_actions'].append(
            "Focus on businesses with 4+ star ratings and 20+ reviews"
        )
    
    # Strategy recommendations
    website_penetration = len([b for b in data if b.get('website')]) / len(data) * 100 if data else 0
    
    if website_penetration < 30:
        recommendations['strategy_recommendations'].append(
            "High opportunity market - aggressive outreach recommended"
        )
    elif website_penetration < 60:
        recommendations['strategy_recommendations'].append(
            "Moderate opportunity - selective targeting recommended"
        )
    else:
        recommendations['strategy_recommendations'].append(
            "Saturated market - premium positioning required"
        )
    
    # Target categories
    category_analysis = analyze_by_category(data)
    best_categories = sorted(
        category_analysis.items(),
        key=lambda x: x[1]['opportunity_percentage'],
        reverse=True
    )[:5]
    
    for category, stats in best_categories:
        if stats['opportunity_percentage'] > 50:
            recommendations['target_categories'].append({
                'category': category,
                'opportunity_percentage': stats['opportunity_percentage'],
                'total_businesses': stats['total']
            })
    
    # Priority leads
    priority_leads = sorted(
        opportunities,
        key=lambda x: x.get('lead_score', 0),
        reverse=True
    )[:10]
    
    for lead in priority_leads:
        recommendations['priority_leads'].append({
            'name': lead.get('name', ''),
            'score': lead.get('lead_score', 0),
            'category': lead.get('category', ''),
            'phone': lead.get('phone', '')
        })
    
    return recommendations
