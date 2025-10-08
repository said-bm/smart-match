# Query Examples and Expected Outputs

This document provides comprehensive examples of natural language queries and their expected facet outputs.

## Mobile & Electronics

### Example 1: Basic Smartphone Query
**Query:** `"iPhone 13"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone 13"
}
```

### Example 2: Detailed Smartphone Query
**Query:** `"Looking for iPhone 13 with 256GB in blue color under $800"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone 13",
  "storage": "256GB",
  "color": "blue",
  "price_ranges": {"max": 800}
}
```

### Example 3: Android Device with Network
**Query:** `"Samsung Galaxy S21 5G with dual sim"`

**Expected Output:**
```json
{
  "brand": "Samsung",
  "model": "Galaxy S21",
  "network": ["5G"],
  "dual_sim": true
}
```

### Example 4: Refurbished Device
**Query:** `"Refurbished iPhone 11 black 128GB"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone 11",
  "color": "black",
  "storage": "128GB",
  "backbox_grade": "refurbished"
}
```

### Example 5: Tablet with Specs
**Query:** `"iPad Pro 12.9 inch with 512GB and Apple Pencil support"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPad Pro",
  "screen_size": "12.9 inch",
  "storage": "512GB"
}
```

## Computing & Laptops

### Example 6: Gaming Laptop
**Query:** `"Gaming laptop with RTX 3060 and 16GB RAM under $1500"`

**Expected Output:**
```json
{
  "cat_id": "laptops",
  "graphic_card": "NVIDIA RTX 3060",
  "memory": "16GB",
  "price_ranges": {"max": 1500}
}
```

### Example 7: MacBook with Specs
**Query:** `"MacBook Pro with M1 chip and 512GB SSD"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "MacBook Pro",
  "processor": "M1",
  "storage_ssd": "512GB SSD",
  "storage_type": "SSD"
}
```

### Example 8: Business Laptop
**Query:** `"Dell laptop with Intel i7, touchscreen, and webcam"`

**Expected Output:**
```json
{
  "brand": "Dell",
  "cat_id": "laptops",
  "processor": "Intel i7",
  "touchscreen": true,
  "webcam": true
}
```

### Example 9: Desktop Computer
**Query:** `"HP desktop with AMD processor and 1TB HDD"`

**Expected Output:**
```json
{
  "brand": "HP",
  "processor_type": "AMD",
  "storage": "1TB",
  "storage_type": "HDD"
}
```

### Example 10: Monitor
**Query:** `"27 inch 4K monitor with HDMI"`

**Expected Output:**
```json
{
  "screen_size": "27 inch",
  "hdmi_input": true
}
```

## Home Appliances

### Example 11: Coffee Machine
**Query:** `"Espresso coffee machine with energy class A++"`

**Expected Output:**
```json
{
  "cat_id": "home_appliances",
  "coffee_machine_type": "espresso",
  "energy_class": "A++"
}
```

### Example 12: Washing Machine
**Query:** `"Front load washing machine 8kg capacity"`

**Expected Output:**
```json
{
  "cat_id": "home_appliances",
  "washing_machine_type": "front_load",
  "capacity": "8kg"
}
```

### Example 13: Refrigerator
**Query:** `"French door fridge with 500L capacity and A+ energy rating"`

**Expected Output:**
```json
{
  "fridge_type": "french_door",
  "capacity": "500L",
  "energy_class": "A+"
}
```

### Example 14: Dishwasher
**Query:** `"Built-in dishwasher with energy class A+++"`

**Expected Output:**
```json
{
  "dishwasher_type": "built_in",
  "energy_class": "A+++"
}
```

### Example 15: Microwave Oven
**Query:** `"1200W microwave oven with convection"`

**Expected Output:**
```json
{
  "oven_type": "microwave",
  "power": "1200W"
}
```

## Gaming

### Example 16: Gaming Console
**Query:** `"PlayStation 5 with extra controller"`

**Expected Output:**
```json
{
  "brand": "Sony",
  "console_type": "PlayStation",
  "model": "PS5",
  "controllers_number": 2
}
```

### Example 17: Video Game
**Query:** `"PS5 games rated 18+ in action genre"`

**Expected Output:**
```json
{
  "compatible_gaming_console": ["PS5"],
  "pegi": "18",
  "video_game_genre": "action"
}
```

### Example 18: Nintendo Game
**Query:** `"Nintendo Switch games suitable for kids, PEGI 7"`

**Expected Output:**
```json
{
  "console_type": "Nintendo Switch",
  "compatible_gaming_console": ["Nintendo Switch"],
  "pegi": "7"
}
```

### Example 19: Xbox Series X
**Query:** `"Xbox Series X racing games"`

**Expected Output:**
```json
{
  "console_type": "Xbox",
  "model": "Series X",
  "compatible_gaming_console": ["Xbox Series X"],
  "video_game_genre": "racing"
}
```

## Price Range Queries

### Example 20: Under Price
**Query:** `"Smartphones under $500"`

**Expected Output:**
```json
{
  "cat_id": "smartphones",
  "price_ranges": {"max": 500}
}
```

### Example 21: Over Price
**Query:** `"Laptops over $2000"`

**Expected Output:**
```json
{
  "cat_id": "laptops",
  "price_ranges": {"min": 2000}
}
```

### Example 22: Price Range
**Query:** `"Gaming console between $400 and $600"`

**Expected Output:**
```json
{
  "cat_id": "gaming_consoles",
  "price_ranges": {"min": 400, "max": 600}
}
```

### Example 23: Exact Price
**Query:** `"iPhone priced at $699"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone",
  "price": 699
}
```

## Condition/Grade Queries

### Example 24: New Product
**Query:** `"New Samsung Galaxy S21"`

**Expected Output:**
```json
{
  "brand": "Samsung",
  "model": "Galaxy S21",
  "backbox_grade": "new"
}
```

### Example 25: Like New
**Query:** `"Like new MacBook Air"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "MacBook Air",
  "backbox_grade": "like_new"
}
```

### Example 26: Good Condition
**Query:** `"iPad in good condition"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPad",
  "backbox_grade": "good"
}
```

### Example 27: Excellent Condition
**Query:** `"Excellent condition iPhone 12"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone 12",
  "backbox_grade": "excellent"
}
```

## Special Offers & Deals

### Example 28: Clearance Sale
**Query:** `"iPhone on clearance sale"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone",
  "deals_type": "clearance"
}
```

### Example 29: Bundle Deal
**Query:** `"PS5 bundle with games"`

**Expected Output:**
```json
{
  "console_type": "PlayStation",
  "model": "PS5",
  "deals_type": "bundle"
}
```

### Example 30: Black Friday
**Query:** `"Black Friday deals on laptops"`

**Expected Output:**
```json
{
  "cat_id": "laptops",
  "deals_type": "black_friday"
}
```

## Complex Multi-Facet Queries

### Example 31: Comprehensive Laptop Query
**Query:** `"Dell XPS 15 laptop with Intel i9, 32GB RAM, 1TB SSD, RTX 3050, touchscreen, under $2500"`

**Expected Output:**
```json
{
  "brand": "Dell",
  "model": "XPS 15",
  "cat_id": "laptops",
  "processor": "Intel i9",
  "memory": "32GB",
  "storage_ssd": "1TB SSD",
  "storage_type": "SSD",
  "graphic_card": "RTX 3050",
  "touchscreen": true,
  "price_ranges": {"max": 2500}
}
```

### Example 32: Comprehensive Smartphone Query
**Query:** `"Samsung Galaxy S22 Ultra 5G, 512GB, black, dual sim, with 108MP camera, under $1200, like new condition"`

**Expected Output:**
```json
{
  "brand": "Samsung",
  "model": "Galaxy S22 Ultra",
  "network": ["5G"],
  "storage": "512GB",
  "color": "black",
  "dual_sim": true,
  "camera": "108MP",
  "price_ranges": {"max": 1200},
  "backbox_grade": "like_new"
}
```

### Example 33: Gaming Setup
**Query:** `"PS5 console with 2 controllers and 18+ action games"`

**Expected Output:**
```json
{
  "console_type": "PlayStation",
  "model": "PS5",
  "controllers_number": 2,
  "pegi": "18",
  "video_game_genre": "action"
}
```

## Edge Cases & Natural Language Variations

### Example 34: Conversational Query
**Query:** `"I'm looking for a good deal on an iPhone, preferably blue, with at least 128 gigs"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone",
  "color": "blue",
  "storage": "128GB",
  "deals_type": "good_deal"
}
```

### Example 35: Abbreviated Query
**Query:** `"MBP M2 16GB"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "MacBook Pro",
  "processor": "M2",
  "memory": "16GB"
}
```

### Example 36: Multiple Alternatives
**Query:** `"iPhone 13 or 14 in blue or white"`

**Expected Output:**
```json
{
  "brand": "Apple",
  "model": "iPhone 13",
  "color": "blue"
}
```
*Note: LLM will typically choose the first mentioned option*

### Example 37: Vague Query
**Query:** `"Something for gaming"`

**Expected Output:**
```json
{
  "cat_id": "gaming"
}
```

### Example 38: Very Specific Technical Query
**Query:** `"Laptop with NVIDIA RTX 3060 Ti, 16:9 screen, HDMI output, IPS display"`

**Expected Output:**
```json
{
  "cat_id": "laptops",
  "graphic_card": "NVIDIA RTX 3060 Ti",
  "screen_format": "16:9",
  "hdmi_output": true,
  "screen_type": "IPS"
}
```

## Tips for Best Results

1. **Be Specific**: More details = more accurate facets
2. **Use Natural Language**: Write as you would speak
3. **Include Key Attributes**: Brand, model, specs, price, condition
4. **Use Common Terms**: "5G" instead of "fifth generation network"
5. **Specify Units**: "256GB" not just "256"
6. **Price Keywords**: "under", "over", "between", "around"
7. **Condition Keywords**: "new", "refurbished", "like new", "excellent"

## Testing Your Queries

Use the test script to try these examples:

```bash
python test_api.py
```

Or test individually:

```bash
curl -X POST http://localhost:8000/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY_HERE", "include_metadata": true}'
```

