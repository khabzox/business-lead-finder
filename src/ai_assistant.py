"""
AI Assistant Module using Groq API
Provides AI-powered analysis and recommendations for business leads.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from config.settings import load_config

logger = logging.getLogger(__name__)

def initialize_groq_client() -> Optional[Groq]:
    """Initialize Groq client with API key."""
    try:
        config = load_config()
        api_key = config.get('groq_api_key') or os.getenv('GROQ_API_KEY')
        
        if not api_key or api_key == 'your_groq_api_key_here':
            logger.warning("Groq API key not configured. AI features disabled.")
            return None
        
        return Groq(api_key=api_key)
    
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")
        return None

def analyze_business_with_ai(business: Dict[str, Any], client: Optional[Groq] = None) -> Dict[str, Any]:
    """
    Use AI to analyze a business and provide insights.
    
    Args:
        business: Business data dictionary
        client: Groq client instance
    
    Returns:
        AI analysis results
    """
    if not client:
        client = initialize_groq_client()
    
    if not client:
        return {"error": "AI client not available"}
    
    try:
        # Prepare business data for AI analysis
        business_info = f"""
        Business Name: {business.get('name', 'Unknown')}
        Category: {business.get('category', 'Unknown')}
        Rating: {business.get('rating', 'N/A')}/5
        Reviews: {business.get('review_count', 0)}
        Website: {"Yes" if business.get('website') else "NO WEBSITE"}
        Address: {business.get('address', 'N/A')}
        Phone: {business.get('phone', 'N/A')}
        Lead Score: {business.get('lead_score', 0)}/100
        """
        
        prompt = f"""
        Analyze this business for website development opportunities:
        
        {business_info}
        
        Provide:
        1. Opportunity Level (High/Medium/Low)
        2. Key selling points for approaching them
        3. Estimated website budget range (in USD)
        4. Best approach strategy
        5. Potential objections and how to handle them
        
        Keep response concise and actionable.
        """
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_analysis = response.choices[0].message.content
        
        return {
            "ai_analysis": ai_analysis,
            "opportunity_score": extract_opportunity_score(ai_analysis),
            "estimated_budget": extract_budget_range(ai_analysis),
            "approach_strategy": extract_strategy(ai_analysis)
        }
    
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return {"error": f"AI analysis failed: {str(e)}"}

def generate_personalized_email(business: Dict[str, Any], client: Optional[Groq] = None) -> str:
    """
    Generate personalized email template using AI.
    
    Args:
        business: Business data dictionary
        client: Groq client instance
    
    Returns:
        Personalized email template
    """
    if not client:
        client = initialize_groq_client()
    
    if not client:
        return generate_fallback_email(business)
    
    try:
        business_info = f"""
        Business: {business.get('name', 'Unknown')}
        Category: {business.get('category', 'Unknown')}
        Rating: {business.get('rating', 'N/A')}/5 ({business.get('review_count', 0)} reviews)
        Location: {business.get('address', 'Marrakesh')}
        Website Status: {"Has website" if business.get('website') else "NO WEBSITE"}
        """
        
        prompt = f"""
        Create a personalized email template for a web developer reaching out to this business:
        
        {business_info}
        
        The email should:
        - Be professional but friendly
        - Mention specific details about their business
        - Highlight the opportunity (especially if no website)
        - Include clear value proposition
        - End with a soft call-to-action
        - Be in English
        - Keep it under 150 words
        
        Format: Subject line + Email body
        """
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Email generation failed: {e}")
        return generate_fallback_email(business)

def generate_fallback_email(business: Dict[str, Any]) -> str:
    """Generate fallback email when AI is not available."""
    business_name = business.get('name', 'Your Business')
    category = business.get('category', 'business')
    rating = business.get('rating', 0)
    
    return f"""
Subject: Professional Website for {business_name}

Dear {business_name} Team,

I noticed your excellent {rating}-star rating and wanted to reach out about creating a professional website for your {category}.

A modern website could help you:
• Attract more customers online
• Showcase your services/products
• Accept online bookings/orders
• Stand out from competitors

Would you be interested in a brief conversation about how a website could benefit your business?

Best regards,
[Your Name]
[Your Contact Information]
"""

def extract_opportunity_score(analysis: str) -> str:
    """Extract opportunity level from AI analysis."""
    analysis_lower = analysis.lower()
    if 'high' in analysis_lower and 'opportunity' in analysis_lower:
        return 'High'
    elif 'medium' in analysis_lower and 'opportunity' in analysis_lower:
        return 'Medium'
    elif 'low' in analysis_lower and 'opportunity' in analysis_lower:
        return 'Low'
    return 'Medium'

def extract_budget_range(analysis: str) -> str:
    """Extract budget estimate from AI analysis."""
    # Simple extraction - could be improved with regex
    if '$' in analysis:
        import re
        budget_match = re.search(r'\$[\d,]+-\$?[\d,]+', analysis)
        if budget_match:
            return budget_match.group()
    return '$800-$2000'

def extract_strategy(analysis: str) -> str:
    """Extract approach strategy from AI analysis."""
    lines = analysis.split('\n')
    for line in lines:
        if 'strategy' in line.lower() or 'approach' in line.lower():
            return line.strip()
    return 'Direct contact with value proposition focus'

def batch_analyze_businesses(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze multiple businesses with AI in batch.
    
    Args:
        businesses: List of business dictionaries
    
    Returns:
        List of businesses with AI analysis added
    """
    client = initialize_groq_client()
    
    if not client:
        logger.warning("AI analysis skipped - no Groq client available")
        return businesses
    
    analyzed_businesses = []
    
    for i, business in enumerate(businesses):
        try:
            logger.info(f"AI analyzing business {i+1}/{len(businesses)}: {business.get('name', 'Unknown')}")
            
            # Add AI analysis to business data
            ai_results = analyze_business_with_ai(business, client)
            business['ai_analysis'] = ai_results
            
            # Generate personalized email
            business['personalized_email'] = generate_personalized_email(business, client)
            
            analyzed_businesses.append(business)
            
            # Rate limiting - Groq free tier limits
            import time
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"Failed to analyze business {business.get('name', 'Unknown')}: {e}")
            business['ai_analysis'] = {"error": str(e)}
            analyzed_businesses.append(business)
    
    return analyzed_businesses
