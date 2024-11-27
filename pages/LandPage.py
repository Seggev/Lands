from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

LBL_PRICE = "span.pricebox.pricebox-post_promo"
LBL_ACRES = "span.textbox.textbox-property_acreage"
LBL_APN = "span.textbox.textbox-apn"
LBL_DATE = "span.posted-by-snippet-date"


def get_area_by_apn(apn):
    dash_index = apn.find("-")
    if dash_index != -1:
        return apn[:dash_index]
    else:
        return ""


class LandPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def print_details(self):
        try:
            price = self.get_text(By.CSS_SELECTOR, LBL_PRICE)
            acres = self.get_text(By.CSS_SELECTOR, LBL_ACRES)
            apn = self.get_text(By.CSS_SELECTOR, LBL_APN)
            offer = int(float(price.replace('$', '').replace(',', ''))) / 4
            print(f"Price: {price}")
            print(f"Acres: {acres}")
            print(f"APN: {apn}")
            print(f"Offer: {offer}")
        except Exception as e:
            print(f"Error in LandPage.print_details: {str(e)}")

    def get_details(self):
        price = self.get_text(By.CSS_SELECTOR, LBL_PRICE)
        acres = self.get_text(By.CSS_SELECTOR, LBL_ACRES)
        apn = self.get_text(By.CSS_SELECTOR, LBL_APN)
        area = get_area_by_apn(apn)
        date = self.get_text(By.CSS_SELECTOR, LBL_DATE)
        offer = "N\A"
        try:
            offer = int(float(price.replace('$', '').replace(',', ''))) / 4
        except Exception as e:
            print(f"Error getting offer: {str(e)}")
        return [price, acres, apn, area, offer, date]
