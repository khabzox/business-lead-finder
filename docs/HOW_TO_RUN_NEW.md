# 🚀 How to Run Business Lead Finder

This guide shows you all the different ways to run the Business Lead Finder, from the simplest one-command approach to advanced configuration options.

## ⚡ Super Quick Start (Recommended)

### Option 1: Setup Once, Use Anywhere

```bash
# Run setup first (only once needed)
setup.bat

# Now you can use 'blf' from anywhere on your system!
blf                          # Interactive mode with guided prompts
blf restaurants marrakech    # Quick search for restaurants
blf cafes casablanca        # Find cafes in Casablanca
blf demo                    # Comprehensive feature demonstration
```

**Benefits:**
- ✅ Works from any directory
- ✅ Shortest commands possible
- ✅ Auto-completion support
- ✅ Professional workflow

### Option 2: Direct Commands (No Setup)

```bash
# Works immediately without any setup
blf.bat                      # Interactive mode
blf.bat restaurants marrakech # Quick targeted search
blf.bat demo                # Feature demonstration
```

**Benefits:**
- ✅ No configuration required
- ✅ Portable across systems
- ✅ Immediate availability
- ✅ Perfect for testing

## 🛠️ Alternative Launch Methods

### Python Methods

#### Standard Python Execution

```bash
python main.py              # Main entry point
python main.py --help       # Show all available commands
python main.py restaurants marrakech 10  # Direct search
```

#### Quick Python Launcher

```bash
python blf.py               # Quick launcher with shortcuts
```

### PowerShell (Windows)

```powershell
# PowerShell version with enhanced features
.\blf.ps1                   # Interactive mode
.\blf.ps1 restaurants marrakech  # Quick search
```

### Advanced Python Commands

```bash
# Full command syntax with all options
python main.py search --location "Marrakesh, Morocco" --categories restaurants --max-results 20 --output results.json

# Check specific business
python main.py check --business-name "Restaurant Atlas" --phone "+212524443322"

# Generate report
python main.py report --input results.json --output report.html
```

## ✨ Command Examples by Use Case

### Interactive Mode (Best for Beginners)

```bash
# Start guided experience
blf
# or
python main.py
```

**What happens:**
1. Prompts for target location (default: Marrakesh, Morocco)
2. Shows available business categories
3. Asks for number of results desired
4. Displays results in formatted table
5. Offers export options

### Quick Searches (Most Common)

```bash
# Format: blf [category] [city] [optional: count]
blf restaurants marrakech   # Find restaurants in Marrakech
blf cafes casablanca       # Find cafes in Casablanca
blf hotels fez             # Find hotels in Fez
blf spas rabat 15          # Find 15 spas in Rabat
blf demo                   # See all features in action
```

### Advanced Searches

```bash
# Multiple categories
python main.py search -l "Marrakesh, Morocco" -c restaurants hotels cafes

# Save to specific file
python main.py search -l "Casablanca, Morocco" -c restaurants -o casablanca_restaurants.json

# Export as CSV
python main.py search -l "Marrakesh, Morocco" -c hotels -f csv -o hotels.csv

# Limit results
python main.py search -l "Rabat, Morocco" -c spas -m 10
```

### Google Maps Integration

```bash
# Enhanced search with Google Maps
python main.py search --location "Marrakesh, Morocco" --categories restaurants --use-google-maps

# Google Maps only (maximum email discovery)
python main.py search --location "Casablanca, Morocco" --categories hotels --google-maps-only

# Combined with AI analysis
python main.py search --location "Fez, Morocco" --categories spas --use-google-maps --ai-analysis
```

## 🇲🇦 Morocco Multi-City Options

### Quick City Search

```bash
# Search specific cities
quick_city.bat marrakesh           # Standard search
quick_city.bat casablanca mega     # MEGA search mode
```

### All Cities at Once

```bash
# Search all 10 major Morocco cities
search_all_cities.bat              # Standard size for all cities
python quick_search/quick_all_cities_search.py --all-cities --search-size mega
```

### Interactive City Selection

```bash
# Menu-driven city selection
quick_search.bat                   # Windows batch
quick_search.ps1                   # PowerShell version
python quick_search/quick_all_cities_search.py --interactive
```

## 📊 Report and Export Commands

### Generate Reports

```bash
# HTML report (opens in browser)
python main.py report -i results/leads.json -o report.html

# PDF report
python main.py report -i results/leads.json -o report.pdf -f pdf
```

### Export Data

```bash
# CSV export (Excel-compatible)
python main.py export -i results/leads.json -o leads.csv -f csv

# VCF contacts (address book)
python main.py export -i results/leads.json -o contacts.vcf -f vcf

# Excel format
python main.py export -i results/leads.json -o data.xlsx -f xlsx
```

### Analysis Commands

```bash
# Analyze lead quality
python main.py analyze -i results/leads.json

# Save analysis
python main.py analyze -i results/leads.json -o analysis.json
```

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file for custom settings:

```env
# Default location
DEFAULT_LOCATION=Marrakesh, Morocco

# Search limits
MAX_RESULTS_PER_SEARCH=50
DELAY_BETWEEN_REQUESTS=1

# Optional API keys (improve results)
SERPAPI_KEY=your_free_key
GOOGLE_PLACES_API_KEY=your_key
```

### Command Line Configuration

```bash
# Override default location
python main.py search -l "Tangier, Morocco" -c restaurants

# Increase result limit
python main.py search -l "Marrakesh, Morocco" -c hotels -m 100

# Change output format
python main.py search -l "Casablanca, Morocco" -c cafes -f csv
```

## 🚨 Troubleshooting Common Issues

### Issue: "blf command not found"

**Solution:**
```bash
# Run setup again
setup.bat

# Or use direct command
blf.bat restaurants marrakech
```

### Issue: "No results found"

**Solutions:**
```bash
# Try different city
blf restaurants casablanca

# Try different category
blf hotels marrakech

# Increase search limit
python main.py search -l "Marrakesh, Morocco" -c restaurants -m 100
```

### Issue: "Slow performance"

**Solutions:**
```bash
# Reduce search size
python main.py search -l "Marrakesh, Morocco" -c restaurants -m 20

# Add delays
echo "DELAY_BETWEEN_REQUESTS=2" >> .env

# Use test mode for quick results
python quick_search/quick_all_cities_search.py --city marrakesh --search-size test
```

### Issue: "Rate limiting errors"

**Solutions:**
```bash
# Increase delay in .env file
echo "DELAY_BETWEEN_REQUESTS=3" >> .env

# Use smaller batch sizes
python main.py search -l "Marrakesh, Morocco" -c restaurants -m 25
```

## 📝 Getting Help

### Built-in Help

```bash
# General help
blf --help
python main.py --help

# Command-specific help
python main.py search --help
python main.py report --help
python main.py export --help
```

### Quick Reference

```bash
# Show all available commands
blf demo

# List supported cities
python quick_search/quick_all_cities_search.py --list-cities

# Test your setup
blf restaurants marrakech 2
```

## 🎯 Recommended Workflows

### First-Time Users

1. **Setup**: Run `setup.bat`
2. **Test**: Try `blf demo`
3. **Practice**: Run `blf restaurants marrakech 5`
4. **Explore**: Try `blf --help`

### Daily Usage

1. **Morning leads**: `blf restaurants marrakech 10`
2. **Generate report**: `python main.py report -i results/*.json -o daily_report.html`
3. **Export contacts**: `python main.py export -i results/*.json -o contacts.csv -f csv`

### Advanced Users

1. **Multi-city search**: `search_all_cities.bat`
2. **Custom analysis**: `python main.py analyze -i results/*.json`
3. **Automated reporting**: Schedule with Task Scheduler

---

**Choose the method that works best for your workflow!** 🚀

For more information:
- [QUICK_START.md](QUICK_START.md) - Complete beginner guide
- [CLI_GUIDE.md](CLI_GUIDE.md) - Full command reference
- [FEATURES.md](FEATURES.md) - All available features
