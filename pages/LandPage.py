from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

LBL_PRICE = "span.pricebox.pricebox-post_promo"
LBL_ACRES = "span.textbox.textbox-property_acreage"
LBL_APN = "span.textbox.textbox-apn"

class LandPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def print_details(self):
        price = self.get_text(By.CSS_SELECTOR, LBL_PRICE)
        acres = self.get_text(By.CSS_SELECTOR, LBL_ACRES)
        apn = self.get_text(By.CSS_SELECTOR, LBL_APN)
        offer = int(float(price.replace('$', '').replace(',', '')))/4
        print(f"Price: {price}")
        print(f"Acres: {acres}")
        print(f"APN: {apn}")
        print(f"Offer: {offer}")

    def get_details(self):
        price = self.get_text(By.CSS_SELECTOR, LBL_PRICE)
        acres = self.get_text(By.CSS_SELECTOR, LBL_ACRES)
        apn = self.get_text(By.CSS_SELECTOR, LBL_APN)
        offer = int(float(price.replace('$', '').replace(',', ''))) / 4
        return [price,acres,apn, offer]