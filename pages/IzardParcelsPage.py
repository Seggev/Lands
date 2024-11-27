from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


URL = "https://www.actdatascout.com/RealProperty/Arkansas/Izard"
BTN_PARCEL = '#PublicSearchTypePanel ul.nav li a[href="#rpparcel"]'
TXT_PARCEL = "#ParcelNumber"
BTN_SEARCH = "#RPParcelSubmit"
LBL_APN = 'td[data-test="parcelNumber"]'
BTN_DETAILS = 'button[name^="submitLink"]'
LBL_NAME = 'td[class="col-lg-8"]'
BTN_BACK_TO_RESULTS = 'a[href="/RealProperty/BackToPublicResults"]'
BTN_BACK_TO_SEARCH = 'a[href="/RealProperty/Index"]'


class IzardParcelsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url=URL)

    def click_parcel(self):
        self.click_element(By.CSS_SELECTOR, BTN_PARCEL)

    def insert_apn(self, apn):
        self.enter_text(By.CSS_SELECTOR,TXT_PARCEL,apn)

    def click_search(self):
        self.wait_for_element(By.CSS_SELECTOR,BTN_SEARCH,2).click()

    def wait_for_apns(self):
        self.wait_for_element(By.CSS_SELECTOR, LBL_APN)

    def get_apns(self):
        apns = self.find_elements(By.CSS_SELECTOR, LBL_APN)
        apn_list = []
        for apn in apns:
            apn_list.append(apn.text)
        return apn_list

    def get_details_buttons(self):
        return self.find_elements(By.CSS_SELECTOR, BTN_DETAILS)

    def click_back_to_results(self):
        self.click_element(By.CSS_SELECTOR,BTN_BACK_TO_RESULTS)

    def click_back_to_search(self):
        self.click_element(By.CSS_SELECTOR,BTN_BACK_TO_SEARCH)

    def click_button_in_new_tab(self, button):
        # Use ActionChains to perform CONTROL/COMMAND + click
        actions = ActionChains(self.driver)

        # Open link in new tab (Control+Click for Windows/Linux, Command+Click for Mac)
        if self.is_mac():
            actions.key_down(Keys.COMMAND).click(button).key_up(Keys.COMMAND).perform()
        else:
            actions.key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()

        # Switch to the new tab
        self.switch_to_new_tab()