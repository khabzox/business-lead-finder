# Enhanced Website Detection

## Overview
The enhanced website detection system uses AI-powered domain generation and intelligent pattern matching to find business websites that traditional methods might miss.

## How It Works

### 1. Domain Generation
The system generates multiple possible domain variations for each business:

- **Business name patterns**: `businessname.com`, `business-name.com`
- **Category combinations**: `restaurantname.com`, `hotelname.com`
- **Location combinations**: `name-marrakech.com`, `name-morocco.com`
- **AI-generated patterns**: Using Groq AI for creative domain suggestions

### 2. Domain Validation
Each generated domain is checked for:
- DNS resolution
- HTTP/HTTPS accessibility
- Final URL (following redirects)
- Response status codes

### 3. Intelligent Fallbacks
If primary patterns fail, the system tries:
- Common Moroccan TLDs (.ma, .co.ma)
- Alternative spellings
- Abbreviated forms
- French language patterns

## Test Results

### Successful Detections
- **La Mamounia** → `mamounia.com` ✅
- **Riad Yasmine** → `riad-yasmine.com` ✅

### Common Patterns Found
- Hotels often use: `hotelname.com` or `name-hotel.com`
- Restaurants use: `restaurantname.com` or `name-restaurant.com`
- Riads use: `riad-name.com` or `riadname.com`

## Configuration

### Domain Generation Limits
- Maximum domains to check: 15 (configurable)
- Delay between checks: 0.1 seconds
- Timeout per domain: 5 seconds

### Supported TLDs
- `.com` (primary)
- `.ma` (Morocco - very important!)
- `.co.ma` (Morocco commercial)
- `.org`
- `.net`

## Usage

```python
from website_checker import enhanced_website_detection

# Detect website for a business
result = enhanced_website_detection("La Mamounia", "hotel")

if result['website_found']:
    print(f"Website found: {result['website_url']}")
    print(f"Domains checked: {len(result['domains_checked'])}")
else:
    print("No website found")
    print(f"Tried {len(result['domains_checked'])} domains")
```

## Return Format

```python
{
    'website_found': bool,
    'website_url': str or None,
    'domains_checked': list,
    'domains_found': list,
    'detection_method': str
}
```

## Running the Test

```bash
cd docs/website-detection
python test_website_detection.py
```

This will test the detection system against known businesses and show the domain generation process in action.
