"""
Business Lead Service
High-level service for business lead generation and analysis
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import asdict
import json
from datetime import datetime
from pathlib import Path

try:
    from ..data.real_sources import real_data_collector, BusinessData
    from ..core.config import config, SCORING_CONFIG, SEARCH_CONFIG
    from ..website_checker import enhanced_website_detection
    from ..business_search import calculate_lead_score
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from data.real_sources import real_data_collector, BusinessData
    from core.config import config, SCORING_CONFIG, SEARCH_CONFIG
    from website_checker import enhanced_website_detection
    from business_search import calculate_lead_score

logger = logging.getLogger(__name__)

class LeadAnalysisResult:
    """Result of lead analysis"""
    def __init__(
        self, 
        businesses: List[BusinessData], 
        total_found: int,
        high_priority_count: int,
        no_website_count: int,
        avg_rating: float,
        sources_used: List[str]
    ):
        self.businesses = businesses
        self.total_found = total_found
        self.high_priority_count = high_priority_count
        self.no_website_count = no_website_count
        self.avg_rating = avg_rating
        self.sources_used = sources_used
        self.timestamp = datetime.now()

class BusinessLeadService:
    """Main service for business lead generation"""
    
    def __init__(self):
        self.data_collector = real_data_collector
    
    async def search_leads(
        self, 
        category: str, 
        location: str = None,
        max_results: int = None,
        enhance_with_website_check: bool = True
    ) -> LeadAnalysisResult:
        """Search for business leads with full analysis"""
        
        # Use defaults if not provided
        if location is None:
            location = SEARCH_CONFIG.default_location
        if max_results is None:
            max_results = SEARCH_CONFIG.max_results_per_source
        
        logger.info(f"Searching for {category} in {location} (max: {max_results})")
        
        # Collect raw business data
        businesses = await self.data_collector.collect_business_data(
            query=category,
            location=location,
            max_results=max_results
        )
        
        if not businesses:
            logger.warning("No businesses found")
            return LeadAnalysisResult(
                businesses=[],
                total_found=0,
                high_priority_count=0,
                no_website_count=0,
                avg_rating=0.0,
                sources_used=[]
            )
        
        # Enhance with website detection if requested
        if enhance_with_website_check:
            businesses = await self._enhance_with_website_detection(businesses)
        
        # Calculate lead scores
        businesses = self._calculate_lead_scores(businesses)
        
        # Sort by lead score (highest first)
        businesses.sort(key=lambda b: b.raw_data.get('lead_score', 0), reverse=True)
        
        # Generate analysis
        analysis = self._analyze_results(businesses)
        
        return analysis
    
    async def _enhance_with_website_detection(self, businesses: List[BusinessData]) -> List[BusinessData]:
        """Enhance business data with website detection"""
        logger.info(f"Enhancing {len(businesses)} businesses with website detection")
        
        enhanced_businesses = []
        
        for business in businesses:
            try:
                # Only check if no website already found
                if not business.website:
                    logger.debug(f"Checking website for: {business.name}")
                    
                    # Use enhanced website detection
                    result = enhanced_website_detection(business.name, business.category)
                    
                    if result.get('website_found'):
                        business.website = result['website_url']
                        logger.info(f"Found website for {business.name}: {business.website}")
                    
                    # Add small delay to respect rate limits
                    await asyncio.sleep(0.1)
                
                enhanced_businesses.append(business)
                
            except Exception as e:
                logger.warning(f"Error enhancing {business.name}: {e}")
                enhanced_businesses.append(business)  # Include anyway
                continue
        
        return enhanced_businesses
    
    def _calculate_lead_scores(self, businesses: List[BusinessData]) -> List[BusinessData]:
        """Calculate lead scores for businesses"""
        logger.info(f"Calculating lead scores for {len(businesses)} businesses")
        
        for business in businesses:
            try:
                # Convert BusinessData to format expected by calculate_lead_score
                business_dict = {
                    'name': business.name,
                    'category': business.category,
                    'address': business.address,
                    'phone': business.phone,
                    'website': business.website,
                    'rating': business.rating,
                    'review_count': business.review_count
                }
                
                # Calculate score
                score = calculate_lead_score(business_dict)
                
                # Store in raw_data for sorting
                if business.raw_data is None:
                    business.raw_data = {}
                business.raw_data['lead_score'] = score
                
                # Log high-priority leads
                if score >= 80:
                    logger.info(f"High priority lead: {business.name} (Score: {score})")
                
            except Exception as e:
                logger.warning(f"Error calculating score for {business.name}: {e}")
                if business.raw_data is None:
                    business.raw_data = {}
                business.raw_data['lead_score'] = 0
        
        return businesses
    
    def _analyze_results(self, businesses: List[BusinessData]) -> LeadAnalysisResult:
        """Analyze the results and generate insights"""
        total_found = len(businesses)
        
        if total_found == 0:
            return LeadAnalysisResult(
                businesses=[],
                total_found=0,
                high_priority_count=0,
                no_website_count=0,
                avg_rating=0.0,
                sources_used=[]
            )
        
        # Count metrics
        high_priority_count = sum(
            1 for b in businesses 
            if b.raw_data.get('lead_score', 0) >= 80
        )
        
        no_website_count = sum(
            1 for b in businesses 
            if not b.website
        )
        
        # Calculate average rating (excluding 0 ratings)
        ratings = [b.rating for b in businesses if b.rating > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
        
        # Get sources used
        sources_used = list(set(b.source for b in businesses))
        
        logger.info(f"Analysis complete: {total_found} total, {high_priority_count} high priority, {no_website_count} without website")
        
        return LeadAnalysisResult(
            businesses=businesses,
            total_found=total_found,
            high_priority_count=high_priority_count,
            no_website_count=no_website_count,
            avg_rating=avg_rating,
            sources_used=sources_used
        )
    
    def save_results(self, analysis: LeadAnalysisResult, filename: str = None) -> Path:
        """Save analysis results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_leads_{timestamp}.json"
        
        filepath = config.results_dir / filename
        
        # Convert to serializable format
        results_data = {
            'metadata': {
                'timestamp': analysis.timestamp.isoformat(),
                'total_found': analysis.total_found,
                'high_priority_count': analysis.high_priority_count,
                'no_website_count': analysis.no_website_count,
                'avg_rating': analysis.avg_rating,
                'sources_used': analysis.sources_used
            },
            'businesses': []
        }
        
        for business in analysis.businesses:
            business_data = asdict(business)
            # Add lead score to main data
            business_data['lead_score'] = business.raw_data.get('lead_score', 0)
            results_data['businesses'].append(business_data)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Results saved to: {filepath}")
        return filepath
    
    def get_summary_stats(self, analysis: LeadAnalysisResult) -> Dict[str, Any]:
        """Get summary statistics from analysis"""
        if not analysis.businesses:
            return {
                'total_businesses': 0,
                'data_sources': [],
                'lead_distribution': {},
                'website_stats': {},
                'rating_stats': {}
            }
        
        # Lead score distribution
        high_priority = sum(1 for b in analysis.businesses if b.raw_data.get('lead_score', 0) >= 80)
        medium_priority = sum(1 for b in analysis.businesses if 60 <= b.raw_data.get('lead_score', 0) < 80)
        low_priority = sum(1 for b in analysis.businesses if b.raw_data.get('lead_score', 0) < 60)
        
        # Rating distribution
        low_rated = sum(1 for b in analysis.businesses if 2.0 <= b.rating <= 3.5)
        high_rated = sum(1 for b in analysis.businesses if b.rating > 4.0)
        no_rating = sum(1 for b in analysis.businesses if b.rating == 0)
        
        return {
            'total_businesses': analysis.total_found,
            'data_sources': analysis.sources_used,
            'lead_distribution': {
                'high_priority': high_priority,
                'medium_priority': medium_priority,
                'low_priority': low_priority
            },
            'website_stats': {
                'with_website': analysis.total_found - analysis.no_website_count,
                'without_website': analysis.no_website_count,
                'percentage_without': (analysis.no_website_count / analysis.total_found * 100) if analysis.total_found > 0 else 0
            },
            'rating_stats': {
                'average_rating': analysis.avg_rating,
                'low_rated_2_3_stars': low_rated,
                'high_rated_4_plus': high_rated,
                'no_rating': no_rating
            }
        }

# Global service instance
lead_service = BusinessLeadService()
