#!/usr/bin/env python3
"""
Test email fields in sample data
"""

import json
import sys
import os
from rich.console import Console
from rich.table import Table

console = Console()

def test_sample_data_emails():
    """Test that sample data contains email fields"""
    
    console.print("🧪 Testing Sample Data Email Fields")
    
    # Test the sample data we generated
    sample_files = [
        "results/sample_data/casablanca_morocco/restaurants_sample_data.json",
        "results/sample_data/rabat_morocco/cafes_sample_data.json"
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            console.print(f"\n📁 Testing: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                businesses = json.load(f)
            
            console.print(f"📊 Found {len(businesses)} businesses")
            
            # Analyze email fields
            with_email = 0
            with_emails = 0
            with_phone = 0
            with_website = 0
            
            table = Table(title="Sample Business Data")
            table.add_column("Name", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Emails", style="magenta")
            table.add_column("Phone", style="blue")
            table.add_column("Website", style="yellow")
            
            for business in businesses[:5]:  # Show first 5
                name = business.get('name', 'Unknown')[:20]
                email = business.get('email', 'None')
                emails = ', '.join(business.get('emails', []))
                phone = business.get('phone', 'None')
                website = 'Yes' if business.get('website') else 'No'
                
                if business.get('email'):
                    with_email += 1
                if business.get('emails'):
                    with_emails += 1
                if business.get('phone'):
                    with_phone += 1
                if business.get('website'):
                    with_website += 1
                
                table.add_row(name, email[:30], emails[:30], phone, website)
            
            console.print(table)
            
            console.print(f"\n📊 Statistics:")
            console.print(f"• Businesses with email field: {with_email}/{len(businesses)}")
            console.print(f"• Businesses with emails field: {with_emails}/{len(businesses)}")
            console.print(f"• Businesses with phone: {with_phone}/{len(businesses)}")
            console.print(f"• Businesses with website: {with_website}/{len(businesses)}")
            
        else:
            console.print(f"❌ File not found: {file_path}")
    
    console.print(f"\n✅ Email field testing completed!")

if __name__ == "__main__":
    test_sample_data_emails()
