from pages.ApacheDetailsPage import ApacheDetailsPage
from pages.ApacheParcelsPage import ApacheParcelsPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.ExcelHandler import ExcelHandler

#################################
SUBDIVIDION = "CONCHO LAKELAND"
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
excel_handler = ExcelHandler(f"../Apache_apns_{SUBDIVIDION}.xlsx")

parcels = []

parcels_page = ApacheParcelsPage(driver)
parcels_page.click_advanced()
parcels_page.select_vacant_land()
parcels_page.insert_subdivision(SUBDIVIDION)
parcels_page.click_search()
parcels_page.click_first_apn()
# apns = parcels_page.get_apns()
# apns[0].click()
details_page = ApacheDetailsPage(driver)
try:
    while details_page.is_next_appears():
        apn = details_page.get_apn()
        details_page.click_parcel_details()
        parcel_size = details_page.get_parcel_size()
        details_page.click_owner_info()
        owner_name = details_page.get_owner_name()
        if "LLC" in owner_name:
            continue
        owner_address = details_page.get_owner_address()
        city = details_page.get_owner_city()
        state = details_page.get_state()
        zip = details_page.get_zip()

        print(f"APN: {apn}")
        print(f"SIZE: {parcel_size}")
        print(f"NAME: {owner_name}")
        print(f"ADRS: {owner_address}")
        print(f"CITY: {city}")
        print(f"STATE: {state}")
        print(f"ZIP: {zip}")
        parcels.append({"apn":apn,
                        "size":parcel_size,
                        "name":owner_name,
                        "address":owner_address,
                        "city":city,
                        "state": state,
                        "zip": zip
                        })
        details_page.click_next()
        details_page = ApacheDetailsPage(driver)
        if apn == "107-30-053":
            break
except Exception as e:
    print(f"Error in loop: {str(e)}" )

excel_handler.create_excel(parcels,"APNS")



