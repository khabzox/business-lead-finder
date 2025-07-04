# How to Run Business Lead Finder

## 🚀 Super Easy (Recommended)

### Option 1: Setup Once, Use Anywhere
```bash
# Run setup first (only once)
setup.bat

# Now you can use 'blf' from anywhere!
blf                          # Interactive mode
blf restaurants marrakech    # Quick search
blf cafes casablanca        # Find cafes
blf demo                    # Demo mode
```

### Option 2: Direct Commands
```bash
# No setup needed - works immediately
blf.bat                      # Interactive mode
blf.bat restaurants marrakech # Quick search
blf.bat demo                # Demo mode
```

## 🛠️ Alternative Methods

### Python Methods
```bash
python main.py              # Standard Python way
python blf.py               # Quick launcher
```

### PowerShell (Windows)
```powershell
.\blf.ps1                   # PowerShell version
```

## ✨ Command Examples

### Interactive Mode (Easiest)
```bash
blf                         # Asks questions step by step
```

### Quick Searches
```bash
blf restaurants marrakech   # Find restaurants in Marrakech
blf cafes casablanca       # Find cafes in Casablanca
blf hotels fez             # Find hotels in Fez
blf spas rabat             # Find spas in Rabat
blf shops tangier          # Find shops in Tangier
```

### Demo & Help
```bash
blf demo                   # See all features in action
blf --help                 # Show help information
```

## 🎯 What Each Command Does

**`blf`** → Interactive mode with guided questions

**`blf restaurants marrakech`** → Finds restaurants, scores leads, identifies businesses without websites

**`blf demo`** → Shows French language support, website detection, and lead scoring

## 📁 Results

All results are saved to the `results/` folder:
- JSON files with business data
- Lead scores (2-3 star businesses = highest priority)
- Website status and contact information

## 💡 Pro Tips

1. **Start with interactive mode** (`blf`) if you're new
2. **Use quick commands** (`blf restaurants marrakech`) for repeated searches
3. **Check the demo** (`blf demo`) to see all features
4. **Results are saved automatically** - check the `results/` folder

## 🔧 Troubleshooting

**"Command not found"?**
- Use `blf.bat` instead of `blf`
- Or run `setup.bat` first

**No results found?**
- Check internet connection
- Try different cities
- Use interactive mode for guidance

**Want to see what's happening?**
- Check the `results/` folder for saved data
- Look at the logs in the `logs/` folder
