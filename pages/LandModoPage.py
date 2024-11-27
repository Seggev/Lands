from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

URL = "https://www.landmodo.com"
BTN_SEARCH = ("button[type=\"submit\"].btn.btn_home_search.btn-block.btn-lg, button["
              "type=\"submit\"].btn.btn-primary.btn-block")
TXT_MIN_PRICE = "min_price"
TXT_MAX_PRICE = "max_price"
BTN_NEXT = "a[rel=\"next\"][aria-label=\"next\"]"
TXT_SEARCH_LOCATION = "input.form-control.googleSuggest.googleLocation.pac-target-input#location_google_maps_homepage"
BTN_VIEW_MORE = "a.btn.btn-success.col-sm-5.view-details.rmargin"


class LandModoPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, URL)

    def click_search(self):
        self.click_element(By.CSS_SELECTOR,
                                 BTN_SEARCH)

    def insert_min_price(self, min_price):
        self.enter_text(By.ID, TXT_MIN_PRICE, min_price)

    def insert_max_price(self, max_price):
        self.enter_text(By.ID, TXT_MAX_PRICE, max_price)

    def get_locations_as_text(self):
        self.wait_for_element(By.CSS_SELECTOR, "div.post-location-snippet.bmargin.font-sm")
        location_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.post-location-snippet.bmargin.font-sm")
        locations_as_text = []
        for element in location_elements:
            locations_as_text.append(element.text)
        return locations_as_text

    def click_next_page(self):
        next_button = self.wait_for_element(By.CSS_SELECTOR, BTN_NEXT)
        if next_button:
            self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
            self.click_element(By.CSS_SELECTOR,BTN_NEXT)
        else:
            print("Next button not found")

    def is_next_button_present(self):
        return len(self.find_elements(By.CSS_SELECTOR, BTN_NEXT)) > 0

    def insert_location_search_query(self, query):
        self.enter_text(By.CSS_SELECTOR, TXT_SEARCH_LOCATION, query)

    def get_all_lands_in_page(self):
        return self.driver.find_elements(By.CSS_SELECTOR, BTN_VIEW_MORE)

    def get_all_lands_as_links(self):
        lands_as_links = []
        self.wait_for_element(By.CSS_SELECTOR,BTN_VIEW_MORE)
        lands = self.driver.find_elements(By.CSS_SELECTOR, BTN_VIEW_MORE)
        for land in lands:
            lands_as_links.append(land.get_attribute('href'))
        return lands_as_links
