from time import sleep

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from pages.BasePage import BasePage

URL = "https://www.land.com"
TXT_SEARCH_LOCATION = "#placard-info p"
BTN_NEXT = "(//div[@class='_4f9ac'][span[contains(text(), 'Next')]])"


class LandComPage(BasePage):
    def __init__(self, driver, min_price=0, max_price=0):
        if min_price > 0 and max_price > 0:
            super().__init__(driver, f"{URL}/United-States/all-land/{min_price}-{max_price}/")
        else:
            super().__init__(driver, URL)

    def is_next_button_present(self):
        self.scroll_to_last_element()
        self.wait_for_element(By.XPATH, BTN_NEXT, 1)
        is_appears = len(self.find_elements(By.XPATH, BTN_NEXT)) > 0
        self.scroll_to_first_element()
        return is_appears

    def click_next_page(self):
        if self.is_next_button_present():
            next_button = self.find_element(By.XPATH, BTN_NEXT)
            self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
        else:
            print("Next button not found")

    def get_locations_as_text(self):
        self.wait_for_element(By.CSS_SELECTOR, TXT_SEARCH_LOCATION)
        sleep(0.2)
        location_elements = self.driver.find_elements(By.CSS_SELECTOR, TXT_SEARCH_LOCATION)
        locations_as_text = []
        for element in location_elements:
            # Add retry mechanism for stale element reference
            for _ in range(3):  # Retry up to 3 times
                try:
                    locations_as_text.append(element.text)
                    break  # Exit the retry loop if successful
                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException encountered. Retrying... {_}")
                    location_elements = self.driver.find_elements(By.CSS_SELECTOR, TXT_SEARCH_LOCATION)
        return locations_as_text

    def scroll_to_last_element(self):
        locations = self.find_elements(By.CSS_SELECTOR, TXT_SEARCH_LOCATION)
        if len(locations) > 0:
            self.driver.execute_script("arguments[0].scrollIntoView();", locations[-1])

    def scroll_to_first_element(self):
        locations = self.find_elements(By.CSS_SELECTOR, TXT_SEARCH_LOCATION)
        if len(locations) > 0:
            self.driver.execute_script("arguments[0].scrollIntoView();", locations[0])

