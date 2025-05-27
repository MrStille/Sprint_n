from email.mime.text import MIMEText

import allure
import requests
from requests_toolbelt import MultipartEncoder

from Data import Data


class Steps:
    @staticmethod
    @allure.step("Регистрация нового пользователя")
    def register_new_user(user):
        sign_url = Data.SITE_URL + '/signup'
        data = {
            "email": user["email"],
            "password": user["password"],
            "submitPassword": user["password"]
        }
        response = requests.post(sign_url, data=data)
        return response

    @staticmethod
    @allure.step("Регистрация нового пользователя с валидацией")
    def register_new_user_ok(user):
        sign_url = Data.SITE_URL + '/signup'
        data = {
            "email": user["email"],
            "password": user["password"],
            "submitPassword": user["password"]
        }
        response = requests.post(sign_url, data=data)
        assert response.status_code == 201
        return {
            "email": user["email"],
            "password": user["password"],
            "access_token": response.json()["access_token"]["access_token"]
        }

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(user):
        login_url = Data.SITE_URL + '/signin'
        data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(login_url, data=data)
        print(f"email={user['email']}, password={user['password']}")
        return response

    @staticmethod
    @allure.step("Логин пользователя c валидацией")
    def login_user_ok(user):
        login_url = Data.SITE_URL + '/signin'
        data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(login_url, data=data)
        assert response.status_code == 201
        return {
            "email": data["email"],
            "password": data["password"],
            "access_token": response.json()["token"]["access_token"]
        }

    @staticmethod
    @allure.step("Создание нового объявления")
    def create_ads(user, ads):
        create_url = Data.SITE_URL + '/create-listing'
        m = MultipartEncoder(
            fields={'name': ads["name"],
                    'condition': ads["condition"],
                    'city': ads["city"],
                    'category':ads["category"],
                    'description':ads["description"],
                    'price': str(ads["price"]),
                    }
        )
        headers = {'Content-Type': m.content_type,'Authorization':"Bearer " + user["access_token"]}
        response = requests.post(create_url, data=m, headers=headers)
        return response

    @staticmethod
    @allure.step("Создать новое объявление и вернуть его данные")
    def create_ads_ok(user, ads):
        created_ad = Steps.create_ads(user, ads)
        assert  created_ad.status_code == 201
        return created_ad.json()

    @staticmethod
    @allure.step("Изменить данные объявления")
    def patch_ads(user, ads):
        create_url = Data.SITE_URL + '/update-offer/'+ str(ads["id"])
        data = MultipartEncoder(
            fields={
                'name': ads["name"],
                'condition': ads["condition"],
                'city': ads["city"],
                'category': ads["category"],
                'description': ads["description"],
                'price': str(ads["price"]),
            }
        )
        headers = {'Content-Type': data.content_type,'Authorization':"Bearer " + user["access_token"]}
        response = requests.patch(create_url, data=data, headers=headers)
        return response

    @staticmethod
    @allure.step("Удалить объявление")
    def delete_ads(user, ads):
        delete_url = Data.SITE_URL + '/listings/' + str(ads["id"])
        headers = {'Authorization':"Bearer " + user["access_token"]}
        response = requests.delete(delete_url, headers=headers)
        return response

    @staticmethod
    def search_ads(ads):
        search_url = Data.SITE_URL + f'/offers/1/?name={ads["name"]}&category={ads["category"]}&city={ads["city"]}'
        response = requests.get(search_url)
        return response

    @staticmethod
    def add_field( name, value):
        text = MIMEText(value)
        text.add_header('Content-disposition', f'form-data; name="{name}"')
        return text