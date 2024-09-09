from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, url=''):
        self.driver = driver
        self.url = url
        if url:
            self.driver.get(url)

    def find_element(self, by, value):
        """Find a single element."""
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        """Find multiple elements."""
        return self.driver.find_elements(by, value)

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def click_element(self, by, value):
        """Click on an element."""
        element = self.wait_for_element(by, value)
        element.click()

    def enter_text(self, by, value, text):
        """Enter text into an input field."""
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """Get text from an element."""
        element = self.wait_for_element(by, value)
        return element.text

    def is_element_present(self, by, value):
        """Check if an element is present on the page."""
        try:
            self.find_element(by, value)
            return True
        except:
            return False

    def go_to_url(self, url):
        """Navigate to a given URL."""
        self.driver.get(url)

    def close_browser(self):
        """Close the browser."""
        self.driver.quit()
