# Business Lead Finder

A powerful CLI tool to find local businesses without websites in Morocco. Built specifically for French-speaking businesses with smart lead scoring that prioritizes 2-3 star businesses (highest opportunity).

## 🚀 Super Quick Start

**1. Run Setup:**
```bash
setup.bat
```

**2. Start Finding Leads:**
```bash
blf                          # Interactive mode
blf restaurants marrakech    # Quick search
blf cafes casablanca        # Find cafes
blf demo                    # See all features
```

That's it! See [QUICK_START.md](QUICK_START.md) for more details.

## 🎯 Overview

Business Lead Finder helps web developers and digital agencies discover high-quality business prospects by:

- **Finding businesses without websites** - Your biggest opportunities
- **Smart lead scoring** - Low-rated businesses (2-3 stars) score highest
- **French language support** - Perfect for Morocco's market
- **Morocco-specific patterns** - Supports .ma domains and local business patterns
- **Professional reports** - Export-ready data for CRM or outreach

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.8+ installed
- Internet connection
- No credit card required for basic functionality

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/business-lead-finder.git
cd business-lead-finder

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env
```

### 3. Easy Setup (Recommended)

Run the setup script to create the `blf` command:

```bash
# Run setup (Windows)
setup.bat

# Now you can use short commands anywhere:
blf                          # Interactive mode
blf restaurants marrakech    # Quick search
blf cafes casablanca        # Find cafes
blf demo                    # Run demo
```

### 4. Alternative Ways to Run

**Method 1: Short batch command**
```bash
blf.bat                      # Interactive mode
blf.bat restaurants marrakech # Quick search
```

**Method 2: Python launcher**
```bash
python blf.py               # Quick launcher
```

**Method 3: Traditional method**
```bash
python main.py              # Standard way
```

### 5. First Run

```bash
# Interactive mode (recommended for beginners)
blf
# or
python main.py

# Direct search
blf restaurants marrakech
# or  
python main.py restaurants marrakech
```

## 🖥️ CLI Commands Guide

### Simple Commands (After Setup)

**Interactive Mode**
```bash
blf                    # Start interactive mode
```

**Quick Search**
```bash
blf restaurants marrakech    # Find restaurants in Marrakech
blf cafes casablanca        # Find cafes in Casablanca  
blf hotels fez               # Find hotels in Fez
blf spas rabat               # Find spas in Rabat
```

**Demo & Help**
```bash
blf demo                     # Run demonstration
blf --help                   # Show help
```

### Interactive Mode

**Best for beginners** - Guided experience with prompts

```bash
blf
# or
python main.py
```

**What it does:**
- Prompts for location (default: Marrakesh, Morocco)
- Shows available categories (restaurants, hotels, cafes, etc.)  
- Asks for number of results
- Guides you through the entire process

### Advanced Commands

**Find businesses by location and category**

```bash
# Traditional format (still supported)
python main.py search --location "Marrakesh, Morocco" --categories restaurants hotels --max-results 50 --output results/leads.json
```

**Parameters:**
- `--location, -l` (required): Target location
- `--categories, -c` (required): Business types to search (space-separated)
- `--max-results, -m`: Maximum results per category (default: 50)
- `--output, -o`: Save results to file
- `--format, -f`: Output format (json, csv)

**Examples:**
```bash
# Search restaurants only
python main.py search -l "Marrakesh, Morocco" -c restaurants

# Search multiple categories
python main.py search -l "Casablanca, Morocco" -c restaurants hotels spas cafes

# Save results to specific file
python main.py search -l "Marrakesh, Morocco" -c hotels -o hotel_leads.json

# Limit results and save as CSV
python main.py search -l "Marrakesh, Morocco" -c restaurants -m 20 -f csv -o restaurants.csv
```

### Check Command

**Verify if a specific business has a website**

```bash
python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"
```

**Parameters:**
- `--business-name, -n` (required): Name of business to check
- `--phone, -p`: Business phone number (helps verification)
- `--address, -a`: Business address (improves accuracy)

**Examples:**
```bash
# Basic website check
python main.py check -n "Riad Zitoun"

# Enhanced check with contact info
python main.py check -n "Restaurant Atlas" -p "+212524443322" -a "Medina, Marrakesh"
```

### Report Command

**Generate professional HTML reports**

```bash
python main.py report --input results/leads.json --output reports/business_report.html
```

**Parameters:**
- `--input, -i` (required): Input data file (JSON format)
- `--output, -o`: Output report file path
- `--format, -f`: Report format (html, pdf, json)
- `--template`: Custom template to use

**Examples:**
```bash
# Generate HTML report (opens in browser)
python main.py report -i leads.json -o report.html

# Generate PDF report
python main.py report -i leads.json -o report.pdf -f pdf

# Auto-generate output name
python main.py report -i results/hotel_leads.json
```

### Export Command

**Export data to various formats**

```bash
python main.py export --input results/leads.json --output exports/leads.csv --format csv
```

**Parameters:**
- `--input, -i` (required): Input data file
- `--output, -o` (required): Output file path
- `--format, -f` (required): Export format (csv, json, xlsx, vcf)
- `--filter`: Filter criteria (e.g., "no_website=true")

**Examples:**
```bash
# Export to Excel-compatible CSV
python main.py export -i leads.json -o leads.csv -f csv

# Export only businesses without websites
python main.py export -i leads.json -o no_website_leads.csv -f csv --filter "no_website=true"

# Export contact cards (VCF format)
python main.py export -i leads.json -o contacts.vcf -f vcf

# Export to Excel
python main.py export -i leads.json -o data.xlsx -f xlsx
```

### Analyze Command

**Analyze existing lead data**

```bash
python main.py analyze --input results/leads.json
```

**Parameters:**
- `--input, -i` (required): Input data file to analyze
- `--output, -o`: Save analysis to file
- `--metrics`: Specific metrics to analyze

**Examples:**
```bash
# Basic analysis
python main.py analyze -i leads.json

# Save analysis results
python main.py analyze -i leads.json -o analysis_report.json

# Analyze specific metrics
python main.py analyze -i leads.json --metrics conversion_potential market_saturation
```

### Help Commands

**Get help for any command**

```bash
# General help
python main.py --help

# Help for specific command
python main.py search --help
python main.py report --help
python main.py export --help
```

## 📊 Understanding Your Results

### Lead Scoring System

Each business gets a score from 0-100 based on:

- **Rating (30 points)**: Higher rated businesses are more likely to invest
- **Reviews (20 points)**: More reviews = established business
- **Website Absence (25 points)**: No website = your opportunity
- **Category (15 points)**: Some business types have higher potential
- **Social Media (10 points)**: Shows tech-savviness

**Score Interpretation:**
- **90-100**: 🔥 Excellent leads - Top priority
- **70-89**: ⭐ Good leads - Strong potential
- **50-69**: 📈 Medium leads - Worth considering  
- **Below 50**: 📋 Low priority - Contact when capacity allows

### File Outputs

**JSON Files:**
- Raw data for further processing
- Used as input for other commands
- Contains all business information

**HTML Reports:**
- Professional presentation format
- Open in any web browser
- Perfect for client presentations

**CSV Files:**
- Excel-compatible format
- Easy to sort and filter
- Import into CRM systems

## 🎯 Practical Workflow Examples

### Scenario 1: New Market Research

```bash
# 1. Search for businesses in new city
python main.py search -l "Casablanca, Morocco" -c restaurants hotels -o casablanca_leads.json

# 2. Generate professional report
python main.py report -i casablanca_leads.json -o casablanca_market_report.html

# 3. Export high-priority leads to CSV
python main.py export -i casablanca_leads.json -o priority_leads.csv -f csv --filter "lead_score>=70"

# 4. Analyze market opportunity
python main.py analyze -i casablanca_leads.json -o market_analysis.json
```

### Scenario 2: Daily Lead Generation

```bash
# Morning routine - find today's leads
python main.py search -l "Marrakesh, Morocco" -c restaurants cafes -m 30 -o daily_leads.json

# Check a specific business someone mentioned
python main.py check -n "Café Central" -p "+212524567890"

# Generate daily report
python main.py report -i daily_leads.json -o daily_report_$(date +%Y%m%d).html
```

### Scenario 3: Client Presentation Prep

```bash
# Comprehensive search for presentation
python main.py search -l "Marrakesh, Morocco" -c restaurants hotels spas -m 100 -o presentation_data.json

# Generate beautiful HTML report
python main.py report -i presentation_data.json -o client_presentation.html

# Export contact sheet for follow-up
python main.py export -i presentation_data.json -o contact_list.csv -f csv
```

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file with your configuration:

```env
# Default search location
DEFAULT_LOCATION=Marrakesh, Morocco

# Search limits
MAX_RESULTS_PER_SEARCH=50
DELAY_BETWEEN_REQUESTS=1

# Free API keys (optional - improves results)
SERPAPI_KEY=your_free_serpapi_key
FOURSQUARE_CLIENT_ID=your_free_foursquare_id
FOURSQUARE_CLIENT_SECRET=your_free_foursquare_secret

# Premium APIs (optional)
GOOGLE_PLACES_API_KEY=your_google_places_key
YELP_API_KEY=your_yelp_key

# Output preferences
EXPORT_FORMAT=csv,json
REPORT_FORMAT=html
```

### Command Aliases

Create shortcuts for frequent commands:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
alias bf-search='python /path/to/business-lead-finder/main.py search'
alias bf-report='python /path/to/business-lead-finder/main.py report'
alias bf-check='python /path/to/business-lead-finder/main.py check'

# Usage:
bf-search -l "Marrakesh, Morocco" -c restaurants
bf-report -i leads.json -o report.html
```

## 📁 Project Structure

```
business-lead-finder/
├── main.py                 # Main CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── CLI_GUIDE.md          # Detailed CLI documentation
├── .vscode/
│   └── coding_rules.md   # Development guidelines
├── src/                  # Source code
│   ├── cli_interface.py  # CLI command handling
│   ├── business_search.py # Business search logic
│   ├── website_checker.py # Website detection
│   ├── data_processor.py # Data processing & export
│   ├── report_generator.py # Report generation
│   ├── utils.py         # Utility functions
│   ├── simple_cli.py    # Fallback CLI (no dependencies)
│   └── config/
│       └── settings.py  # Configuration management
├── results/             # Search results storage
│   ├── sample_leads.json
│   ├── leads_report.html
│   └── leads.csv
└── logs/               # Application logs
    └── business_finder.log
```

## 🆓 Free Implementation

This tool works completely **free without any credit card** using:

### Primary Data Sources (100% Free)

1. **OpenStreetMap Nominatim**
   - Unlimited geocoding and business search
   - Global coverage including Morocco
   - No API key required

2. **Public Business Directories**
   - Web scraping of public listings
   - Contact information extraction
   - Social media profile detection

3. **Search Engine Results**
   - Public business information
   - Website detection algorithms
   - Review aggregation

### Optional Premium Upgrades

1. **SerpAPI** (100 searches/month free)
   - Enhanced search results
   - More accurate business data

2. **Foursquare Places** (1000 requests/day free)
   - Rich business information
   - Better categorization

3. **Google Places API** (Premium)
   - Highest quality data
   - Real-time information

## 🎯 Target Market: Morocco

### Optimized for Moroccan Businesses

- **Primary Cities**: Marrakesh, Casablanca, Rabat, Fez
- **Key Sectors**: Tourism, Hospitality, Food & Beverage
- **Language Support**: French, Arabic, English business names
- **Cultural Considerations**: Riad vs Hotel classification

### High-Opportunity Categories

1. **Restaurants & Cafes** - Low website adoption, high potential
2. **Hotels & Riads** - Direct booking opportunities
3. **Spas & Wellness** - Growing sector, tech adoption
4. **Tour Operators** - High-value, seasonal business
5. **Retail Shops** - E-commerce opportunities

## ⚠️ Important Notes

### Rate Limiting

The tool includes automatic rate limiting to respect API guidelines:
- 1-second delay between requests by default
- Configurable via environment variables
- Prevents account suspension

### Data Accuracy

- Business information accuracy depends on source quality
- Website detection is comprehensive but not 100% perfect
- Phone numbers and addresses should be verified before outreach
- Regular data refresh recommended for active campaigns

### Legal Compliance

- All data sources are publicly available
- Respects robots.txt and API terms of service
- No unauthorized scraping or data collection
- Users responsible for GDPR/privacy compliance in outreach

## 🚀 Getting Started Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned and dependencies installed
- [ ] Test run with `python main.py interactive`
- [ ] First search completed for Marrakesh restaurants
- [ ] HTML report generated and reviewed
- [ ] Contact data exported to CSV
- [ ] Ready for business outreach!

## 📞 Support & Community

- **Issues**: GitHub Issues for bug reports
- **Features**: GitHub Discussions for feature requests  
- **Documentation**: Check CLI_GUIDE.md for detailed examples
- **Code**: See .vscode/coding_rules.md for contribution guidelines

---

**Start finding your next clients in the Marrakesh market today!** 🇲🇦✨
