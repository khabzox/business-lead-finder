# Google Maps CLI Integration Guide

## Overview

The Business Lead Finder now includes **Google Maps scraping** as an optional CLI feature, enabling enhanced business discovery with automatic email extraction.

## 🗺️ Google Maps Features

### Enhanced Discovery
- **Email Extraction**: Automatically discover business email addresses
- **Contact Information**: Phone numbers, addresses, ratings
- **Website Detection**: Identify businesses without websites
- **FREE Service**: No API keys or payments required

### Integration Options
1. **Standard Search**: Use existing data sources only
2. **Enhanced Search**: Combine standard + Google Maps  
3. **Google Maps Only**: Use Google Maps scraping exclusively

## 📋 Prerequisites

### Install Dependencies
```powershell
pip install selenium
```

### Download Chrome WebDriver
1. Visit: https://chromedriver.chromium.org/
2. Download version matching your Chrome browser
3. Add to PATH or place in project directory

## 🚀 CLI Usage

### Basic Commands

#### Standard Search (existing functionality)
```powershell
python main.py search --location "Marrakesh, Morocco" --categories restaurants --filter no-website
```

#### Enhanced Search (Standard + Google Maps)
```powershell
python main.py search --location "Marrakesh, Morocco" --categories hotels --use-google-maps
```

#### Google Maps Only (with email discovery)
```powershell
python main.py search --location "Casablanca, Morocco" --categories spas --google-maps-only --max-results 10
```

### Advanced Options

#### Combined with AI Analysis
```powershell
python main.py search --location "Fez, Morocco" --categories restaurants cafes --use-google-maps --ai-analysis --max-results 20
```

#### Export Results with Emails
```powershell
python main.py search --location "Rabat, Morocco" --categories hotels --google-maps-only --output results/rabat_hotels.json --format json
```

#### Filter for High Opportunities
```powershell
python main.py search --location "Tangier, Morocco" --categories spas --use-google-maps --filter no-website --sort-by lead-score
```

## 🎯 Interactive Mode

Start interactive mode with Google Maps options:

```powershell
python main.py interactive
```

The interactive mode will guide you through:
1. Location selection
2. Business categories
3. Google Maps options
4. Filtering preferences
5. AI analysis options

## 📊 Command Reference

### Search Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--use-google-maps` | Enable Google Maps scraping | `--use-google-maps` |
| `--google-maps-only` | Use ONLY Google Maps | `--google-maps-only` |
| `--headless` | Run browser in background | `--headless` |
| `--max-results` | Limit results per category | `--max-results 15` |
| `--filter` | Filter by website status | `--filter no-website` |
| `--ai-analysis` | Enable AI lead scoring | `--ai-analysis` |

### Filter Options
- `all`: All businesses
- `no-website`: Businesses without websites (high opportunity)
- `bad-website`: Businesses with poor websites

### Sort Options
- `lead-score`: By opportunity score (default)
- `rating`: By business rating
- `name`: Alphabetically

## 📈 Enhanced Output

### With Google Maps Enabled
The output includes additional information:
- **Email Addresses**: Direct contact emails
- **Enhanced Contact Info**: Phone, address, ratings
- **Contact Level**: Complete, Good, or Basic
- **Email Discovery Stats**: Count of businesses with emails

### Sample Output
```
📊 SEARCH RESULTS SUMMARY
Total Businesses Found: 15
Without Website: 12 (80.0%)
Average Lead Score: 87.3/100
📧 With Email Addresses: 8 (53.3%)
🗺️ Google Maps Data Enhanced: 10 businesses

🏆 TOP OPPORTUNITIES
┌──────┬────────────────────┬───────────┬────────┬────────────┬────────────────┬──────────────┬──────────────┐
│ Rank │ Business Name      │ Category  │ Rating │ Lead Score │ Website Status │ Email Count  │ Contact Level│
├──────┼────────────────────┼───────────┼────────┼────────────┼────────────────┼──────────────┼──────────────┤
│ 1    │ Restaurant Atlas   │ Restaurant│ 4.5⭐  │ 95/100     │ ❌ NO WEBSITE  │ 📧 2         │ 🔥 COMPLETE  │
│ 2    │ Cafe Marrakesh     │ Cafe      │ 4.3⭐  │ 89/100     │ ❌ NO WEBSITE  │ 📧 1         │ ⚡ GOOD      │
└──────┴────────────────────┴───────────┴────────┴────────────┴────────────────┴──────────────┴──────────────┘

📞 CONTACT INFORMATION (Top 5)
┌─────────────────────┬──────────────────┬───────────────────────────────┬─────────────────────────────┐
│ Business            │ Phone            │ Emails                        │ Address                     │
├─────────────────────┼──────────────────┼───────────────────────────────┼─────────────────────────────┤
│ Restaurant Atlas    │ +212524443322    │ contact@atlas.ma, info@atlas │ Marrakesh Medina, Morocco   │
│ Cafe Marrakesh      │ +212524556677    │ hello@cafemarrakesh.ma        │ Jemaa el-Fnaa, Marrakesh   │
└─────────────────────┴──────────────────┴───────────────────────────────┴─────────────────────────────┘

📧 EMAIL OUTREACH TIPS:
• Use professional email templates
• Personalize messages based on business type
• Mention specific website benefits for their industry
• Include your portfolio examples
• Follow up within 3-5 business days
```

## 🔧 System Status

Check Google Maps availability:
```powershell
python main.py status
```

This shows:
- Google Maps scraper status
- Available features
- Installation requirements
- Recommendations

## 🛠️ Troubleshooting

### Google Maps Not Available
```
❌ Google Maps scraping not available
Install: pip install selenium
Download: Chrome WebDriver
```

**Solution:**
1. Install selenium: `pip install selenium`
2. Download ChromeDriver
3. Restart the application

### Chrome Driver Issues
```
Error: Chrome driver not found
```

**Solution:**
1. Download ChromeDriver matching your Chrome version
2. Add to PATH or place in project directory
3. Ensure executable permissions

### Slow Performance
- Use `--headless` flag for faster execution
- Reduce `--max-results` for quicker searches
- Use `--google-maps-only` for focused scraping

## 📁 File Integration

### Results Structure
Google Maps results integrate with existing file structure:
```
results/cities/{city}/searches/
├── gmaps_restaurants_2025_01_04.json
├── combined_hotels_2025_01_04.json
└── standard_cafes_2025_01_04.json
```

### Email Data Format
```json
{
  "name": "Restaurant Atlas",
  "emails": ["contact@atlas.ma", "info@atlas.ma"],
  "phone": "+212524443322",
  "address": "Marrakesh Medina, Morocco",
  "source": "google_maps_scraper",
  "lead_score": 95,
  "contact_level": "complete"
}
```

## 🎯 Best Practices

1. **Start with Enhanced Search**: Use `--use-google-maps` for best results
2. **Filter for Opportunities**: Use `--filter no-website` to focus on high-value leads
3. **Save Results**: Always use `--output` to track discoveries
4. **Enable AI Analysis**: Combine with `--ai-analysis` for lead scoring
5. **Use Interactive Mode**: Great for guided setup and learning

## 🚀 Next Steps

1. Test with sample searches
2. Experiment with different locations and categories
3. Compare standard vs enhanced results
4. Build email outreach templates
5. Track conversion rates

---

**🎉 Google Maps scraping integration is now complete and ready for use!**
