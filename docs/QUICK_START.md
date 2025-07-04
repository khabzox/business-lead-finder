# 🚀 Business Lead Finder - Quick Start Guide

Welcome to the Business Lead Finder! This guide will get you up and running in minutes to start finding high-quality business leads in Morocco.

## ⚡ Super Quick Start (30 seconds)

### 1. One-Command Setup

```bash
setup.bat
```

### 2. Start Finding Leads

```bash
# Interactive mode (best for beginners)
blf

# Quick targeted search
blf restaurants marrakech

# Find cafes in Casablanca
blf cafes casablanca

# See all features
blf demo
```

## 🎯 What You'll Get

- **Businesses without websites** - Your biggest opportunities
- **Smart lead scoring** - 2-3 star businesses get highest priority
- **Contact information** - Names, phones, addresses, emails
- **Professional reports** - Ready for client presentations
- **Export options** - CSV, JSON, Excel formats

## 🖥️ Command Options

### Interactive Mode (Recommended for Beginners)

```bash
blf
# or
python main.py
```

**What happens:**

1. Prompts for location (default: Marrakesh, Morocco)
2. Shows business categories (restaurants, hotels, cafes, etc.)
3. Asks for number of results
4. Guides you through the process
5. Shows results in a beautiful table
6. Offers to export data

### Quick Search Mode

```bash
# Format: blf [category] [city] [optional: number]
blf restaurants marrakech     # Find restaurants in Marrakesh
blf hotels casablanca        # Find hotels in Casablanca
blf cafes fez 10             # Find 10 cafes in Fez
blf spas rabat               # Find spas in Rabat
```

### Advanced Commands

```bash
# Full command format
python main.py search --location "Marrakesh, Morocco" --categories restaurants --max-results 20

# Save results to file
python main.py search -l "Casablanca, Morocco" -c hotels -o hotel_leads.json

# Export to CSV
python main.py search -l "Marrakesh, Morocco" -c restaurants -f csv -o restaurants.csv
```

## 🇲🇦 Morocco Cities Quick Search

### Available Cities

- **Marrakesh** - Tourist capital, high restaurant opportunity
- **Casablanca** - Business hub, diverse opportunities
- **Rabat** - Political capital, government services
- **Fez** - Cultural center, traditional businesses
- **Tangier** - Port city, international businesses
- **Agadir** - Beach resort, hospitality focus
- **Meknes** - Imperial city, tourism potential
- **Oujda** - Eastern gateway, cross-border trade
- **Tetouan** - Northern culture, artisan businesses
- **Essaouira** - Coastal charm, tourism and crafts

### Multi-City Search

```bash
# Search all major cities (organized by city)
search_all_cities.bat

# Interactive city selection
quick_search.bat

# PowerShell version
quick_search.ps1
```

## 📊 Understanding Your Results

### Lead Scoring (0-100 points)

- **90-100**: 🔥 **Excellent** - Contact immediately
- **70-89**: ⭐ **Good** - High potential leads
- **50-69**: 📈 **Medium** - Worth considering
- **Below 50**: 📋 **Low** - Contact when capacity allows

### What Makes a High Score?

1. **No Website** (25 points) - Your biggest opportunity
2. **2-3 Star Rating** (30 points) - Ready for improvement
3. **Multiple Reviews** (20 points) - Established business
4. **High-Value Category** (15 points) - Hotels, restaurants
5. **Social Media Presence** (10 points) - Tech-aware

## 📁 File Outputs

### Result Files (in `results/` folder)

- **JSON files** - Raw data for further processing
- **CSV files** - Excel-compatible, easy to sort
- **HTML reports** - Professional presentation format

### Example Output

```text
results/
├── business_leads_20250704_124110.json    # Raw lead data
├── restaurants_Marrakech_20250704.csv     # CSV export
└── cities/
    ├── marrakesh/searches/                 # City-organized results
    └── casablanca/searches/
```

## 🎯 Practical Examples

### Scenario 1: Finding Restaurant Leads in Marrakesh

```bash
# Step 1: Search for restaurants
blf restaurants marrakesh 20

# Step 2: Generate professional report
python main.py report -i results/restaurants_Marrakech_*.json -o marrakesh_restaurants_report.html

# Step 3: Export high-priority leads
python main.py export -i results/restaurants_Marrakech_*.json -o priority_leads.csv -f csv --filter "lead_score>=70"
```

### Scenario 2: Market Research for New City

```bash
# Step 1: Comprehensive search
python main.py search -l "Casablanca, Morocco" -c restaurants hotels cafes -m 50 -o casablanca_market.json

# Step 2: Analyze opportunities
python main.py analyze -i casablanca_market.json

# Step 3: Create presentation
python main.py report -i casablanca_market.json -o casablanca_presentation.html
```

### Scenario 3: Daily Lead Generation

```bash
# Morning routine (find today's leads)
blf restaurants marrakesh 10
blf cafes marrakesh 5

# Check specific business
python main.py check -n "Restaurant Atlas" -p "+212524443322"

# Export for follow-up
python main.py export -i results/daily_*.json -o daily_contacts.csv -f csv
```

## 🗺️ Google Maps Integration

### Enhanced Email Discovery

```bash
# Use Google Maps for email extraction
python main.py search --location "Marrakesh, Morocco" --categories restaurants --use-google-maps

# Google Maps only (maximum email discovery)
python main.py search --location "Casablanca, Morocco" --categories hotels --google-maps-only

# Combined with AI analysis
python main.py search --location "Fez, Morocco" --categories spas --use-google-maps --ai-analysis
```

### Benefits

- **📧 Email Extraction** - Direct contact information
- **📞 Phone Numbers** - Verified contact details
- **🎯 Enhanced Targeting** - Focus on businesses without websites
- **🆓 Free Service** - No API keys required

## 🔧 Configuration

### Environment Setup

Create a `.env` file for your preferences:

```env
# Default location
DEFAULT_LOCATION=Marrakesh, Morocco

# Search preferences
MAX_RESULTS_PER_SEARCH=50
DELAY_BETWEEN_REQUESTS=1

# API keys (optional - improves results)
SERPAPI_KEY=your_free_key
FOURSQUARE_CLIENT_ID=your_id
```

### Common Settings

```bash
# Change default city
echo "DEFAULT_LOCATION=Casablanca, Morocco" >> .env

# Increase search results
echo "MAX_RESULTS_PER_SEARCH=100" >> .env

# Add delay for stability
echo "DELAY_BETWEEN_REQUESTS=2" >> .env
```

## 🆓 Completely Free

- **No credit card required**
- **No API keys needed** for basic functionality
- **Unlimited searches** using public data sources
- **Full feature access** without payment

## ⚠️ Important Tips

### Best Practices

1. **Start Small**: Begin with 10-20 results to test
2. **Use Delays**: Respect rate limits (default: 1 second)
3. **Verify Data**: Double-check contact info before outreach
4. **Regular Updates**: Refresh data monthly for accuracy

### Legal & Ethical Use

- All data comes from public sources
- Respect business privacy in outreach
- Follow local regulations (GDPR, etc.)
- Use for legitimate business purposes only

## 🚨 Troubleshooting

### Common Issues

**Issue**: `blf` command not found
**Solution**: Run `setup.bat` again

**Issue**: No results found
**Solution**: Try a larger city or different category

**Issue**: Slow performance
**Solution**: Reduce `MAX_RESULTS_PER_SEARCH` in `.env`

**Issue**: Rate limiting errors
**Solution**: Increase `DELAY_BETWEEN_REQUESTS` in `.env`

### Getting Help

```bash
# General help
blf --help

# Command-specific help
python main.py search --help
python main.py report --help
```

## 🎉 You're Ready

### Quick Success Checklist

- [ ] Run `setup.bat` ✅
- [ ] Test with `blf demo` ✅
- [ ] Try `blf restaurants marrakech` ✅
- [ ] Generate first report ✅
- [ ] Export to CSV ✅
- [ ] Ready for business outreach! 🚀

---

**Start finding your next clients in Morocco today!** 🇲🇦✨

For more detailed information, see:

- [CLI_GUIDE.md](CLI_GUIDE.md) - Complete command reference
- [GOOGLE_MAPS_CLI_GUIDE.md](GOOGLE_MAPS_CLI_GUIDE.md) - Google Maps features
- [FEATURES.md](FEATURES.md) - All available features
