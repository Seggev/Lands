from datetime import datetime
from pathlib import Path
from time import sleep

from pages.ApacheDetailsPage import ApacheDetailsPage
from pages.ApacheParcelsPage import ApacheParcelsPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.ApacheTreasurerPage import ApacheTreasurerPage
from utils.ExcelHandler import ExcelHandler

#################################
SUBDIVISION = "CONCHO LAKELAND"
SILENT_MODE = True
#################################

print("Starting script")
chrome_options = Options()
if SILENT_MODE:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"Apache_apns_{SUBDIVISION}-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
excel_handler = ExcelHandler(full_file_name)

parcels = []

parcels_page = ApacheParcelsPage(driver)
parcels_page.click_advanced()
parcels_page.select_vacant_land()
parcels_page.insert_subdivision(SUBDIVISION)
parcels_page.click_search()
parcels_page.click_first_apn()
details_page = ApacheDetailsPage(driver)
try:
    while details_page.is_next_appears():
        apn = details_page.get_apn()
        details_page.click_parcel_details()
        parcel_size = details_page.get_parcel_size()
        details_page.click_owner_info()
        owner_name = details_page.get_owner_name()
        if "LLC" in owner_name or "INC." in owner_name:
            print(f"Skipping Owner {owner_name}")
            details_page.click_next()
            details_page = ApacheDetailsPage(driver)
            continue
        state = details_page.get_state()
        if "AZ" in state:
            print(f"Skipping state {state}, apn is {apn}")
            details_page.click_next()
            details_page = ApacheDetailsPage(driver)
            continue
        owner_address = details_page.get_owner_address()
        city = details_page.get_owner_city()
        zip = details_page.get_zip()
        account = details_page.get_account_number()

        print(f"APN: {apn}")
        print(f"SIZE: {parcel_size}")
        print(f"NAME: {owner_name}")
        print(f"ADRS: {owner_address}")
        print(f"CITY: {city}")
        print(f"STATE: {state}")
        print(f"ZIP: {zip}")
        print(f"ACCOUNT: {account}")
        parcels.append({"apn": apn,
                        "size": parcel_size,
                        "name": owner_name,
                        "address": owner_address,
                        "city": city,
                        "state": state,
                        "zip": zip,
                        "account": account
                        })
        details_page.click_next()
        details_page = ApacheDetailsPage(driver)
except Exception as e:
    print(f"Error in loop: {str(e)}")

for parcel in parcels:
    tres_page = ApacheTreasurerPage(driver, parcel["account"])
    tax_due = tres_page.get_tax_due()
    print(f"Tax: {tax_due}")
    parcel["tax"] = tax_due

excel_handler.create_excel(parcels, "APNS")
