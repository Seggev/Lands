from datetime import datetime
from pathlib import Path
from collections import Counter
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.LandComPage import LandComPage
from pages.LandModoPage import LandModoPage
from pages.LandSearchPage import LandSearchPage
from utils.ExcelHandler import ExcelHandler
from utils.GeocodeAPI import GeocodeAPI

###################################################
MIN_PRICE = 2800
MAX_PRICE = 4000
API_KEY = ""
SILENT_MODE = True
###################################################

print("Starting script")
root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"Range-{MIN_PRICE}-{MAX_PRICE}-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
excel_handler = ExcelHandler(full_file_name)

# Initialize dictionaries to store locations for each site
site_locations = {
    'landmodo': [],
    'landcom': [],
    'landsearch': []
}

g_locations = {
    'landmodo': [],
    'landcom': [],
    'landsearch': []
}

counties = Counter()
geo = GeocodeAPI(API_KEY)

# Setup Chrome driver
chrome_options = Options()
if SILENT_MODE:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Scrape LandModoPage
print("Scraping LandModo...")
main_page = LandModoPage(driver)
main_page.click_search()
main_page.insert_min_price(MIN_PRICE)
main_page.insert_max_price(MAX_PRICE)
main_page.click_search()
while main_page.is_next_button_present():
    site_locations['landmodo'].extend(main_page.get_locations_as_text())
    main_page.click_next_page()

# Scrape LandComPage
print("Scraping Land.com...")
main_page = LandComPage(driver, MIN_PRICE, MAX_PRICE)
while main_page.is_next_button_present():
    site_locations['landcom'].extend(main_page.get_locations_as_text())
    main_page.click_next_page()

# Scrape LandSearch
print("Scraping LandSearch...")
main_page = LandSearchPage(driver, MIN_PRICE, MAX_PRICE)
while True:
    if API_KEY:
        current_locations = main_page.get_location_on_page()
        g_locations['landsearch'].extend(current_locations)
    else:
        site_locations['landsearch'].extend(main_page.get_location_on_page())
    if not main_page.is_next_button_appears():
        break
    main_page.click_next()
    sleep(1)

# Process locations with geocoding if API_KEY is present
if API_KEY:
    for site, locations in site_locations.items():
        print(f"Processing {site} locations...")
        for location in locations:
            g_location = geo.get_county_and_state(location)
            print(g_location)
            g_locations[site].append(g_location)
            county = g_location[0]
            counties[county] += 1

# Create Excel sheets
print("Creating Excel file...")
if API_KEY:
    # Create separate sheets for each site's geocoded locations
    for site, locations in g_locations.items():
        if locations:  # Only create sheet if there are locations
            excel_handler.create_excel(locations, f"{site}_locations")

    # Create county counts sheet
    county_data = [{"County": county, "Count": count} for county, count in counties.items()]
    excel_handler.edit_excel(file_path=full_file_name, sheet_name="county_counts", data=county_data)
else:
    # Create separate sheets for each site's raw locations
    for site, locations in site_locations.items():
        if locations:  # Only create sheet if there are locations
            excel_handler.create_excel(locations, f"{site}_locations")

print(f"Locations saved to {full_file_name}")
print(f"Location counts by site:")
for site in site_locations.keys():
    count = len(site_locations[site]) if not API_KEY else len(g_locations[site])
    print(f"{site}: {count} locations")