from pages.BasePage import BasePage
from selenium.webdriver.common.by import By

# CSS/XPATH selectors stored as constants
LBL_NAME = 'td[class="col-lg-8"]'
LBL_PARCEL = "//div[@id='printArea']//span[contains(text(),'Parcel:')]"
LBL_ADDRESS = "//td[text()='Mailing Address:']/following-sibling::td"

class IzardDetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_details(self):
        # Create a dictionary to store the extracted details
        details = {}

        # Extract owner name
        owner_name_element = self.wait_for_element(By.CSS_SELECTOR, LBL_NAME)
        details['owner_name'] = owner_name_element.text

        # Extract parcel ID
        parcel_element = self.find_element(By.XPATH, LBL_PARCEL)
        parcel_text = parcel_element.text
        parcel_id = parcel_text.split("Parcel: ")[1].split("\n")[0]
        details['parcel_id'] = parcel_id

        # Extract mailing address, city, state, and zip
        address_element = self.find_element(By.XPATH, LBL_ADDRESS)
        address_lines = address_element.text.split("\n")

        # First line is the street address
        details['owner_address'] = address_lines[0]

        # Second line contains the city, state, and zip
        city_state_zip = address_lines[1]
        details['owner_city'] = city_state_zip.split(",")[0].strip()

        # Extract state
        details['owner_state'] = city_state_zip.split(",")[1].split()[0].strip()

        # Extract zip code
        details['owner_zip'] = city_state_zip.split()[-1].strip()

        return details
