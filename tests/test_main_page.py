
import allure
import pytest

from tests.conftest import main_page
from utils.taxi_tariff import TaxiTariff
from utils.trip_type import TripType
from utils.trip_mode import TripMode


class TestMainPage:
    POINT_A = "Хамовнический Вал, 34"
    POINT_B = "Зубовский бульвар, 37"

    @allure.title("Точки начала и конца маршрута видны на карте, если указать маршрут")
    def test_add_route_shows_start_end_points_on_map(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.assert_start_point_a_visible(self.POINT_A)
        main_page.assert_start_point_b_visible(self.POINT_B)

    @allure.title("Блок-меню выбора маршрута виден слева от карты, если указать маршрут")
    def test_add_route_shows_start_end_points_on_map(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.assert_route_picker_menu_is_visible()

    @allure.title("Ввести одинаковый адрес в 'Откуда' и 'Куда', блок-меню показывает текст бесплатно")
    def test_add_route_shows_start_end_points_on_map(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_A)
        main_page.assert_free_trip()

    @allure.title("При переключении между видами маршрута (Оптимальный\Быстрый) происходит смена активного таба и "
                  "пересчет времени и стоимости маршрута")
    def test_switch_mode_recalculate_trip_total(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.assert_selected_tab(TripMode.FAST)
        fast_total_result = main_page.get_total_trip_result()
        fast_total_duration = main_page.get_total_trip_duration()
        main_page.switch_mode(TripMode.OPTIMUM)
        main_page.assert_selected_tab(TripMode.OPTIMUM)
        optimum_total_result = main_page.get_total_trip_result()
        optimum_total_duration = main_page.get_total_trip_duration()
        assert fast_total_result != optimum_total_result
        assert fast_total_duration != optimum_total_duration

    @allure.title("При переключении на вид маршрута Свой происходит смена активного таба и становятся активны типы "
                  "передвижения (Машина, Пешком, Такси, Велосипед, Самокат, Драйв)")
    def test_switching_mode_to_own_activate_all_trip_types(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.switch_mode(TripMode.OWN)
        main_page.assert_selected_tab(TripMode.OWN)
        main_page.assert_all_trip_types_available()

    @allure.title("При выборе вида маршрута Быстрый активна кнопка Вызвать такси")
    def test_taxi_available_in_fast_mode(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.switch_mode(TripMode.FAST)
        main_page.assert_selected_tab(TripMode.FAST)
        main_page.assert_button_call_taxi_is_visible()

    @allure.title("При выборе вида маршрута Свой, типа передвижения Драйв активна кнопка Забронировать")
    def test_book_button_available_in_own_mode_and_trip_drive(self, main_page):
        main_page.type_route(self.POINT_A, self.POINT_B)
        main_page.switch_mode(TripMode.OWN)
        main_page.assert_selected_tab(TripMode.OWN)
        main_page.click_button_trip_type(TripType.DRIVE)
        main_page.assert_button_book_is_visible()

    @allure.title("Форма заказа такси открывается и доступны 6 тарифов, Рабочий тариф активный")
    def test_taxi_order_has_6_tariffs(self, main_page_set_trip):
        main_page_set_trip.assert_all_taxi_types_available()
        main_page_set_trip.assert_taxi_tariff_is_selected(TaxiTariff.WORK)

    @allure.title("Проверяем информацию о всех тарифах такси")
    @pytest.mark.parametrize("taxi_tariff, name, title, description", [
        [TaxiTariff.WORK, "Рабочий", "Для деловых особ, которых отвлекают",
         '— В салоне нет доступа к асоциальным сетям\n— Выдвижной столик для ноутбука'],
        [TaxiTariff.SLEEPY, "Сонный", "Если мысли не выходят из головы",
         "— Вас сопровождает спутник с тремя высшими образованиями\n— Можете обсудить любую тему — от трендов в Тик-токе до квантовой механики"],
        [TaxiTariff.TALKING, "Разговорчивый", "Для тех, кто не выспался",
         "— В салоне кресло-кровать\n— На сиденье мыгкая игрушка — по желанию\n— Водитель ведёт плавно, чтобы вы дремали сладко"],
        [TaxiTariff.COMFORTING, "Утешительный", "Если хочется свернуться калачиком",
         "— В салоне мягкий плед и носовые платки\n— Водитель за звуконепроницаемой шторкой\n— Персональное ведёрко с мороженым"],
        [TaxiTariff.HOLIDAY, "Отпускной", "Если пришла пора отдохнуть",
         "— В салоне массажное кресло\n— В бардачке — расслабляющие маски для лица и патчи."],
        [TaxiTariff.GLOSSY, "Глянцевый", "Если нужно блистать",
         "— В салоне неоновая подсветка\n— С потолка автомобиля непрерывно летят блёстки\n— Салон прошёл верификацию на инстаграммность у лучших экспертов"],
    ])
    def test_taxi_has_correct_information(self, main_page_set_trip, taxi_tariff, name, title, description):
        main_page_set_trip.click_taxi_tariff(taxi_tariff)
        main_page_set_trip.click_button_taxi_info(taxi_tariff)
        main_page_set_trip.assert_taxi_pop_info(taxi_tariff, name, title, description)

    @allure.title("Заказ такси с тарифом Рабочий и появления формы ожидания заказа")
    def test_order_taxi(self, main_page_set_trip):
        main_page_set_trip.click_taxi_tariff(TaxiTariff.WORK)
        main_page_set_trip.open_form_request_to_taxi_order()
        main_page_set_trip.click_button_order_taxi()
        main_page_set_trip.assert_taxi_searching_form_is_visible()

    @allure.title("Заказ такси с тарифом Рабочий и ожидания назначения машины")
    def test_order_taxi_and_wait_car_is_found(self, main_page_set_trip):
        page = main_page_set_trip
        page.click_taxi_tariff(TaxiTariff.WORK)
        taxi_cost = page.get_taxi_tariff_cost(TaxiTariff.WORK)
        page.open_form_request_to_taxi_order()
        page.click_button_order_taxi()
        page.wait_taxi_is_found()
        taxi_cost_detailed = page.get_taxi_cost_in_burger_menu()
        assert taxi_cost == taxi_cost_detailed

    @pytest.mark.xfail(reason = "Кнопка 'Отменить' не работает")
    @allure.title("Сделать заказ такси и отменить его")
    def test_order_and_cancel_taxi(self, main_page_set_trip):
        page = main_page_set_trip
        page.click_taxi_tariff(TaxiTariff.WORK)
        page.open_form_request_to_taxi_order()
        page.click_button_order_taxi()
        page.assert_taxi_searching_form_is_visible()
        page.click_button_cancel_order_taxi()
        page.order_form_is_closed()
