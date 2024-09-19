from pages.CochisePage import CochisePage
from utils.ApiClient import ApiClient
from utils.ExcelHandler import ExcelHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

###################################
APN_PREFIX = "40"
MIN_ACRES = 0.14
MAX_ACRES = 1
SILENT_MODE = True
###################################

print("Starting script")
apn_list = []
api_client = ApiClient("https://services6.arcgis.com")
excel_handler = ExcelHandler(f"../Cochise_apns_{APN_PREFIX}.xlsx")
chrome_options = Options()
if SILENT_MODE:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
co_page = CochisePage(driver)

for i in range(10):
    count_response = api_client.cochise_get_parcel_count(APN_PREFIX + str(i), MIN_ACRES, MAX_ACRES)
    data_response = api_client.cochise_query_parcel_info(APN_PREFIX + str(i), MIN_ACRES, MAX_ACRES)
    for apn_idx in range(len(data_response["features"])):
        data_response["features"][apn_idx]["attributes"].pop("fcv")
        data_response["features"][apn_idx]["attributes"].pop("ag_operator")
        data_response["features"][apn_idx]["attributes"].pop("mkt_area")
        data_response["features"][apn_idx]["attributes"].pop("mkt_subarea")
        data_response["features"][apn_idx]["attributes"].pop("Shape__Area")
        data_response["features"][apn_idx]["attributes"].pop("Shape__Length")
        apn = data_response["features"][apn_idx]["attributes"]["apn"]
        print(f"APN: {apn}")
        try:
            co_page.insert_apn(apn)
            tax = co_page.get_tax()
            co_page.click_owner_history()
            date = co_page.get_effective_date()
            print(f"Tax: {tax}")
            print(f"Date: {date}")
            co_page.click_new_parcel()
            data_response["features"][apn_idx]["attributes"]["Tax"] = tax
            data_response["features"][apn_idx]["attributes"]["Date"] = date
        except Exception as e:
            print(f"Unable to get tax {e}")
        apn_list.append(data_response["features"][apn_idx]["attributes"])





excel_handler.create_excel(apn_list,"APNS")
