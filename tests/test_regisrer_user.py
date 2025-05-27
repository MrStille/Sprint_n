import allure

from steps.steps import Steps


class TestRegisterUser:

    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, new_user):
        new_user_response = Steps.register_new_user(new_user)
        assert new_user_response.status_code == 201
        assert new_user_response.json()["user"]["id"] > 0
        assert new_user_response.json()["user"]["email"] == new_user["email"]
        assert len(new_user_response.json()["access_token"]["access_token"]) > 10

    @allure.title("Регистрация пользователя с уже существующим почтовым адресом")
    def test_register_new_user_with_used_email(self, new_user):
        new_user_response = Steps.register_new_user(new_user)
        new_user_second_try = Steps.register_new_user(new_user)
        assert new_user_response.status_code == 201
        assert new_user_second_try.status_code == 400
        assert new_user_second_try.json()["message"] ==  'Почта уже используется'
