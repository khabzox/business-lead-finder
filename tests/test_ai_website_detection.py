#!/usr/bin/env python3
"""
Test script for AI-powered website detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from website_checker import enhanced_website_search
from config.settings import load_config
import json

def test_ai_domain_generation():
    """Test AI-powered domain generation and website detection."""
    print("🤖 Testing AI-Powered Website Detection")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Test cases
    test_businesses = [
        {"name": "Café Argana", "category": "restaurant"},
        {"name": "Restaurant Atlas", "category": "restaurant"},
        {"name": "Hotel La Mamounia", "category": "hotel"},
        {"name": "Riad Yasmine", "category": "hotel"},
        {"name": "Spa Wellness", "category": "spa"}
    ]
    
    results = []
    
    for business in test_businesses:
        print(f"\n🔍 Testing: {business['name']}")
        print("-" * 30)
        
        # Run enhanced website search
        result = enhanced_website_search(
            business_name=business['name'],
            category=business['category'],
            config=config
        )
        
        results.append(result)
        
        # Display results
        print(f"Business: {result['business_name']}")
        print(f"Website Found: {'✅ YES' if result['website_found'] else '❌ NO'}")
        
        if result['website_found']:
            print(f"Website URL: {result['website_url']}")
            print(f"Quality Score: {result['quality_score']}/100")
            if result['details'].get('title'):
                print(f"Page Title: {result['details']['title']}")
            print(f"Total Working Domains: {result['details'].get('total_domains_found', 0)}")
        
        print(f"Domains Checked: {len(result['domains_checked'])}")
        print(f"Domains: {', '.join(result['domains_checked'][:5])}{'...' if len(result['domains_checked']) > 5 else ''}")
        
        if result['working_domains']:
            print("\n🌐 Working Domains Found:")
            for domain in result['working_domains']:
                print(f"  • {domain['url']} (Score: {domain['business_score']})")
        
        print()
    
    # Save results
    with open('results/ai_website_detection_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n📊 SUMMARY")
    print("=" * 50)
    total_tested = len(results)
    websites_found = sum(1 for r in results if r['website_found'])
    
    print(f"Total Businesses Tested: {total_tested}")
    print(f"Websites Found: {websites_found}")
    print(f"Success Rate: {websites_found/total_tested*100:.1f}%")
    
    print(f"\n📁 Results saved to: results/ai_website_detection_test.json")

if __name__ == "__main__":
    test_ai_domain_generation()
