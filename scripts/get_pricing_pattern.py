from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.LandPage import LandPage
from pages.MainPage import MainPage

COUNTY_TO_SEARCH = "Izard County AR"

print("Starting script")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
main_page = MainPage(driver)
main_page.click_search()
main_page.insert_location_search_query(COUNTY_TO_SEARCH)
lands_links = main_page.get_all_lands_as_links()

while main_page.is_next_button_present():
    for land_link in lands_links:
        main_page.open_link_in_a_new_tab(land_link)
        land_page = LandPage(driver)
        land_page.print_details()
        print("###################")
        land_page.close_most_recent_tab()
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab
        sleep(1)

    main_page.click_next_page()

