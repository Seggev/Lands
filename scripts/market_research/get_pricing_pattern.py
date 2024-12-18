import os
from datetime import datetime
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.LandPage import LandPage
from pages.LandModoPage import LandModoPage
from utils.ExcelHandler import ExcelHandler

###################################################
COUNTY_TO_SEARCH = "Sandoval county NM"
SILENT_MODE = True
###################################################


print("Starting script")
root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"{COUNTY_TO_SEARCH}-Demand-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
chrome_options = Options()
if SILENT_MODE:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
main_page = LandModoPage(driver)
main_page.click_search()
main_page.insert_location_search_query(COUNTY_TO_SEARCH)
main_page.click_search()
lands_links = main_page.get_all_lands_as_links()
data = {"Price": [], "Acres": [], "APN": [], "Area": [], "Date": [], "Offer": [], "Link": []}
try:
    while main_page.is_next_button_present():
        for land_link in lands_links:
            main_page.open_link_in_a_new_tab(land_link)
            land_page = LandPage(driver)
            land_page.print_details()
            details = land_page.get_details()
            data["Price"].append(details[0])
            data["Acres"].append(details[1])
            data["APN"].append(details[2])
            data["Area"].append(details[3])
            data["Offer"].append(details[4])
            data["Date"].append(details[5])
            data["Link"].append(land_link)
            print(f"Link: {land_link}")
            land_page.close_most_recent_tab()
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

        main_page.click_next_page()
        sleep(1)
        lands_links = main_page.get_all_lands_as_links()
except Exception as e:
    print(f"An error occurred: {str(e)}")



excel_handler = ExcelHandler(full_file_name)
excel_handler.create_excel(data, COUNTY_TO_SEARCH)
