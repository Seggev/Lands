from time import sleep
from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

BTN_ADVANCE = '#tabs > li:nth-child(2) > a'
TXT_SUBDIVISION = '#token-input-PlattedLegalIDSubdivision'
OPTION_VACANT = '#accountTypeID > option:nth-child(20)'
BTN_SEARCH = 'input[type=submit]'
BTN_SELECT_SUBDIVISION = 'li[class="token-input-dropdown-item2 token-input-selected-dropdown-item"]'
LBL_PARCELS = 'tr.tableRow1 > td > a > table > tbody > tr > td:first-child b, tr.tableRow2 > td > a > table > tbody > tr > td:first-child b'
BTN_NEXT = "//a[contains(text(), 'Next->')]"

CSS = By.CSS_SELECTOR
XPATH = By.XPATH


class ApacheParcelsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url='https://eagleassessor.co.apache.az.us/assessor/taxweb/search.jsp?guest=true')

    def click_advanced(self):
        self.click_element(CSS, BTN_ADVANCE)

    def insert_subdivision(self, text):
        self.enter_text(CSS, TXT_SUBDIVISION, text)
        sleep(2)
        self.click_element(CSS,BTN_SELECT_SUBDIVISION)

    def select_vacant_land(self):
        self.click_element(CSS, OPTION_VACANT)

    def click_search(self):
        self.click_element(CSS, BTN_SEARCH)

    def get_parcels_text(self):
        apns_as_text = []
        apns = self.get_apns()
        for apn in apns:
            apns_as_text.append(apn.text)
        return apns_as_text

    def get_apns(self):
        return  self.find_elements(CSS,LBL_PARCELS)

    def click_first_apn(self):
        self.click_element(CSS, LBL_PARCELS)

    def click_next(self):
        self.click_element(XPATH,BTN_NEXT)

    def is_next_appears(self):
        return self.wait_for_element(XPATH,BTN_NEXT,5)

