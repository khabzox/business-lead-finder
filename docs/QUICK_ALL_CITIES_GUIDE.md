# Quick All Cities Search Guide

**Find business opportunities across ALL major Morocco cities with one command!**

## 🇲🇦 Supported Cities

This tool supports comprehensive business searches across all major Morocco cities:

| Priority | City | Arabic | Description | Population | Business Density |
|----------|------|--------|-------------|------------|------------------|
| P1 | 🔴 **Marrakesh** | مراكش | Tourist capital - Red City | 928,850 | Very High |
| P2 | 💼 **Casablanca** | الدار البيضاء | Economic capital - Business hub | 3,359,818 | Extremely High |
| P3 | 🏛️ **Rabat** | الرباط | Political capital - Government seat | 577,827 | High |
| P4 | 🏺 **Fez** | فاس | Cultural capital - Imperial city | 1,112,072 | High |
| P5 | ⚓ **Tangier** | طنجة | Northern gateway - Port city | 947,952 | High |
| P6 | 🏖️ **Agadir** | أكادير | Atlantic coast - Beach resort | 421,844 | Medium-High |
| P7 | 🏰 **Meknes** | مكناس | Imperial city - Historical center | 632,079 | Medium |
| P8 | 🌍 **Oujda** | وجدة | Eastern gateway - Border city | 494,252 | Medium |
| P9 | 🎭 **Tetouan** | تطوان | Northern cultural center | 380,787 | Medium |
| P10 | 🌊 **Essaouira** | الصويرة | Coastal gem - Windsurfing capital | 77,966 | Medium |

## 🚀 Quick Start Options

### Option 1: Using BLF Command (After Setup)

#### Search All Cities

```bash
blf all-cities
```

#### Search Specific City

```bash
blf restaurants marrakech
blf hotels casablanca
blf cafes fez
```

### Option 2: Interactive Mode (Recommended for Beginners)

#### Windows Batch

```cmd
quick_search.bat
```

#### PowerShell

```powershell
quick_search.ps1
```

#### Python Direct

```bash
python quick_all_cities_search.py --interactive
```

**What it does:**
- Shows you a menu of all cities
- Lets you choose search size (test/standard/mega)
- Guides you through the entire process
- Perfect for first-time users

### Option 3: Search Specific City

#### Windows Batch
```bash
quick_city.bat marrakesh           # Standard search
quick_city.bat casablanca mega     # MEGA search 
quick_city.bat rabat test          # Quick test
```

**Python:**
```bash
python quick_all_cities_search.py --city marrakesh
python quick_all_cities_search.py --city casablanca --search-size mega
python quick_all_cities_search.py --city rabat --search-size test
```

### Option 3: Search ALL Cities at Once

**Windows Batch:**
```bash
search_all_cities.bat              # Standard search all cities
```

**PowerShell:**
```bash
search_all_cities.ps1              # Standard search all cities
```

**Python:**
```bash
python quick_all_cities_search.py --all-cities
python quick_all_cities_search.py --all-cities --search-size mega
```

## 📊 Search Sizes

Choose the right search size for your needs:

| Size | Results per City | Time per City | Total Results (10 cities) | Best For |
|------|------------------|---------------|---------------------------|----------|
| 🧪 **Test** | ~1,000 businesses | 2-5 minutes | ~10,000 | Quick testing, demos |
| 📊 **Standard** | ~50,000 businesses | 30-60 minutes | ~500,000 | Regular business searches |
| 🚀 **MEGA** | ~200,000 businesses | 2-4 hours | ~2,000,000 | Complete market analysis |

## 🏙️ City-Specific Business Categories

Each city is optimized for different business types:

### 🔴 Marrakesh - Tourism & Hospitality
- **High Priority**: hotels, riads, restaurants, spas, tour_operators
- **Areas**: Medina, Jemaa el-Fnaa, Majorelle, Hivernage, Gueliz

### 💼 Casablanca - Business Services  
- **High Priority**: consulting, accounting, law_firms, real_estate, business_hotels
- **Areas**: Centre-ville, Maarif, Gauthier, Anfa, Ain Diab

### 🏛️ Rabat - Government & Professional
- **High Priority**: government_contractors, consulting, law_firms, diplomatic_services
- **Areas**: Agdal, Hay Riad, Souissi, Centre-ville, Hassan

### 🏺 Fez - Traditional Crafts & Culture
- **High Priority**: handicrafts, pottery, leather_goods, cultural_tourism
- **Areas**: Fez el Bali, Fez el Jdid, Ville Nouvelle, Zouagha

### ⚓ Tangier - Port & International Business
- **High Priority**: shipping, logistics, import_export, international_services
- **Areas**: Centre-ville, Port, Malabata, Tanger Med

## 📁 Results Organization

All results are automatically organized by city for easy management:

```
results/cities/
├── marrakesh/
│   ├── searches/           # Search result files
│   ├── reports/            # Generated reports
│   ├── exports/            # Export files
│   └── analytics/          # Analysis data
├── casablanca/
│   ├── searches/
│   ├── reports/
│   ├── exports/
│   └── analytics/
└── [other cities]/
    ├── searches/
    ├── reports/
    ├── exports/
    └── analytics/
```

## 🎯 Lead Scoring

The system uses Morocco-specific lead scoring:

### Score Factors:
1. **Website Absence** (30 points) - No website = higher opportunity
2. **Rating Range** (25 points) - 2-3 star businesses score highest
3. **Review Count** (15 points) - Fewer reviews = more opportunity
4. **Contact Info** (10 points) - Available phone number
5. **Business Category** (15 points) - High-value categories (tourism, hospitality)
6. **City Priority** (5 points) - Major cities score higher

### Opportunity Levels:
- **EXCELLENT** (80-100 points) - Top prospects, immediate outreach
- **HIGH** (70-79 points) - Strong prospects, priority follow-up
- **MEDIUM** (60-69 points) - Good prospects, regular follow-up
- **LOW** (40-59 points) - Basic prospects, bulk outreach

## 💡 Usage Examples

### Example 1: Test All Cities
```bash
# Quick test of all cities (fast overview)
python quick_all_cities_search.py --all-cities --search-size test
```

### Example 2: Deep Dive into Marrakesh
```bash
# Comprehensive Marrakesh search
python quick_all_cities_search.py --city marrakesh --search-size mega
```

### Example 3: Business Hub Analysis
```bash
# Focus on economic centers
python quick_all_cities_search.py --city casablanca --search-size standard
python quick_all_cities_search.py --city rabat --search-size standard
```

### Example 4: Tourism Market Research
```bash
# Tourism-focused cities
python quick_all_cities_search.py --city marrakesh --search-size mega
python quick_all_cities_search.py --city agadir --search-size standard
python quick_all_cities_search.py --city essaouira --search-size standard
```

## 🔄 Automation & Scheduling

Set up automated searches across all cities:

```bash
# Setup automation
python quick_all_cities_search.py --schedule

# Or use the automated scheduler
python scripts/automated_scheduler.py --start
```

## 📋 Command Reference

### List Available Cities
```bash
python quick_all_cities_search.py --list-cities
```

### Interactive Mode
```bash
python quick_all_cities_search.py --interactive
```

### Single City Search
```bash
python quick_all_cities_search.py --city [CITY] --search-size [SIZE]
```

### All Cities Search
```bash
python quick_all_cities_search.py --all-cities --search-size [SIZE]
```

### Available Cities:
`marrakesh`, `casablanca`, `rabat`, `fez`, `tangier`, `agadir`, `meknes`, `oujda`, `tetouan`, `essaouira`

### Available Sizes:
`test`, `standard`, `mega`

## 🎨 Results Analysis

After running searches, you can analyze results:

```bash
# Show results summary
python scripts/show_results.py

# Enhanced analysis with charts
python scripts/enhanced_analysis.py
```

## 🔧 Troubleshooting

### Common Issues:

1. **Script not found**: Make sure you're in the project root directory
2. **Python not found**: Ensure Python 3.8+ is installed and in PATH
3. **Permission errors**: Run PowerShell as Administrator if needed
4. **Large file sizes**: Use smaller search sizes for testing

### Getting Help:

```bash
python quick_all_cities_search.py --help
```

## 🚀 Next Steps

1. Start with interactive mode to get familiar
2. Try a test search on your target city
3. Run standard searches for serious prospecting
4. Use MEGA searches for comprehensive market analysis
5. Set up automation for regular lead generation

**Happy lead hunting! 🇲🇦**
