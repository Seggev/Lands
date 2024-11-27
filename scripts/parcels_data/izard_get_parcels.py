import random
from datetime import datetime
from pathlib import Path
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.IzardDetailsPage import IzardDetailsPage
from pages.IzardParcelsPage import IzardParcelsPage
from utils.ApiClient import ApiClient
from utils.ExcelHandler import ExcelHandler

###################################################
APN_PREFIX = "800"
SILENT_MODE = False
###################################################

def get_parcel_size(api_client, state, apn, fips_codes):
    url = "parcels/v2/by_apn.json"
    params = {
        "state": state,
        "apn": apn,
        "fips_codes": fips_codes
    }

    # Make the GET request
    response = api_client.get(url, params=params)

    # Check if there was an error in the response
    if 'error' in response:
        print(f"Error: {response['error']}")
        return None

    # Parse the acreage from the response
    parcels = response.get('parcels', [])
    if parcels:
        acreage = parcels[0].get('acreage', 'N/A')
        return acreage
    else:
        print("Parcel data not found.")
        return None



print("Starting script")
root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"Izard-APNS-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
excel_handler = ExcelHandler(full_file_name)
base_url = "https://parcels.id.land"
client = ApiClient(base_url)
chrome_options = Options()
if SILENT_MODE:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
apns = []
start_of_range = 0
end_of_range = 10

while start_of_range < end_of_range-1:
    page = IzardParcelsPage(driver)
    page.click_parcel()
    try:
        for i in range(start_of_range, end_of_range):
            print(f"{i:04}")
            start_of_range = i
            page.insert_apn(f"{APN_PREFIX}-{i:04}")
            page.click_search()
            page.wait_for_apns()
            apns.extend(page.get_apns())
            buttons = page.get_details_buttons()
            for btn in buttons:
                page.click_button_in_new_tab(btn)
                details_page = IzardDetailsPage(driver)
                owner_details = details_page.get_details()
                parcel_size = get_parcel_size(client, owner_details['owner_state'], owner_details['parcel_id'], "05065")
                owner_details['size'] = parcel_size
                print(f"Owner details: {owner_details}")
                details_page.close_current_tab_and_focus_on_first()


    except Exception as e:
        print(f"failed on {start_of_range}")
        start_of_range = start_of_range -1

excel_handler.create_excel(apns, "Izard apns")

