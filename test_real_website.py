#!/usr/bin/env python3
"""
Real website detection test - Check if Café Argana website exists
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import json
from website_checker import clean_domain_name, extract_title_from_content

def check_website_exists(url: str) -> dict:
    """Check if a website exists and return details."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for business indicators
            business_indicators = [
                'argana', 'cafe', 'restaurant', 'menu', 'contact', 
                'about', 'reservation', 'marrakech', 'morocco'
            ]
            
            parking_indicators = [
                'domain for sale', 'parked domain', 'buy this domain',
                'domain parking', 'coming soon', 'under construction'
            ]
            
            business_score = sum(1 for indicator in business_indicators if indicator in content)
            parking_score = sum(1 for indicator in parking_indicators if indicator in content)
            
            title = extract_title_from_content(response.text)
            
            return {
                'exists': True,
                'status_code': response.status_code,
                'title': title,
                'content_length': len(response.text),
                'business_score': business_score,
                'parking_score': parking_score,
                'is_real_business': business_score > parking_score and business_score > 0,
                'final_url': response.url
            }
        else:
            return {
                'exists': False,
                'status_code': response.status_code,
                'error': f'HTTP {response.status_code}'
            }
    
    except requests.exceptions.RequestException as e:
        return {
            'exists': False,
            'error': str(e)
        }

def test_cafe_argana():
    """Test the specific Café Argana case."""
    print("🎯 REAL WEBSITE TEST: Café Argana")
    print("=" * 50)
    
    # Test domains based on the pattern you mentioned
    test_domains = [
        'restaurantargana.com',  # The one you mentioned
        'cafeargana.com',
        'argana.com',
        'arganarestaurant.com',
        'arganamarrakech.com',
        'argana.ma'
    ]
    
    results = []
    
    for domain in test_domains:
        print(f"\n🔍 Testing: {domain}")
        print("-" * 30)
        
        # Test both HTTP and HTTPS
        for protocol in ['https://', 'http://']:
            full_url = f"{protocol}{domain}"
            print(f"  Checking: {full_url}")
            
            result = check_website_exists(full_url)
            result['domain'] = domain
            result['protocol'] = protocol
            result['full_url'] = full_url
            
            if result.get('exists'):
                print(f"  ✅ FOUND! Status: {result['status_code']}")
                print(f"     Title: {result.get('title', 'No title')}")
                print(f"     Business Score: {result['business_score']}")
                print(f"     Parking Score: {result['parking_score']}")
                print(f"     Real Business: {'YES' if result['is_real_business'] else 'NO'}")
                print(f"     Final URL: {result['final_url']}")
                
                results.append(result)
                break  # Found working protocol, no need to test the other
            else:
                print(f"  ❌ Not found: {result.get('error', 'Unknown error')}")
        
        if not any(r['domain'] == domain for r in results):
            # Add the failed result
            result['domain'] = domain
            results.append(result)
    
    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/cafe_argana_website_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 SUMMARY")
    print("=" * 50)
    
    working_sites = [r for r in results if r.get('exists') and r.get('is_real_business')]
    
    if working_sites:
        print(f"🎉 SUCCESS! Found {len(working_sites)} working website(s):")
        for site in working_sites:
            print(f"  ✅ {site['full_url']}")
            print(f"     Title: {site.get('title', 'No title')}")
            print(f"     Score: {site['business_score']}/10")
    else:
        print("❌ No working business websites found")
        
    print(f"\n📁 Results saved to: results/cafe_argana_website_test.json")

if __name__ == "__main__":
    test_cafe_argana()
