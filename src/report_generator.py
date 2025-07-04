"""
Report Generator Module for Business Lead Finder
Generates comprehensive reports from business lead data.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

def generate_report(leads_data: List[Dict], output_path: str, format_type: str = 'html') -> str:
    """
    Generate comprehensive business lead report.
    
    Args:
        leads_data: List of business lead dictionaries
        output_path: Path where to save the report
        format_type: Report format ('html', 'json', 'csv')
    
    Returns:
        Path to generated report file
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format_type.lower() == 'html':
            return generate_html_report(leads_data, output_path)
        elif format_type.lower() == 'json':
            return generate_json_report(leads_data, output_path)
        elif format_type.lower() == 'csv':
            return generate_csv_report(leads_data, output_path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
    except Exception as e:
        print(f"Error generating report: {e}")
        return None

def generate_html_report(leads_data: List[Dict], output_path: str) -> str:
    """Generate HTML report."""
    
    # Calculate summary statistics
    total_leads = len(leads_data)
    without_websites = len([lead for lead in leads_data if not lead.get('website')])
    high_scoring = len([lead for lead in leads_data if lead.get('lead_score', 0) >= 70])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Business Lead Finder Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: #007bff; color: white; padding: 20px; border-radius: 8px; }}
            .summary {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }}
            .lead-card {{ background: white; border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; }}
            .high-score {{ border-left: 4px solid #28a745; }}
            .medium-score {{ border-left: 4px solid #ffc107; }}
            .low-score {{ border-left: 4px solid #dc3545; }}
            .no-website {{ background: #fff3cd; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Business Lead Finder Report</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary">
            <h2>📊 Summary Statistics</h2>
            <ul>
                <li><strong>Total Businesses Found:</strong> {total_leads}</li>
                <li><strong>Businesses Without Websites:</strong> {without_websites} ({without_websites/max(total_leads,1)*100:.1f}%)</li>
                <li><strong>High-Potential Leads:</strong> {high_scoring} ({high_scoring/max(total_leads,1)*100:.1f}%)</li>
                <li><strong>Potential Revenue:</strong> ${high_scoring * 2000:,}</li>
            </ul>
        </div>
        
        <div class="leads-section">
            <h2>🏢 Business Leads</h2>
    """
    
    # Add each lead
    for lead in leads_data:
        score = lead.get('lead_score', 0)
        score_class = 'high-score' if score >= 70 else 'medium-score' if score >= 40 else 'low-score'
        website_class = 'no-website' if not lead.get('website') else ''
        
        html_content += f"""
            <div class="lead-card {score_class} {website_class}">
                <h3>{lead.get('name', 'Unknown Business')}</h3>
                <p><strong>Category:</strong> {lead.get('category', 'N/A')}</p>
                <p><strong>Address:</strong> {lead.get('address', 'N/A')}</p>
                <p><strong>Phone:</strong> {lead.get('phone', 'N/A')}</p>
                <p><strong>Rating:</strong> {lead.get('rating', 'N/A')}/5 ({lead.get('review_count', 0)} reviews)</p>
                <p><strong>Website:</strong> {'❌ NOT FOUND' if not lead.get('website') else '✅ ' + lead.get('website')}</p>
                <p><strong>Lead Score:</strong> {score}/100</p>
                <p><strong>Opportunity:</strong> {'High - No website found!' if not lead.get('website') else 'Medium - Has website'}</p>
            </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

def generate_json_report(leads_data: List[Dict], output_path: str) -> str:
    """Generate JSON report."""
    report_data = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_leads': len(leads_data),
            'without_websites': len([lead for lead in leads_data if not lead.get('website')]),
            'high_scoring': len([lead for lead in leads_data if lead.get('lead_score', 0) >= 70])
        },
        'leads': leads_data
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return output_path

def generate_csv_report(leads_data: List[Dict], output_path: str) -> str:
    """Generate CSV report."""
    try:
        import pandas as pd
        
        # Convert to DataFrame
        df = pd.DataFrame(leads_data)
        
        # Save to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        return output_path
    except ImportError:
        # Fallback to manual CSV writing
        import csv
        
        if not leads_data:
            return output_path
        
        # Get all possible fieldnames
        fieldnames = set()
        for lead in leads_data:
            fieldnames.update(lead.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads_data)
        
        return output_path

def create_email_template(lead_data: Dict[str, Any]) -> str:
    """Create personalized email template for a lead."""
    business_name = lead_data.get('name', 'Business')
    category = lead_data.get('category', '').lower()
    rating = lead_data.get('rating', 0)
    review_count = lead_data.get('review_count', 0)
    
    if 'restaurant' in category or 'cafe' in category:
        template_type = 'restaurant'
    elif 'hotel' in category or 'riad' in category:
        template_type = 'hotel'
    else:
        template_type = 'general'
    
    templates = {
        'restaurant': f"""
Subject: Professional Website for {business_name}

Dear {business_name} Team,

I noticed that {business_name} has excellent reviews ({rating}/5 stars with {review_count}+ reviews) but no website yet.

A professional website could help you:
🍽️ Showcase your menu and specialties
📱 Accept online reservations
⭐ Display customer reviews
📍 Help tourists find you easily

I specialize in creating websites for restaurants in Marrakesh.

Would you be interested in a brief conversation this week?

Best regards,
[Your Name]
[Your Contact]
""",
        'hotel': f"""
Subject: Increase Direct Bookings for {business_name}

Dear {business_name} Management,

I found {business_name} and was impressed by your {rating}-star rating!

I noticed you don't have a website yet, which means missing out on direct bookings.

A professional website would help you:
🏨 Showcase rooms and amenities
💰 Accept direct bookings (avoid commission fees)
🌍 Reach international travelers
📸 Display beautiful property photos

Would you like to discuss how this could increase your revenue?

Best regards,
[Your Name]
[Your Contact]
""",
        'general': f"""
Subject: Professional Website for {business_name}

Dear {business_name} Team,

I came across {business_name} and was impressed by your {rating}-star rating and {review_count}+ reviews!

I noticed you don't have a website yet, which could be limiting your growth potential.

A professional website could help you:
✨ Increase visibility online
📱 Reach more customers
💼 Look more professional
📞 Make it easier for customers to contact you

Would you be interested in a quick conversation about how a website could benefit your business?

Best regards,
[Your Name]
[Your Contact]
"""
    }
    
    return templates[template_type]
