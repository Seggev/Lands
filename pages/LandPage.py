from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

LBL_PRICE = "span.pricebox.pricebox-post_promo"
LBL_ACRES = "span.textbox.textbox-property_acreage"
LBL_APN = "span.textbox.textbox-apn"

class LandPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def print_details(self):
        price_element = self.driver.find_element(By.CSS_SELECTOR, LBL_PRICE)
        acres_element = self.driver.find_element(By.CSS_SELECTOR, LBL_ACRES)
        apn_element = self.driver.find_element(By.CSS_SELECTOR, LBL_APN)
        offer = int(float(price_element.text.replace('$', '').replace(',', '')))/4
        print(f"Price: {price_element.text}")
        print(f"Acres: {acres_element.text}")
        print(f"APN: {apn_element.text}")
        print(f"Offer: {offer}")