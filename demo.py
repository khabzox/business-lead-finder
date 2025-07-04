#!/usr/bin/env python3
"""
Business Lead Finder - Comprehensive Demo
Shows all enhanced features including AI analysis and filtering.
"""

import json
import os
from datetime import datetime

def main():
    print("🎯 BUSINESS LEAD FINDER - COMPREHENSIVE DEMO")
    print("=" * 60)
    
    # Demo data
    demo_businesses = [
        {
            "name": "Restaurant Atlas",
            "category": "restaurant",
            "address": "Rue Moulay Ismail, Medina, Marrakesh",
            "phone": "+212524443322",
            "email": "",
            "website": "",
            "rating": 4.2,
            "review_count": 87,
            "lat": 31.6295,
            "lon": -7.9811,
            "source": "openstreetmap",
            "lead_score": 85,
            "last_updated": datetime.now().isoformat()
        },
        {
            "name": "Cafe Central",
            "category": "cafe",
            "address": "Avenue Mohammed V, Gueliz, Marrakesh",
            "phone": "+212524332211",
            "email": "",
            "website": "",
            "rating": 4.5,
            "review_count": 124,
            "lat": 31.6340,
            "lon": -8.0088,
            "source": "foursquare",
            "lead_score": 92,
            "last_updated": datetime.now().isoformat()
        },
        {
            "name": "Hotel Riad Marrakesh",
            "category": "hotel",
            "address": "Derb Sidi Ahmed Souissi, Medina, Marrakesh",
            "phone": "+212524387654",
            "email": "info@hotelriad.com",
            "website": "http://oldsite.example.com",
            "rating": 3.8,
            "review_count": 45,
            "lat": 31.6318,
            "lon": -7.9890,
            "source": "serpapi",
            "lead_score": 65,
            "website_quality_score": 35,
            "last_updated": datetime.now().isoformat()
        },
        {
            "name": "Spa Wellness Marrakesh",
            "category": "spa",
            "address": "Rue de la Kasbah, Medina, Marrakesh",
            "phone": "+212524556677",
            "email": "",
            "website": "",
            "rating": 4.7,
            "review_count": 203,
            "lat": 31.6239,
            "lon": -7.9886,
            "source": "manual",
            "lead_score": 95,
            "last_updated": datetime.now().isoformat()
        }
    ]
    
    # Create demo data file
    os.makedirs("demo_data", exist_ok=True)
    with open("demo_data/businesses.json", "w") as f:
        json.dump(demo_businesses, f, indent=2)
    
    print(f"✅ Created demo data with {len(demo_businesses)} businesses")
    
    # Show analysis
    print("\n📊 BUSINESS ANALYSIS")
    print("-" * 30)
    
    # Calculate stats
    total_businesses = len(demo_businesses)
    without_websites = len([b for b in demo_businesses if not b.get('website')])
    with_poor_websites = len([b for b in demo_businesses if b.get('website') and b.get('website_quality_score', 100) < 50])
    avg_lead_score = sum(b.get('lead_score', 0) for b in demo_businesses) / total_businesses
    
    print(f"📈 Total Businesses: {total_businesses}")
    print(f"❌ Without Websites: {without_websites} ({without_websites/total_businesses*100:.1f}%)")
    print(f"🔧 With Poor Websites: {with_poor_websites} ({with_poor_websites/total_businesses*100:.1f}%)")
    print(f"⭐ Average Lead Score: {avg_lead_score:.1f}/100")
    
    # Show opportunities
    print("\n🎯 TOP OPPORTUNITIES")
    print("-" * 30)
    
    # Sort by lead score
    sorted_businesses = sorted(demo_businesses, key=lambda x: x.get('lead_score', 0), reverse=True)
    
    for i, business in enumerate(sorted_businesses, 1):
        name = business.get('name', 'Unknown')
        category = business.get('category', 'Unknown')
        rating = business.get('rating', 0)
        lead_score = business.get('lead_score', 0)
        phone = business.get('phone', 'N/A')
        website_status = "❌ NO WEBSITE" if not business.get('website') else "✅ HAS WEBSITE"
        
        print(f"{i}. {name}")
        print(f"   📱 {phone} | ⭐ {rating}/5 | 🎯 {lead_score}/100")
        print(f"   📍 {category.title()} | {website_status}")
        print()
    
    # Show filtering examples
    print("\n🔍 FILTERING EXAMPLES")
    print("-" * 30)
    
    # No website filter
    no_website_businesses = [b for b in demo_businesses if not b.get('website')]
    print(f"🚫 Businesses WITHOUT websites: {len(no_website_businesses)}")
    for business in no_website_businesses:
        print(f"   • {business['name']} ({business['category']})")
    
    # Poor website filter
    poor_website_businesses = [b for b in demo_businesses if b.get('website') and b.get('website_quality_score', 100) < 50]
    print(f"\n🔧 Businesses with POOR websites: {len(poor_website_businesses)}")
    for business in poor_website_businesses:
        print(f"   • {business['name']} ({business['category']})")
    
    # AI Analysis simulation
    print("\n🤖 AI ANALYSIS SIMULATION")
    print("-" * 30)
    
    for business in sorted_businesses[:2]:  # Top 2 businesses
        print(f"🏢 {business['name']}")
        print(f"📊 Lead Score: {business['lead_score']}/100")
        print(f"⭐ Rating: {business['rating']}/5 ({business['review_count']} reviews)")
        
        # Simulate AI analysis
        if not business.get('website'):
            print("🎯 AI OPPORTUNITY ANALYSIS:")
            print("   • HIGH PRIORITY: No website despite excellent ratings")
            print("   • APPROACH: Emphasize missed online opportunities")
            print("   • BUDGET ESTIMATE: $800-$1,500 for professional website")
            print("   • SUCCESS PROBABILITY: 85% (high rating + no website)")
            
            # Sample personalized email
            print("\n📧 AI-GENERATED EMAIL TEMPLATE:")
            print(f"   Subject: Professional Website for {business['name']}")
            print(f"   Dear {business['name']} Team,")
            print(f"   I noticed your excellent {business['rating']}-star rating with {business['review_count']}+ reviews!")
            print(f"   However, I couldn't find a website for your {business['category']}.")
            print(f"   A professional website could help you reach even more customers...")
        else:
            print("🔧 AI IMPROVEMENT ANALYSIS:")
            print("   • MEDIUM PRIORITY: Website exists but needs improvement")
            print("   • APPROACH: Focus on modernization and mobile optimization")
            print("   • BUDGET ESTIMATE: $500-$1,200 for website upgrade")
            print("   • SUCCESS PROBABILITY: 65% (existing website shows digital awareness)")
        
        print()
    
    # Generate sample files
    print("\n📁 GENERATING SAMPLE FILES")
    print("-" * 30)
    
    # Create results directory
    os.makedirs("demo_results", exist_ok=True)
    
    # Export no-website businesses to CSV
    no_website_csv = "demo_results/no_website_opportunities.csv"
    with open(no_website_csv, "w") as f:
        f.write("Name,Category,Phone,Address,Rating,Lead Score,Opportunity\n")
        for business in no_website_businesses:
            f.write(f"{business['name']},{business['category']},{business['phone']},{business['address']},{business['rating']},{business['lead_score']},High Priority\n")
    
    print(f"✅ Exported {len(no_website_businesses)} high-priority leads to: {no_website_csv}")
    
    # Generate analysis report
    analysis_report = "demo_results/analysis_report.json"
    analysis_data = {
        "generated_at": datetime.now().isoformat(),
        "total_businesses": total_businesses,
        "without_websites": without_websites,
        "with_poor_websites": with_poor_websites,
        "avg_lead_score": avg_lead_score,
        "top_opportunities": [
            {
                "name": b["name"],
                "category": b["category"],
                "lead_score": b["lead_score"],
                "phone": b["phone"],
                "opportunity_type": "No Website" if not b.get("website") else "Website Improvement"
            }
            for b in sorted_businesses[:5]
        ],
        "recommendations": [
            f"Focus on {without_websites} businesses without websites first",
            f"Average lead score is {avg_lead_score:.1f}/100 - good quality leads",
            f"High-rating businesses without websites have 85%+ success probability",
            f"Estimated revenue potential: ${(without_websites * 1200):,}"
        ]
    }
    
    with open(analysis_report, "w") as f:
        json.dump(analysis_data, f, indent=2)
    
    print(f"✅ Generated analysis report: {analysis_report}")
    
    # CLI Commands to try
    print("\n🔧 CLI COMMANDS TO TRY")
    print("-" * 30)
    print("1. Export no-website businesses:")
    print("   python main.py export --input demo_data/businesses.json --output demo_results/leads.csv --format csv --filter \"no_website=true\"")
    print()
    print("2. Generate HTML report:")
    print("   python main.py report --input demo_data/businesses.json --output demo_results/report.html --format html")
    print()
    print("3. Analyze data with AI (if Groq API key configured):")
    print("   python main.py analyze --input demo_data/businesses.json --output demo_results/ai_analysis.json")
    print()
    print("4. Search with filtering:")
    print("   python main.py search --location \"Marrakesh, Morocco\" --categories restaurants --filter no-website --ai-analysis")
    
    print("\n🎉 DEMO COMPLETE!")
    print("Check the 'demo_results' folder for generated files.")

if __name__ == "__main__":
    main()
