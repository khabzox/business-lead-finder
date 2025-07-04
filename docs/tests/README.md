# Test Documentation

This directory contains test scripts and demonstrations for the Business Lead Finder.

## Available Tests

### 1. Lead Scoring Test (`test_lead_scoring.py`)

**Purpose**: Demonstrates that the lead scoring algorithm correctly prioritizes businesses with low ratings (2-3 stars) as high-opportunity leads.

**Key Insight**: Businesses with 2-3 star ratings are most likely to not have websites and represent the highest opportunity for web design services.

**Usage**:
```bash
cd docs/tests
python test_lead_scoring.py
```

**Expected Output**:
- Businesses with 2-3 star ratings get the highest scores (85-100 points)
- Businesses without websites get +30 bonus points
- Businesses with few reviews get additional points
- High-rated businesses (4+ stars) get lower priority scores

### 2. Website Detection Test (`test_website_detection.py`)

**Purpose**: Tests the enhanced website detection system with French language patterns and real business examples.

**Key Features**:
- **French Language Support**: Morocco is French-speaking, so businesses often use French patterns
- **Real Examples**: Includes Café Argana (restaurantargana.com) as a real example
- **Pattern Generation**: Tests AI-powered and rule-based domain generation

**Usage**:
```bash
cd docs/tests
python test_website_detection.py
```

**Test Cases**:
1. **La Mamounia** - Famous luxury hotel
2. **Café Argana** - Real example: domain is `restaurantargana.com` (adds "restaurant")
3. **Riad Yasmine** - Traditional Moroccan accommodation
4. **Le Jardin** - French-named restaurant

**Expected Behavior**:
- Should find websites for established businesses
- Should try French patterns: restaurant-, cafe-, hotel-, riad-, le-, la-
- Should handle accented characters and special names
- Should report domains checked and success/failure

## French Language Patterns

Since Morocco is French-speaking, the system includes these French patterns:

### Business Prefixes
- `restaurant` - for cafes and restaurants
- `hotel` - for accommodations
- `riad` - traditional Moroccan house
- `dar` - Arabic for house
- `maison` - French for house
- `le`, `la` - French articles

### Location Suffixes
- `marrakech`, `marrakesh` - city variations
- `maroc` - French for Morocco
- `medina` - old city
- `gueliz` - modern district

### Real Examples
- **Café Argana** → `restaurantargana.com` (adds "restaurant")
- **Le Jardin** → `lejardin-marrakech.com` (keeps French article)
- **Riad Atlas** → `riad-atlas.ma` (uses local TLD)

## Running Tests

### Prerequisites
Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

### Environment Setup
The tests use the same environment as the main application:
```bash
# Copy environment file
cp .env.example .env.local

# Add your API keys
FOURSQUARE_API_KEY=your_key_here
SERPAPI_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

### Run Individual Tests
```bash
# Test lead scoring
python docs/tests/test_lead_scoring.py

# Test website detection
python docs/tests/test_website_detection.py
```

## Test Results Interpretation

### Lead Scoring Results
- **Score 85-100**: HIGH priority (low-rated businesses without websites)
- **Score 60-84**: MEDIUM priority (mixed factors)
- **Score 0-59**: LOW priority (high-rated businesses with websites)

### Website Detection Results
- **✅ Found**: Website successfully detected
- **❌ Not Found**: No website detected after checking all patterns
- **Domains Checked**: Number of domain patterns attempted
- **Expected Domain**: Known correct domain for validation

## Adding New Tests

To add new test cases:

1. Create a new test file in `docs/tests/`
2. Follow the existing pattern with Rich console output
3. Include real business examples when possible
4. Document expected results
5. Update this README with the new test

## French Business Naming Conventions

Common patterns in Moroccan business names:
- **Café/Restaurant**: Often use "Café" or add "Restaurant" to domain
- **Hotels**: Use "Hotel", "Riad", "Dar", or "Maison"
- **French Articles**: "Le", "La", "Les" are common
- **Location Names**: Include city or district names
- **Arabic Elements**: Mix of Arabic and French words

Example transformations:
- `Café de France` → `cafe-de-france.com`
- `Restaurant Al Fassia` → `restaurant-alfassia.com`
- `Le Tobsil` → `letobsil.com` or `restaurant-tobsil.com`
