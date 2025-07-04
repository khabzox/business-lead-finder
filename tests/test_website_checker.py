#!/usr/bin/env python3
"""
Test Enhanced Website Checker
Tests the improved website detection system with real examples.
"""

import sys
import os
sys.path.append('src')

from website_checker import check_website_status, generate_potential_domains
import json

def test_cafe_argana():
    """Test with Café Argana example."""
    print("🧪 Testing Enhanced Website Checker")
    print("=" * 50)
    
    # Test case: Café Argana
    business_data = {
        "name": "Café Argana",
        "category": "cafe",
        "address": "Place Jemaa el-Fna, Medina, Marrakesh",
        "phone": "+212524443322",
        "website": ""  # Simulate no website info
    }
    
    print(f"🏪 Testing Business: {business_data['name']}")
    print(f"📍 Location: {business_data['address']}")
    print()
    
    # Test domain generation
    print("🌐 Generated Potential Domains:")
    domains = generate_potential_domains(business_data['name'])
    for i, domain in enumerate(domains[:10], 1):
        print(f"   {i:2d}. {domain}")
    print()
    
    # Test website checking
    print("🔍 Checking Website Status...")
    result = check_website_status(business_data)
    
    print("\n📊 Results:")
    print(f"   Has Website: {'✅ YES' if result['has_website'] else '❌ NO'}")
    if result['website_url']:
        print(f"   Website URL: {result['website_url']}")
        print(f"   Quality Score: {result['website_quality_score']}/100")
        print(f"   Detection Method: {result['detection_method']}")
        print(f"   Confidence: {result['confidence_score']}%")
    
    if result['potential_domains']:
        print(f"   Domains Tested: {len(result['potential_domains'])}")
    
    return result

def test_multiple_businesses():
    """Test with multiple businesses."""
    print("\n" + "=" * 50)
    print("🧪 Testing Multiple Businesses")
    print("=" * 50)
    
    test_businesses = [
        {
            "name": "Restaurant Atlas",
            "category": "restaurant",
            "address": "Medina, Marrakesh"
        },
        {
            "name": "Hotel La Mamounia", 
            "category": "hotel",
            "address": "Marrakesh"
        },
        {
            "name": "Spa Wellness Center",
            "category": "spa", 
            "address": "Gueliz, Marrakesh"
        }
    ]
    
    results = []
    
    for business in test_businesses:
        print(f"\n🏪 Testing: {business['name']}")
        result = check_website_status(business)
        
        print(f"   Result: {'✅ Found Website' if result['has_website'] else '❌ No Website'}")
        if result['website_url']:
            print(f"   URL: {result['website_url']}")
            print(f"   Quality: {result['website_quality_score']}/100")
        
        results.append({
            'business': business,
            'result': result
        })
    
    return results

if __name__ == "__main__":
    # Test Café Argana specifically
    argana_result = test_cafe_argana()
    
    # Test multiple businesses
    multiple_results = test_multiple_businesses()
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 SUMMARY")
    print("=" * 50)
    
    if argana_result['has_website']:
        print(f"✅ SUCCESS: Found Café Argana website!")
        print(f"   URL: {argana_result['website_url']}")
        print(f"   This business should NOT be in the 'no-website' leads!")
    else:
        print("❌ Could not find Café Argana website")
        print("   This may be due to domain variations or rate limiting")
    
    # Count businesses with websites found
    found_websites = sum(1 for r in multiple_results if r['result']['has_website'])
    total_tested = len(multiple_results)
    
    print(f"\n📊 Overall Results:")
    print(f"   Businesses Tested: {total_tested + 1}")
    print(f"   Websites Found: {found_websites + (1 if argana_result['has_website'] else 0)}")
    print(f"   Detection Rate: {((found_websites + (1 if argana_result['has_website'] else 0)) / (total_tested + 1) * 100):.1f}%")
    
    print("\n💡 Next Steps:")
    print("   1. Update business data with found websites")
    print("   2. Re-run lead analysis with corrected data") 
    print("   3. Focus on businesses that truly have no websites")
