# Quick Start Guide

## Super Easy Setup

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
