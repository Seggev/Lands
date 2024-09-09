from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.MainPage import MainPage


MIN_PRICE = 1000
MAX_PRICE = 1200

print("Starting script")
locations = []
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
    print(location)

