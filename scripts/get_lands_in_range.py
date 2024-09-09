from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.MainPage import MainPage
from utils.GeocodeAPI import GeocodeAPI

MIN_PRICE = 1000
MAX_PRICE = 1200
HAS_API = False
API_KEY=""

print("Starting script")
locations = []
geo = GeocodeAPI(API_KEY)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
main_page = MainPage(driver)
main_page.click_search()
main_page.insert_min_price(MIN_PRICE)
main_page.insert_max_price(MAX_PRICE)
main_page.click_search()
while main_page.is_next_button_present():
    locations.extend(main_page.get_locations_as_text())
    main_page.click_next_page()

for location in locations:
    if HAS_API:
        print(geo.get_county_and_state(location))
    else:
        print(location)

