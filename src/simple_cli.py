"""
Simple CLI Interface for Business Lead Finder (No Rich dependency)
Basic command-line interface for testing when rich is not available.
"""

import argparse
import sys
from typing import Dict, Any, Optional

def create_basic_cli_parser() -> argparse.ArgumentParser:
    """Create basic command line interface parser."""
    parser = argparse.ArgumentParser(
        description='Business Lead Finder - Find businesses without websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels
  python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
  python main.py report --input data/leads.json --output results/report.html
  python main.py export --format csv --output results/leads.csv
  python main.py interactive
        '''
    )
    
    # Add common arguments
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for businesses')
    search_parser.add_argument('--location', '-l', required=True, help='Location to search')
    search_parser.add_argument('--categories', '-cat', nargs='+', required=True, 
                               help='Business categories to search')
    search_parser.add_argument('--max-results', '-m', type=int, default=50, 
                               help='Maximum results per category')
    search_parser.add_argument('--output', '-o', help='Output file path')
    search_parser.add_argument('--format', '-f', choices=['json', 'csv', 'html'], 
                               default='json', help='Output format')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check website status')
    check_parser.add_argument('--business-name', '-n', required=True, help='Business name')
    check_parser.add_argument('--phone', '-p', help='Business phone number')
    check_parser.add_argument('--address', '-a', help='Business address')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('--input', '-i', required=True, help='Input data file')
    report_parser.add_argument('--output', '-o', required=True, help='Output report file')
    report_parser.add_argument('--format', '-f', choices=['html', 'pdf', 'json'], 
                               default='html', help='Report format')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--input', '-i', required=True, help='Input data file')
    export_parser.add_argument('--output', '-o', required=True, help='Output file')
    export_parser.add_argument('--format', '-f', choices=['csv', 'json', 'xlsx'], 
                               default='csv', help='Export format')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    
    return parser

def handle_basic_cli_command(args, config: Dict[str, Any]) -> bool:
    """Handle CLI commands with basic functionality."""
    try:
        if args.command == 'search':
            return handle_search_command(args, config)
        elif args.command == 'check':
            return handle_check_command(args, config)
        elif args.command == 'report':
            return handle_report_command(args, config)
        elif args.command == 'export':
            return handle_export_command(args, config)
        elif args.command == 'interactive':
            return handle_interactive_command(args, config)
        else:
            print(f"Unknown command: {args.command}")
            return False
    except Exception as e:
        print(f"Error handling command: {e}")
        return False

def handle_search_command(args, config: Dict[str, Any]) -> bool:
    """Handle search command."""
    print(f"🔍 Searching for {', '.join(args.categories)} in {args.location}...")
    print(f"📊 Max results per category: {args.max_results}")
    
    # For now, create sample data
    sample_businesses = [
        {
            "name": "Restaurant Atlas",
            "category": "restaurant",
            "address": "Medina, Marrakesh",
            "phone": "+212 5 24 44 33 22",
            "rating": 4.2,
            "review_count": 127,
            "website": None,
            "lead_score": 85
        },
        {
            "name": "Riad Zitoun",
            "category": "hotel",
            "address": "Derb Zitoun, Marrakesh",
            "phone": "+212 5 24 38 91 40",
            "rating": 4.5,
            "review_count": 89,
            "website": None,
            "lead_score": 92
        }
    ]
    
    print(f"\n✅ Found {len(sample_businesses)} businesses")
    for business in sample_businesses:
        website_status = "❌ NO WEBSITE" if not business['website'] else "✅ Has website"
        print(f"  📍 {business['name']} - {business['rating']}/5 stars - {website_status}")
    
    # Save results if output specified
    if args.output:
        import json
        import os
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(sample_businesses, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {args.output}")
    
    return True

def handle_check_command(args, config: Dict[str, Any]) -> bool:
    """Handle website check command."""
    print(f"🔍 Checking website status for: {args.business_name}")
    
    # Simple website check simulation
    website_found = False  # Simulate no website found
    
    if website_found:
        print("✅ Website found!")
    else:
        print("❌ No website found - This is a potential lead!")
        print("💡 Opportunity: This business could benefit from a professional website")
    
    return True

def handle_report_command(args, config: Dict[str, Any]) -> bool:
    """Handle report generation command."""
    print(f"📊 Generating {args.format} report from {args.input}...")
    
    try:
        import json
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📈 Processing {len(data)} business records...")
        
        # Simple report generation
        if args.format == 'html':
            generate_simple_html_report(data, args.output)
        else:
            print(f"📄 {args.format} format not implemented yet")
        
        print(f"✅ Report saved to {args.output}")
        return True
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False

def handle_export_command(args, config: Dict[str, Any]) -> bool:
    """Handle data export command."""
    print(f"📤 Exporting data from {args.input} to {args.format} format...")
    
    try:
        import json
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if args.format == 'csv':
            export_to_csv(data, args.output)
        elif args.format == 'json':
            import shutil
            shutil.copy(args.input, args.output)
        else:
            print(f"❌ Format {args.format} not supported yet")
            return False
        
        print(f"✅ Data exported to {args.output}")
        return True
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def handle_interactive_command(args, config: Dict[str, Any]) -> bool:
    """Handle interactive mode."""
    print("🎯 Welcome to Business Lead Finder Interactive Mode!")
    print("=" * 50)
    
    try:
        location = input("📍 Enter location (e.g., 'Marrakesh, Morocco'): ").strip()
        if not location:
            location = "Marrakesh, Morocco"
        
        print("\n📋 Available categories:")
        categories = ["restaurants", "hotels", "cafes", "spas", "shops", "services"]
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        cat_input = input("\n🔢 Enter category numbers (comma-separated, e.g., 1,2,3): ").strip()
        selected_categories = []
        if cat_input:
            for num in cat_input.split(','):
                try:
                    idx = int(num.strip()) - 1
                    if 0 <= idx < len(categories):
                        selected_categories.append(categories[idx])
                except ValueError:
                    pass
        
        if not selected_categories:
            selected_categories = ["restaurants", "hotels"]
        
        max_results = input("\n📊 Max results per category (default 20): ").strip()
        if not max_results:
            max_results = 20
        else:
            try:
                max_results = int(max_results)
            except ValueError:
                max_results = 20
        
        print(f"\n🚀 Starting search...")
        print(f"📍 Location: {location}")
        print(f"📋 Categories: {', '.join(selected_categories)}")
        print(f"📊 Max results: {max_results}")
        
        # Simulate the search
        import time
        time.sleep(1)
        
        print("\n✅ Search completed!")
        print("💡 Use 'python main.py search' for full functionality")
        
        return True
    except KeyboardInterrupt:
        print("\n\n👋 Interactive mode cancelled.")
        return True

def generate_simple_html_report(data, output_path):
    """Generate a simple HTML report."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Business Lead Finder Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: #007bff; color: white; padding: 20px; }}
            .business {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
            .no-website {{ background: #fff3cd; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Business Lead Finder Report</h1>
            <p>Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        <h2>📊 Found {len(data)} businesses</h2>
    """
    
    for business in data:
        website_status = "❌ NO WEBSITE" if not business.get('website') else "✅ Has website"
        no_website_class = "no-website" if not business.get('website') else ""
        
        html_content += f"""
        <div class="business {no_website_class}">
            <h3>{business.get('name', 'Unknown')}</h3>
            <p><strong>Category:</strong> {business.get('category', 'N/A')}</p>
            <p><strong>Address:</strong> {business.get('address', 'N/A')}</p>
            <p><strong>Phone:</strong> {business.get('phone', 'N/A')}</p>
            <p><strong>Rating:</strong> {business.get('rating', 'N/A')}/5</p>
            <p><strong>Website:</strong> {website_status}</p>
            <p><strong>Lead Score:</strong> {business.get('lead_score', 0)}/100</p>
        </div>
        """
    
    html_content += "</body></html>"
    
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def export_to_csv(data, output_path):
    """Export data to CSV format."""
    import csv
    import os
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not data:
        return
    
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
