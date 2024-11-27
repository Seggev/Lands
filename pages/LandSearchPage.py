from time import sleep

from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

URL = "https://www.landsearch.com"
LBL_CONTAINER = 'div[class="preview-content"]'
LBL_COUNTY = 'span[class="g-e preview__subterritory"]'
LBL_ADDRESS = 'div[class^="preview__location g-e"]'
BTN_NEXT = 'a[rel="next"]'

class LandSearchPage(BasePage):
    def __init__(self, driver, min_price=0, max_price=0):
        if min_price > 0 and max_price > 0:
            super().__init__(driver,
                             f"{URL}/properties/filter/format=sales,price[max]={max_price},price[min]={min_price}/")
        else:
            super().__init__(driver, URL)

    def get_location_on_page(self):
        self.wait_for_element(By.CSS_SELECTOR, LBL_CONTAINER)
        containers = self.find_elements(By.CSS_SELECTOR, LBL_CONTAINER)
        locations = []

        for container in containers:
            sleep(0.3)
            self.scroll_to_element(container)
            county = self.get_text_with_retry(container, By.CSS_SELECTOR, LBL_COUNTY)
            address = self.get_text_with_retry(container, By.CSS_SELECTOR, LBL_ADDRESS)

            if county and address:
                state = address.split(',')[1].strip()[:2]
                locations.append((county, state))

        return locations



    def is_next_button_appears(self):
        return self.wait_for_element(By.CSS_SELECTOR,BTN_NEXT,3) is not None

    def click_next(self):
        self.click_element(By.CSS_SELECTOR, BTN_NEXT)
