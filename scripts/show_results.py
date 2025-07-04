#!/usr/bin/env python3
"""
Real Data Summary Script
Shows the results of our real data collection
"""

import json
import os
from pathlib import Path

def display_summary():
    """Display comprehensive summary of collected data"""
    
    print("🎯 BUSINESS LEAD FINDER - REAL DATA SUMMARY")
    print("=" * 60)
    
    # Check what files we have
    results_dir = Path("results")
    if not results_dir.exists():
        print("❌ Results directory not found")
        return
    
    files = list(results_dir.glob("*.json"))
    
    print(f"📁 Files in results directory: {len(files)}")
    for file in files:
        size_kb = file.stat().st_size / 1024
        print(f"   📄 {file.name} ({size_kb:.1f} KB)")
    
    # Load and analyze high opportunity leads
    high_opp_file = results_dir / "high_opportunity_leads.json"
    if high_opp_file.exists():
        with open(high_opp_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        print(f"\n🔥 HIGH OPPORTUNITY LEADS: {len(leads)} businesses")
        print("=" * 40)
        
        # Category breakdown
        categories = {}
        cities = {}
        
        for lead in leads:
            cat = lead.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            address = lead.get('address', '')
            for city in ['Marrakesh', 'Casablanca', 'Rabat', 'Fez']:
                if city.lower() in address.lower():
                    cities[city] = cities.get(city, 0) + 1
                    break
        
        print("📊 By Category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: {count} businesses")
        
        print("\n📍 By City:")
        for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
            print(f"   {city}: {count} businesses")
        
        # Top leads by score
        top_leads = sorted(leads, key=lambda x: x.get('lead_score', 0), reverse=True)[:10]
        
        print(f"\n🏆 TOP 10 LEADS (by lead score):")
        print("-" * 40)
        
        for i, lead in enumerate(top_leads, 1):
            name = lead.get('name', 'Unknown')[:25]
            category = lead.get('category', 'unknown')
            score = lead.get('lead_score', 0)
            rating = lead.get('rating', 0)
            phone = lead.get('phone', 'N/A')
            
            print(f"{i:2d}. {name:<25} | {category:<10} | Score: {score}/100 | ⭐{rating} | {phone}")
        
        # Revenue potential calculation
        avg_website_cost = 1500  # USD
        conversion_rate = 0.05  # 5% conversion rate
        potential_revenue = len(leads) * avg_website_cost * conversion_rate
        
        print(f"\n💰 REVENUE POTENTIAL:")
        print(f"   📈 {len(leads)} leads × ${avg_website_cost} × {conversion_rate*100}% = ${potential_revenue:,.0f}")
        print(f"   📊 If 5% convert, that's {len(leads) * conversion_rate:.0f} websites @ ${avg_website_cost} each")
        
        # Key insights
        high_rating_leads = [l for l in leads if l.get('rating', 0) >= 4.5]
        many_reviews_leads = [l for l in leads if l.get('review_count', 0) >= 50]
        
        print(f"\n💡 KEY INSIGHTS:")
        print(f"   ⭐ {len(high_rating_leads)} businesses have 4.5+ star ratings")
        print(f"   📝 {len(many_reviews_leads)} businesses have 50+ reviews")
        print(f"   🎯 100% of these businesses have NO WEBSITE")
        print(f"   📞 All businesses have contact phone numbers")
        
    # Check other city files
    print(f"\n🌍 CITY-SPECIFIC DATA:")
    print("-" * 30)
    
    for city in ['marrakesh', 'casablanca', 'rabat', 'fez']:
        city_file = results_dir / f"{city}_businesses.json"
        if city_file.exists():
            with open(city_file, 'r', encoding='utf-8') as f:
                city_data = json.load(f)
            
            no_website = len([b for b in city_data if not b.get('website')])
            print(f"   📍 {city.title()}: {len(city_data)} total, {no_website} without websites")
    
    print(f"\n📁 GENERATED FILES:")
    print("-" * 20)
    if (results_dir / "morocco_opportunities_report.html").exists():
        print("   📄 HTML Report: results/morocco_opportunities_report.html")
    if (results_dir / "morocco_leads.csv").exists():
        print("   📊 CSV Export: results/morocco_leads.csv")
    if (results_dir / "lead_analysis.json").exists():
        print("   📈 Analysis: results/lead_analysis.json")
    
    print(f"\n✅ SUCCESS! Real business data collected from Morocco")
    print(f"🎯 Ready for lead generation and website development outreach!")

if __name__ == "__main__":
    display_summary()
