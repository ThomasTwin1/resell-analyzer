from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus

# User input
search_term = input("Search eBay item: ")

# Encode search term
encoded_search = quote_plus(search_term)

# URLs
active_url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_search}"

sold_url = (
    f"https://www.ebay.com/sch/i.html?"
    f"_nkw={encoded_search}&LH_Sold=1&LH_Complete=1"
)

# -------------------------
# CHROME OPTIONS
# -------------------------

options = webdriver.ChromeOptions()

# Open browser maximized
options.add_argument("--start-maximized")

# Hide Selenium automation flag
options.add_experimental_option(
    "excludeSwitches",
    ["enable-automation"]
)

# Disable automation extension
options.add_experimental_option(
    "useAutomationExtension",
    False
)

# Hide automation-controlled browser features
options.add_argument(
    "--disable-blink-features=AutomationControlled"
)

# Create Chrome browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Hide webdriver property from websites
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

# -------------------------
# FUNCTION TO COUNT LISTINGS
# -------------------------

def count_listings(url):

    driver.get(url)

    try:
        # Wait until listings appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".s-item")
            )
        )

        # Find listing elements
        items = driver.find_elements(
            By.CSS_SELECTOR,
            ".s-item"
        )

        count = len(items)

        # Remove junk entry
        if count > 0:
            count -= 1

        return count

    except:
        print("Listings did not load.")
        return 0

# -------------------------
# GET EBAY DATA
# -------------------------

active_count = count_listings(active_url)

sold_count = count_listings(sold_url)

# Close browser
driver.quit()

# -------------------------
# CALCULATIONS
# -------------------------

if active_count > 0:
    sell_through = (
        sold_count / active_count
    ) * 100
else:
    sell_through = 0

total_market_data = (
    sold_count + active_count
)

# -------------------------
# MARKET DEMAND LOGIC
# -------------------------

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

# -------------------------
# OUTPUT
# -------------------------

print("\n--- eBay Market Data ---")

print(f"Search Term: {search_term}")

print(f"Active Listings: {active_count}")

print(f"Sold Listings: {sold_count}")

print(f"Sell-Through Rate: {sell_through:.1f}%")

print(f"Market Data Size: {total_market_data}")

print(f"Market Confidence: {confidence}")

print(f"Market Demand: {demand}")