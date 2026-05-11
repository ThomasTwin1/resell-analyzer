import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# User input
search_term = input("Search eBay item: ")

# Encode search term for URL
encoded_search = quote_plus(search_term)

# Browser-like headers
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

# URLs
active_url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_search}"

sold_url = (
    f"https://www.ebay.com/sch/i.html?"
    f"_nkw={encoded_search}&LH_Sold=1&LH_Complete=1"
)

# Request pages
active_response = requests.get(active_url, headers=headers)
sold_response = requests.get(sold_url, headers=headers)

# DEBUG INFO
print("\n--- DEBUG INFO ---")
print("Active status:", active_response.status_code)
print("Sold status:", sold_response.status_code)
print("Active page length:", len(active_response.text))
print("Sold page length:", len(sold_response.text))

# Save HTML pages for debugging
with open("active_debug.html", "w", encoding="utf-8") as file:
    file.write(active_response.text)

with open("sold_debug.html", "w", encoding="utf-8") as file:
    file.write(sold_response.text)

# Parse HTML
active_soup = BeautifulSoup(active_response.text, "html.parser")
sold_soup = BeautifulSoup(sold_response.text, "html.parser")

# Find listings
active_items = active_soup.select(".s-item")
sold_items = sold_soup.select(".s-item")

# Count listings
active_count = len(active_items)
sold_count = len(sold_items)

# Remove junk entry
if active_count > 0:
    active_count -= 1

if sold_count > 0:
    sold_count -= 1

# Sell-through calculation
if active_count > 0:
    sell_through = (sold_count / active_count) * 100
else:
    sell_through = 0

# Market size
total_market_data = sold_count + active_count

# Market demand logic
if total_market_data < 5:
    confidence = "LOW CONFIDENCE"
    demand = "⚠️ NOT ENOUGH DATA"

elif total_market_data < 15:
    confidence = "MEDIUM CONFIDENCE"

    if sell_through >= 50:
        demand = "👍 DECENT DEMAND"
    elif sell_through >= 25:
        demand = "🐢 SLOW DEMAND"
    else:
        demand = "❌ WEAK DEMAND"

else:
    confidence = "HIGH CONFIDENCE"

    if sell_through >= 50:
        demand = "🔥 HOT MARKET"
    elif sell_through >= 25:
        demand = "👍 DECENT DEMAND"
    elif sell_through >= 10:
        demand = "🐢 SLOW DEMAND"
    else:
        demand = "❌ DEAD MARKET"

# Final output
print("\n--- eBay Market Data ---")
print(f"Search Term: {search_term}")
print(f"Active Listings: {active_count}")
print(f"Sold Listings: {sold_count}")
print(f"Sell-Through Rate: {sell_through:.1f}%")
print(f"Market Data Size: {total_market_data}")
print(f"Market Confidence: {confidence}")
print(f"Market Demand: {demand}")

print("\nSaved debug files:")
print("active_debug.html")
print("sold_debug.html")