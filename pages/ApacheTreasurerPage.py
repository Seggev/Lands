from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

TXT_PARCEL = "#TaxAParcelID"
BTN_SEARCH = " input[type=submit]"
# LBL_TOTAL_DUE = "//div[@id='totals']//tr[td[contains(text(), 'Total Due')]]/td[last()]"
LBL_TOTAL_DUE = "#totals .hasLabel .label + td[align='right']"

CSS = By.CSS_SELECTOR

class ApacheTreasurerPage(BasePage):
    def __init__(self, driver, account):
        super().__init__(driver,f"https://eagletreasurer.co.apache.az.us:8443/treasurer/treasurerweb/account.jsp?guest=true&account={account}" )

    def insert_apn(self, apn):
        self.enter_text(CSS, TXT_PARCEL, apn)

    def click_search(self):
        self.click_element(CSS, BTN_SEARCH)

    def get_tax_due(self):
        return self.get_text(By.CSS_SELECTOR, LBL_TOTAL_DUE)

