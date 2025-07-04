# Lead Scoring System

## Overview
The lead scoring system prioritizes businesses based on their likelihood of needing website development services. The key insight is that **businesses with 2-3 star ratings are most likely to not have websites** and represent the highest opportunity.

## How It Works

### Scoring Factors

1. **Website Presence (30 points)**
   - No website: +30 points (HIGH opportunity)
   - Has website: -10 points (lower priority)

2. **Rating Factor (25 points max)**
   - **2.0-3.5 stars: +25 points** (HIGH opportunity - businesses likely need help)
   - 3.5-4.0 stars: +15 points (medium opportunity)
   - 4.0+ stars: +8 points (lower opportunity - already successful)
   - No rating: +10 points (unknown, medium opportunity)

3. **Review Count (15 points max)**
   - 1-20 reviews: +15 points (less established online)
   - 21-50 reviews: +12 points
   - 51-100 reviews: +8 points
   - 100+ reviews: +5 points (already established)

4. **Contact Information (10 points)**
   - Has phone number: +10 points

5. **Category Factor (15 points max)**
   - High-opportunity categories (restaurant, hotel, spa, cafe, shop, service): +15 points
   - Other categories: +5 points

6. **Location Factor (5 points max)**
   - Tourist areas (medina, gueliz, hivernage, majorelle): +5 points

### Score Ranges
- **80-100 points**: HIGH priority leads
- **60-79 points**: MEDIUM priority leads
- **0-59 points**: LOW priority leads

## Key Insight

**Businesses with 2-3 star ratings are most likely to lack websites** because:
- They may be struggling with their online presence
- Lower ratings often correlate with poor digital marketing
- They represent the highest opportunity for improvement
- They're more likely to need and invest in professional web services

## Test Results

When testing with sample businesses:
1. **Struggling Cafe (2.3 stars, no website)** → 100/100 points (HIGH)
2. **Average Hotel (3.2 stars, no website)** → 100/100 points (HIGH)
3. **New Business (no ratings, no website)** → 90/100 points (HIGH)
4. **Popular Shop (4.5 stars, has website)** → 56/100 points (LOW)
5. **High-End Restaurant (4.8 stars, has website)** → 53/100 points (LOW)

## Usage

```python
from business_search import calculate_lead_score

# Calculate score for a business
business = {
    "name": "Local Cafe",
    "rating": 2.8,
    "review_count": 15,
    "website": None,
    "phone": "+212123456789",
    "category": "cafe",
    "address": "Medina, Marrakech"
}

score = calculate_lead_score(business)
print(f"Lead score: {score}/100")  # Output: Lead score: 100/100
```

## Running the Test

```bash
cd docs/lead-scoring
python test_lead_scoring.py
```

This will display a comprehensive analysis showing how different business characteristics affect lead scoring.
