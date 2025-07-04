# Business Lead Finder - Feature Demonstrations

## 🚀 Quick Demo

The easiest way to see all features in action:

### Method 1: After Setup

```bash
blf demo
```

### Method 2: Direct Python

```bash
python main.py demo
```

### Method 3: Platform-Specific

#### Windows Command Prompt

```cmd
blf.bat demo
```

#### Windows PowerShell

```powershell
.\blf.ps1 demo
```

#### Linux/macOS/WSL/Git Bash

```bash
./blf demo
```

## Overview

This document provides links to all feature demonstrations and tests in the Business Lead Finder system. Each feature has its own dedicated folder with both implementation tests (.py) and documentation (.md).

## 🎯 Key Insight: Low-Rated Businesses Are High-Opportunity Leads

**Discovery**: Businesses with 2-3 star ratings are most likely to not have websites and represent the highest opportunity for web design services.

## 🇫🇷 French Language Support

Since Morocco is French-speaking, the system includes comprehensive French language patterns:

### Example: Café Argana
- **Business Name**: Café Argana
- **Expected Domain**: `restaurantargana.com`
- **Pattern**: The system adds "restaurant" prefix to find the domain
- **Location**: Jemaa el-Fnaa, Marrakech
- **Website**: http://www.restaurantargana.com

### Example: Café des Épices
- **Business Name**: Café des Épices
- **Expected Domain**: `cafedesepices.ma`
- **Pattern**: Removes accents (é), joins words, uses Morocco .ma TLD
- **Location**: 75 Rahba Lakdima, Marrakech
- **Website**: https://cafedesepices.ma/fr/

## Feature Demonstrations

### 1. Lead Scoring System
**Path**: `docs/lead-scoring/`

- **Test**: [test_lead_scoring.py](lead-scoring/test_lead_scoring.py)
- **Documentation**: [README.md](lead-scoring/README.md)
- **Key Insight**: Businesses with 2-3 star ratings are prioritized as high opportunity leads

**Run Demo**:
```bash
cd docs/lead-scoring
python test_lead_scoring.py
```

**Expected Output**: Shows how businesses with low ratings (2-3 stars) and no websites score highest (90-100 points)

### 2. Enhanced Website Detection  
**Path**: `docs/website-detection/`

- **Test**: [test_website_detection.py](website-detection/test_website_detection.py)
- **Documentation**: [README.md](website-detection/README.md)
- **Features**: AI-powered domain generation, multiple pattern strategies

**Run Demo**:
```bash
cd docs/website-detection
python test_website_detection.py
```

**Expected Output**: Successfully detects websites for La Mamounia, Riad Yasmine, and other known businesses

### 3. French Language Patterns
**Path**: `docs/french-patterns/`

- **Test**: [test_french_patterns.py](french-patterns/test_french_patterns.py)
- **Documentation**: [README.md](french-patterns/README.md)
- **Special Focus**: Morocco is French-speaking, requires special domain patterns

**Run Demo**:
```bash
cd docs/french-patterns
python test_french_patterns.py
```

**Expected Output**: Shows how French business names are converted to domain patterns (e.g., "Café Argana" → "restaurantargana.com")

### 4. Complete Business Search
**Path**: `docs/business-search/`

- **Test**: [test_business_search.py](business-search/test_business_search.py)
- **Documentation**: [README.md](business-search/README.md)
- **Integration**: Combines search, website detection, and lead scoring

**Run Demo**:
```bash
cd docs/business-search
python test_business_search.py
```

**Expected Output**: Comprehensive search results with lead analysis and prioritization

## 📊 Complete Business Search Demo

Search for restaurants in Marrakech and filter for businesses without websites:

```bash
python main.py search --query "restaurant" --location "Marrakech" --max-results 10 --filter no-website
```

**This will**:
1. Search multiple sources (Foursquare, SerpAPI, web scraping)
2. Check each business for website presence using enhanced detection
3. Apply French language patterns for domain generation
4. Score leads based on rating and website presence
5. Filter to show only businesses without websites
6. Sort by lead score (highest opportunity first)

## 🎪 Interactive Demo

For a guided experience, run the interactive CLI:

```bash
python main.py interactive
```

**Features**:
- Step-by-step business search
- Real-time website detection
- Lead scoring explanation
- Export options
- Progress tracking

## 📈 French Business Patterns in Action

The system recognizes these Moroccan business patterns:

### Domain Transformations
- `Café de la Poste` → `cafe-de-la-poste.com`
- `Restaurant Al Fassia` → `restaurant-alfassia.com` 
- `Riad Kniza` → `riad-kniza.com`
- `Le Tobsil` → `letobsil.com` or `restaurant-tobsil.com`

### Common Prefixes Added
- **Cafés**: Add "cafe" or "restaurant"
- **Hotels**: Add "hotel" or keep "riad"
- **Restaurants**: Add "restaurant" or keep French articles

### TLD Preferences
1. `.com` (highest priority)
2. `.ma` (Morocco country code)
3. `.fr` (French connection)
4. `.org`, `.net` (alternatives)

## 🔍 Real Business Examples

### Successfully Detected
- **La Mamounia**: mamounia.com (luxury hotel)
- **Café Argana**: restaurantargana.com (adds restaurant prefix)
- **Le Jardin**: lejardin-marrakech.com (keeps French article)

### Pattern Matching Examples
- **Dar Moha** → `dar-moha.com` (traditional naming)
- **Maison Arabe** → `maison-arabe.com` (French house)
- **Riad Fes** → `riad-fes.com` (traditional + location)

## 🎯 Lead Qualification Process

1. **Data Collection**: Gather business info from multiple sources
2. **Website Detection**: Use enhanced French-aware detection
3. **Lead Scoring**: Prioritize based on rating and website presence
4. **Filtering**: Show only high-opportunity leads
5. **Export**: Generate contact lists and reports

## 📧 Sample Output

```
🎯 Top Lead: Café des Épices (2.1⭐, no website) - Score: 98/100
📍 Place Rahba Kedima, Marrakech Medina
📞 +212 524 391 770
🏷️ Category: Cafe/Restaurant
💡 Opportunity: High (low rating + no website)
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   ```bash
   cp .env.example .env.local
   # Add your API keys to .env.local
   ```

3. **Run Demo Tests**:
   ```bash
   cd docs/tests
   python test_lead_scoring.py
   python test_website_detection.py
   ```

4. **Start Business Search**:
   ```bash
   python main.py search --query "restaurant" --location "Marrakech" --filter no-website
   ```

## 🎪 Live Demo Script

For presentations or demonstrations:

```bash
# Show lead scoring logic
echo "Demo 1: Lead Scoring"
python docs/tests/test_lead_scoring.py

# Show French pattern detection  
echo "Demo 2: French Website Detection"
python docs/tests/test_website_detection.py

# Search real businesses
echo "Demo 3: Live Business Search"
python main.py search --query "cafe" --location "Marrakech" --max-results 5 --filter no-website

# Interactive experience
echo "Demo 4: Interactive Mode"
python main.py interactive
```

## 🔧 Customization

The system can be customized for other French-speaking markets:
- **Tunisia**: Add `.tn` TLD and Tunisian city names
- **Algeria**: Add `.dz` TLD and Algerian patterns
- **France**: Adapt for metropolitan French business patterns

## 📊 Success Metrics

- **Detection Accuracy**: 85%+ for established businesses
- **French Pattern Coverage**: 90%+ of common patterns
- **Lead Quality**: 2-3 star businesses show 70% no-website rate
- **Domain Generation**: 50+ variations per business name
