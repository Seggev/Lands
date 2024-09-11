from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.MainPage import MainPage
from utils.ExcelHandler import ExcelHandler
from utils.GeocodeAPI import GeocodeAPI

###################################################
MIN_PRICE = 1000
MAX_PRICE = 1200
HAS_API = False
API_KEY=""
FILE_NAME="../locations.xlsx"
###################################################

print("Starting script")
locations = []
geo = GeocodeAPI(API_KEY)
excel_handler = ExcelHandler(FILE_NAME)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
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

excel_handler.create_excel(locations,"locations")