# Business Lead Finder

A powerful command-line tool to find local businesses without websites and identify potential clients for web development services.

## 🎯 Overview

Business Lead Finder helps web developers and digital agencies discover high-quality business prospects by:

- **Finding businesses without websites** - Your biggest opportunities
- **Scoring leads automatically** - Prioritize your outreach efforts  
- **Generating professional reports** - Present findings to clients or team
- **Exporting contact data** - Ready for CRM import or calling campaigns
- **Supporting multiple data sources** - Free APIs prioritized, no credit card required

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
# Edit .env with your preferred settings
```

### 3. First Run

```bash
# Interactive mode (recommended for beginners)
python main.py interactive

# Or direct search
python main.py search --location "Your City" --categories restaurants hotels
```

## 🖥️ CLI Commands

### Basic Commands

- **Interactive Mode**: `python main.py interactive`
- **Search**: `python main.py search --location "City" --categories restaurants hotels`
- **Generate Report**: `python main.py report --input results/leads.json --output report.html`
- **Export Data**: `python main.py export --input results/leads.json --output leads.csv --format csv`
- **Check Website**: `python main.py check --business-name "Business Name"`

### Get Detailed Help

```bash
# See all commands
python main.py --help

# Get help for specific command
python main.py search --help
python main.py report --help
```

**📖 For complete CLI documentation, see [docs/CLI_GUIDE.md](docs/CLI_GUIDE.md)**

## 📊 Features

### Lead Scoring System (0-100 points)
- **Rating Weight**: 30 points
- **Review Count**: 20 points  
- **Website Absence**: 25 points
- **Business Category**: 15 points
- **Social Media Presence**: 10 points

### Output Formats
- **JSON**: Raw data for processing
- **HTML**: Professional reports for presentations
- **CSV**: Excel-compatible for analysis
- **VCF**: Contact cards for import

### Data Sources
- **Free APIs**: OpenStreetMap, public directories
- **Optional Premium**: Google Places, Yelp, SerpAPI
- **Web Scraping**: Public business listings

## 📁 Project Structure

```
business-lead-finder/
├── main.py                 # CLI entry point
├── requirements.txt        # Dependencies
├── .env.example           # Configuration template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── .vscode/
│   └── rules/
│       └── coding_rules.md # Development guidelines
├── src/                  # Source code
│   ├── cli_interface.py  # CLI commands
│   ├── business_search.py # Search logic
│   ├── website_checker.py # Website detection
│   ├── data_processor.py # Data processing
│   ├── report_generator.py # Report generation
│   ├── simple_cli.py    # Basic CLI fallback
│   ├── utils.py         # Utilities
│   └── config/
│       └── settings.py  # Configuration
├── docs/                # Documentation
│   ├── CLI_GUIDE.md    # Detailed CLI guide
│   └── FEATURES.md     # Feature documentation
├── results/            # Generated outputs
└── logs/              # Application logs
```

## 🔧 Configuration

### Environment Variables (.env file)

```env
# Basic Configuration
DEFAULT_LOCATION=Your Default City
MAX_RESULTS_PER_SEARCH=50
DELAY_BETWEEN_REQUESTS=1

# Free API Keys (Optional)
SERPAPI_KEY=your_free_key
FOURSQUARE_CLIENT_ID=your_id
FOURSQUARE_CLIENT_SECRET=your_secret

# Premium APIs (Optional)
GOOGLE_PLACES_API_KEY=your_key
YELP_API_KEY=your_key

# Output Settings
EXPORT_FORMAT=csv,json
REPORT_FORMAT=html
```

### Business Categories

Configurable in `src/config/settings.py`:
- High Priority: restaurants, hotels, cafes, spas
- Medium Priority: shops, services, entertainment
- Custom categories can be added

## 🆓 Free Implementation

This tool works completely **free without any credit card**:

### Free Data Sources
1. **OpenStreetMap Nominatim** - Unlimited geocoding
2. **Public Business Directories** - Web scraping
3. **Search Engine Results** - Public information
4. **Social Media APIs** - Basic business info

### Optional Upgrades
1. **SerpAPI** - 100 free searches/month
2. **Foursquare** - 1000 free requests/day
3. **Google Places** - Premium accuracy

## 🎯 Use Cases

### Web Development Agencies
- Find businesses without websites
- Generate client prospect lists
- Create market analysis reports
- Track outreach campaigns

### Freelance Developers
- Discover local opportunities
- Build client pipeline
- Research competition
- Prepare sales presentations

### Digital Marketing
- Identify businesses needing online presence
- Analyze market gaps
- Generate lead lists
- Export to CRM systems

## 🚀 Development

### Coding Standards
- **No Classes**: Function-only architecture
- **Type Hints**: Full type annotation
- **Error Handling**: Comprehensive try-catch
- **Logging**: Structured logging throughout
- **Documentation**: Docstrings for all functions

**📖 See [.vscode/rules/coding_rules.md](.vscode/rules/coding_rules.md) for complete guidelines**

### Testing
```bash
# Run basic functionality test
python main.py interactive

# Test search functionality
python main.py search --location "Test City" --categories restaurants --max-results 5

# Generate sample report
python main.py report --input results/sample_leads.json --output test_report.html
```

## 📞 Support

- **Documentation**: Check [docs/](docs/) folder
- **Issues**: GitHub Issues for bug reports
- **Features**: GitHub Discussions for requests
- **Code**: Follow [coding rules](.vscode/rules/coding_rules.md)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Ready to find your next clients? Start with `python main.py interactive`** 🚀
