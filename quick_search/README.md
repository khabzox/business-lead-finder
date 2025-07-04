# 🚀 Quick Search Tools

This folder contains all the quick search tools for finding business opportunities in Morocco cities.

## 📁 Files Overview

### 🐍 Python Scripts

- **`quick_all_cities_search.py`** - Main script for searching all Morocco cities
- **`quick_marrakesh_search.py`** - Legacy Marrakesh-specific search (superseded by all-cities script)

### 🖥️ Batch Scripts (Windows)

- **`quick_search.bat`** - Windows batch file for quick searches
- **`quick_search.ps1`** - PowerShell script for quick searches  
- **`quick_city.bat`** - City-specific batch search

## 🎯 Quick Usage

### List All Cities

```powershell
python quick_search/quick_all_cities_search.py --list-cities
```

### Search Specific City

```powershell
python quick_search/quick_all_cities_search.py --city marrakesh --search-size test
```

### Search All Cities

```powershell
python quick_search/quick_all_cities_search.py --all-cities --search-size test
```

### Interactive Mode

```powershell
python quick_search/quick_all_cities_search.py --interactive
```

## 📊 Search Sizes

- **`test`** - Quick test search (hundreds of results)
- **`standard`** - Standard search (thousands of results)
- **`mega`** - Massive search (maximum scale)

## 🏙️ Supported Cities

- 🔴 Marrakesh (مراكش)
- 💼 Casablanca (الدار البيضاء)
- 🏛️ Rabat (الرباط)
- 🏺 Fez (فاس)
- ⚓ Tangier (طنجة)
- 🏖️ Agadir (أكادير)
- 🏰 Meknes (مكناس)
- 🌍 Oujda (وجدة)
- 🎭 Tetouan (تطوان)
- 🌊 Essaouira (الصويرة)

## 📁 Results Location

All search results are saved in: `results/cities/{city_name}/searches/`

## 💡 Tips

- Use `--interactive` for guided menu-driven searches
- Results include lead scoring and opportunity analysis
- Each city has its own organized folder structure
- Focus on businesses with 'opportunity_level': 'EXCELLENT'
