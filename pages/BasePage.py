from selenium.webdriver import ActionChains, Keys
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
        return WebDriverWait(self.driver, timeout).until(
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

    def open_link_in_a_new_tab(self, url):
        """Open a URL in a new tab."""
        # Open the URL in a new tab using JavaScript
        self.driver.execute_script(f"window.open('{url}', '_blank');")

        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_most_recent_tab(self):
        """Close the most recent tab and switch back to the original tab."""
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles

        # Check if there is more than one tab
        if len(all_windows) > 1:
            # Close the most recent tab
            self.driver.close()

            # Switch to the original tab
            for window in all_windows:
                if window != current_window:
                    self.driver.switch_to.window(window)
                    break
        else:
            print("There is only one tab open, cannot close the most recent tab.")
