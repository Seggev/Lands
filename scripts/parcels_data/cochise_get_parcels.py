import os
from datetime import datetime
from pathlib import Path

from pages.CochisePage import CochisePage
from utils.ApiClient import ApiClient
from utils.ExcelHandler import ExcelHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

###################################
APN_PREFIX = "406"
MIN_ACRES = 0.14
MAX_ACRES = 1
SILENT_MODE = True
BASE_URL = "https://services6.arcgis.com"


###################################

def get_parcel_count(api_client, apn_prefix, acres_min=0.14, acres_max=1):
    endpoint = "/Yxem0VOcqSy8T6TE/arcgis/rest/services/Cad_Parcel_TaxInfo/FeatureServer/0/query"
    where_clause = (
        f"((apn LIKE '{apn_prefix}%') AND (accttype = 'Vacant') AND "
        f"(owner_name1 NOT LIKE '%LLC') AND (acres >= {acres_min}) AND (acres <= {acres_max}) AND "
        "(state <> 'AZ') AND (owner_name1 NOT LIKE '%PROPERTIES%'))"
    )

    params = {
        "f": "json",
        "where": where_clause,
        "returnIdsOnly": "true",
        "returnCountOnly": "true",
        "returnGeometry": "false",
        "spatialRel": "esriSpatialRelIntersects"
    }
    return api_client.get(endpoint, params)


def query_parcel_info(api_client, apn_prefix, acres_min=0.14, acres_max=1):
    endpoint = "/Yxem0VOcqSy8T6TE/arcgis/rest/services/Cad_Parcel_TaxInfo/FeatureServer/0/query"
    where_clause = (
        f"((apn LIKE '{apn_prefix}%') AND (accttype = 'Vacant') AND "
        f"(owner_name1 NOT LIKE '%LLC') AND (acres >= {acres_min}) AND (acres <= {acres_max}) AND "
        "(state <> 'AZ') AND (owner_name1 NOT LIKE '%PROPERTIES%'))"
    )

    params = {
        "f": "json",
        "where": where_clause,
        "returnGeometry": "true",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*",
        "orderByFields": "OBJECTID ASC",
        "outSR": "102100"
    }
    return api_client.get(endpoint, params)


print("Starting script")
apn_list = []
api_client = ApiClient(BASE_URL)
root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"Cochise_apns_{APN_PREFIX}-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
print(f"full_file_name: {full_file_name}")
excel_handler = ExcelHandler(full_file_name)
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
    count_response = get_parcel_count(api_client, APN_PREFIX + str(i), MIN_ACRES, MAX_ACRES)
    data_response = query_parcel_info(api_client, APN_PREFIX + str(i), MIN_ACRES, MAX_ACRES)
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

excel_handler.create_excel(apn_list, "APNS")
