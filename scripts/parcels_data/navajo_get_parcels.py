from datetime import datetime
import time
from pathlib import Path

from utils.ApiClient import ApiClient
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from utils.ExcelHandler import ExcelHandler

print("Starting script")

client = ApiClient("")
books = [103, 104, 105, 106, 108, 109, 110, 111, 201, 202, 205,
         206, 207, 210, 212, 303, 309, 403, 404, 925, 983]
# books = [103]

def get_blocks_count_by_book(book):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://apps.navajocountyaz.gov/webmap/WebMap.aspx",
        "X-Requested-With": "XMLHttpRequest"
    }
    params = {
        "type": "map",
        "searchstr": "",
        "book": str(book)
    }
    html = ApiClient("").get("https://apps.navajocountyaz.gov/webmap/HttpHandlers/BookMap.ashx", params=params,
                             headers=headers)["content"]
    root = ET.fromstring(html)
    count = len(root.findall('Item'))
    return count

def get_parcels(book, block):
    url = "https://apps.navajocountyaz.gov/webmap/HttpHandlers/ExportKml.ashx"
    filter_value = f"{book}-{block}"
    params = {
        "filter": "apn",
        "filtervalue": filter_value,
        "_": int(time.time() * 1000)
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7,es-AR;q=0.6,es;q=0.5",
        "Referer": "https://apps.navajocountyaz.gov/webmap/WebMap.aspx",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = client.get(url, params, headers)
    response_content = response["content"].replace("ï»¿", "")
    if isinstance(response_content, bytes):
        if response_content.startswith(b'\xef\xbb\xbf'):
            response_content = response_content[3:]
        response_content = response_content.decode('utf-8')
    else:
        # If response_content is already a string
        if response_content.startswith('\ufeff'):
            response_content = response_content[len('\ufeff'):]
    try:
        root = ET.fromstring(response_content)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(response_content)

    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    apns = []

    for placemark in root.findall('.//kml:Placemark', namespace):
        apn_element = placemark.find('kml:apn', namespace)
        if apn_element is not None and apn_element.text:
            apns.append(apn_element.text)
    return apns


def get_parcel_details(apn):
    response = client.get("https://apps.navajocountyaz.gov/navajowebpayments/propertyinformation",
                          params={"apn": apn})
    content = response["content"]
    soup = BeautifulSoup(content, 'html.parser')

    details = {
        "apn": apn,
        "owner_name": "",
        "address": "",
        "city": "",
        "state": "",
        "zip_code": "",
        "size": "",
        "tax": "",
        "date": "",
        "zoning": ""
    }

    # Extract ownership details
    span_element = soup.find('span', id='lblOwnership_NextYear')
    if span_element:
        raw_text = span_element.decode_contents(formatter="html")
        formatted_text = raw_text.replace('<br>', ', ').replace('<br/>', ', ').strip()

        # Extracting the information into meaningful variables
        parts = [part.strip() for part in formatted_text.split(',')]
        if len(parts) == 3:
            owner_name = parts[0]
            address = parts[1]
            city_state_zip = parts[2]

            # Using regex to extract city, state, and zip
            city_state_zip_pattern = re.match(r'^(.*?)[\s]+([A-Z]{2})[\s]+(\d+)$', city_state_zip)
            if city_state_zip_pattern:
                city = city_state_zip_pattern.group(1)
                state = city_state_zip_pattern.group(2)
                zipcode = city_state_zip_pattern.group(3)

                # Assign extracted details to the dictionary
                details['owner_name'] = owner_name
                details['address'] = address
                details['city'] = city
                details['state'] = state
                details['zipcode'] = zipcode

    # Extract size details
    size_span_element = soup.find('span', id='lblSize_NextYear')
    if size_span_element:
        acres = size_span_element.text.strip()
        details['acres'] = acres

    # Extract assessment type details
    assessment_type_span_element = soup.find('span', id='lblAssessmentType_NextYear')
    if assessment_type_span_element:
        assessment_type = assessment_type_span_element.text.strip()
        details['assessment_type'] = assessment_type

    # Extract last sold date details
    last_sold_span_element = soup.find('span', id='lblLastSold_NextYear')
    if last_sold_span_element:
        last_sold_text = last_sold_span_element.text.strip()
        last_sold_date_match = re.search(r'(\d{2}/\d{2}/\d{4})', last_sold_text)
        if last_sold_date_match:
            last_sold_date = last_sold_date_match.group(1)
            details['last_sold_date'] = last_sold_date

    # Extract zoning details
    zoning_span_element = soup.find('span', id='lblPrimaryZoning')
    if zoning_span_element:
        zoning = zoning_span_element.text.strip()
        details['zoning'] = zoning

        # Extract tax balance
        tax_table = soup.find('table', id='grdTaxHistory')
        if tax_table:
            for row in tax_table.find_all('tr')[1:]:  # Skip the header row
                cells = row.find_all('td')
                if len(cells) > 1:
                    year_balance = cells[0].text.strip()
                    balance = cells[1].text.strip().replace('$', '').replace(',', '')
                    try:
                        tax = float(balance)
                        details['tax'] = tax
                        break  # Assuming we want the balance from the most recent year
                    except ValueError:
                        continue

    return details


data = []
for book in books:
    blocks = get_blocks_count_by_book(book)
    for block in range(1,blocks):
        parcels = get_parcels(book, block)
        for par in parcels:
            details = get_parcel_details(par)
            vacant = "Vacant" in details["zoning"]
            in_az = "AZ" in details["state"]
            if not vacant or in_az:
                continue
            print(details["apn"])
            data.append(details)

root_dir = Path(__file__).parent.parent.parent
date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
file_name = f"Navajo_apns-books-{books}-{date_str}.xlsx"
full_file_name = root_dir / 'data' / file_name
excel_handler = ExcelHandler(full_file_name)
excel_handler.create_excel(data,"apns")