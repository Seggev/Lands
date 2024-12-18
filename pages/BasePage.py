from time import sleep

from selenium.common import TimeoutException, StaleElementReferenceException, JavascriptException
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

    def wait_for_element(self, by, value, timeout=8):
        """Wait for an element to be present and visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Timeout: Element not found within {timeout} seconds: ({by}, {value})")
            return None

    def wait_for(self,element, timeout=3):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of(element)
            )
        except TimeoutException:
            print(f"Timeout: Element not found within {timeout} seconds")
            return None

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
        if element is not None:
            return element.text
        else:
            # Optionally log or raise an exception if the element is not found
            print(f"Element not found: {by} = {value}")
            return ""

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

    def scroll_to_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_start(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_text_with_retry(self, parent_element, by, selector, max_attempts=3, timeout=10):
        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(parent_element, timeout).until(
                    EC.presence_of_element_located((by, selector))
                )
                return element.text
            except (StaleElementReferenceException, TimeoutException):
                if attempt == max_attempts - 1:
                    print(f"Failed to get text for selector {selector} after {max_attempts} attempts")
                    return None

    def scroll_to_element(self, element, max_retries=3, wait_time=1):
        for attempt in range(max_retries):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                return True
            except (StaleElementReferenceException, JavascriptException) as e:
                if attempt < max_retries - 1:  # If it's not the last attempt
                    print(f"Scroll attempt {attempt + 1} failed. Retrying in {wait_time} second(s)...")
                    sleep(wait_time)
                else:
                    print(f"Failed to scroll to element after {max_retries} attempts: {str(e)}")
                    return False
        return False

    def is_mac(self):
        # This method can be used to detect if the test is running on a macOS system
        import platform
        return platform.system() == "Darwin"

    def switch_to_new_tab(self):
        # Get the current window handles and switch to the new one
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def close_current_tab_and_focus_on_first(self):
        """
        Closes the current tab and switches focus to the first tab.
        """
        # Close the current tab
        self.driver.close()

        # Get all window handles and switch to the first one
        first_tab = self.driver.window_handles[0]
        self.driver.switch_to.window(first_tab)