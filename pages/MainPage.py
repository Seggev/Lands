from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

URL = "https://www.landmodo.com"
BTN_SEARCH = ("button[type=\"submit\"].btn.btn_home_search.btn-block.btn-lg, button["
              "type=\"submit\"].btn.btn-primary.btn-block")
TXT_MIN_PRICE = "min_price"
TXT_MAX_PRICE = "max_price"
BTN_NEXT = "a[rel=\"next\"][aria-label=\"next\"]"


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, URL)

    def click_search(self):
        self.driver.find_element(By.CSS_SELECTOR,
                                 BTN_SEARCH).click()

    def insert_min_price(self, min_price):
        self.driver.find_element(By.ID, TXT_MIN_PRICE).send_keys(min_price)

    def insert_max_price(self, max_price):
        self.driver.find_element(By.ID, TXT_MAX_PRICE).send_keys(max_price)

    def get_locations_as_text(self):
        location_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.post-location-snippet.bmargin.font-sm")
        locations_as_text = []
        for element in location_elements:
            locations_as_text.append(element.text)
        return locations_as_text

    def click_next_page(self):
        self.driver.find_element(By.CSS_SELECTOR, BTN_NEXT).click()

    def is_next_button_present(self):
        return len(self.find_elements(By.CSS_SELECTOR, BTN_NEXT)) > 0