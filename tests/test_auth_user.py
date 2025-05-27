import allure

from steps.steps import Steps


class TestAuthUser:

    @allure.title("Успешный логин пользователя")
    def test_auth_user(self, registered_user):
        response = Steps.login_user(registered_user)
        assert response.status_code == 201
        assert response.json()["user"]["id"] > 0
        assert response.json()["user"]["email"] == registered_user["email"]
        assert len(response.json()["token"]["access_token"]) > 10
