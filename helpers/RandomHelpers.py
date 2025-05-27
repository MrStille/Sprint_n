import string
import random

from Data import Data


class RandomHelpers:
    @staticmethod
    def get_email():
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(10))
        return f"test-{random_string}@yandex.ru"


    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def get_random_user():
        return {
            "email": RandomHelpers.get_email(),
            "password": Data.COMMON_PASSWORD,
        }