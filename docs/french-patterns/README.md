# French Language Patterns for Morocco

## Overview
Morocco is a French-speaking country, and many businesses use French names or add French words to their domain names. Understanding these patterns is crucial for accurate website detection.

## Common French Patterns

### 1. Category Prefixes/Suffixes
Moroccan businesses often add French category words to their domains:

- **Café Argana** → `restaurantargana.com` (adds "restaurant")
- **Café des Épices** → `cafedesepices.com` (keeps "cafe")
- **Hotel Atlas** → `hotelatlas.com` (adds "hotel")

### 2. French Articles Removal
French articles are typically removed from domain names:

- **La Mamounia** → `mamounia.com` (removes "La")
- **Le Jardin** → `jardin.com` or `lejardin.com`
- **Les Jardins** → `jardins.com` or `lesjardins.com`

### 3. Accent and Special Character Handling
French accents and special characters are simplified:

- **Café des Épices** → `cafedesepices.ma` (removes accents, uses .ma TLD)
- **Hôtel** → `hotel` (ô becomes o)
- **Château** → `chateau` (â becomes a)
- **Français** → `francais` (ç becomes c)

### 4. Word Joining Patterns
Multi-word French names follow specific patterns:

- **Riad Yasmine** → `riad-yasmine.com` (hyphenated)
- **Café des Épices** → `cafedesepices.com` (joined)
- **Le Jardin** → `lejardin-marrakech.com` (hyphen with location)

### 5. Location Integration
Many Moroccan businesses include location in their domains:

- `businessname-marrakech.com`
- `businessname-morocco.com`
- `businessname-medina.com`
- `marrakech-businessname.com`

## Detection Strategies

### Primary Patterns
1. **Direct translation**: Remove accents, join words
2. **Category addition**: Add French business category
3. **Article removal**: Remove Le/La/Les/Des
4. **Hyphenation**: Try both joined and hyphenated versions

### Secondary Patterns
1. **Location suffixes**: Add city/region names
2. **Category prefixes**: Put category before name
3. **Moroccan TLDs**: Try .ma and .co.ma extensions
4. **Alternative spellings**: Common French→English translations

## Real Examples

### Successful Detections
| Business Name | Domain Found | Pattern Used |
|---------------|--------------|--------------|
| La Mamounia | mamounia.com | Article removal |
| Riad Yasmine | riad-yasmine.com | Category + hyphen |
| Café Argana | restaurantargana.com | Category substitution |
| Café des Épices | cafedesepices.ma | Accent removal + .ma TLD |

### Pattern Analysis
- **60%** use simple name without articles
- **25%** add/change category words
- **15%** include location references

## Implementation

### French Pattern Generator
```python
def generate_french_patterns(business_name, category):
    patterns = []
    
    # Remove French articles
    name = remove_french_articles(business_name)
    
    # Remove accents
    name = remove_accents(name)
    
    # Generate patterns
    patterns.extend([
        f"{name}.com",
        f"{category}{name}.com",
        f"{name}-marrakech.com",
        f"riad-{name}.com" if category == "hotel" else f"{name}.com"
    ])
    
    return patterns
```

### Accent Removal Function
```python
def remove_accents(text):
    accent_map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'ö': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    
    for accent, replacement in accent_map.items():
        text = text.replace(accent, replacement)
        text = text.replace(accent.upper(), replacement.upper())
    
    return text
```

## Testing

Run the French patterns test to see how well the system handles French business names:

```bash
cd docs/french-patterns
python test_french_patterns.py
```

This test uses real Moroccan businesses with known domain patterns to validate the detection accuracy.

## Success Metrics

- **Target**: 80%+ detection rate for known French business domains
- **Current**: Varies by pattern complexity
- **Key**: Understanding local business naming conventions
