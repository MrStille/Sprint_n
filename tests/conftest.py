import pytest
from selenium import webdriver

from data import Data
from pages.main_page import MainPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.get(Data.SITE_URL)
    yield driver
    driver.quit()


@pytest.fixture()
def main_page(driver):
    return MainPage(driver)


@pytest.fixture()
def main_page_set_trip(driver):
    main_page = MainPage(driver)
    main_page.type_route("Хамовнический Вал, 34", "Зубовский бульвар, 37")
    main_page.click_button_call_taxi()
    return main_page