# Quick Start Guide

## 🚀 NEW: Quick Search Tools (Organized!)

All quick search tools are now in the `quick_search/` folder for better organization.

### Step 1: Quick Commands
```powershell
# List all supported cities (10 major Morocco cities)
python quick_search/quick_all_cities_search.py --list-cities

# Search specific city (test mode - hundreds of results)
python quick_search/quick_all_cities_search.py --city marrakesh --search-size test

# Search all cities at once (test mode)
python quick_search/quick_all_cities_search.py --all-cities --search-size test

# Interactive mode (easiest - guided menus)
python quick_search/quick_all_cities_search.py --interactive
```

### Step 2: Or Use the Quick Launcher
```powershell
# Shows all available commands with examples
quick_launcher.bat
```

## 🎯 What Each Command Does

### `--list-cities`
- Shows all 10 supported Morocco cities with Arabic names
- Displays descriptions, population, and priority info
- Includes: Marrakesh, Casablanca, Rabat, Fez, Tangier, Agadir, Meknes, Oujda, Tetouan, Essaouira

### `--city [city_name] --search-size [size]`
- **test**: Hundreds of results (quick)
- **standard**: Thousands of results (comprehensive)
- **mega**: Maximum scale (massive)

### `--all-cities --search-size [size]`
- Searches all 10 Morocco cities simultaneously
- Results organized by city in separate folders
- Lead scoring and opportunity analysis for each city

### `--interactive`
- Menu-driven interface with guided options
- Best for beginners or complex searches
- Step-by-step process

## 📁 Results Organization
All search results are saved in: `results/cities/{city_name}/searches/`

Each city has its own organized structure:
- Analytics folder
- Reports folder  
- Exports folder
- Search results with timestamps

## 🏛️ Legacy Methods (Still Available)

### Super Easy Setup (Original)

### Step 1: Run Setup
```bash
setup.bat
```

### Step 2: Use Simple Commands
```bash
# Interactive mode (easiest)
blf

# Quick searches
blf restaurants marrakech
blf cafes casablanca  
blf hotels fez

# Demo
blf demo
```

## What Each Command Does

### `blf` (Interactive Mode)
- Asks you questions step by step
- Guides you through the whole process
- Best for beginners

### `blf restaurants marrakech`
- Finds restaurants in Marrakech
- Shows lead scores
- Identifies businesses without websites

### `blf demo`
- Shows all features working
- Uses real Moroccan businesses
- Demonstrates French language support

## Alternative Methods

If you prefer the traditional way:

```bash
# Method 1: Direct Python
python main.py

# Method 2: Python launcher
python blf.py

# Method 3: Batch file
blf.bat
```

## Quick Examples

```bash
# Find high-opportunity restaurant leads in Marrakech
blf restaurants marrakech

# Find cafes in Casablanca
blf cafes casablanca

# Interactive mode with guided setup
blf

# See all features in action
blf demo
```

## After Running Commands

Results are saved to the `results/` folder:
- JSON files with business data
- Lead scores and website status
- Ready for follow-up or CRM import

## Troubleshooting

**Command not found?**
- Run `setup.bat` first
- Or use `blf.bat` instead of `blf`

**No results found?**
- Check your internet connection
- Try different city names
- Use interactive mode (`blf`) for guided help
