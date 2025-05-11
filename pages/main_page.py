import re
import time
from time import thread_time

import allure
from selenium.webdriver.common.by import By

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from utils.taxi_tariff import TaxiTariff
from utils.trip_type import TripType
from utils.trip_mode import TripMode


class MainPage(BasePage):

    @allure.step("Выбрать маршруты от {address_from} до {address_to}")
    def type_route(self, address_from, address_to):
        self.wait_element_visible(MainPageLocators.FROM_INPUT).send_keys(address_from)
        self.wait_element_visible(MainPageLocators.TO_INPUT).send_keys(address_to)

    def assert_start_point_a_visible(self, expected_address):
        self.wait_element_visible(MainPageLocators.LABEL_A)
        point_a_name = self.wait_element_visible(MainPageLocators.LABEL_A_TEXT).text
        assert expected_address.lower() in point_a_name.lower()

    def assert_start_point_b_visible(self, expected_address):
        self.wait_element_visible(MainPageLocators.LABEL_B)
        point_a_name = self.wait_element_visible(MainPageLocators.LABEL_B_TEXT).text
        assert expected_address.lower() in point_a_name.lower()

    def assert_route_picker_menu_is_visible(self):
        self.wait_element_visible(MainPageLocators.ROUTE_FORM_PICKER)
        self.wait_element_visible(MainPageLocators.PICKER_MODE_FAST)
        self.wait_element_visible(MainPageLocators.PICKER_MODE_OPTIMUM)
        self.wait_element_visible(MainPageLocators.PICKER_MODE_OWN)

    @allure.step("Проверяем, что блоке меню поездка написано 'Авто Бесплатно' и длительность 'В пути 0 мин'")
    def assert_free_trip(self):
        self.wait_element_visible(MainPageLocators.ROUTE_FORM_PICKER)
        total = self.wait_element_visible(MainPageLocators.TRIP_TOTAL).text
        duration = self.wait_element_visible(MainPageLocators.TRIP_DURATION).text
        assert total == "Авто Бесплатно"
        assert duration == "В пути 0 мин."

    def assert_selected_tab(self, mode):
        tab = MainPage.get_tab_locator(mode)
        css_class = self.wait_element_visible(tab).get_attribute("class")
        assert "active" in css_class

    @allure.step("Проверяем, что в табе 'Свой' доступны все типы движения на маршруте")
    def assert_all_trip_types_available(self):
        self.trip_type_is_available(TripType.CAR)
        self.trip_type_is_available(TripType.WALK)
        self.trip_type_is_available(TripType.TAXI)
        self.trip_type_is_available(TripType.BIKE)
        self.trip_type_is_available(TripType.SCOOTER)
        self.trip_type_is_available(TripType.DRIVE)

    def trip_type_is_available(self, trip_type):
        css_class = self.wait_element_visible(self.get_trip_type(trip_type)).get_attribute("class")
        assert "disable" not in css_class

    def get_trip_type(self, trip_type):
        if trip_type == TripType.CAR:
            return MainPageLocators.TRIP_TYPE_CAR
        elif trip_type == TripType.WALK:
            return MainPageLocators.TRIP_TYPE_WALK
        elif trip_type == TripType.TAXI:
            return MainPageLocators.TRIP_TYPE_TAXI
        elif trip_type == TripType.BIKE:
            return MainPageLocators.TRIP_TYPE_BIKE
        elif trip_type == TripType.SCOOTER:
            return MainPageLocators.TRIP_TYPE_SCOOTER
        elif trip_type == TripType.DRIVE:
            return MainPageLocators.TRIP_TYPE_DRIVE

    @allure.step("Проверяем, что все типы такси доступны для заказа")
    def assert_all_taxi_types_available(self):
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.WORK.value))
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.TALKING.value))
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.SLEEPY.value))
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.GLOSSY.value))
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.COMFORTING.value))
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, TaxiTariff.HOLIDAY.value))

    @allure.step("Проверяем")
    def assert_taxi_tariff_is_selected(self, taxi_tariff):
        css_class = (self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK_BUTTON, taxi_tariff.value)).get_attribute("class"))
        assert "active" in css_class

    @allure.step("Выбираем тариф такси {taxi_tariff}")
    def click_taxi_tariff(self, taxi_tariff):
        self.wait_element_visible(self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK, taxi_tariff.value)).click()

    def get_taxi_tariff_button(self, taxi_type):
        if type(taxi_type) is TaxiTariff:
            return self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK_BUTTON, taxi_type.value)
        else:
            raise TypeError("Wrong type of taxi_type")

    @allure.step("")
    def get_taxi_tariff_cost(self, taxi_tariff):
        # loc = self.format_locator(MainPageLocators.TAXI_TARIFF_COST_TXT, taxi_tariff.value)
        cost = self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_TARIFF_COST_TXT, taxi_tariff.value)).text
        return MainPage.get_cost_from_str(cost)

    def get_pop_up_name(self, taxi_type):
        if taxi_type == TaxiTariff.WORK:
            return self.format_locator(MainPageLocators.TAXI_POP_UP_NAME, 1)

    @allure.step("Переключить таб в блоке маршруты на {mode}")
    def switch_mode(self, mode):
        self.wait_element_visible(MainPage.get_tab_locator(mode)).click()

    def get_total_trip_result(self):
        return self.wait_element_visible(MainPageLocators.TRIP_TOTAL).text

    def get_total_trip_duration(self):
        return self.wait_element_visible(MainPageLocators.TRIP_DURATION).text

    @allure.step("Нажать на тип движения {trip_type}")
    def click_button_trip_type(self, trip_type):
        self.wait_element_visible(self.get_trip_type(trip_type)).click()

    @allure.step("Нажать на кнопку информации о типе такси {taxi_tariff}")
    def click_button_taxi_info(self, taxi_tariff):
        self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_TARIFF_BLOCK_BUTTON, taxi_tariff.value)).click()

    @allure.step("Проверяем, что кнопка вызвать такси видна")
    def assert_button_call_taxi_is_visible(self):
        assert self.wait_element_visible(MainPageLocators.BUTTON_CALL_TAXI).is_displayed() == True

    @allure.step("Проверяем, что кнопка вызвать забронировать видна")
    def assert_button_book_is_visible(self):
        assert self.wait_element_visible(MainPageLocators.BUTTON_BOOK).is_displayed() == True

    @allure.step("Проверяем, что форма такси поп-ап содержит ожидаемые данные.")
    def assert_taxi_pop_info(self, taxi_tariff, expected_name, expected_title, expected_description):
        actual_name = self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_POP_UP_NAME, taxi_tariff.value)).text
        actual_title = self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_POP_UP_TITLE, taxi_tariff.value)).text
        actual_description = self.wait_element_visible(
            self.format_locator(MainPageLocators.TAXI_POP_UP_DESCRIPTION, taxi_tariff.value)).text
        assert actual_name == expected_name
        assert actual_title == expected_title
        assert actual_description == expected_description

    @allure.step("Нажать вызвать такси")
    def click_button_call_taxi(self):
        self.wait_element_visible(MainPageLocators.BUTTON_CALL_TAXI).click()

    @allure.step("Нажать на кнопку ввести номер и заказать такси")
    def click_button_order_taxi(self):
        self.wait_element_visible(MainPageLocators.TAXI_ORDER_BUTTON).click()

    @allure.step("Открыть форму Требования к заказу если она закрыта")
    def open_form_request_to_taxi_order(self):
        reqs_order = self.wait_element_visible(MainPageLocators.TAXI_REQS_HEADER)
        if not self.driver.find_element(*MainPageLocators.TAXI_REQS_NOTEBOOK_TABLE).is_displayed():
            reqs_order.click()
        self.wait_element_visible(MainPageLocators.TAXI_REQS_NOTEBOOK_TABLE).click()

    @allure.step("Проверяем что форма ожидания заказа, загрузилась и таймер работает")
    def assert_taxi_searching_form_is_visible(self):
        title = self.wait_element_visible(MainPageLocators.TAXI_ORDERED_TITLE).text
        self.wait_util_element_text_changes(MainPageLocators.TAXI_ORDER_TIMER, '00:00')
        time_waiting_taxi_before = self.driver.find_element(*MainPageLocators.TAXI_ORDER_TIMER).text.replace(":", "")
        time.sleep(5)
        time_waiting_taxi_after = self.driver.find_element(*MainPageLocators.TAXI_ORDER_TIMER).text.replace(":", "")
        assert title == "Поиск машины"
        assert int(time_waiting_taxi_after) < int(time_waiting_taxi_before)

    @allure.step("Ожидаем нахождения машины. Номер выбранной машины соответствует шаблону ж 911 зд")
    def wait_taxi_is_found(self):
        car_plate_number = self.wait_element_visible_custom_duration(MainPageLocators.TAXI_ORDERED_ID, 35).text
        car_arriving_time = self.wait_element_visible(MainPageLocators.TAXI_ORDERED_TITLE).text
        plate_pattern = "^[а-я]{1}.*\d{3}.*[а-я]{2}$"
        if not re.search(plate_pattern, car_plate_number):
            assert True == False
        assert "и приедет" in car_arriving_time

    @allure.step("Открываем дополнительные данные о заказе такси")
    def click_taxi_burger_button(self):
        self.wait_element_visible(MainPageLocators.TAXI_ORDER_BURGER_MENU).click()

    @allure.step("Получаем стоимость заказа такси из дополнительных данных о заказе")
    def get_taxi_cost_in_burger_menu(self):
        self.click_taxi_burger_button()
        taxi_cost_txt = self.wait_element_visible(MainPageLocators.TAXI_ORDER_DETAILED_INFO_COST).text
        return MainPage.get_cost_from_str(taxi_cost_txt)

    @allure.step("Нажать на кнопку отмена заказа такси")
    def click_button_cancel_order_taxi(self):
        self.wait_element_visible(MainPageLocators.TAXI_ORDER_CANCEL).click()

    @allure.step("Проверяем, что форма ожидания заказа такси закрыта")
    def order_form_is_closed(self):
        self.wait_element_not_visible(MainPageLocators.TAXI_ORDERED_TITLE)


    @staticmethod
    def get_cost_from_str(txt):
        cost = re.search("\d+", txt)
        if cost:
            return float(cost.group())
        return -1

    @staticmethod
    def get_tab_locator(mode):
        if mode == TripMode.OPTIMUM:
            return MainPageLocators.PICKER_MODE_OPTIMUM
        elif mode == TripMode.FAST:
            return MainPageLocators.PICKER_MODE_FAST
        elif mode == TripMode.OWN:
            return MainPageLocators.PICKER_MODE_OWN
