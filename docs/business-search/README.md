# Business Search & Lead Scoring

## Overview
The business search system combines multiple data sources to find businesses in Morocco and automatically scores them based on their potential as web development leads.

## How It Works

### 1. Multi-Source Search
The system searches across multiple APIs and sources:

- **Foursquare API**: Rich business data with ratings and reviews
- **SerpAPI**: Google search results for comprehensive coverage
- **Nominatim**: OpenStreetMap data for location verification
- **Web Scraping**: Morocco-specific business directories

### 2. Data Enrichment
Each business found is enriched with:

- Contact information (phone, address)
- Business ratings and review counts
- Category classification
- Geographic location data
- Website presence detection

### 3. Lead Scoring
Businesses are automatically scored (0-100) based on:

- **Website presence** (30 points for no website)
- **Rating level** (25 points for 2-3 star businesses)
- **Review count** (15 points for fewer reviews)
- **Contact availability** (10 points for phone number)
- **Business category** (15 points for high-opportunity categories)
- **Location factors** (5 points for tourist areas)

## Search Categories

### High-Opportunity Categories
- Restaurants
- Hotels and Riads
- Cafes and Bars
- Spas and Wellness
- Shops and Retail
- Professional Services

### Geographic Coverage
- **Marrakech**: Tourist hub with many businesses
- **Casablanca**: Business capital
- **Fez**: Cultural center
- **Rabat**: Government seat
- **Tangier**: Northern gateway

## Lead Prioritization

### High Priority (80-100 points)
- No website + low ratings (2-3 stars)
- New businesses with no online presence
- Service businesses in tourist areas

### Medium Priority (60-79 points)
- Has basic website but poor ratings
- Established businesses with outdated web presence
- Businesses with limited online reviews

### Low Priority (0-59 points)
- Well-established businesses with good websites
- High-rated businesses (4+ stars)
- Businesses with strong online presence

## Search Results Analysis

### Typical Results by Category

| Category | Avg Businesses Found | % Without Website | Avg Lead Score |
|----------|---------------------|-------------------|----------------|
| Restaurants | 25-50 | 60-70% | 75 |
| Hotels | 15-30 | 40-50% | 65 |
| Cafes | 20-40 | 70-80% | 80 |
| Shops | 30-60 | 80-90% | 85 |

### Success Metrics
- **Coverage**: Find 80%+ of businesses in target area
- **Accuracy**: 90%+ correct contact information
- **Relevance**: 70%+ of high-scored leads are genuine opportunities

## Usage Examples

### Basic Search
```python
from business_search import search_businesses_all_sources

businesses = search_businesses_all_sources(
    query="restaurant",
    location="Marrakech",
    max_results=50
)

print(f"Found {len(businesses)} restaurants")
```

### Search with Lead Scoring
```python
from business_search import search_businesses_all_sources, calculate_lead_score

businesses = search_businesses_all_sources("cafe", "Casablanca", 30)

# Score and sort leads
for business in businesses:
    business['lead_score'] = calculate_lead_score(business)

# Sort by lead score (highest first)
businesses.sort(key=lambda x: x['lead_score'], reverse=True)

# Show top leads
for business in businesses[:10]:
    print(f"{business['name']}: {business['lead_score']}/100")
```

### Filter High-Priority Leads
```python
# Get only high-priority leads
high_priority_leads = [
    business for business in businesses 
    if business['lead_score'] >= 80
]

# Further filter: no website + low ratings
prime_leads = [
    business for business in high_priority_leads
    if not business.get('website') and 
       business.get('rating', 0) >= 2.0 and 
       business.get('rating', 0) <= 3.5
]
```

## Configuration

### Search Limits
- Maximum results per source: 50
- Total search timeout: 60 seconds
- Rate limiting: 1 request per second

### Data Sources Priority
1. Foursquare (most reliable)
2. SerpAPI (comprehensive)
3. Nominatim (location data)
4. Web scraping (fallback)

## Running Tests

Test the complete search and scoring pipeline:

```bash
cd docs/business-search
python test_business_search.py
```

This will:
- Search multiple categories and locations
- Score all found businesses
- Show lead distribution analysis
- Display top opportunities

## Performance Optimization

### Search Speed
- Parallel API calls where possible
- Caching of repeated location queries
- Smart result deduplication

### Data Quality
- Multiple source validation
- Phone number format standardization
- Address geocoding verification
- Duplicate business detection

## Integration

The business search integrates with:
- **Website Detection**: Enhance website presence data
- **Lead Scoring**: Automatic prioritization
- **Report Generation**: Export results
- **CLI Interface**: Interactive searching
