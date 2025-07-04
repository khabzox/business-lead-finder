#!/usr/bin/env python3
"""
Test script for enhanced website detection with fallback domain generation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from website_checker import generate_fallback_domains, clean_domain_name
import json

def test_domain_generation():
    """Test domain generation and cleaning."""
    print("🔧 Testing Domain Generation & Cleaning")
    print("=" * 50)
    
    # Test cases
    test_businesses = [
        {"name": "Café Argana", "category": "restaurant"},
        {"name": "Restaurant Atlas", "category": "restaurant"},
        {"name": "Hotel La Mamounia", "category": "hotel"},
        {"name": "Riad Yasmine", "category": "hotel"},
        {"name": "Spa Wellness", "category": "spa"},
        {"name": "Les Jardins de l'Agdal", "category": "restaurant"},
        {"name": "Café de la Poste", "category": "cafe"}
    ]
    
    results = []
    
    for business in test_businesses:
        print(f"\n🏢 Business: {business['name']}")
        print(f"📂 Category: {business['category']}")
        print("-" * 40)
        
        # Generate domain variations
        domains = generate_fallback_domains(business['name'], business['category'])
        
        print(f"🌐 Generated {len(domains)} domain variations:")
        
        cleaned_domains = []
        for domain in domains:
            cleaned = clean_domain_name(domain)
            if cleaned:
                cleaned_domains.append(cleaned)
                print(f"  ✅ {cleaned}")
            else:
                print(f"  ❌ {domain} (invalid)")
        
        results.append({
            'business_name': business['name'],
            'category': business['category'],
            'generated_domains': domains,
            'cleaned_domains': cleaned_domains,
            'valid_count': len(cleaned_domains)
        })
    
    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/domain_generation_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n📊 SUMMARY")
    print("=" * 50)
    total_businesses = len(results)
    total_domains = sum(r['valid_count'] for r in results)
    avg_domains = total_domains / total_businesses if total_businesses > 0 else 0
    
    print(f"Total Businesses: {total_businesses}")
    print(f"Total Valid Domains: {total_domains}")
    print(f"Average Domains per Business: {avg_domains:.1f}")
    
    print(f"\n📁 Results saved to: results/domain_generation_test.json")

def test_specific_case():
    """Test the specific Café Argana case."""
    print("\n🎯 SPECIFIC TEST: Café Argana")
    print("=" * 50)
    
    business_name = "Café Argana"
    category = "restaurant"
    
    print(f"Business: {business_name}")
    print(f"Category: {category}")
    print(f"Expected: Should generate 'restaurantargana.com' or 'cafeargana.com'")
    
    domains = generate_fallback_domains(business_name, category)
    
    print(f"\nGenerated domains:")
    for domain in domains:
        cleaned = clean_domain_name(domain)
        status = "✅" if cleaned else "❌"
        print(f"  {status} {domain} → {cleaned}")
    
    # Check if we got the expected domain
    expected_domains = ['restaurantargana.com', 'cafeargana.com', 'argana.com']
    found_expected = []
    
    for domain in domains:
        cleaned = clean_domain_name(domain)
        if cleaned in expected_domains:
            found_expected.append(cleaned)
    
    print(f"\n🎯 Expected domains found: {found_expected}")
    
    if found_expected:
        print("✅ SUCCESS: Found expected domain variations")
    else:
        print("❌ ISSUE: Did not find expected domain variations")

if __name__ == "__main__":
    test_domain_generation()
    test_specific_case()
