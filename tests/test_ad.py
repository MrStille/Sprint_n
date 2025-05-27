import allure

from helpers.AdHelper import AdHelper
from helpers.AssertHelper import AssertHelper
from helpers.RandomHelpers import RandomHelpers
from steps.steps import Steps
from tests.conftest import logged_user


class TestAd:

    @allure.title("Создание объявления")
    def test_create_ads(self, logged_user):
        expected_ads = AdHelper.get_random_ads()
        response = Steps.create_ads(logged_user, expected_ads)
        actual_ads = response.json()
        Steps.delete_ads(logged_user, actual_ads)

        assert response.status_code == 201
        assert actual_ads["id"] > 0
        assert actual_ads["name"] == expected_ads["name"]
        assert actual_ads["city"] == expected_ads["city"]
        assert actual_ads["condition"] == expected_ads["condition"]
        assert actual_ads["description"] == expected_ads["description"]
        assert actual_ads["price"] == expected_ads["price"]

    @allure.title("Редактирование объявления")
    def test_update_ads(self, logged_user, created_ads):
        update_ads = {"id": created_ads["id"],
                     "name": created_ads["name"] + "aaa",
                     "condition": "Новое",
                     "category": "Книги",
                     "city": "Новосибирск",
                     "description": created_ads["description"] + "aaa",
                     "price": "130"
                     }

        response = Steps.patch_ads(logged_user, update_ads)
        actual_updated_ads = response.json()
        searched_ads_response = Steps.search_ads(update_ads)
        assert response.status_code == 200
        AssertHelper.assert_ads(actual_updated_ads, update_ads)
        assert searched_ads_response.status_code == 200
        assert len(searched_ads_response.json()["offers"]) == 1
        searched_ads = searched_ads_response.json()["offers"][0]
        AssertHelper.assert_ads(update_ads, searched_ads)

    @allure.title("Пользователь не может отредактировать объявление другого пользователя")
    def test_update_ads_by_another_user(self, logged_user, created_ads):
        user_b = RandomHelpers.get_random_user()
        user_b_register = Steps.register_new_user_ok(user_b)
        user_b_logged = Steps.login_user_ok(user_b_register)
        update_ads = created_ads.copy()
        update_ads["name"] = created_ads["name"] + "aaa"
        response = Steps.patch_ads(user_b_logged, update_ads)
        searched_ads_response = Steps.search_ads(created_ads)
        assert response.status_code == 401
        assert searched_ads_response.status_code == 200
        assert len(searched_ads_response.json()["offers"]) == 1
        assert searched_ads_response.json()["offers"][0]["name"] == created_ads["name"]

    @allure.title("Удаление объявления")
    def test_delete_ads(self, logged_user):
        ad = AdHelper.get_random_ads()
        created_ads2 = Steps.create_ads_ok(logged_user, ad)
        response = Steps.delete_ads(logged_user, created_ads2)
        searched_ads_response = Steps.search_ads(created_ads2)
        assert response.status_code == 200
        assert searched_ads_response.status_code == 200
        assert len(searched_ads_response.json()["offers"]) == 0


