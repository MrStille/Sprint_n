from helpers.RandomHelpers import RandomHelpers


class AdHelper:
    @staticmethod
    def get_random_ads():
        return {
            "name": RandomHelpers.generate_random_string(10),
            "category": "Книги",
            "condition": "Новое",
            "city": "Новосибирск",
            "description": RandomHelpers.generate_random_string(40),
            "price": 1001
        }