from exceptiongroup import catch
from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

TXT_APN = 'input[name="parcelNumber_input"]'
BTN_SUBMIT = 'input[type="submit"]'
LBL_TAX = 'tfoot[class="k-grid-footer"]'
BTN_NEW_PARCEL ='a[href="/Parcel/NewParcel"]'
BTN_OWNER_HISTORY = 'a[href="/Parcel/OwnerHistory"]'
LBL_DATE = '#Grid > table > tbody > tr:nth-child(1) > td:nth-child(1)'

class CochisePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url='https://parcelinquirytreasurer.cochise.az.gov/Parcel/TaxSummary')

    def insert_apn(self,apn, retries=3):
        try:
            if retries < 1:
                return
            self.enter_text(By.CSS_SELECTOR,TXT_APN,apn)
            self.click_element(By.CSS_SELECTOR,BTN_SUBMIT)
        except Exception as e:
            self.go_to_url('https://parcelinquirytreasurer.cochise.az.gov/Parcel/TaxSummary')
            self.insert_apn(apn,retries-1)

    def get_tax(self):
        tax = self.get_text(By.CSS_SELECTOR,LBL_TAX)
        return tax.replace("Total Due:","").replace("\n","").replace("$","")

    def click_new_parcel(self):
        try:
            self.click_element(By.CSS_SELECTOR,BTN_NEW_PARCEL)
        except Exception as e:
            self.go_to_url('https://parcelinquirytreasurer.cochise.az.gov/Parcel/TaxSummary')

    def click_owner_history(self):
        self.click_element(By.CSS_SELECTOR,BTN_OWNER_HISTORY)

    def get_effective_date(self):
        return self.get_text(By.CSS_SELECTOR, LBL_DATE)