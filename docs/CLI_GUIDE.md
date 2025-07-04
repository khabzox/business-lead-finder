# 🖥️ CLI Commands Guide

This guide covers all command-line interface options for the Business Lead Finder.

## 🚀 Quick Start Commands

### After Setup (Global `blf` command)

```bash
blf                          # Interactive mode
blf restaurants marrakech    # Quick search
blf demo                    # Feature demonstration
blf --help                  # Show all options
```

### Without Setup (Direct Methods)

#### Universal Python Method

```bash
python main.py              # Interactive mode
python main.py restaurants marrakech    # Quick search
python main.py demo         # Feature demonstration
python main.py --help       # Show all options
```

#### Platform-Specific Scripts

##### Windows Command Prompt

```cmd
blf.bat                     # Interactive mode
blf.bat restaurants marrakech # Quick search
blf.bat demo               # Feature demonstration
```

##### Windows PowerShell

```powershell
.\blf.ps1                  # Interactive mode
.\blf.ps1 restaurants marrakech # Quick search
.\blf.ps1 demo             # Feature demonstration
```

##### Linux/macOS/WSL/Git Bash

```bash
./blf                      # Interactive mode
./blf restaurants marrakech # Quick search
./blf demo                 # Feature demonstration
```

## 🔧 Setup Instructions

Before using the CLI commands, you need to set up the Business Lead Finder. Choose the method that works best for your system:

### Automatic Setup (Recommended)

#### Windows Users

```cmd
# Command Prompt
setup.bat

# PowerShell
.\setup.ps1

# Git Bash/WSL
chmod +x setup.sh
./setup.sh
```

#### Linux/macOS Users

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

If the automatic setup doesn't work, you can still use the application by calling Python directly:

```bash
python main.py [command] [options]
```

This method works on any system with Python 3.8+ installed.

### Verification

Test your setup with:

```bash
blf demo                    # If setup worked
python main.py demo         # If using manual method
```

## 🎯 Interactive Mode

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

## Search Command

**Find businesses by location and category**

```bash
python main.py search --location "Sample City" --categories restaurants hotels --max-results 50 --output results/leads.json
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
python main.py search -l "Sample City" -c restaurants

# Search multiple categories
python main.py search -l "Another City" -c restaurants hotels spas cafes

# Save results to specific file
python main.py search -l "Sample City" -c hotels -o hotel_leads.json

# Limit results and save as CSV
python main.py search -l "Sample City" -c restaurants -m 20 -f csv -o restaurants.csv
```

## Check Command

**Verify if a specific business has a website**

```bash
python main.py check --business-name "Sample Business" --phone "+1234567890"
```

**Parameters:**
- `--business-name, -n` (required): Name of business to check
- `--phone, -p`: Business phone number (helps verification)
- `--address, -a`: Business address (improves accuracy)

**Examples:**
```bash
# Basic website check
python main.py check -n "Sample Hotel"

# Enhanced check with contact info
python main.py check -n "Sample Restaurant" -p "+1234567890" -a "123 Main St"
```

## Report Command

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

## Export Command

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

## Analyze Command

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

## Help Commands

**Get help for any command**

```bash
# General help
python main.py --help

# Help for specific command
python main.py search --help
python main.py report --help
python main.py export --help
```

## Understanding Results

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

## Practical Workflow Examples

### Scenario 1: New Market Research

```bash
# 1. Search for businesses in new city
python main.py search -l "New City" -c restaurants hotels -o new_city_leads.json

# 2. Generate professional report
python main.py report -i new_city_leads.json -o market_report.html

# 3. Export high-priority leads to CSV
python main.py export -i new_city_leads.json -o priority_leads.csv -f csv --filter "lead_score>=70"

# 4. Analyze market opportunity
python main.py analyze -i new_city_leads.json -o market_analysis.json
```

### Scenario 2: Daily Lead Generation

```bash
# Morning routine - find today's leads
python main.py search -l "Target City" -c restaurants cafes -m 30 -o daily_leads.json

# Check a specific business someone mentioned
python main.py check -n "Sample Café" -p "+1234567890"

# Generate daily report
python main.py report -i daily_leads.json -o daily_report.html
```

### Scenario 3: Client Presentation Prep

```bash
# Comprehensive search for presentation
python main.py search -l "Client City" -c restaurants hotels spas -m 100 -o presentation_data.json

# Generate beautiful HTML report
python main.py report -i presentation_data.json -o client_presentation.html

# Export contact sheet for follow-up
python main.py export -i presentation_data.json -o contact_list.csv -f csv
```

## Advanced Configuration

### Environment Variables

Create a `.env` file with your configuration:

```env
# Default search location
DEFAULT_LOCATION=Sample City

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
bf-search -l "Sample City" -c restaurants
bf-report -i leads.json -o report.html
```
