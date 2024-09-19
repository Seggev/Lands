from time import sleep
from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

BTN_ADVANCE = ''
LBL_OWNER_NAME = "//td[b[text()='Owner Name']] | //span[text()='Owner Name']/following-sibling::br/following-sibling::span/span[contains(@class, 'text')]"
LBL_OWNER_ADDRESS = "//td[b[text()='Owner Address']] | //span[text()='Address1']/following-sibling::br/following-sibling::span/span[contains(@class, 'text')]"
LBL_APN = "//td[strong[text()='Parcel Number']]"
BTN_NEXT = "//a[contains(text(), 'Next->')]"
BTN_PARCEL_DETAILS = "//td[@id='left_column']//a[text()='Parcel Detail']"
BTN_OWNER_INFO = "//td[@id='left_column']//a[text()='Owner Information']"
BTN_SALE_HISTORY = "//div[@id='left']//a[text()='Sale History']"
BTN_VIEW_TAX = "//div[@id='left']//a[text()='View this account in Eagle Treasurer']"
BTN_ACCOUNT_SUMMARY = "//div[@id='externalLinks']//a[text()='View this account in Eagle Assessor']"
LBL_PARCEL_SIZE = "//span[text()='Parcel Size']/following-sibling::br/following-sibling::span//span[contains(@class, 'text')]"
LBL_CITY = "//span[text()='City']/following-sibling::br/following-sibling::span/span[contains(@class, 'text')]"
LBL_STATE = "//span[text()='State']/following-sibling::br/following-sibling::span/span[contains(@class, 'text')]"
LBL_ZIP = "//span[text()='Zip']/following-sibling::br/following-sibling::span/span[contains(@class, 'text')]"
LBL_LAST_DATE = "(//table[@id='SelectedGroupHTMLSummary']//tr/td[5]//span[@class='text'])[last()]"
LBL_TOTAL_DUE = "//tr[./td[normalize-space()='Total Due']]//td[@align='right']"

CSS = By.CSS_SELECTOR
XPATH = By.XPATH


class ApacheDetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_owner_name(self):
        return self.get_text(XPATH, LBL_OWNER_NAME).replace("Owner Name ", "")

    def get_owner_address(self):
        return self.get_text(XPATH, LBL_OWNER_ADDRESS).replace("Owner Address ", "")

    def get_owner_city(self):
        return self.get_text(XPATH, LBL_CITY)

    def get_state(self):
        return self.get_text(XPATH, LBL_STATE)

    def get_zip(self):
        return self.get_text(XPATH, LBL_ZIP)

    def get_apn(self):
        return self.get_text(XPATH, LBL_APN).replace("Parcel Number ", "")

    def get_last_date(self):
        if self.wait_for_element(XPATH, LBL_LAST_DATE, 3):
            return self.get_text(XPATH, LBL_LAST_DATE)
        return "N\A"

    def get_parcel_size(self):
        return self.get_text(XPATH, LBL_PARCEL_SIZE)

    def get_tax_due(self):
        return self.get_text(XPATH, LBL_TOTAL_DUE)

    def click_next(self):
        self.click_element(XPATH, BTN_NEXT)

    def click_parcel_details(self):
        self.click_element(XPATH, BTN_PARCEL_DETAILS)

    def click_owner_info(self):
        self.click_element(XPATH, BTN_OWNER_INFO)

    def click_sale_history(self):
        if self.wait_for_element(XPATH, BTN_SALE_HISTORY, 1):
            self.click_element(XPATH, BTN_SALE_HISTORY)

    def click_view_tax(self):
        self.click_element(XPATH, BTN_VIEW_TAX)

    def click_account_summary(self):
        self.click_element(XPATH, BTN_ACCOUNT_SUMMARY)

    def is_next_appears(self):
        return self.wait_for_element(XPATH, BTN_NEXT, 5)
