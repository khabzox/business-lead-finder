# 🚀 How to Run Business Lead Finder

This comprehensive guide shows you all the different ways to run the Business Lead Finder across different operating systems and environments.

## ⚡ Quick Start (Any OS)

### Option 1: Automatic Setup (Recommended)

#### Windows Users

##### Command Prompt

```cmd
setup.bat
```

##### PowerShell

```powershell
.\setup.ps1
```

##### Git Bash/WSL

```bash
chmod +x setup.sh
./setup.sh
```

#### Linux/macOS Users

```bash
# Make executable (if needed)
chmod +x setup.sh

# Run setup
./setup.sh
```

**After setup, use from anywhere:**

```bash
blf demo                     # Test the installation
blf restaurants marrakech    # Start finding leads
blf --help                   # Show all options
```

### Option 2: Direct Python Execution (Always Works)

```bash
# Works on any OS with Python installed
python main.py restaurants marrakech
python main.py --help
python main.py demo
```

## 🖥️ Platform-Specific Instructions

### Windows

#### Method 1: Windows Batch File

```cmd
# From project directory
blf.bat restaurants marrakech
blf.bat demo
blf.bat --help
```

#### Method 2: PowerShell Script

```powershell
# From project directory
.\blf.ps1 restaurants marrakech
.\blf.ps1 demo
.\blf.ps1 --help
```

#### Method 3: Auto-Setup (Recommended)

```cmd
# Run once to setup global 'blf' command
setup.bat

# Then use anywhere
blf restaurants marrakech
blf demo
```

#### Method 4: Git Bash (Windows)

```bash
# Make executable
chmod +x blf setup.sh

# Run setup
./setup.sh

# Use the command
blf restaurants marrakech
```

### Linux/macOS

#### Method 1: Bash Script

```bash
# Make executable (if not already)
chmod +x blf

# Use from project directory
./blf restaurants marrakech
./blf demo
```

#### Method 2: Auto-Setup (Recommended)

```bash
# Run once to setup global 'blf' command
chmod +x setup.sh
./setup.sh

# Then use anywhere
blf restaurants marrakech
```

### WSL (Windows Subsystem for Linux)

```bash
# Same as Linux
chmod +x setup.sh
./setup.sh

# Use the command
blf restaurants marrakech
```

### WSL (Windows Subsystem for Linux)

```bash
# Same as Linux
chmod +x setup.sh blf
./setup.sh

# Use globally after setup
blf restaurants marrakech
```

## 🔧 Python Detection & Setup

The setup script automatically detects Python in these locations:

### Windows
- `python3` or `python` in PATH
- `C:\Python*\python.exe`
- `C:\Program Files\Python*\python.exe`
- `%USERPROFILE%\AppData\Local\Programs\Python\Python*\python.exe`

### Linux/macOS
- `python3` or `python` in PATH
- `/usr/bin/python3`
- `/usr/local/bin/python3`
- `/opt/python*/bin/python3`
- Homebrew: `/usr/local/Cellar/python*/bin/python3`
- Conda: `~/anaconda3/bin/python` or `~/miniconda3/bin/python`

### Manual Python Path
If automatic detection fails, you can:

1. **Find your Python installation:**
   ```bash
   # Windows
   where python
   where python3
   
   # Linux/macOS
   which python3
   which python
   whereis python3
   ```

2. **Use direct path:**
   ```bash
   # Example for Windows
   /c/Python312/python.exe main.py restaurants marrakech
   
   # Example for Linux/macOS
   /usr/bin/python3 main.py restaurants marrakech
   ```

## 📋 Command Examples by Environment

### Interactive Mode (Recommended for Beginners)

```bash
# Any method works:
blf                          # After setup
python main.py               # Direct Python
./blf                        # Linux/macOS local
blf.bat                      # Windows batch
```

### Quick Searches

```bash
# Find restaurants in Marrakech
blf restaurants marrakech           # Global command
python main.py restaurants marrakech # Direct Python
./blf restaurants marrakech         # Local script

# Find hotels in Casablanca
blf hotels casablanca 20            # Limit to 20 results
python main.py hotels casablanca 20

# Multiple categories
python main.py search -l "Marrakech, Morocco" -c restaurants hotels cafes
```

### Advanced Usage

```bash
# Generate reports
python main.py report -i results/leads.json -o report.html

# Export data
python main.py export -i results/leads.json -o leads.csv -f csv

# Check specific business
python main.py check -n "Restaurant Atlas" -p "+212524443322"
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### "Command not found" errors

**Issue:** `blf: command not found` or `bash: blf: command not found`

**Solutions:**
1. **Run setup first:**
   ```bash
   # Windows
   setup.bat
   
   # Linux/macOS/WSL
   ./setup.sh
   ```

2. **Reload shell configuration:**
   ```bash
   # Bash
   source ~/.bashrc
   
   # Zsh
   source ~/.zshrc
   
   # Or restart terminal
   ```

3. **Use local script:**
   ```bash
   ./blf restaurants marrakech    # Instead of global 'blf'
   ```

#### Python not found errors

**Issue:** "Python was not found" or "python: command not found"

**Solutions:**
1. **Install Python 3.8+:**
   - **Windows:** Download from [python.org](https://python.org/downloads/) or `winget install Python.Python.3`
   - **macOS:** Download from [python.org](https://python.org/downloads/) or `brew install python`
   - **Linux:** `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (RHEL/CentOS)

2. **Check installation:**
   ```bash
   python3 --version
   python --version
   ```

3. **Add to PATH (if needed):**
   - **Windows:** Add Python installation directory to system PATH
   - **Linux/macOS:** Usually automatic, but check `/usr/bin` or `/usr/local/bin`

#### Permission errors

**Issue:** Permission denied when running scripts

**Solutions:**
```bash
# Make scripts executable (Linux/macOS/WSL)
chmod +x setup.sh blf

# Windows: Run PowerShell as Administrator
# Then: .\setup.ps1
```

#### Windows Store Python conflicts

**Issue:** Windows Store Python stub interfering

**Solutions:**
1. **Disable Windows Store Python alias:**
   - Settings → Apps → App execution aliases
   - Turn off "python.exe" and "python3.exe"

2. **Use specific Python path:**
   ```bash
   # Find your real Python installation
   /c/Python312/python.exe main.py restaurants marrakech
   ```

#### PATH not updating

**Issue:** Setup completes but `blf` still not found

**Solutions:**
1. **Restart terminal/command prompt**
2. **Reload configuration:**
   ```bash
   source ~/.bashrc    # Linux/macOS
   ```
3. **Use full path temporarily:**
   ```bash
   /full/path/to/business-lead-finder/blf restaurants marrakech
   ```

## 📝 Environment-Specific Setup Files

The project includes multiple setup files for different environments:

- **`setup.bat`** - Windows Command Prompt/PowerShell
- **`setup.ps1`** - Windows PowerShell (enhanced)
- **`setup.sh`** - Linux/macOS/WSL/Git Bash
- **`blf.bat`** - Windows batch launcher
- **`blf.ps1`** - Windows PowerShell launcher
- **`blf`** - Unix/Linux executable script

## 🎯 Recommended Workflows

### First-Time Users
1. **Install Python 3.8+** if not already installed
2. **Run appropriate setup script** for your OS
3. **Test with:** `blf demo`
4. **Start searching:** `blf restaurants marrakech`

### Daily Usage
1. **Quick searches:** `blf restaurants marrakech 10`
2. **Generate reports:** `python main.py report -i results/*.json -o daily_report.html`
3. **Export contacts:** `python main.py export -i results/*.json -o contacts.csv -f csv`

### Power Users
1. **Multi-city searches:** Use advanced command options
2. **Automated workflows:** Schedule with cron/Task Scheduler
3. **Custom integrations:** Use Python API directly

---

**The goal is to make it work seamlessly on any system!** 🚀

Choose the method that works best for your environment, and remember you can always fall back to direct Python execution if needed.

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

## 🚨 Comprehensive Troubleshooting

### "Command not found" Errors

#### Windows PowerShell
```powershell
# Issue: setup.bat not recognized
# Solution: Use proper PowerShell syntax
.\setup.bat

# Or use PowerShell version
.\setup.ps1
```

#### Git Bash (Windows)
```bash
# Issue: bash: setup.bat: command not found
# Solution: Use bash script instead
chmod +x setup.sh
./setup.sh
```

#### Linux/macOS
```bash
# Issue: Permission denied
# Solution: Make script executable
chmod +x setup.sh
./setup.sh

# Issue: blf: command not found after setup
# Solution: Reload shell configuration
source ~/.bashrc    # for bash
source ~/.zshrc     # for zsh
```

### Python Issues

#### Windows Store Python Conflict
```bash
# Issue: "Python was not found; run without arguments to install from Microsoft Store"
# Solution: Use full Python path or disable Windows Store alias

# Option 1: Find real Python installation
which python3
ls -la /c/Python*/python.exe

# Option 2: Use direct Python method
python main.py restaurants marrakech
```

#### Python Version Issues
```bash
# Check Python version
python --version
python3 --version

# Minimum requirement: Python 3.8+
# If too old, update Python from python.org
```

#### Missing Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or use specific Python
python -m pip install -r requirements.txt
```

### Cross-Platform Solutions

#### Universal Python Method (Works Everywhere)
```bash
# If all else fails, use direct Python execution
python main.py restaurants marrakech 5
python main.py demo
python main.py --help
```

#### Manual PATH Setup
```bash
# Add project directory to PATH manually

# Windows (Command Prompt - Admin required)
setx PATH "%PATH%;C:\path\to\business-lead-finder"

# Windows (PowerShell - Admin required)
$env:PATH += ";C:\path\to\business-lead-finder"

# Linux/macOS (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH="/path/to/business-lead-finder:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Environment-Specific Fixes

**WSL (Windows Subsystem for Linux):**
```bash
# Ensure proper line endings
dos2unix setup.sh
chmod +x setup.sh
./setup.sh
```

**macOS Catalina+ (zsh default):**
```bash
# Setup might modify ~/.bashrc but you're using zsh
# Copy the PATH export to ~/.zshrc manually
echo 'export PATH="/path/to/business-lead-finder:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Virtual Environments:**
```bash
# If using conda/virtualenv, activate first
conda activate your_env
# or
source venv/bin/activate

# Then run setup
./setup.sh
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
